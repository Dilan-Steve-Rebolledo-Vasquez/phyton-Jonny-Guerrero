from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends

# Nombre de la base de datos
nombre_bd = "bd_clientes_3407186.sqlite3"

# URL de conexión
url_bd = f"sqlite:///{nombre_bd}"

# Motor de la base de datos
motor_db = create_engine(
    url_bd,
    connect_args={"check_same_thread": False}
)

# Obtener sesión
def obtener_sesion():
    with Session(motor_db) as mi_sesion:
        yield mi_sesion

# Dependencia para FastAPI
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]

# Crear tablas
def crear_bd():
    SQLModel.metadata.create_all(motor_db)