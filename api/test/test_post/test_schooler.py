from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_schooler():
    schooler = {"name": "Alex", "age": 15, "class_id": 1}
    response = client.post("/add/schooler", json=schooler)
    assert response.status_code == 201
    assert "Added new schooler" in response.json()

def test_insert_schooler_empty_name():
    schooler = {"name": "", "age": 15, "class_id": 1}
    response = client.post("/add/schooler", json=schooler)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
    
def test_insert_schooler_missing_name():
    schooler = {"age": 15, "class_id": 1}
    response = client.post("/add/schooler", json=schooler)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
    
def test_insert_schooler_missing_age():
    schooler = {"name": "Alex", "class_id": 1}
    response = client.post("/add/schooler", json=schooler)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_schooler_missing_class_id():
    schooler = {"name": "Alex", "age": 15}
    response = client.post("/add/schooler", json=schooler)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"