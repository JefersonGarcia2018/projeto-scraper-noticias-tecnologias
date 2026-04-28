import pytest
from fastapi.testclient import TestClient
from main import app
import builtins

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_login_admin():
    # As the lifespan creates this user implicitly, we can try to login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_create_user_unauthorized():
    # Sem token de Admin
    response = client.post(
        "/api/v1/users/",
        json={"username": "colab2", "email": "colab2@teste.com", "password": "123", "role": "colaborador"}
    )
    assert response.status_code == 401
