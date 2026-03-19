from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_review_returns_201(client):
        response = client.post("/reviews", json={
            "movie_id": 1,
            "critic_name": "Test Critic",
            "movie_link": "m/test_movie",
            "score": "8/10",
            "review": "A fantastic film"
        })
        assert response.status_code == 200
