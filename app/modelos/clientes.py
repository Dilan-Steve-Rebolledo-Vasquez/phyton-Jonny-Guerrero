from pydantic import BaseModel

# por continuar la explicacion
from sqlmodel import SQLModel, Field, Relationship

# tabla de ejemplo
# class ClienteEjemplo(SQLModel, table=True):
#     nombre: str = Field(default=None)
#     edad: int = Field(default=None)


class ClienteBase(BaseModel):
    # atributos
    nombre: str
    edad: int
    descripcion: str | None


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int | None = None