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

def test_register_missing_username(client):
    response = client.post("/register", json={
        "password": "testpassword"
    })
    assert response.status_code == 422

def test_register_missing_password(client):
    response = client.post("/register", json={
        "username": "newuser"
    })
    assert response.status_code == 422
