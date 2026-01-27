from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VoteCreate(BaseModel):
    """투표 생성 요청"""
    choice: str = Field(..., min_length=1, max_length=100, description="선택한 옵션")


class VoteData(BaseModel):
    """투표 데이터"""
    poll_id: int
    choice: str
    voted_at: datetime


class VoteResponse(BaseModel):
    """투표 응답"""
    success: bool
    message: str
    data: Optional[VoteData] = None


class VoteErrorResponse(BaseModel):
    """투표 에러 응답"""
    success: bool = False
    error: str
    message: str
