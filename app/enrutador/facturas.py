from datetime import datetime
from fastapi import APIRouter, HTTPException

from ..listas_app import (
    lista_clientes,
    lista_facturas
)

from ..modelos.facturas import (
    Factura,
    FacturaCrear,
    FacturaEditar
)

ruta_facturas = APIRouter()


# GET TODAS LAS FACTURAS
@ruta_facturas.get(
    "/facturas",
    response_model=list[Factura]
)
async def listar_facturas():
    return lista_facturas


# GET FACTURA POR ID
@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(id: int):

    for factura in lista_facturas:

        if factura.id == id:
            return factura

    return {
        "mensaje": f"No existe factura con id {id}"
    }


# POST CREAR FACTURA
@ruta_facturas.post(
    "/facturas/{cliente_id}",
    response_model=Factura
)
async def crear_facturas(
    cliente_id: int,
    datos_factura: FacturaCrear
):

    cliente_encontrado = None

    for cliente in lista_clientes:

        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:

        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe"
        )

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = str(datetime.now())
    factura_val.cliente = cliente_encontrado

    lista_facturas.append(factura_val)

    return factura_val


# PUT EDITAR FACTURA
@ruta_facturas.put("/facturas/{id}")
async def editar_factura(
    id: int,
    datos_factura: FacturaEditar
):

    for i, factura in enumerate(lista_facturas):

        if factura.id == id:

            factura_editada = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_editada.id = id

            lista_facturas[i] = factura_editada

            return {
                "mensaje": "Factura actualizada correctamente",
                "factura": factura_editada
            }

    return {
        "mensaje": f"No existe factura con id {id}"
    }


# DELETE FACTURA
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int):

    for i, factura in enumerate(lista_facturas):

        if factura.id == id:

            factura_eliminada = lista_facturas.pop(i)

            return {
                "mensaje": "Factura eliminada correctamente",
                "factura": factura_eliminada
            }

    return {
        "mensaje": f"No existe factura con id {id}"
    }