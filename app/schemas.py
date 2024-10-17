from pydantic import BaseModel
from typing import List
from app.models import EstadoEnvio

class MedicamentoCreate(BaseModel):
    nombre: str
    existencia: int
    gramaje: str
    
class PedidoCreate(BaseModel):
    solicitante: str
    medicamento_id: int
    cantidad: int
    
class MedicamentoEnFormula(BaseModel):
    medicamento_id: int
    cantidad: int

class FormulaCreate(BaseModel):
    nombre: str
    medicamentos: List[MedicamentoEnFormula]
    
class EstadoFormulaUpdate(BaseModel):
    estado: EstadoEnvio  