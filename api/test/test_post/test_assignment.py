from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_add_assignment():
    assignment = {
        "teacher_id": 1,
        "subject_id": 1,
        "title": "Homework 1",
        "description": "Solve problems 1-10",
        "assign_type": "homework",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/assignment", json=assignment)
    assert response.status_code == 201
    assert "New assignment was added" in response.json()

def test_insert_assignment_missing_teacher_id():
    assignment = {
        "subject_id": 1,
        "title": "Homework 1",
        "description": "Solve problems 1-10",
        "assign_type": "homework",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_assignment_missing_subject_id():
    assignment = {
        "teacher_id": 1,
        "title": "Homework 1",
        "description": "Solve problems 1-10",
        "assign_type": "homework",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_assignment_missing_title():
    assignment = {
        "teacher_id": 1,
        "subject_id": 1,
        "description": "Solve problems 1-10",
        "assign_type": "homework",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
    
def test_insert_assignment_missing_description():
    assignment = {
        "teacher_id": 1,
        "subject_id":1,
        "title": "Homework 1",
        "assign_type": "homework",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
    
def test_insert_assignment_missing_assign_type():
    assignment = {
        "teacher_id": 1,
        "subject_id": 1,
        "title": "Homework 1",
        "description": "Solve problems 1-10",
        "deadline": "2025-08-10"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"

def test_insert_assignment_missing_deadline():
    assignment = {
        "teacher_id": 1,
        "subject_id": 1,
        "title": "Homework 1",
        "description": "Solve problems 1-10",
        "assign_type": "homework"
    }
    response = client.post("/add/schooler", json=assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"