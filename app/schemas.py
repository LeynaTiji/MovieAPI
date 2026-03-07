from pydantic import BaseModel
from typing import Optional, List

class MovieBase(BaseModel):
    title: Optional[str]
    info: Optional[str]
    rating: Optional[str]
    age: Optional[str]
    genre: Optional[str]
    director: Optional[str]
    authors: Optional[str]
    cast: Optional[str]
    year: Optional[int]

class MovieCreate(MovieBase):
    pass


class ReviewBase(BaseModel):
    critic_name: Optional[str]
    top_critic: Optional[bool]
    score: Optional[int]
    review: Optional[str]

class ReviewCreate(ReviewBase):
    movie_id: int

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True

class Movie(MovieCreate):
    id: int
    #nest revies inside movies
    reviews: List[Review] = []

    class Config:
        from_attributes = True