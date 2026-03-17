from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

# create and manage database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
          
#default endpoint
@app.get("/")
def root():
    return {"message": "Movie API is running"}

# # update db with created movie
# @app.post("/movies", response_model=schemas.Movie)
# def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
#     db_movie = models.Movie(**movie.dict())
#     db.add(db_movie)
#     db.commit()
#     db.refresh(db_movie)
#     return db_movie

#--- Movie Endpoints---

# limit set to 50 to allow pagination of movies
@app.get("/movies")
def get_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# get movie by id
@app.get("/movies/by-id")
def get_movies_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(
        models.Movie.id == movie_id
    ).all()
    # reference from https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

# get movie by rotten tomatoes link
@app.get("/movies/by-link")
def get_movies_id(movie_link: str, db: Session = Depends(get_db)):
    movie =  db.query(models.Movie).filter(
        models.Movie.link == movie_link
    ).all()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

#--- Review Endpoints---

# limit reviews to 50 per page 
@app.get("/reviews")
def get_reviews(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Review).offset(skip).limit(limit).all()

# get review by rotten tomatoes movie link
@app.get("/reviews/by-link")
def get_movies_id(review_link = str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(
        models.Review.movie_link == review_link
    ).offset(skip).limit(limit).all()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review