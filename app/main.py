from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas, hf_semantic_analysis

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
@app.get("/movies", response_model=list[schemas.Movie])
def get_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# get movie by id
@app.get("/movies/by-id", response_model=list[schemas.MovieBase])
def get_movies_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(
        models.Movie.id == movie_id
    ).all()
    # reference from https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

# get movie by rotten tomatoes link
@app.get("/movies/by-link", response_model=list[schemas.MovieBase])
def get_movies_id(movie_link: str, db: Session = Depends(get_db)):
    movie =  db.query(models.Movie).filter(
        models.Movie.link == movie_link
    ).all()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie


#--- Review Endpoints---

# limit reviews to 50 per page 
@app.get("/reviews", response_model=list[schemas.Review])
def get_reviews(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Review).offset(skip).limit(limit).all()

# get review by rotten tomatoes movie link
@app.get("/reviews/by-link", response_model=list[schemas.Review])
def get_movies_id(review_link: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(
        models.Review.movie_link == review_link
    ).offset(skip).limit(limit).all()

    if not review:
        raise HTTPException(status_code=404, detail="Reviews not found")
    
    return review


# # summary and semantic analysis of reviews for specified movie
@app.get("/reviews/semantics/by-link", response_model=list[schemas.Review])
def get_review_semantics(movie_link: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(
        models.Review.movie_link == movie_link
    ).all()

    if not review:
        raise HTTPException(status_code=404, detail="Reviews not found")

    #iterate through reviews to get review text
    review_texts = [r.review for r in reviews]

    analysis = hf_semantic_analysis.summerise_reviews(review_texts)

    

    
    