from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

# CONFIGURA AQUÍ TUS DATOS REALES DE DBEAVER
DATABASE_URL = "postgresql+psycopg2://postgres:YpBqmFM#1gX9*Yr2Jj9$7fy9XqYzje@localhost:5432/app_clientes"

engine = create_engine(DATABASE_URL)

# Generador de la sesión para las rutas
def obtener_sesion():
    with Session(engine) as sesion:
        yield sesion

# Variable que importamos en los enrutadores
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]