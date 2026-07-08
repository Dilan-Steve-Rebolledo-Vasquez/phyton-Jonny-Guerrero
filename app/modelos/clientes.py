from sqlmodel import Field, SQLModel

class ClienteBase(SQLModel):
    nombre: str
    edad: int
    descripcion: str | None = None

class Cliente(ClienteBase, table=True):
    __tablename__ = "cliente"  # Forzamos el nombre exacto de la tabla en PostgreSQL
    id: int | None = Field(default=None, primary_key=True)

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass