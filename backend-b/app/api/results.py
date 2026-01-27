from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.result import ResultResponse
from ..services.result_service import ResultService
from ..utils.rate_limit import limiter

router = APIRouter()


@router.get(
    "/topics/{topic_id}/results",
    response_model=ResultResponse,
    summary="투표 결과 조회"
)
@limiter.limit("60/minute")
async def get_results(
    request: Request,
    topic_id: int,
    db: Session = Depends(get_db)
):
    service = ResultService(db)
    result = service.get_results(topic_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "TOPIC_NOT_FOUND",
                "message": "존재하지 않는 주제입니다"
            }
        )

    return ResultResponse(
        success=True,
        data=result
    )
