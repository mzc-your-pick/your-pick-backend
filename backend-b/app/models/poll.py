from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class Poll(Base):
    """투표(Poll) 모델 - 백엔드 A가 관리, 여기서는 조회용"""
    __tablename__ = "polls"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    matchup_id = Column(BigInteger, ForeignKey("matchups.id"), nullable=False)
    title = Column(String(200), nullable=False)
    poll_type = Column(String(20), nullable=False)  # 'VS' | 'PASS_FAIL' | 'MULTI'
    options = Column(JSON, nullable=False)  # ["A셰프", "B셰프", "C셰프"]
    status = Column(String(20), default="OPEN")  # 'OPEN' | 'CLOSED'
    panel_result = Column(JSON, nullable=True)  # {"A셰프": 70, "B셰프": 30}
    result_revealed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    closed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Poll(id={self.id}, title={self.title}, status={self.status})>"
