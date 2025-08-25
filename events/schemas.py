from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=255)
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
