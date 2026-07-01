from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..listas_app import (
    lista_clientes,
    lista_facturas,
    lista_transacciones
)

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
async def listar_transacciones():
    return lista_transacciones


@ruta_transacciones.get("/transacciones/{id}")
async def obtener_transaccion(id: int):

    for transaccion in lista_transacciones:

        if transaccion.id == id:
            return transaccion

    return {
        "mensaje": f"No existe transaccion con id {id}"
    }


@ruta_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionesCrear,
    cliente_id: int
):

    cliente_encontrado = None

    for c in lista_clientes:

        if c.id == cliente_id:
            cliente_encontrado = c
            break

    if not cliente_encontrado:

        raise HTTPException(
            status_code=400,
            detail=f"No existe cliente con id {cliente_id}"
        )

    factura_encontrada = None

    for f in lista_facturas:

        if f.id == factura_id:
            factura_encontrada = f
            break

    if factura_encontrada:

        if factura_encontrada.cliente.id == cliente_id:

            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = len(lista_transacciones) + 1
            transaccion_val.factura_id = factura_id

            lista_transacciones.append(
                transaccion_val
            )

            factura_encontrada.transacciones.append(
                transaccion_val
            )

            return {
                "mensaje": f"Transaccion agregada a factura {factura_encontrada.id}",
                "factura": factura_encontrada
            }

        return {
            "mensaje": "La factura pertenece a otro cliente",
            "factura": factura_encontrada
        }

    transaccion_val = Transacciones.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.id = len(lista_transacciones) + 1
    transaccion_val.factura_id = len(lista_facturas) + 1

    factura = FacturaCrear(
        cliente=cliente_encontrado,
        fecha=str(datetime.now()),
        transacciones=[transaccion_val]
    )

    factura_val = Factura.model_validate(
        factura.model_dump()
    )

    factura_val.id = len(lista_facturas) + 1

    lista_facturas.append(factura_val)
    lista_transacciones.append(transaccion_val)

    return {
        "mensaje": "Factura creada automáticamente",
        "transaccion": transaccion_val
    }


@ruta_transacciones.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar
):

    for i, transaccion in enumerate(lista_transacciones):

        if transaccion.id == id:

            transaccion_editada = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_editada.id = id
            transaccion_editada.factura_id = transaccion.factura_id

            lista_transacciones[i] = transaccion_editada

            return {
                "mensaje": "Transaccion actualizada correctamente",
                "transaccion": transaccion_editada
            }

    return {
        "mensaje": f"No existe transaccion con id {id}"
    }


@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for i, transaccion in enumerate(lista_transacciones):

        if transaccion.id == id:

            transaccion_eliminada = lista_transacciones.pop(i)

            return {
                "mensaje": "Transaccion eliminada correctamente",
                "transaccion": transaccion_eliminada
            }

    return {
        "mensaje": f"No existe transaccion con id {id}"
    }