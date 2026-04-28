from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    summary: Optional[str] = None
    link: str
    image_url: Optional[str] = None
    published_date: Optional[str] = None

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
