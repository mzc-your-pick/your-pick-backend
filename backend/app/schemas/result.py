from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional


class ChoiceResult(BaseModel):
    count: int
    percent: float


class VoteResults(BaseModel):
    total: int
    results: Dict[int, ChoiceResult]


class ResultData(BaseModel):
    topic_id: int
    topic_title: str
    vote_type: int
    actual_result: Optional[int] = None
    public_votes: VoteResults
    participants: Optional[List[str]] = None
    match: Optional[bool] = None

    @field_validator('participants', mode='before')
    @classmethod
    def split_participants(cls, v):
        if isinstance(v, str):
            return [p.strip() for p in v.split(',') if p.strip()]
        return v


class ResultResponse(BaseModel):
    success: bool
    data: Optional[ResultData] = None
    error: Optional[str] = None
    message: Optional[str] = None
