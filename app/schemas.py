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

class Review(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(ReviewBase):
    movie_id: int

class Movie_Review(Movie):
    
    #nest revies inside movies
    reviews: List[Review] = []

    model_config = ConfigDict(from_attributes=True)

class YearlySummary(BaseModel):
    year: int
    count: int
    percentage: float

class PopularGenre(BaseModel):
    genre: str
    total_movies: int
    yearly_breakdown: list[YearlySummary]

class ListofGenres(BaseModel):
    genres: list[PopularGenre]

    model_config = ConfigDict(from_attributes=True)

class Genre(BaseModel):
    genre: str
    count: int
    percentage: float

class TopGenresDecade(BaseModel):
    decade: str
    total_movies: int
    top_genres: list[Genre]

class DecadeSummary(BaseModel):
    decades: list[TopGenresDecade]

    model_config = ConfigDict(from_attributes=True)



class AIReviewAnalysis(BaseModel):
    movie: Movie
    sentiment_label: Optional[str]
    sentiment_score: Optional[float]

    model_config = ConfigDict(from_attributes=True)



class MovieRecommendation(BaseModel):
    movie_title: str
    year: int
    genre: str
    reason: str

class MovieRecs(BaseModel):
    mood: str
    recommendations: list[MovieRecommendation]
    
    model_config = ConfigDict(from_attributes=True)
