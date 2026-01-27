from fastapi import APIRouter, Depends, Request, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..schemas.vote import VoteCreate, VoteResponse, VoteData
from ..services.vote_service import VoteService, VoteError
from ..utils.rate_limit import limiter
from ..config import settings

router = APIRouter()


def get_client_ip(request: Request) -> str:
    """클라이언트 IP 추출"""
    # 프록시/로드밸런서 뒤에 있을 경우
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host or "unknown"


@router.post(
    "/polls/{poll_id}/votes",
    response_model=VoteResponse,
    status_code=201,
    summary="투표하기",
    description="대중 투표 저장. 중복투표 불가."
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def create_vote(
    request: Request,
    poll_id: int,
    vote_data: VoteCreate,
    x_fingerprint: Optional[str] = Header(None, alias="X-Fingerprint"),
    db: Session = Depends(get_db)
):
    """
    투표하기

    - **poll_id**: 투표 ID
    - **choice**: 선택한 옵션 (예: "A셰프")
    - **X-Fingerprint**: 브라우저 fingerprint (헤더)
    """
    # IP, fingerprint 추출
    ip = get_client_ip(request)
    fingerprint = x_fingerprint or "no-fingerprint"

    service = VoteService(db)

    try:
        vote, voted_at = service.create_vote(
            poll_id=poll_id,
            choice=vote_data.choice,
            ip=ip,
            fingerprint=fingerprint
        )

        return VoteResponse(
            success=True,
            message="투표가 완료되었습니다",
            data=VoteData(
                poll_id=poll_id,
                choice=vote_data.choice,
                voted_at=voted_at
            )
        )

    except VoteError as e:
        status_codes = {
            "POLL_NOT_FOUND": 404,
            "POLL_CLOSED": 410,
            "INVALID_CHOICE": 400,
            "ALREADY_VOTED": 409
        }
        raise HTTPException(
            status_code=status_codes.get(e.error_code, 400),
            detail={
                "success": False,
                "error": e.error_code,
                "message": e.message
            }
        )
