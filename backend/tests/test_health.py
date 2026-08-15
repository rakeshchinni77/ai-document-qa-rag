import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data

def test_report_endpoint():
    response = client.get("/report")
    assert response.status_code == 200
    data = response.json()
    assert data["context_precision"] == 0.90
    assert data["faithfulness"] == 0.85
    assert data["system_status"] == "healthy"
