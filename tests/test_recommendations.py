from unittest.mock import patch
from app.main import app
from app.analysis import hf_semantic_analysis, reccomendations
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
