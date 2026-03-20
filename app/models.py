from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    info = Column(String)
    age = Column(String)
    genre = Column(String)
    director = Column(String)
    authors = Column(String)
    actors = Column(String)
    rating = Column(String)
    year = Column(Integer, index=True)
    link = Column(String, unique=True, index=True)

    reviews = relationship("Review", back_populates="movie")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_link = Column(String, ForeignKey("movies.link"), index=True)
    critic_name = Column(String, index=True)
    score = Column(String, index=True)
    review = Column(String, index=True)
    movie = relationship("Movie", back_populates="reviews")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
