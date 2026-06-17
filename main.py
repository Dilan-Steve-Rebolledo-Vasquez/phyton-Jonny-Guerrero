from fastapi import FastAPI
from modelos.clientes import cliente, clienteCrear, clienteEditar

app = FastAPI()

lista_clientes:list[cliente] = []

@app.get("/clientes")
async def listar_clientes():
    #Creacion de sms mas adecuado al usuario
    return {"clientes": lista_clientes}

@app.get("/clientes/{id}")
async def listar_cliente(id:int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

@app.post("/clientes", response_model=cliente)
async def crear_clientes(datos_cliente:clienteCrear):
    cliente_val = cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes)+1
    lista_clientes.append(cliente_val)
    return cliente_val

@app.put("/clientes/{id}")
def editar_clientes(id:int, datos_cliente:clienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
    return {"mensaje": "Se actualizo el cliente satisfactoriamente.", "cliente": cliente_val}

@app.delete("/clientes/{id}")
async def eliminar_clientes(id:int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = cliente.model_validate(obj_cliente.model_dump())
            cliente_val.id = id
            lista_clientes.pop(i)
    return {"mensaje": "Se elimino el cliente satisfactoriamente.", "cliente": cliente_val}