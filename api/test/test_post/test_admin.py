from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_admin_success():
    data = {"name": "TestAdmin"}
    response = client.post("/add/admin", json=data)
    assert response.status_code == 201
    assert response.json() == "Added new admin - 5"

def test_insert_admin_no_name():
    data = {}
    response = client.post("/add/admin", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin name must be provided"

def test_insert_admin_empty_name():
    data = {"name": ""}
    response = client.post("/add/admin", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin name must be provided"