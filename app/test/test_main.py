from fastapi.testclient import TestClient
from app.main import app
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def test_create_medicamento():
    response = client.post("/medicamentos/", json={"nombre": "Losartan2", "existencia": 10, "gramaje": "50mg"})
    assert response.status_code == 200
    assert response.json()["medicamento"]["nombre"] == "Losartan2"
    assert response.json()["medicamento"]["existencia"] == 10
    assert response.json()["medicamento"]["gramaje"] == "50mg"

def test_obtener_todos_los_medicamentos():
    response = client.get("/medicamentos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test_create_pedido():
    client.post("/medicamentos/", json={"nombre": "Paracetamol", "existencia": 20, "gramaje": "500mg"})
    
    response = client.post("/pedidos/", json={"solicitante": "Cliente1", "medicamento_id": 1, "cantidad": 5})
    assert response.status_code == 200
    assert response.json()["pedido"]["solicitante"] == "Cliente1"
    assert response.json()["pedido"]["cantidad"] == 5

def test_create_pedido():
    client.post("/medicamentos/", json={"nombre": "Paracetamol", "existencia": 20, "gramaje": "500mg"})
    
    response = client.post("/pedidos/", json={"solicitante": "Cliente1", "medicamento_id": 1, "cantidad": 5})
    assert response.status_code == 200
    assert response.json()["pedido"]["solicitante"] == "Cliente1"
    assert response.json()["pedido"]["cantidad"] == 5

def test_obtener_todos_los_pedidos():
    response = client.get("/pedidos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test_create_formula():
    client.post("/medicamentos/", json={"nombre": "Ibuprofeno", "existencia": 50, "gramaje": "200mg"})
    
    response = client.post("/formulas/", json={"nombre": "Formula1", "medicamento_id": 1, "cantidad": 10})
    assert response.status_code == 200
    assert response.json()["formula"]["nombre"] == "Formula1"
    assert response.json()["formula"]["cantidad"] == 10

def test_actualizar_estado_a_recibido():
    client.post("/medicamentos/", json={"nombre": "Aspirina", "existencia": 30, "gramaje": "100mg"})
    client.post("/pedidos/", json={"solicitante": "Cliente2", "medicamento_id": 1, "cantidad": 5})

    response = client.put("/pedidos/1/recibido/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Pedido actualizado a recibido y cantidad de medicamentos actualizada"

def test_actualizar_estado_formula():
    client.post("/medicamentos/", json={"nombre": "Antibiótico", "existencia": 50, "gramaje": "500mg"})
    client.post("/formulas/", json={"nombre": "Formula2", "medicamento_id": 1, "cantidad": 5})

    response = client.put("/formulas/1/estado", json={"estado": "Recibido"})
    assert response.status_code == 200
    assert response.json()["formula"]["estado"] == "Recibido"
