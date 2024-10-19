
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from pydantic import BaseModel

class EstadoEnvio(enum.Enum):
    solicitado = "Solicitado"
    en_proceso = "En proceso"
    enviado = "Enviado"
    recibido = "Recibido"

class Medicamento(Base):
    __tablename__ = 'medicamentos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    existencia = Column(Integer)
    gramaje = Column(String)

class Formula(Base):
    __tablename__ = 'formulas'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    medicamento_id = Column(Integer, ForeignKey('medicamentos.id'))
    cantidad = Column(Integer)
    estado = Column(Enum(EstadoEnvio), default=EstadoEnvio.solicitado)
    medicamento = relationship("Medicamento")

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True)
    solicitante = Column(String)
    medicamento_id = Column(Integer, ForeignKey('medicamentos.id'))
    cantidad = Column(Integer)
    estado = Column(Enum(EstadoEnvio), default=EstadoEnvio.solicitado)

    medicamento = relationship("Medicamento")

class MedicamentoSchema(BaseModel):
    id: int
    nombre: str  
    class Config:
        orm_mode = True

class PedidoSchema(BaseModel):
    id: int
    solicitante: str
    medicamento: MedicamentoSchema  
    cantidad: int
    estado: EstadoEnvio

    class Config:
        orm_mode = True
        
        
class FormulaSchema(BaseModel):
    id: int
    nombre: str
    medicamento_id :int
    cantidad: int
    estado: EstadoEnvio
    medicamento: MedicamentoSchema
    
    class Config:
        orm_mode = True