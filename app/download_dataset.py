import kagglehub
import pandas as pd
from sqlalchemy.orm import Session
from app import models, database

def load_dataset(db):
    # download latest version of rotten tomatoes dataset from kaggle
    path = kagglehub.dataset_download("stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset")

    print("Path to dataset files:", path)

    #csv metadata file paths
    movies_csv = f"{path}/rotten_tomatoes_movies.csv"
    reviews_csv = f"{path}/rotten_tomatoes_critic_reviews.csv"

    movies_df = pd.read_csv(movies_csv)
    reviews_df = pd.read_csv(reviews_csv)

    print(movies_df.columns)
    print(reviews_df.columns)

    #check if database already contains movies
    movie_count = db.query(models.Movie).count()
    review_count = db.query(models.Review).count()

    if movie_count > 0 & review_count > 0:
        print("Database already populated")
        return
    
    movie_ids = {}
    #insert movie from dataset into db
    for _, row in movies_df.iterrows():
        title = row.get("movie_title") or None
        age = row.get("content_rating") or None
        director = row.get("directors") or None
        genre = row.get("genres") or None
        authors = row.get("authors") or None

        #convert date into just year integer
        date = row.get("original_release_date")
        if pd.notna(date):
            try:
                year = pd.to_datetime(date).year
            except:
                year = None

        #map id to db movie id
        rt_link = row.get("id")

        movie = models.Movie(
            title = title,
            age=age,
            director=director,
            genre=genre,
            authors=authors,
            year=year
        )

        db.add(movie)
        
        #store id map to link with reviews
        movie_ids[rt_link] = movie.id

    db.commit()
    db.refresh(movie)

    # iterate through reviews csv
    for _, row in reviews_df.iterrows():
        rt_link = row.get("id")

        if rt_link not in movie_ids:
            continue
        
        review = models.Review(
            movie_id = movie_ids[rt_link],
            review=row.get("review_content", "") or None,
            critic_name = row.get("critic_name", "") or None,
            top_critic = row.get("top_critic", "") or None,
            score = row.get("review_score", "") or None,
        )

        db.add(review)

    db.commit()
    db.refresh(review)

    print("Dataset has loaded")
