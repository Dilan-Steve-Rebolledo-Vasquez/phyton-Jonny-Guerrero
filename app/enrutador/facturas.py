from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..conexion_bd import Sesion_dependencia

from ..modelos.clientes import Cliente

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
async def listar_facturas(
    sesion: Sesion_dependencia
):

    return sesion.exec(
        select(Factura)
    ).all()


# GET FACTURA POR ID
@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(
    id: int,
    sesion: Sesion_dependencia
):

    factura = sesion.get(
        Factura,
        id
    )

    if factura:
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
    datos_factura: FacturaCrear,
    sesion: Sesion_dependencia
):

    cliente_encontrado = sesion.get(
        Cliente,
        cliente_id
    )

    if not cliente_encontrado:

        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe"
        )

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.fecha = str(
        datetime.now()
    )

    factura_val.cliente_id = cliente_id

    sesion.add(
        factura_val
    )

    sesion.commit()

    sesion.refresh(
        factura_val
    )

    return factura_val


# PUT EDITAR FACTURA
@ruta_facturas.put("/facturas/{id}")
async def editar_factura(
    id: int,
    datos_factura: FacturaEditar,
    sesion: Sesion_dependencia
):

    factura = sesion.get(
        Factura,
        id
    )

    if not factura:

        return {
            "mensaje": f"No existe factura con id {id}"
        }

    factura.fecha = datos_factura.fecha
    factura.cliente_id = datos_factura.cliente_id

    sesion.add(
        factura
    )

    sesion.commit()

    sesion.refresh(
        factura
    )

    return {
        "mensaje": "Factura actualizada correctamente",
        "factura": factura
    }


# DELETE FACTURA
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(
    id: int,
    sesion: Sesion_dependencia
):

    factura = sesion.get(
        Factura,
        id
    )

    if not factura:

        return {
            "mensaje": f"No existe factura con id {id}"
        }

    sesion.delete(
        factura
    )

    sesion.commit()

    return {
        "mensaje": "Factura eliminada correctamente",
        "factura": factura
    }