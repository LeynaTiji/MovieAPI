from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_genre_popularity_200(client):
    response = client.get("/movies/genre/popularity")
    assert response.status_code == 200

def test_genre_popularity_genres_list(client):
    response = client.get("/movies/genre/popularity")
    assert "genres" in response.json()
    assert isinstance(response.json()["genres"], list)

def test_genre_popularity_contains_drama(client):
    response = client.get("/movies/genre/popularity")
    genres = [g["genre"] for g in response.json()["genres"]]
    assert "Drama" in genres