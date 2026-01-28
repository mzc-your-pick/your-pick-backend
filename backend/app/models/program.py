from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    image_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    topics = relationship("Topic", back_populates="program")

    def __repr__(self):
        return f"<Program(id={self.id}, title={self.title})>"
