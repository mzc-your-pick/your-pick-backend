from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..database import Base


class ParticipantImage(Base):
    __tablename__ = "participant_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(BigInteger, ForeignKey("topics.id"), nullable=False)
    participant_name = Column(String(100), nullable=False)
    image_url = Column(String(512), nullable=False)

    topic = relationship("Topic", back_populates="participant_images")

    __table_args__ = (
        Index("idx_topic", "topic_id"),
    )

    def __repr__(self):
        return f"<ParticipantImage(id={self.id}, name={self.participant_name})>"
