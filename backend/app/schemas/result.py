from pydantic import BaseModel
from typing import Dict, Optional


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
    participants: Optional[str] = None
    match: Optional[bool] = None


class ResultResponse(BaseModel):
    success: bool
    data: Optional[ResultData] = None
    error: Optional[str] = None
    message: Optional[str] = None
