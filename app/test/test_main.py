from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_medicamento():
    response = client.post("/medicamentos/", json={"nombre": "Losartan", "existencia": 10, "gramaje": "50mg"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Losartan"
