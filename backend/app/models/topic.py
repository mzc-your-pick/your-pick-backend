from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    topic_title = Column(String(255), nullable=False)
    episode = Column(Integer, nullable=True)
    match_type = Column(String(100), nullable=True)
    participants = Column(Text, nullable=True)
    video_url = Column(String(512), nullable=True)
    vote_type = Column(Integer, nullable=False)  # 1:합불, 2:1대1, 3:다인원
    actual_result = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    program = relationship("Program", back_populates="topics")
    participant_images = relationship("ParticipantImage", back_populates="topic")
    votes = relationship("Vote", back_populates="topic")

    __table_args__ = (
        Index("idx_program", "program_id"),
        Index("idx_episode", "program_id", "episode"),
    )

    def __repr__(self):
        return f"<Topic(id={self.id}, title={self.topic_title})>"
