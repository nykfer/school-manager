from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_teacher_success():
    data = {
        "name": "TestTeacher",
        "age": 30,
        "subject_id": 1,
        "class_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 201
    assert "Added new teacher - TestTeacher" in response.json()

def test_insert_teacher_missing_name():
    data = {
        "age": 30,
        "subject_id": 1,
        "class_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin name must be provided" or "Invalid data inputs"

def test_insert_teacher_empty_name():
    data = {
        "name": "",
        "age": 30,
        "subject_id": 1,
        "class_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Name cannot be an empty string"

def test_insert_teacher_missing_age():
    data = {
        "name": "TestTeacher",
        "subject_id": 1,
        "class_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_teacher_missing_subject_id():
    data = {
        "name": "TestTeacher",
        "age": 30,
        "class_id": 1
    }
    response = client.post("/add/teacher", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
