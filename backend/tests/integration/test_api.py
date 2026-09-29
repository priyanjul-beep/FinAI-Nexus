from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "FinAI Nexus"
    assert data["status"] == "OPERATIONAL"


def test_auth_login():
    res = client.post("/api/v1/auth/login", json={"email": "analyst@finai-nexus.io", "password": "analyst123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "ANALYST"
