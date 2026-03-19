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

def test_get_movie_by_id_missing_param():
    response = client.get("/movies/by-id")
    assert response.status_code == 422

def test_get_movie_by_link_oliver_twist():
    response = client.get("/movies/by-link?movie_link=m/10005499-oliver_twist")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_link_eye():
    response = client.get("/movies/by-link?movie_link=m/10008606-eye")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_404():
    response = client.get("/movies/by-link?movie_link=m/20666666666-car")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

def test_get_movie_by_link_missing_param():
    response = client.get("/movies/by-link")
    assert response.status_code == 422

    