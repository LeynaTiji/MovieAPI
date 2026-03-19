from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movies_by_id():
    response = client.get("/movies/by-id?movie_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movies_by_id():
    response = client.get("/movies/by-id?movie_id=269")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movies_by_id():
    response = client.get("/movies/by-id?movie_id=2000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"