from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Tuple, Optional
from datetime import datetime

from ..models.vote import Vote
from ..models.poll import Poll
from ..utils.voter_id import generate_voter_id


class VoteError(Exception):
    """투표 관련 에러"""
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class VoteService:
    """투표 비즈니스 로직"""

    def __init__(self, db: Session):
        self.db = db

    def get_poll(self, poll_id: int) -> Optional[Poll]:
        """Poll 조회"""
        return self.db.query(Poll).filter(Poll.id == poll_id).first()

    def validate_poll(self, poll: Poll, choice: str) -> None:
        """투표 유효성 검사"""
        # 투표 존재 여부
        if not poll:
            raise VoteError("POLL_NOT_FOUND", "존재하지 않는 투표입니다")

        # 투표 상태 확인
        if poll.status != "OPEN":
            raise VoteError("POLL_CLOSED", "마감된 투표입니다")

        # 선택지 유효성
        if choice not in poll.options:
            raise VoteError("INVALID_CHOICE", f"유효하지 않은 선택지입니다. 가능한 선택: {poll.options}")

    def create_vote(
        self,
        poll_id: int,
        choice: str,
        ip: str,
        fingerprint: str
    ) -> Tuple[Vote, datetime]:
        """
        투표 생성

        Args:
            poll_id: 투표 ID
            choice: 선택한 옵션
            ip: 클라이언트 IP
            fingerprint: 브라우저 fingerprint

        Returns:
            (Vote, voted_at) 튜플

        Raises:
            VoteError: 투표 실패 시
        """
        # Poll 조회 및 검증
        poll = self.get_poll(poll_id)
        self.validate_poll(poll, choice)

        # voter_id 생성
        voter_id = generate_voter_id(ip, fingerprint, poll_id)

        # 투표 생성
        vote = Vote(
            poll_id=poll_id,
            voter_id=voter_id,
            choice=choice
        )

        try:
            self.db.add(vote)
            self.db.commit()
            self.db.refresh(vote)
            return vote, vote.created_at

        except IntegrityError:
            self.db.rollback()
            raise VoteError("ALREADY_VOTED", "이미 투표하셨습니다")

    def has_voted(self, poll_id: int, ip: str, fingerprint: str) -> bool:
        """이미 투표했는지 확인"""
        voter_id = generate_voter_id(ip, fingerprint, poll_id)
        vote = self.db.query(Vote).filter(
            Vote.poll_id == poll_id,
            Vote.voter_id == voter_id
        ).first()
        return vote is not None
