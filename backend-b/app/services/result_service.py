from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict, List

from ..models.vote import Vote
from ..models.poll import Poll
from ..schemas.result import (
    ResultData,
    PublicVotes,
    ChoiceResult,
    Comparison,
    BiggestGap
)


class ResultService:
    """결과 집계 비즈니스 로직"""

    def __init__(self, db: Session):
        self.db = db

    def get_poll(self, poll_id: int) -> Optional[Poll]:
        """Poll 조회"""
        return self.db.query(Poll).filter(Poll.id == poll_id).first()

    def get_vote_counts(self, poll_id: int) -> Dict[str, int]:
        """
        선택지별 투표 수 집계

        Returns:
            {"A셰프": 350, "B셰프": 450, ...}
        """
        results = self.db.query(
            Vote.choice,
            func.count(Vote.id).label("count")
        ).filter(
            Vote.poll_id == poll_id
        ).group_by(
            Vote.choice
        ).all()

        return {row.choice: row.count for row in results}

    def calculate_percentages(
        self,
        counts: Dict[str, int],
        options: List[str]
    ) -> Dict[str, ChoiceResult]:
        """
        퍼센트 계산

        Args:
            counts: 선택지별 투표 수
            options: 전체 옵션 목록 (0표인 옵션도 포함하기 위해)

        Returns:
            {"A셰프": {"count": 350, "percent": 35.0}, ...}
        """
        total = sum(counts.values())

        results = {}
        for option in options:
            count = counts.get(option, 0)
            percent = round((count / total * 100), 1) if total > 0 else 0.0
            results[option] = ChoiceResult(count=count, percent=percent)

        return results

    def calculate_comparison(
        self,
        public_results: Dict[str, ChoiceResult],
        panel_result: Optional[Dict[str, float]]
    ) -> Optional[Comparison]:
        """
        패널 vs 대중 비교 분석

        Args:
            public_results: 대중 투표 결과
            panel_result: 패널 결과 (관리자 입력)

        Returns:
            비교 분석 결과
        """
        if not panel_result or not public_results:
            return None

        # 대중 1등
        public_favorite = max(
            public_results.keys(),
            key=lambda x: public_results[x].percent
        ) if public_results else None

        # 패널 1등
        panel_favorite = max(
            panel_result.keys(),
            key=lambda x: panel_result[x]
        ) if panel_result else None

        # 가장 큰 차이 계산
        biggest_gap = None
        max_gap = 0

        for option, public_data in public_results.items():
            if option in panel_result:
                panel_percent = panel_result[option]
                public_percent = public_data.percent
                gap = abs(panel_percent - public_percent)

                if gap > max_gap:
                    max_gap = gap
                    biggest_gap = BiggestGap(
                        option=option,
                        panel_percent=panel_percent,
                        public_percent=public_percent,
                        gap=round(gap, 1)
                    )

        return Comparison(
            biggest_gap=biggest_gap,
            public_favorite=public_favorite,
            panel_favorite=panel_favorite,
            opinion_match=(public_favorite == panel_favorite)
        )

    def get_results(self, poll_id: int) -> Optional[ResultData]:
        """
        투표 결과 조회

        Args:
            poll_id: 투표 ID

        Returns:
            결과 데이터 또는 None
        """
        poll = self.get_poll(poll_id)
        if not poll:
            return None

        # 투표 수 집계
        counts = self.get_vote_counts(poll_id)
        total = sum(counts.values())

        # 퍼센트 계산
        results = self.calculate_percentages(counts, poll.options)

        # 대중 투표 결과
        public_votes = PublicVotes(
            total=total,
            results=results
        )

        # 비교 분석 (패널 결과가 있을 때만)
        comparison = self.calculate_comparison(results, poll.panel_result)

        return ResultData(
            poll_id=poll.id,
            title=poll.title,
            status=poll.status,
            options=poll.options,
            public_votes=public_votes,
            panel_result=poll.panel_result,
            comparison=comparison,
            result_revealed=poll.result_revealed
        )
