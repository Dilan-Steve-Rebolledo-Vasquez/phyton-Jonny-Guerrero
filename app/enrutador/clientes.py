from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..conexion_bd import Sesion_dependencia
from ..modelos.clientes import Cliente, ClienteCrear, ClienteEditar

ruta_clientes = APIRouter(tags=["Clientes"])

@ruta_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(sesion: Sesion_dependencia):
    # Organizados por ID de forma fija ascendente
    return sesion.exec(select(Cliente).order_by(Cliente.id)).all()

@ruta_clientes.get("/clientes/{id}", response_model=Cliente)
async def obtener_cliente(id: int, sesion: Sesion_dependencia):
    cliente = sesion.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@ruta_clientes.post("/clientes")
async def crear_cliente(datos: ClienteCrear, sesion: Sesion_dependencia):
    nuevo_cliente = Cliente.model_validate(datos)
    sesion.add(nuevo_cliente)
    sesion.commit()
    sesion.refresh(nuevo_cliente)
    
    return {
        "mensaje": f"El cliente '{nuevo_cliente.nombre}' se creó exitosamente con el ID {nuevo_cliente.id}",
        "cliente": nuevo_cliente
    }

@ruta_clientes.put("/clientes/{id}")
async def editar_cliente(id: int, datos: ClienteEditar, sesion: Sesion_dependencia):
    cliente = sesion.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    cliente.nombre = datos.nombre
    cliente.edad = datos.edad
    cliente.descripcion = datos.descripcion
    
    sesion.add(cliente)
    sesion.commit()
    sesion.refresh(cliente)
    
    return {
        "mensaje": f"El cliente '{cliente.nombre}' con ID {cliente.id} se editó exitosamente",
        "cliente": cliente
    }

@ruta_clientes.delete("/clientes/{id}")
async def eliminar_cliente(id: int, sesion: Sesion_dependencia):
    cliente = sesion.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    nombre_cliente = cliente.nombre
    sesion.delete(cliente)
    sesion.commit()
    
    return {"mensaje": f"Cliente '{nombre_cliente}' con ID {id} eliminado con éxito"}