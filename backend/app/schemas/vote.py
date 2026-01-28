from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VoteCreate(BaseModel):
    vote_choice: int = Field(..., description="사용자가 선택한 번호")


class VoteData(BaseModel):
    id: int
    topic_id: int
    vote_choice: int
    voted_at: datetime


class VoteResponse(BaseModel):
    success: bool
    message: str
    data: Optional[VoteData] = None
