from sqlalchemy import Column, Integer, String, Double
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    rating = Column(Double, index=True)
    genre = Column(String, index=True)

