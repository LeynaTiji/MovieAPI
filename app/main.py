from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas
from .download_dataset import load_dataset

@asynccontextmanager
async def lifespan(app: FastAPI):
    #create tables automatically
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # automate loading dataset to db
    print("loading dataset...")
    load_dataset(db)

    db.close()
    yield

app = FastAPI(lifespan=lifespan)

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

# limit set to 50 to allow pagination of movies
@app.get("/movies")
def get_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# limit reviews to 50 per page 
@app.get("/reviews")
def get_reviews(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Review).offset(skip).limit(limit).all()
