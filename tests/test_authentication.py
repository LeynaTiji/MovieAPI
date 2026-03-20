from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_register_returns_200(client):
    response = client.post("/register", json={
            "username": "newuser",
            "password": "testpassword"
        })
    assert response.status_code == 200

def test_register_returns_token(client):
    response = client.post("/register", json={
            "username": "newuser2",
            "password": "testpassword"
        })
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_register_missing_username(self, client):
    response = client.post("/register", json={
        "password": "testpassword"
    })
    assert response.status_code == 422
