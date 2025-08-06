from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_admin():
    admin = {"name": "John Doe"}
    response = client.post("/add/admin", json=admin)
    assert response.status_code == 201
    assert "Added new admin" in response.json()
    
def test_insert_admin_empty_name():
    admin = {"name": ""}
    response = client.post("/add/admin", json=admin)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin name must be provided"

def test_insert_admin_empty_item():
    admin = {}
    response = client.post("/add/admin", json=admin)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin name must be provided"