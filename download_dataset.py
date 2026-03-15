import kagglehub
import pandas as pd
from sqlalchemy.orm import Session
from app import models, database

# download latest version of rotten tomatoes dataset from kaggle
path = kagglehub.dataset_download("andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews")

print("Path to dataset files:", path)

#csv metadata file paths
movies_csv = f"{path}/rotten_tomatoes_movies.csv"
reviews_csv = f"{path}/rotten_tomatoes_movie_reviews.csv"

movies_df = pd.read_csv(movies_csv)
reviews_df = pd.read_csv(reviews_csv)

print(movies_df.columns)
print(reviews_df.columns)

db: Session = database.SessionLocal()

movie_ids = {}
#insert movie from dataset into db
for _, row in movies_df.iterrows():

    title = row.get("title") or None
    age = row.get("ratingContents") or None
    director = row.get("director") or None
    genre = row.get("genre") or None
    authors = row.get("writer") or None

    #convert date into just year integer
    date = row.get("releaseDateStreaming")
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
        review=row.get("reviewText", "") or None,
        critic_name = row.get("criticName", "") or None,
        top_critic = row.get("isTopCritic", "") or None,
        score = row.get("originalScore", "") or None,
    )

    db.add(review)

db.commit()
db.refresh(review)
