from pydantic import BaseModel

class clienteBase(BaseModel):
    nombre: str
    edad: int
    descripcion: str | None 

class clienteCrear(clienteBase):
    pass

class clienteEditar(clienteBase):
    pass

class cliente(clienteBase):
    id: int | None = None