from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_submit_assignment():
    submitted_assignment = {
        "schooler_id": 2,
        "assignment_id": 1,
        "work": "My solution"
    }
    response = client.post("/submit/assignment", json=submitted_assignment)
    assert response.status_code == 201
    assert "Assignment submitted successfully" in response.json()

def test_submit_assignment_missing_schooler_id():
    submitted_assignment = {
        "assignment_id": 1,
        "work": "My solution"
    }
    response = client.post("/submit/assignment", json=submitted_assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs for submitted assignment"

def test_submit_assignment_missing_assignment_id():
    submitted_assignment = {
        "schooler_id": 1,
        "work": "My solution"
    }
    response = client.post("/submit/assignment", json=submitted_assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs for submitted assignment"
    
def test_submit_assignment_missing_work():
    submitted_assignment = {
        "schooler_id":1,
        "assignment_id": 0,
        "work": ""
    }
    response = client.post("/submit/assignment", json=submitted_assignment)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs for submitted assignment"