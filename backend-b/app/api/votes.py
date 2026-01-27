from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.vote import VoteCreate, VoteResponse, VoteData
from ..services.vote_service import VoteService, VoteError
from ..utils.rate_limit import limiter
from ..config import settings

router = APIRouter()


@router.post(
    "/topics/{topic_id}/votes",
    response_model=VoteResponse,
    status_code=201,
    summary="투표하기"
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def create_vote(
    request: Request,
    topic_id: int,
    vote_data: VoteCreate,
    db: Session = Depends(get_db)
):
    service = VoteService(db)

    try:
        vote = service.create_vote(
            topic_id=topic_id,
            vote_choice=vote_data.vote_choice
        )

        return VoteResponse(
            success=True,
            message="투표가 완료되었습니다",
            data=VoteData(
                id=vote.id,
                topic_id=topic_id,
                vote_choice=vote.vote_choice,
                voted_at=vote.created_at
            )
        )

    except VoteError as e:
        status_codes = {
            "TOPIC_NOT_FOUND": 404,
        }
        raise HTTPException(
            status_code=status_codes.get(e.error_code, 400),
            detail={
                "success": False,
                "error": e.error_code,
                "message": e.message
            }
        )
