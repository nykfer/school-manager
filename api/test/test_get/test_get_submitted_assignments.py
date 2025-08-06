from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_submitted_assignments():
    # Using assignment id 1 as example, handed_late True
    response = client.get("/get/submitted/assignments/1/?handed_late=true")
    assert response.status_code in (200, 404)  # Accept 404 if no data
    # If 200, should be a dict
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
