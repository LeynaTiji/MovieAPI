from unittest.mock import patch
from app.main import app
from app.analysis import hf_semantic_analysis
from fastapi.testclient import TestClient

client = TestClient(app)

# mock AI call with patch
def test_returns_200_with_valid_link(client):
        with patch("app.analysis.hf_semantic_analysis.review_semantics", return_value=("POSITIVE", 0.95)):
            response = client.get("/reviews/semantics/by-link?movie_link=m/test_movie")
        assert response.status_code == 200
        assert "sentiment_label" in response.json()
        assert "sentiment_score" in response.json()
        assert "movie" in response.json()

def test_returns_label(client):
        with patch("app.analysis.hf_semantic_analysis.review_semantics", return_value=("POSITIVE", 0.95)):
            response = client.get("/reviews/semantics/by-link?movie_link=m/test_movie")
        assert response.json()["sentiment_label"] == "POSITIVE"

def test_returns_score(client):
        with patch("app.analysis.hf_semantic_analysis.review_semantics", return_value=("POSITIVE", 0.95)):
            response = client.get("/reviews/semantics/by-link?movie_link=m/test_movie")
        assert response.json()["sentiment_score"] == 0.95

def test_no_reviews_returns_404( client):
        response = client.get("/reviews/semantics/by-link?movie_link=/m/no_reviews")
        assert response.status_code == 404
        assert response.json()["detail"] == "No reviews found"

