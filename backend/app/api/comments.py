from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.comment import CommentCreate, CommentUpdate, CommentDelete, CommentResponse, CommentListResponse
from ..services.comment_service import CommentService

router = APIRouter()


@router.get("/topics/{topic_id}/comments", response_model=CommentListResponse, summary="댓글 목록 조회")
async def get_comments(topic_id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    comments = service.get_by_topic(topic_id)
    return CommentListResponse(
        success=True,
        data=comments,
        total=len(comments)
    )


@router.post("/votes/{vote_id}/comments", response_model=CommentResponse, status_code=201, summary="댓글 작성")
async def create_comment(vote_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    service = CommentService(db)
    comment = service.create(vote_id, data)
    return comment


@router.patch("/comments/{comment_id}", response_model=CommentResponse, summary="댓글 수정")
async def update_comment(comment_id: int, data: CommentUpdate, db: Session = Depends(get_db)):
    service = CommentService(db)
    result = service.update(comment_id, data.content, data.comment_password)
    if result == "COMMENT_NOT_FOUND":
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    if result == "WRONG_PASSWORD":
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다")
    return result


@router.delete("/comments/{comment_id}", summary="댓글 삭제")
async def delete_comment(comment_id: int, data: CommentDelete, db: Session = Depends(get_db)):
    service = CommentService(db)
    error = service.delete(comment_id, data.comment_password)
    if error == "COMMENT_NOT_FOUND":
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    if error == "WRONG_PASSWORD":
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다")
    return {"success": True, "message": "댓글이 삭제되었습니다"}
