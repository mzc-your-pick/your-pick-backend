from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    comment_user_name: str = Field(..., max_length=100)
    comment_password: str = Field(..., max_length=255)


class CommentDelete(BaseModel):
    comment_password: str


class CommentResponse(BaseModel):
    id: int
    vote_id: int
    content: str
    comment_user_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    success: bool
    data: list[CommentResponse]
    total: int
