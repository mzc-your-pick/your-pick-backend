from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProgramCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: str = Field(..., max_length=50)
    image_url: Optional[str] = None


class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None


class ProgramResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
