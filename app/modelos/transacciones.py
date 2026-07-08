from sqlmodel import Field, SQLModel

class TransaccionesBase(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class Transacciones(TransaccionesBase, table=True):
    __tablename__ = "transacciones"  # Forzamos el nombre exacto de la tabla en PostgreSQL
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="factura.id")  # Relación directa con la tabla factura

class TransaccionesCrear(TransaccionesBase):
    pass

class TransaccionesEditar(TransaccionesBase):
    pass