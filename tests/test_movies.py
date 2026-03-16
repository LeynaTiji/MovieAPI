from fastapi.testclient import TestClient
from app.main import app

from colours import Colour
client = TestClient(app)

def test_get_movies():
    print(f"{Colour.BLUE}Testing getting movies with limit of 50{Colour.RESET}")
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
