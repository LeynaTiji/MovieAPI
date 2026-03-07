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

db: Session = database.SessionLocal()

movie_ids = {}
#insert movie from dataset into db
for _, row in movies_df.iterrows():
    title = row.get("movie_title") or None
    info = row.get("movie_info") or None
    rating = row.get("critics_consensus") or None
    age = row.get("content_rating") or None
    director = row.get("directors") or None
    genre = row.get("genres") or None
    authors = row.get("authors") or None
    cast = row.get("actors") or None

    #convert date into just year integer
    year = None
    if pd.notna(row.get("original_release_date")):
        year = int(str(row["original_release_date"])[:4])

    #map rt link to db movie id
    rt_link = row.get("rotten_tomatoes_link")

    movie = models.Movie(
        title = title,
        info=info,
        rating=rating,
        age=age,
        director=director,
        genre=genre,
        authors=authors,
        cast=cast,
        year=year
    )

    db.add(movie)
    
    #store id map to link with reviews
    movie_ids[rt_link] = movie.id

db.commit()
db.refresh(movie)

# iterate through reviews csv
for _, row in reviews_df.iterrows():
    rt_link = row.get("rotten_tomatoes_link")

    if rt_link not in movie_ids:
        continue

    #convert date into just year integer
    score = None
    if pd.notna(row.get("review_score")):
        score = int(float(row["review_score"].split("/")[0]))
    
    review = models.Review(
        movie_id = movie_ids[rt_link],
        review=row.get("review_content", "") or None,
        critic_name = row.get("critic_name", "") or None,
        top_critic = row.get("top_critic", "") or None,
        score = score
    )

    db.add(review)

db.commit()
db.refresh(review)
