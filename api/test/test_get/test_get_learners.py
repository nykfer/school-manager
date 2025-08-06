from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_learners_list_schooler():
    response = client.get("/get/learners/list/schooler")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_learners_list_teacher():
    response = client.get("/get/learners/list/teacher")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
