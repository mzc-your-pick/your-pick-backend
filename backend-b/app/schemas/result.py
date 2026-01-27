from pydantic import BaseModel
from typing import Dict, List, Optional


class ChoiceResult(BaseModel):
    """각 선택지별 결과"""
    count: int
    percent: float


class PublicVotes(BaseModel):
    """대중 투표 결과"""
    total: int
    results: Dict[str, ChoiceResult]


class BiggestGap(BaseModel):
    """가장 큰 차이"""
    option: str
    panel_percent: float
    public_percent: float
    gap: float


class Comparison(BaseModel):
    """패널 vs 대중 비교"""
    biggest_gap: Optional[BiggestGap] = None
    public_favorite: Optional[str] = None
    panel_favorite: Optional[str] = None
    opinion_match: bool


class ResultData(BaseModel):
    """결과 데이터"""
    poll_id: int
    title: str
    status: str
    options: List[str]
    public_votes: PublicVotes
    panel_result: Optional[Dict[str, float]] = None
    comparison: Optional[Comparison] = None
    result_revealed: bool


class ResultResponse(BaseModel):
    """결과 응답"""
    success: bool
    data: Optional[ResultData] = None
    error: Optional[str] = None
    message: Optional[str] = None
