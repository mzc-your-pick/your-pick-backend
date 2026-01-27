from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.topic import TopicCreate, TopicUpdate, TopicResponse, ParticipantImageCreate, ParticipantImageResponse
from ..services.topic_service import TopicService

router = APIRouter()


@router.get("/topics", response_model=List[TopicResponse], summary="대결 주제 목록 조회")
async def get_topics(
    program_id: Optional[int] = Query(None, description="프로그램 ID 필터"),
    episode: Optional[int] = Query(None, description="회차 필터"),
    db: Session = Depends(get_db)
):
    service = TopicService(db)
    return service.get_all(program_id=program_id, episode=episode)


@router.get("/topics/{topic_id}", response_model=TopicResponse, summary="대결 주제 상세 조회")
async def get_topic(topic_id: int, db: Session = Depends(get_db)):
    service = TopicService(db)
    topic = service.get_by_id(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="주제를 찾을 수 없습니다")
    return topic


@router.post("/topics", response_model=TopicResponse, status_code=201, summary="대결 주제 생성")
async def create_topic(data: TopicCreate, db: Session = Depends(get_db)):
    service = TopicService(db)
    return service.create(data)


@router.patch("/topics/{topic_id}", response_model=TopicResponse, summary="대결 주제 수정")
async def update_topic(topic_id: int, data: TopicUpdate, db: Session = Depends(get_db)):
    service = TopicService(db)
    topic = service.update(topic_id, data)
    if not topic:
        raise HTTPException(status_code=404, detail="주제를 찾을 수 없습니다")
    return topic


@router.delete("/topics/{topic_id}", summary="대결 주제 삭제")
async def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    service = TopicService(db)
    if not service.delete(topic_id):
        raise HTTPException(status_code=404, detail="주제를 찾을 수 없습니다")
    return {"success": True, "message": "주제가 삭제되었습니다"}


@router.post("/participant-images", response_model=ParticipantImageResponse, status_code=201, summary="참가자 이미지 추가")
async def add_participant_image(data: ParticipantImageCreate, db: Session = Depends(get_db)):
    service = TopicService(db)
    return service.add_participant_image(data)
