from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ParticipantImageResponse(BaseModel):
    id: int
    participant_name: str
    image_url: str

    class Config:
        from_attributes = True


class TopicCreate(BaseModel):
    program_id: int
    topic_title: str = Field(..., max_length=255)
    episode: Optional[int] = None
    match_type: Optional[str] = None
    participants: Optional[str] = None
    video_url: Optional[str] = None
    vote_type: int = Field(..., ge=1, le=3)
    actual_result: Optional[int] = None


class TopicUpdate(BaseModel):
    topic_title: Optional[str] = None
    episode: Optional[int] = None
    match_type: Optional[str] = None
    participants: Optional[str] = None
    video_url: Optional[str] = None
    vote_type: Optional[int] = None
    actual_result: Optional[int] = None


class TopicResponse(BaseModel):
    id: int
    program_id: int
    topic_title: str
    episode: Optional[int] = None
    match_type: Optional[str] = None
    participants: Optional[List[str]] = None
    video_url: Optional[str] = None
    vote_type: int
    actual_result: Optional[int] = None
    created_at: datetime
    participant_images: List[ParticipantImageResponse] = []

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, 'participants') and isinstance(obj.participants, str):
            obj_dict = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            obj_dict['participants'] = [p.strip() for p in obj.participants.split(',') if p.strip()]
            if hasattr(obj, 'participant_images'):
                obj_dict['participant_images'] = obj.participant_images
            return super().model_validate(obj_dict, **kwargs)
        return super().model_validate(obj, **kwargs)


class ParticipantImageCreate(BaseModel):
    topic_id: int
    participant_name: str = Field(..., max_length=100)
    image_url: str = Field(..., max_length=512)
