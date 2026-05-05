from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MovieCreateIn(BaseModel):
    title: str
    director: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = 0
    duration: Optional[int] = None
    is_active: bool = True


class MovieUpdateIn(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None


class MovieOut(BaseModel):
    movie_id: int
    title: str
    director: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = 0
    duration: Optional[int] = None
    is_active: bool
    created_at: datetime