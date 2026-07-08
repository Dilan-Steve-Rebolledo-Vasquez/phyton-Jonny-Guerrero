from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date 

# Este modelo controla lo que pide Swagger al CREAR (Solo cliente y fecha)
class FacturaCrear(SQLModel):
    cliente_id: int = Field(foreign_key="cliente.id")
    fecha: date = Field()

# Este modelo mapea la tabla exacta en PostgreSQL
class Factura(FacturaCrear, table=True):
    __tablename__: str = "factura"

    id: Optional[int] = Field(default=None, primary_key=True)
    valor_total: float = Field(default=0)