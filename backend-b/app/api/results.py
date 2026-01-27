from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.result import ResultResponse
from ..services.result_service import ResultService
from ..utils.rate_limit import limiter

router = APIRouter()


@router.get(
    "/polls/{poll_id}/results",
    response_model=ResultResponse,
    summary="투표 결과 조회",
    description="대중 투표 집계 + 패널 결과 비교"
)
@limiter.limit("60/minute")
async def get_results(
    request: Request,
    poll_id: int,
    db: Session = Depends(get_db)
):
    """
    투표 결과 조회

    - **poll_id**: 투표 ID

    Returns:
        - public_votes: 대중 투표 집계 (count, percent)
        - panel_result: 패널(방송) 결과
        - comparison: 패널 vs 대중 비교 분석
    """
    service = ResultService(db)
    result = service.get_results(poll_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "POLL_NOT_FOUND",
                "message": "존재하지 않는 투표입니다"
            }
        )

    return ResultResponse(
        success=True,
        data=result
    )
