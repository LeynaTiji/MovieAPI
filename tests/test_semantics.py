from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# mock AI call with patch
def test_returns_200_with_valid_link(client):
        with patch("app.hf_semantic_analysis.review_semantics", return_value=("POSITIVE", 0.95)):
            response = client.get("/reviews/semantics/by-link?movie_link=m/test_movie")
        assert response.status_code == 200