from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..conexion_bd import Sesion_dependencia
from ..modelos.transacciones import Transacciones, TransaccionesCrear
from ..modelos.facturas import Factura

ruta_transacciones = APIRouter(tags=["Transacciones"])

# 1. LISTAR TODAS LAS TRANSACCIONES
@ruta_transacciones.get("/transacciones")
async def listar_transacciones(sesion: Sesion_dependencia):
    transacciones = sesion.exec(select(Transacciones).order_by(Transacciones.id)).all()
    return transacciones

# 2. BUSCAR UNA TRANSACCIÓN POR ID (¡La que nos faltaba!)
@ruta_transacciones.get("/transacciones/{id}")
async def obtener_transaccion(id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transacciones, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion

# 3. CREAR TRANSACCIÓN
@ruta_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(factura_id: int, datos: TransaccionesCrear, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="La factura especificada no existe")
    
    datos_dict = datos.model_dump()
    datos_dict["factura_id"] = factura_id
    
    nueva_tx = Transacciones(**datos_dict)
    
    sesion.add(nueva_tx)
    sesion.commit()
    sesion.refresh(nueva_tx)
    
    return {
        "mensaje": f"Transacción registrada con éxito para la factura N° {factura_id}",
        "transaccion": nueva_tx
    }

# 4. ELIMINAR TRANSACCIÓN
@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int, sesion: Sesion_dependencia):
    tx = sesion.get(Transacciones, id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    sesion.delete(tx)
    sesion.commit()
    return {"mensaje": f"Transacción con ID {id} eliminada con éxito"}