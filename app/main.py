from fastapi import FastAPI

from .enrutador import clientes
from .enrutador import facturas
from .enrutador import transacciones

app = FastAPI()

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