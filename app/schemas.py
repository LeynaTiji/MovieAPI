from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MovieBase(BaseModel):
    title: Optional[str]
    info: Optional[str]
    rating: Optional[str]
    age: Optional[str]
    genre: Optional[str]
    director: Optional[str]
    authors: Optional[str]
    actors: Optional[str]
    year: Optional[int]
    link: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class MovieCreate(MovieBase):
    pass

class Movie(MovieCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    critic_name: Optional[str]
    movie_link: Optional[str]
    score: Optional[str]
    review: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(ReviewBase):
    movie_id: int

class Review(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Movie_Review(Movie):
    
    #nest revies inside movies
    reviews: List[Review] = []

    model_config = ConfigDict(from_attributes=True)


class AI_Review_Analysis(BaseModel):
    movie: Movie
    label: Optional[str]
    score: Optional[float]

    model_config = ConfigDict(from_attributes=True)

