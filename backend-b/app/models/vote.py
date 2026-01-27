from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from ..database import Base


class Vote(Base):
    """대중 투표 모델"""
    __tablename__ = "votes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    poll_id = Column(BigInteger, ForeignKey("polls.id"), nullable=False)
    voter_id = Column(String(64), nullable=False)  # SHA256 해시
    choice = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("unique_vote", "poll_id", "voter_id", unique=True),
        Index("idx_poll_choice", "poll_id", "choice"),
    )

    def __repr__(self):
        return f"<Vote(id={self.id}, poll_id={self.poll_id}, choice={self.choice})>"
