from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vote_id = Column(BigInteger, ForeignKey("votes.id"), nullable=False)
    content = Column(Text, nullable=False)
    comment_user_name = Column(String(100), nullable=False)
    comment_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    vote = relationship("Vote", back_populates="comments")

    __table_args__ = (
        Index("idx_vote", "vote_id"),
        Index("idx_created", "created_at"),
    )

    def __repr__(self):
        return f"<Comment(id={self.id}, user={self.comment_user_name})>"
