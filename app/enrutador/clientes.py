from fastapi import APIRouter
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from ..listas_app import lista_clientes

ruta_clientes = APIRouter()


@ruta_clientes.get("/clientes")
async def listar_clientes():
    return {"Clientes": lista_clientes}


@ruta_clientes.get("/clientes/{id}")
async def listar_cliente(id: int):

    for cliente in lista_clientes:

        if cliente.id == id:
            return cliente

    return {
        "mensaje": f"No existe cliente con id {id}"
    }


@ruta_clientes.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):

    cliente_val = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    cliente_val.id = len(lista_clientes) + 1

    lista_clientes.append(cliente_val)

    return cliente_val


@ruta_clientes.put("/clientes/{id}")
def editar_clientes(id: int, datos_cliente: ClienteEditar):

    for i, obj_cliente in enumerate(lista_clientes):

        if obj_cliente.id == id:

            cliente_val = Cliente.model_validate(
                datos_cliente.model_dump()
            )

            cliente_val.id = id

            lista_clientes[i] = cliente_val

            return {
                "mensaje": "Cliente actualizado",
                "Cliente": cliente_val
            }

    return {
        "mensaje": f"No existe cliente con id {id}"
    }


@ruta_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int):

    for i, cliente in enumerate(lista_clientes):

        if cliente.id == id:

            cliente_eliminado = lista_clientes.pop(i)

            return {
                "mensaje": "Cliente eliminado correctamente",
                "cliente": cliente_eliminado
            }

    return {
        "mensaje": f"No existe cliente con id {id}"
    }