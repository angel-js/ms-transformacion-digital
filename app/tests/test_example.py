import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_example_endpoint():
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}  # Adjust based on actual response structure

def test_example_post():
    response = client.post("/api/v1/example", json={"data": "test"})
    assert response.status_code == 201
    assert response.json() == {"data": "test", "status": "success"}  # Adjust based on actual response structure