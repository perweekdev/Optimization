from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReviewBase(BaseModel):
    content: str

class ReviewCreate(ReviewBase):
    movie_id: int

class ReviewResponse(ReviewBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReviewListResponse(ReviewBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    movie_title: str
    username: str

    class Config:
        from_attributes = True