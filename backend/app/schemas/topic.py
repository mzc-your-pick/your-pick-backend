from pydantic import BaseModel, Field, field_validator
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

    @field_validator('participants', mode='before')
    @classmethod
    def split_participants(cls, v):
        if isinstance(v, str):
            return [p.strip() for p in v.split(',') if p.strip()]
        return v


class ParticipantImageCreate(BaseModel):
    topic_id: int
    participant_name: str = Field(..., max_length=100)
    image_url: str = Field(..., max_length=512)
