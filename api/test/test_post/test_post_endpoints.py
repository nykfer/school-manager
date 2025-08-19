"""
Test suite for POST endpoints in api/routers/post.py
Covers: Admin, Teacher, Schooler, Subject, Class, Assignment, SubmittedAssignment
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# Helper data for tests
def unique_email(prefix):
    import uuid
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"

def test_create_admin():
    data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": unique_email("admin"),
        "age": 30
    }
    response = client.post("/admins/", json=data)
    assert response.status_code == 201
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["email"] == data["email"]

def test_create_teacher():
    # Create subject and class first
    subj = client.post("/subjects/", json={"name": "Math"}).json()
    cls = client.post("/classes/", json={"name": "A1"}).json()
    data = {
        "first_name": "Teach",
        "last_name": "Er",
        "email": unique_email("teacher"),
        "age": 40,
        "subject_id": subj["id"],
        "class_id": cls["id"]
    }
    response = client.post("/teachers/", json=data)
    assert response.status_code == 201
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["email"] == data["email"]

def test_create_schooler():
    cls = client.post("/classes/", json={"name": "B1"}).json()
    data = {
        "first_name": "School",
        "last_name": "Er",
        "email": unique_email("schooler"),
        "age": 18,
        "class_id": cls["id"]
    }
    response = client.post("/schoolers/", json=data)
    assert response.status_code == 201
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["email"] == data["email"]

def test_create_subject():
    data = {"name": f"Subject_{unique_email('subj')}"}
    response = client.post("/subjects/", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]

def test_create_class():
    data = {"name": f"Class_{unique_email('cls')}"}
    response = client.post("/classes/", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]

def test_create_assignment():
    subj = client.post("/subjects/", json={"name": f"Subj_{unique_email('asgn')}"}).json()
    cls = client.post("/classes/", json={"name": f"Cls_{unique_email('asgn')}"}).json()
    teacher = client.post("/teachers/", json={
        "first_name": "T",
        "last_name": "A",
        "email": unique_email("asgn_teacher"),
        "age": 35,
        "subject_id": subj["id"],
        "class_id": cls["id"]
    }).json()
    data = {
        "teacher_id": teacher["id"],
        "subject_id": subj["id"],
        "title": f"Assignment {unique_email('asgntitle')}",
        "description": "Test assignment",
        "assign_type": "homework",
        "deadline": "2030-01-01"
    }
    response = client.post("/assignments/", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]

def test_submit_assignment():
    subj = client.post("/subjects/", json={"name": f"Subj_{unique_email('subm')}"}).json()
    cls = client.post("/classes/", json={"name": f"Cls_{unique_email('subm')}"}).json()
    teacher = client.post("/teachers/", json={
        "first_name": "T",
        "last_name": "B",
        "email": unique_email("subm_teacher"),
        "age": 36,
        "subject_id": subj["id"],
        "class_id": cls["id"]
    }).json()
    schooler = client.post("/schoolers/", json={
        "first_name": "S",
        "last_name": "B",
        "email": unique_email("subm_schooler"),
        "age": 17,
        "class_id": cls["id"]
    }).json()
    assignment = client.post("/assignments/", json={
        "teacher_id": teacher["id"],
        "subject_id": subj["id"],
        "title": f"Assignment {unique_email('subm_asgntitle')}",
        "description": "Test assignment",
        "assign_type": "homework",
        "deadline": "2030-01-01"
    }).json()
    data = {
        "schooler_id": schooler["id"],
        "assignment_id": assignment["id"],
        "work": "My homework"
    }
    response = client.post("/assignments/submit/", json=data)
    assert response.status_code == 201
    assert response.json()["work"] == data["work"]
