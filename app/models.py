from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    age = Column(String, index=True)
    genre = Column(String, index=True)
    director = Column(String, index=True)
    authors = Column(String, index=True)
    year = Column(Integer, index=True)
    reviews = relationship("Review", back_populates="movie")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), index=True)
    critic_name = Column(String, index=True)
    top_critic = Column(Boolean, index=True)
    score = Column(String, index=True)
    review = Column(String, index=True)
    movie = relationship("Movie", back_populates="reviews")


