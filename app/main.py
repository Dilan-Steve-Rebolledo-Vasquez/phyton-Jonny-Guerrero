from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from .conexion_bd import engine
from .enrutador.clientes import ruta_clientes
from .enrutador.facturas import ruta_facturas
from .enrutador.transacciones import ruta_transacciones

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# Registrar enrutadores independientes
app.include_router(ruta_clientes)
app.include_router(ruta_facturas)
app.include_router(ruta_transacciones)