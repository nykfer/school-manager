from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_teacher():
    teacher = {"name": "Adam Smith", "age": 44, "subject_id": 3}
    response = client.post("/add/teacher", json=teacher)
    assert response.status_code == 201
    assert "Added new teacher" in response.json()

def test_insert_teacher_missing_name():
    data = {
        "age": 30,
        "subject_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_teacher_empty_name():
    data = {
        "name": "",
        "age": 30,
        "subject_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_teacher_missing_age():
    data = {
        "name": "TestTeacher",
        "subject_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_teacher_missing_subject_id():
    data = {
        "name": "TestTeacher",
        "age": 30
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"