from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict

from ..models.vote import Vote
from ..models.topic import Topic
from ..schemas.result import (
    ResultData,
    VoteResults,
    ChoiceResult
)


class ResultService:
    def __init__(self, db: Session):
        self.db = db

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        return self.db.query(Topic).filter(Topic.id == topic_id).first()

    def get_vote_counts(self, topic_id: int) -> Dict[int, int]:
        """선택지별 투표 수 집계 → {1: 350, 2: 190}"""
        results = self.db.query(
            Vote.vote_choice,
            func.count(Vote.id).label("count")
        ).filter(
            Vote.topic_id == topic_id
        ).group_by(
            Vote.vote_choice
        ).all()

        return {row.vote_choice: row.count for row in results}

    def get_results(self, topic_id: int) -> Optional[ResultData]:
        topic = self.get_topic(topic_id)
        if not topic:
            return None

        counts = self.get_vote_counts(topic_id)
        total = sum(counts.values())

        # 퍼센트 계산
        results = {}
        for choice, count in counts.items():
            percent = round((count / total * 100), 1) if total > 0 else 0.0
            results[choice] = ChoiceResult(count=count, percent=percent)

        public_votes = VoteResults(total=total, results=results)

        # 대중 1위 vs 실제 결과 비교
        match = None
        if topic.actual_result is not None and counts:
            public_favorite = max(counts, key=counts.get)
            match = (public_favorite == topic.actual_result)

        return ResultData(
            topic_id=topic.id,
            topic_title=topic.topic_title,
            vote_type=topic.vote_type,
            actual_result=topic.actual_result,
            public_votes=public_votes,
            participants=topic.participants,
            match=match
        )
