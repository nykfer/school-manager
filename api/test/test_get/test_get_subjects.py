from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_subjects():
    response = client.get("/get/subjects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
