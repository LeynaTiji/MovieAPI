import kagglehub
import pandas as pd
from app import models
from app.database import SessionLocal

def clean(value):
    if pd.isna(value):
        return None
    return value

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

        title = clean(row.get("movie_title"))
        info = clean(row.get("movie_info"))
        age = clean(row.get("content_rating"))
        director = clean(row.get("directors"))
        genre = clean(row.get("genres"))
        authors = clean(row.get("authors"))
        actors = clean(row.get("actors"))
        link = clean(row.get("rotten_tomatoes_link"))

        #convert rating to string
        rating = str(row.get("audience_rating")) if pd.notna(row.get("audience_rating")) else None


        #convert date into just year integer
        date = row.get("original_release_date")
        if pd.notna(date):
            try:
                year = pd.to_datetime(date).year
            except:
                year = None
        else:
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

    # iterate through reviews csv
    for _, row in reviews_df.iterrows():
        rt_link = row.get("rotten_tomatoes_link")

        if rt_link not in movie_links:
            continue
        
        movie_review = models.Review(
            movie_link = movie_links[rt_link],
            review=clean(row.get("review_content")),
            critic_name = clean(row.get("critic_name")),
            score = clean(row.get("review_score")),
        )

        db.add(movie_review)


    db.commit()

    print("Dataset has loaded")


if __name__ == "__main__":
    load_dataset()