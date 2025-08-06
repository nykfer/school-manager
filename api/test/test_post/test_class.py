from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_add_class():
    new_class = {"name": "10A", "teacher_id": 1}
    data = {"new_class":new_class,
            "schoolers":None}
    response = client.post("/add/class", json=data)
    assert response.status_code == 201
    assert "Added new class" in response.json()

def test_insert_class_missing_name():
    data = {
        "teacher_id": 0
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_class_missing_teacher_id():
    data = {
        "name": "11A"
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
