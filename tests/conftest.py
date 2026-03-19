import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app, get_db, models
from app.database import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

#separate db connection

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# override it with test database so API requests tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# seed db
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    
    # insert test data
    db = TestingSessionLocal()
    movie1 = models.Movie(
        id=1,
        title="Test Movie",
        info="A movie about a lot of things",
        age="PG15",
        director="David Jane",
        authors = "Jane Doe, Ben King, Damien",
        actors = "Emma Age, Cleo, Aidan Hell",
        genre="Drama",
        year=2010,
        rating="8.0",
        link="m/test_movie"
    )
    review1 = models.Review(
        id=1,
        movie_link="m/test_movie",
        review="Great film",
        score="8/10",
        critic_name="Test Critic"
    )
    db.add(movie1)
    db.add(review1)

    movie2 = models.Movie(
    id=2,
    title="Test Movie 2",
    info="A thriller about mystery and suspense",
    age="18",
    director="Sarah Collins",
    authors="John Smith, Mary Lane",
    actors="Tom Black, Sarah White, James Grey",
    genre="Mystery & Suspense, Thriller",
    year=1995,
    rating="7.5",
    link="m/test_movie_2"
    )
    review2 = models.Review(
        id=2,
        movie_link="m/test_movie_2",
        review="A gripping and tense watch from start to finish",
        score="7/10",
        critic_name="Jane Reviewer"
    )
    db.add(movie2)
    db.add(review2)
    
    db.commit()
    db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)

# configure client to test db
@pytest.fixture
def client(setup_database):
    with TestClient(app) as client:
        yield client