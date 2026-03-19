from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_reviews():
    response =  client.get("/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reviews_by_link_house():
    response = client.get("/reviews/by-link?movie_link=m/10008706-house")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reviews_by_link_21():
    response = client.get("/reviews/by-link?movie_link=m/10009192-21")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reviews_by_link_404():
    response = client.get("/reviews/by-link?movie_link=m/nomovieexists")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reviews not found"

def test_get_review_by_link_missing_param():
    response = client.get("/reviews/by-link")
    assert response.status_code == 422
