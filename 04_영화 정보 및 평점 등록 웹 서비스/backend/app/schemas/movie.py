from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class MovieBase(BaseModel):
    title: str
    release_date: Optional[date] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True