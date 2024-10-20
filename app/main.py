from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Medicamento, Pedido, EstadoEnvio, Formula, PedidoSchema, FormulaSchema
from app.database import  get_db
from app.schemas import MedicamentoCreate, PedidoCreate, FormulaCreate, EstadoFormulaUpdate
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

origins = [
    "http://localhost:4200", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/medicamentos/")
def obtener_todos_los_medicamentos(db: Session = Depends(get_db)):
    medicamentos = db.query(Medicamento).all()
    return medicamentos

@app.get("/pedidos/", response_model=List[PedidoSchema])
def obtener_todos_los_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    return pedidos

@app.get("/formulas/", response_model=List[FormulaSchema])
def obtener_todas_las_formulas(db: Session = Depends(get_db)):
    formulas = db.query(Formula).all()
    return formulas


@app.put("/pedidos/{pedido_id}/recibido/{medicamento_id}")
def actualizar_estado_a_recibido(pedido_id: int, medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return {"error": "Pedido no encontrado"}
    pedido.estado = EstadoEnvio.recibido
    medicamento.existencia += pedido.cantidad
    db.commit()
    return {"message": "Pedido actualizado a recibido y cantidad de medicamentos actualizada"}

@app.post("/medicamentos/")
def crear_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    
    medicamento_existente = db.query(Medicamento).filter(Medicamento.nombre == medicamento.nombre).first()
    if medicamento_existente:
        raise HTTPException(status_code=400, detail="El medicamento ya existe")

    nuevo_medicamento = Medicamento(
        nombre=medicamento.nombre,
        existencia=medicamento.existencia,
        gramaje=medicamento.gramaje
    )
    db.add(nuevo_medicamento)
    db.commit()
    db.refresh(nuevo_medicamento)
    
    return {"message": "Medicamento creado con éxito", "medicamento": nuevo_medicamento}

@app.post("/pedidos/")
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):

    medicamento = db.query(Medicamento).filter(Medicamento.id == pedido.medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")

    nuevo_pedido = Pedido(
        solicitante=pedido.solicitante,
        medicamento_id=pedido.medicamento_id,
        cantidad=pedido.cantidad
    )
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    return {"message": "Pedido creado ", "pedido": nuevo_pedido}

@app.post("/formulas/")
def crear_formula(formula: FormulaCreate, db: Session = Depends(get_db)):
    medicamento = db.query(Medicamento).filter(Medicamento.id == formula.medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    
    if medicamento.existencia < formula.cantidad:
        raise HTTPException(status_code=400, detail=f"El medicamento {medicamento.nombre} tiene existencia insuficiente")
    
    nueva_formula = Formula(
        nombre = formula.nombre,
        medicamento_id = formula.medicamento_id,
        cantidad = formula.cantidad  
    )
    medicamento.existencia -= formula.cantidad
    db.add(nueva_formula)
    db.commit()
    db.refresh(nueva_formula)
    
    return {"message": "Fórmula creada y cantidades actualizadas correctamente", "formula": nueva_formula}

@app.put("/formulas/{formula_id}/estado")
def actualizar_estado_formula(formula_id: int, estado_update: EstadoFormulaUpdate, db: Session = Depends(get_db)):

    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    
    if not formula:
        raise HTTPException(status_code=404, detail="Fórmula no encontrada")
    
    formula.estado = estado_update.estado
    
    db.commit()
    db.refresh(formula)
    
    return {"message": "Estado de la fórmula actualizado", "formula": formula}