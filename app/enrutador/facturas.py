from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..conexion_bd import Sesion_dependencia
from ..modelos.facturas import Factura, FacturaCrear
from ..modelos.transacciones import Transacciones 

ruta_facturas = APIRouter(tags=["Facturas"])

# 1. LISTAR TODAS LAS FACTURAS (Vuelve a ser el código original que sí funcionaba)
@ruta_facturas.get("/facturas")
async def listar_facturas(sesion: Sesion_dependencia):
    facturas = sesion.exec(select(Factura).order_by(Factura.id)).all()
    return facturas

# 2. BUSCAR UNA FACTURA POR ID
@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

# 3. CREAR UNA FACTURA (Usa FacturaCrear: solo te pedirá cliente_id y fecha)
@ruta_facturas.post("/facturas")
async def crear_factura(datos: FacturaCrear, sesion: Sesion_dependencia):
    datos_dict = datos.model_dump()
    
    # El valor total se inicializa en 0 de forma automática
    datos_dict["valor_total"] = 0
    
    nueva_factura = Factura(**datos_dict)
    
    sesion.add(nueva_factura)
    sesion.commit()
    sesion.refresh(nueva_factura)
    return {
        "mensaje": "Factura creada con éxito",
        "factura": nueva_factura
    }

# 4. ELIMINAR UNA FACTURA (Mantiene el mensaje controlado en español)
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Validamos relación con transacciones antes de borrar
    declaracion = select(Transacciones).where(Transacciones.factura_id == id)
    tiene_transacciones = sesion.exec(declaracion).first()
    
    if tiene_transacciones:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la factura porque tiene transacciones relacionadas en el sistema. Elimina primero sus transacciones."
        )
    
    sesion.delete(factura)
    sesion.commit()
    return {"mensaje": f"Factura con ID {id} eliminada con éxito"}