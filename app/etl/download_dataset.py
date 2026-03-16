import kagglehub
import pandas as pd
from app import models
from app.database import SessionLocal

def load_dataset():

    print("loading dataset...")

    # download latest version of rotten tomatoes dataset from kaggle
    path = kagglehub.dataset_download("stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset")

    #csv metadata file paths
    movies_csv = f"{path}/rotten_tomatoes_movies.csv"
    reviews_csv = f"{path}/rotten_tomatoes_critic_reviews.csv"

    movies_df = pd.read_csv(movies_csv)
    reviews_df = pd.read_csv(reviews_csv)

    # print(movies_df.columns)
    # print(reviews_df.columns)

    db = SessionLocal()
    
    movie_links = {}
    #insert movie from dataset into db
    for _, row in movies_df.iterrows():
        title = row.get("movie_title") or None
        info = row.get("movie_info") or None
        age = row.get("content_rating") or None
        director = row.get("directors") or None
        genre = row.get("genres") or None
        authors = row.get("authors") or None
        actors = row.get("actors") or None
        rating = row.get("audience_rating") or None
        link = row.get("rotten_tomatoes_link") or None

        #convert date into just year integer
        date = row.get("original_release_date")
        if pd.notna(date):
            try:
                year = pd.to_datetime(date).year
            except:
                year = None

        movie = models.Movie(
            title = title,
            info=info,
            age=age,
            director=director,
            genre=genre,
            authors=authors,
            actors=actors,
            rating=rating,
            year=year,
            link=link

        )

        db.add(movie)
        
        #store id map to link with reviews
        movie_links[link] = movie.link

    db.commit()
    db.refresh(movie)

    # iterate through reviews csv
    for _, row in reviews_df.iterrows():
        rt_link = row.get("rotten_tomatoes_link")

        if rt_link not in movie_links:
            continue
        
        movie_review = models.Review(
            movie_link = movie_links[rt_link],
            review=row.get("review_content", "") or None,
            critic_name = row.get("critic_name", "") or None,
            score = row.get("review_score", "") or None,
        )

        db.add(movie_review)

    db.commit()
    db.refresh(movie_review)

    print("Dataset has loaded")


if __name__ == "__main__":
    load_dataset()