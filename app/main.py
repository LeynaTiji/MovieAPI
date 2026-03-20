from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import SessionLocal, engine, Base

from typing import Optional
from collections import defaultdict

from . import models, schemas, auth
from .analysis import hf_semantic_analysis, genre_analysis, reccomendations

app = FastAPI()

Base.metadata.create_all(bind=engine)

# create and manage database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# user registers sucessfully and recieves a unique token
@app.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    already_user = db.query(models.User).filter(models.User.username == user.username).first()

    if already_user:
        raise HTTPException(status_code=400, detail="Username is taken")
    
    db_user = models.User(
        username=user.username,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(db_user)
    db.commit()

    token = auth.create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer" }

# user logs in 
@app.post("/login", response_model=schemas.Token)
def login(input: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == input.username).first()
    verified = auth.verify_password(input.password, user.hashed_password)
    if not user or not verified:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = auth.create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

#default endpoint
@app.get("/")
def root():
    return {"message": "Movie API is running"}

#--------------------------------------------
#              Movie Endpoints
#--------------------------------------------


# limit set to 50 to allow pagination of movies
@app.get("/movies", response_model=list[schemas.Movie])
def get_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# get movie by id
@app.get("/movies/by-id", response_model=list[schemas.MovieBase])
def get_movies_id(movie_id: int = Query(..., description="Movie ID"), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(
        models.Movie.id == movie_id
    ).all()
    # reference from https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

# get movie by rotten tomatoes link
@app.get("/movies/by-link", response_model=list[schemas.MovieBase])
def get_movies_id(movie_link: str = Query(..., description="Rotten Tomatoes Movie Link"), db: Session = Depends(get_db)):
    movie =  db.query(models.Movie).filter(
        models.Movie.link == movie_link
    ).all()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

# analyse genre trends and popularity over the years
@app.get("/movies/genre/popularity", response_model=schemas.ListofGenres)
def get_genre_analysis(start_year: Optional[int] = Query(None, description="Filter from this year"), 
                       end_year: Optional[int] = Query(None, description="Filter to this year"), 
                       db: Session = Depends(get_db)):

    # build query of number of movies by genre and year where they don't equal none
    query = db.query(models.Movie.genre, 
                      models.Movie.year, 
                      func.count(models.Movie.id).label("count"),
                      ).filter(
                        models.Movie.genre.isnot(None), 
                        models.Movie.year.isnot(None),)
    
    #apply filters if passed in
    if start_year:
        query = query.filter(models.Movie.year >= start_year)
    if end_year:
        query = query.filter(models.Movie.year <= end_year)

    # group by genre and year
    genre_year_row = query.group_by(models.Movie.genre, models.Movie.year).all()

    if not genre_year_row:
        raise HTTPException(status_code=404, detail="No genre data found")
    
    # create dictionary
    genre_year_count = defaultdict(dict)
    # total movies per year
    total_movies = defaultdict(int)

    for all_genre, year, count in genre_year_row:
        #split genres when there are multiple per movie
        genres = [g.strip() for g in all_genre.split(",")]
        # add movie to total movies once
        total_movies[year] += count
        
        for genre in genres:
            # add count to each individual genre
            if year in genre_year_count[genre]:
                genre_year_count[genre][year] += count
            else:
                genre_year_count[genre][year] = count
    
    # returns genres in order of most movies made over the years specified
    popular_genres = genre_analysis.genre_popularity(genre_year_count, total_movies)

    return schemas.ListofGenres(
        genres=popular_genres
    )

# analyse genre trends and popularity over the decades, returning top 5 genres of each decade
@app.get("/movies/genre/decade_popularity", response_model=schemas.DecadeSummary)
def get_decade_analysis(start_year: Optional[int] = Query(None, description="Filter from this year"), 
                        end_year: Optional[int] = Query(None, description="Filter to this year"), 
                        db: Session = Depends(get_db)):

    # build query of number of movies by genre and year where they don't equal none
    query = db.query(models.Movie.genre, 
                      models.Movie.year, 
                      func.count(models.Movie.id).label("count"),
                      ).filter(
                        models.Movie.genre.isnot(None), 
                        models.Movie.year.isnot(None),)
    
    #apply filters if passed in
    if start_year:
        query = query.filter(models.Movie.year >= start_year)
    if end_year:
        query = query.filter(models.Movie.year <= end_year)

    # group by genre and year
    genre_year_row = query.group_by(models.Movie.genre, models.Movie.year).all()

    if not genre_year_row:
        raise HTTPException(status_code=404, detail="No genre data found")
    
    # create dictionary
    genre_year_count = defaultdict(dict)
    # total movies per year
    total_movies = defaultdict(int)

    for all_genre, year, count in genre_year_row:
        #split genres when there are multiple per movie
        genres = [g.strip() for g in all_genre.split(",")]
        # add movie to total movies once
        total_movies[year] += count
        
        for genre in genres:
            # add count to each individual genre
            if year in genre_year_count[genre]:
                genre_year_count[genre][year] += count
            else:
                genre_year_count[genre][year] = count
    
    # returns top 5 genres for each decade between years specified
    summary = genre_analysis.decade_summary(genre_year_count)

    return schemas.DecadeSummary(
        decades=summary
    )

# uses Anthropic API and db query to give movie recommendations based on users mood
@app.get("/movies/recommendations", response_model=schemas.MovieRecs)
def get_recommendations(mood: str = Query(..., description="Describe what you're in the mood for, e.g. 'something feel-good and lighthearted'"),
                        genre: Optional[str] = Query(None, description="Preferred genre e.g. 'Comedy'"),
                        decade: Optional[int] = Query(None, description="Preferred decade e.g 1990's"),
                        rec_number: int = Query(5, ge=1, le=20, description="Number of choices to pull from db"),
                        db: Session = Depends(get_db)):
    
    # convert year into decade incase inputted incorrectly
    if decade:
        decade = (decade // 10 ) * 10

    # initial query of db to movies
    movies = db.query(models.Movie).filter(
        models.Movie.genre.isnot(None),
        models.Movie.year.isnot(None),
    )

    if genre:
        movies = movies.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if decade: 
        movies = movies.filter(models.Movie.year >= decade)
        decade_end = decade + 9
        movies = movies.filter(models.Movie.year <= decade_end)
    
    # initial reccomendations to pass to api
    initial_recs = movies.order_by(func.random()).limit(rec_number * 3).all()

    if not initial_recs:
        raise HTTPException(status_code=404, detail="No movies found that match your filters. Please try again")
    
    ai_recs = reccomendations.AI_reccomendations(initial_recs, mood, rec_number)

    return schemas.MovieRecs(
        mood = mood,
        recommendations = ai_recs
    )

#--------------------------------------------
#              Review Endpoints
#--------------------------------------------

# limit reviews to 50 per page 
@app.get("/reviews", response_model=list[schemas.Review])
def get_reviews(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Review).offset(skip).limit(limit).all()

#create a review by id
@app.post("/reviews", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate,
                  db: Session = Depends(get_db)):
    # check movie exists 
    movie = db.query(models.Movie).filter(
        models.Movie.id == review.movie_id
    ).all()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db_review = models.Review(**review.model_dump(exclude={"movie_id"}))
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# update a review by id
@app.put("/reviews/by-review-id", response_model=schemas.Review)
def update_review(review: schemas.ReviewCreate, review_id: int = Query(..., description="Review ID"), db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # setattr to automatically update each field
    for field, value in review.model_dump(exclude={"movie_id"}).items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review

# delete a review by id
@app.delete("/reviews/by-review-id")
def delete_review(review_id: int = Query(..., description="Review ID"), db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"message": f"Review {review_id} deleted successfully"}

# get review by review id
@app.get("/reviews/by-id", response_model=list[schemas.Review])
def get_movies_id(review_id: str = Query(..., description="Review ID"), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(
        models.Review.id == review_id
    ).offset(skip).limit(limit).all()

    if not review:
        raise HTTPException(status_code=404, detail="Reviews not found")
    
    return review

# get review by rotten tomatoes movie link
@app.get("/reviews/by-link", response_model=list[schemas.Review])
def get_movies_id(movie_link: str = Query(..., description="Rotten Tomatoes Movie Link"), skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(
        models.Review.movie_link == movie_link
    ).offset(skip).limit(limit).all()

    if not review:
        raise HTTPException(status_code=404, detail="Reviews not found")
    
    return review

# semantic analysis of reviews for specified movie
@app.get("/reviews/semantics/by-link", response_model=schemas.AIReviewAnalysis)
def get_review_semantics(movie_link: str = Query(..., description="Rotten Tomatoes Movie Link"), db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(
        models.Review.movie_link == movie_link
    ).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    movie =  db.query(models.Movie).filter(
        models.Movie.link == movie_link
    ).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    #iterate through reviews to get review text
    review_texts = [r.review for r in reviews if r.review is not None]

    label, score = hf_semantic_analysis.review_semantics(review_texts)

    return schemas.AIReviewAnalysis(
        movie=movie,
        sentiment_label=label,
        sentiment_score=score
    )

    
    