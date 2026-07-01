from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..conexion_bd import Sesion_dependencia

from ..modelos.clientes import Cliente

from ..modelos.facturas import (
    Factura,
    FacturaCrear
)

from ..modelos.transacciones import (
    Transacciones,
    TransaccionesCrear,
    TransaccionesEditar
)

ruta_transacciones = APIRouter()


@ruta_transacciones.get(
    "/transacciones",
    response_model=list[Transacciones]
)
async def listar_transacciones(
    sesion: Sesion_dependencia
):
    return sesion.exec(
        select(Transacciones)
    ).all()


@ruta_transacciones.get("/transacciones/{id}")
async def obtener_transaccion(
    id: int,
    sesion: Sesion_dependencia
):

    transaccion = sesion.get(
        Transacciones,
        id
    )

    if transaccion:
        return transaccion

    return {
        "mensaje": f"No existe transaccion con id {id}"
    }


@ruta_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionesCrear,
    cliente_id: int,
    sesion: Sesion_dependencia
):

    cliente_encontrado = sesion.get(
        Cliente,
        cliente_id
    )

    if not cliente_encontrado:

        raise HTTPException(
            status_code=400,
            detail=f"No existe cliente con id {cliente_id}"
        )

    factura_encontrada = sesion.get(
        Factura,
        factura_id
    )

    if factura_encontrada:

        if factura_encontrada.cliente_id == cliente_id:

            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.factura_id = factura_id

            sesion.add(
                transaccion_val
            )

            sesion.commit()

            sesion.refresh(
                transaccion_val
            )

            return {
                "mensaje": f"Transaccion agregada a factura {factura_id}",
                "transaccion": transaccion_val
            }

        return {
            "mensaje": "La factura pertenece a otro cliente"
        }

    transaccion_val = Transacciones.model_validate(
        datos_transaccion.model_dump()
    )

    factura = FacturaCrear(
        cliente_id=cliente_id,
        fecha=str(datetime.now())
    )

    factura_val = Factura.model_validate(
        factura.model_dump()
    )

    sesion.add(
        factura_val
    )

    sesion.commit()

    sesion.refresh(
        factura_val
    )

    transaccion_val.factura_id = factura_val.id

    sesion.add(
        transaccion_val
    )

    sesion.commit()

    sesion.refresh(
        transaccion_val
    )

    return {
        "mensaje": "Factura creada automáticamente",
        "transaccion": transaccion_val
    }


@ruta_transacciones.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar,
    sesion: Sesion_dependencia
):

    transaccion = sesion.get(
        Transacciones,
        id
    )

    if not transaccion:

        return {
            "mensaje": f"No existe transaccion con id {id}"
        }

    transaccion.cantidad = datos_transaccion.cantidad
    transaccion.vr_unitario = datos_transaccion.vr_unitario
    transaccion.descripcion = datos_transaccion.descripcion

    sesion.add(
        transaccion
    )

    sesion.commit()

    sesion.refresh(
        transaccion
    )

    return {
        "mensaje": "Transaccion actualizada correctamente",
        "transaccion": transaccion
    }


@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(
    id: int,
    sesion: Sesion_dependencia
):

    transaccion = sesion.get(
        Transacciones,
        id
    )

    if not transaccion:

        return {
            "mensaje": f"No existe transaccion con id {id}"
        }

    sesion.delete(
        transaccion
    )

    sesion.commit()

    return {
        "mensaje": "Transaccion eliminada correctamente",
        "transaccion": transaccion
    }