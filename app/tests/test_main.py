from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_get_secure_data():
    response = client.get("/secure-data", headers={"Authorization": "Bearer <token>"})
    assert response.status_code == 200
    assert "message" in response.json()
