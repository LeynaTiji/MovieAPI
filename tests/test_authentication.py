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

def test_register_duplicate_username(client):
    client.post("/register", json={
        "username": "duplicateuser",
        "password": "testpassword"
    })
    response = client.post("/register", json={
        "username": "duplicateuser",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username is taken"

def test_login_returns_200(client):
    client.post("/register", json={
        "username": "loginuser",
        "password": "testpassword"
    })
    response = client.post("/login", data={
        "username": "loginuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/register", json={
        "username": "loginuser3",
        "password": "testpassword"
    })
    response = client.post("/login", data={
        "username": "loginuser3",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_user_not_found(client):
    response = client.post("/login", data={
        "username": "doesnotexist",
        "password": "testpassword"
    })
    assert response.status_code == 401

def test_protected_endpoint_without_token(client):
    response = client.post("/reviews", json={
        "movie_id": 1,
        "critic_name": "Test Critic",
        "movie_link": "m/test_movie",
        "score": "8/10",
        "review": "A fantastic film"
    })
    assert response.status_code == 401

def test_protected_endpoint_with_token(client):
    response = client.post("/register", json={
        "username": "authuser",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    response = client.post("/reviews",
        json={
            "movie_id": 1,
            "critic_name": "Test Critic",
            "movie_link": "m/test_movie",
            "score": "8/10",
            "review": "A fantastic film"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_protected_endpoint_with_invalid_token(client):
    response = client.post("/reviews",
        json={
            "movie_id": 1,
            "critic_name": "Test Critic",
            "movie_link": "m/test_movie",
            "score": "8/10",
            "review": "A fantastic film"
        },
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    assert response.status_code == 401