from sqlalchemy.orm import Session
from typing import Optional

from ..models.vote import Vote
from ..models.topic import Topic


class VoteError(Exception):
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class VoteService:
    def __init__(self, db: Session):
        self.db = db

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        return self.db.query(Topic).filter(Topic.id == topic_id).first()

    def create_vote(self, topic_id: int, vote_choice: int) -> Vote:
        topic = self.get_topic(topic_id)
        if not topic:
            raise VoteError("TOPIC_NOT_FOUND", "존재하지 않는 주제입니다")

        vote = Vote(
            topic_id=topic_id,
            vote_choice=vote_choice
        )

        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote
