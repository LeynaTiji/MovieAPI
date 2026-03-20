from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_review_returns_201(client, auth_headers):
    response = client.post("/reviews", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    },
    headers=auth_headers
    )
    assert response.status_code == 200

def test_return_review_data(client, auth_headers):
    response = client.post("/reviews", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "/m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    },
    headers=auth_headers
    )
    body = response.json()
    #check values are correct as post
    assert body["critic_name"] == "Test Critic"
    assert body["review"] == "A fantastic film"  

def test_return_404(client, auth_headers):
    response = client.post("/reviews", json={
        "movie_id": 999,
        "critic_name": "Test Critic",
        "movie_link": "/m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    },
    headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

def test_update_review(client, auth_headers):
    response = client.put("/reviews/by-review-id?review_id=3", json={
        "movie_id": 2,
        "critic_name": "Updated Critic",
        "movie_link": "m/test_movie_2",
        "score": "9/10",
        "review": "Even better on rewatch"
    },
    headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["critic_name"] == "Updated Critic"
    assert response.json()["score"] == "9/10"

def test_update_review_not_found(client, auth_headers):
    response = client.put("/reviews/by-review-id?review_id=999", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "/m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    },
    headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_update_review_missing_id(client, auth_headers):
    response = client.put("/reviews/by-review-id", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "/m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    },
    headers=auth_headers
    )
    assert response.status_code == 422

def test_delete_review_returns_200(client, auth_headers):
    response = client.delete("/reviews/by-review-id?review_id=3", headers=auth_headers)
    assert response.status_code == 200
    assert "Review 3 deleted successfully" in response.json()["message"]

def test_delete_review_not_found(client, auth_headers):
        response = client.delete("/reviews/by-review-id?review_id=999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Review not found"

def test_delete_review_missing_id(client, auth_headers):
        response = client.delete("/reviews/by-review-id", headers=auth_headers)
        assert response.status_code == 422
