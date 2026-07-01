from fastapi import APIRouter
from sqlmodel import select

from app.modelos.clientes import (
    Cliente,
    ClienteCrear,
    ClienteEditar
)

from ..conexion_bd import Sesion_dependencia

ruta_clientes = APIRouter()


@ruta_clientes.get("/clientes")
def listar_clientes(
    sesion: Sesion_dependencia
):
    clientes = sesion.exec(
        select(Cliente)
    ).all()

    return {
        "Clientes": clientes
    }


@ruta_clientes.get("/clientes/{id}")
def listar_cliente(
    id: int,
    sesion: Sesion_dependencia
):

    cliente = sesion.get(
        Cliente,
        id
    )

    if cliente:
        return cliente

    return {
        "mensaje": f"No existe cliente con id {id}"
    }


@ruta_clientes.post(
    "/clientes",
    response_model=Cliente
)
def crear_clientes(
    datos_cliente: ClienteCrear,
    sesion: Sesion_dependencia
):

    cliente_val = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    sesion.add(cliente_val)

    sesion.commit()

    sesion.refresh(cliente_val)

    return cliente_val


@ruta_clientes.put("/clientes/{id}")
def editar_clientes(
    id: int,
    datos_cliente: ClienteEditar,
    sesion: Sesion_dependencia
):

    cliente = sesion.get(
        Cliente,
        id
    )

    if cliente is None:
        return {
            "mensaje": f"No existe cliente con id {id}"
        }

    datos = datos_cliente.model_dump()

    cliente.nombre = datos["nombre"]
    cliente.edad = datos["edad"]
    cliente.descripcion = datos["descripcion"]

    sesion.add(cliente)

    sesion.commit()

    sesion.refresh(cliente)

    return {
        "mensaje": "Cliente actualizado",
        "Cliente": cliente
    }


@ruta_clientes.delete("/clientes/{id}")
def eliminar_cliente(
    id: int,
    sesion: Sesion_dependencia
):

    cliente = sesion.get(
        Cliente,
        id
    )

    if cliente is None:
        return {
            "mensaje": f"No existe cliente con id {id}"
        }

    sesion.delete(cliente)

    sesion.commit()

    return {
        "mensaje": "Cliente eliminado correctamente",
        "cliente": cliente
    }