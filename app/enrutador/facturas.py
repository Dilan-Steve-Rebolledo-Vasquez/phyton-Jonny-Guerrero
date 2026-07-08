from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..conexion_bd import Sesion_dependencia
from ..modelos.facturas import Factura, FacturaCrear
from ..modelos.transacciones import Transacciones 
# Importamos el modelo de Cliente para poder buscar sus datos de forma aislada
from ..modelos.clientes import Cliente 

ruta_facturas = APIRouter(tags=["Facturas"])

# 1. LISTAR TODAS LAS FACTURAS (Uniendo la información de forma segura)
@ruta_facturas.get("/facturas")
async def listar_facturas(sesion: Sesion_dependencia):
    facturas = sesion.exec(select(Factura).order_by(Factura.id)).all()
    
    resultado = []
    for factura in facturas:
        # Buscamos el cliente asignado a esta factura
        cliente_info = sesion.get(Cliente, factura.cliente_id)
        
        # Buscamos todas las transacciones vinculadas a esta factura
        tx_info = sesion.exec(select(Transacciones).where(Transacciones.factura_id == factura.id)).all()
        
        # Juntamos todo en un diccionario estructurado
        resultado.append({
            "id": factura.id,
            "fecha": factura.fecha,
            "valor_total": factura.valor_total,
            "cliente_id": factura.cliente_id,
            "cliente": cliente_info,
            "transacciones": tx_info
        })
        
    return resultado

# 2. BUSCAR UNA FACTURA POR ID (Uniendo la información de forma segura)
@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Buscamos sus datos relacionados de forma independiente
    cliente_info = sesion.get(Cliente, factura.cliente_id)
    tx_info = sesion.exec(select(Transacciones).where(Transacciones.factura_id == id)).all()
    
    return {
        "id": factura.id,
        "fecha": factura.fecha,
        "valor_total": factura.valor_total,
        "cliente_id": factura.cliente_id,
        "cliente": cliente_info,
        "transacciones": tx_info
    }

# 3. CREAR UNA FACTURA (Se mantiene igual)
@ruta_facturas.post("/facturas")
async def crear_factura(datos: FacturaCrear, sesion: Sesion_dependencia):
    datos_dict = datos.model_dump()
    datos_dict["valor_total"] = 0
    
    nueva_factura = Factura(**datos_dict)
    
    sesion.add(nueva_factura)
    sesion.commit()
    sesion.refresh(nueva_factura)
    return {
        "mensaje": "Factura creada con éxito",
        "factura": nueva_factura
    }

# 4. ELIMINAR UNA FACTURA (Se mantiene igual)
@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
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