from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_movies():
    print("Testing getting movies with limit of 50")
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
