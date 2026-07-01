from fastapi import FastAPI

from .enrutador import clientes
from .enrutador import facturas
from .enrutador import transacciones
from .conexion_bd import crear_bd
from .modelos.clientes import Cliente
from .modelos.facturas import Factura
from .modelos.transacciones import Transacciones

app = FastAPI()

@app.on_event("startup")
def iniciar_bd():
    crear_bd()

app.include_router(
    clientes.ruta_clientes,
    tags=["Clientes"]
)

app.include_router(
    facturas.ruta_facturas,
    tags=["Facturas"]
)

app.include_router(
    transacciones.ruta_transacciones,
    tags=["Transacciones"]
)