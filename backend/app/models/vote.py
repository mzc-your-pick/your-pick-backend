from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    topic_id = Column(BigInteger, ForeignKey("topics.id"), nullable=False)
    vote_choice = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    topic = relationship("Topic", back_populates="votes")
    comments = relationship("Comment", back_populates="vote")

    __table_args__ = (
        Index("idx_topic_choice", "topic_id", "vote_choice"),
    )

    def __repr__(self):
        return f"<Vote(id={self.id}, topic_id={self.topic_id}, choice={self.vote_choice})>"
