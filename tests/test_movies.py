from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id_1():
    response = client.get("/movies/by-id?movie_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id_269():
    response = client.get("/movies/by-id?movie_id=269")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id_not_found():
    response = client.get("/movies/by-id?movie_id=2000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

