from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_classes():
    response = client.get("/get/classes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
