from pydantic import BaseModel

class factura(BaseModel):
    id: int
    fecha: str
    total: int
    cliente: str | None