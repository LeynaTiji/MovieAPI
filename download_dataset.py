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
