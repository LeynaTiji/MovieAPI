from unittest.mock import patch
from app.main import app
from app.analysis import reccomendations
from fastapi.testclient import TestClient

client = TestClient(app)

MOCK_AI_RECS = [
    {
        "movie_title": "Test Movie",
        "year": 2010,
        "genre": "Drama",
        "reason": "A drama you will love that matches your mood perfectly."
    }
]

def test_recommendations_returns_200(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something dramatic")
    assert response.status_code == 200

def test_recommendations_returns_mood(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something dramatic")
    assert response.json()["mood"] == "something dramatic"

def test_recommendations_returns_list(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something dramatic")
    assert isinstance(response.json()["recommendations"], list)

def test_recommendations_with_genre_filter(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something dramatic&genre=Drama")
    assert response.status_code == 200

def test_recommendations_decade(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something classic&decade=2013")
    assert response.status_code == 200

def test_recommendations_all_inputs(client):
    with patch("app.analysis.reccomendations.AI_reccomendations", return_value=MOCK_AI_RECS):
        response = client.get("/movies/recommendations?mood=something classic&genre=Drama&decade=2013&rec_number=5")
    assert response.status_code == 200

def test_recommendations_no_movies_returns_404(client):
    response = client.get("/movies/recommendations?mood=something dramatic&decade=1800")
    assert response.status_code == 404

def test_recommendations_rec_number_too_high(client):
    response = client.get("/movies/recommendations?mood=something dramatic&rec_number=99")
    assert response.status_code == 422

def test_recommendations_rec_number_too_low(client):
    response = client.get("/movies/recommendations?mood=something dramatic&rec_number=0")
    assert response.status_code == 422

def test_recommendations_mood_required(client):
    response = client.get("/movies/recommendations")
    assert response.status_code == 422
