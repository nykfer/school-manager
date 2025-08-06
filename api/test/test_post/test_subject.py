from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_insert_subject():
    subject = {"name":"Physic"}
    response = client.post("/add/subject", json=subject)
    
    assert response.status_code == 201
    assert "Added new subject -" in response.json()

def test_insert_subject_empty_name():
    subject = {"name":""}
    response = client.post("/add/subject", json=subject)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"
    
def test_insert_empty_item():
    subject = {}
    response = client.post("/add/subject", json=subject)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data inputs"