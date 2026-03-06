from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    rating: str
    genre: str

class Movie(MovieCreate):
    id: int

    class Config:
        orm_mode = True