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

def test_genre_popularity_yearly_breakdown_exists(client):
    response = client.get("/movies/genre/popularity")
    first_genre = response.json()["genres"][0]
    assert "yearly_breakdown" in first_genre
    assert isinstance(first_genre["yearly_breakdown"], list)

def test_genre_popularity_with_start_year(client):
    response = client.get("/movies/genre/popularity?start_year=2000")
    assert response.status_code == 200
    # check only movie1 (2010) should be returned, not movie2 (1995)
    genres = [g["genre"] for g in response.json()["genres"]]
    assert "Drama" in genres

def test_genre_popularity_with_end_year(client):
    response = client.get("/movies/genre/popularity?end_year=2000")
    assert response.status_code == 200
    # only movie2 (1995) should be returned
    genres = [g["genre"] for g in response.json()["genres"]]
    assert "Mystery & Suspense" in genres

def test_genre_popularity_with_year_range(client):
    response = client.get("/movies/genre/popularity?start_year=2005&end_year=2015")
    assert response.status_code == 200
    genres = [g["genre"] for g in response.json()["genres"]]
    assert "Drama" in genres

def test_genre_popularity_total_movies_is_int(client):
    response = client.get("/movies/genre/popularity")
    first_genre = response.json()["genres"][0]
    assert isinstance(first_genre["total_movies"], int)

def test_genre_popularity_no_data_returns_404(client):
    # year range with no movies
    response = client.get("/movies/genre/popularity?start_year=1800&end_year=1850")
    assert response.status_code == 404
    assert response.json()["detail"] == "No genre data found"