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

def test_return_review_data(client):
    response = client.post("/reviews", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "/m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    })
    print(response.status_code)
    print(response.json())  # add this
    body = response.json()
    #check values are correct as post
    assert body["critic_name"] == "Test Critic"
    assert body["review"] == "A fantastic film"  