from datetime import datetime

from fastapi import FastAPI, HTTPException
from .modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from .modelos.facturas import Factura, FacturaCrear
from .modelos.transacciones import Transacciones, TransaccionesCrear
from .enrutador import clientes
from .listas_app import lista_clientes, lista_facturas, lista_transacciones

app = FastAPI()

app.include_router(clientes.ruta_clientes, tags=["Clientes"])

# ---- endopoint de facturas-----


@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas


@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    # cliente_encontrado = [c for c in lista_clientes if c.id == cliente_id]
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # si no existe cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )

    # crear la factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val


# endpoint de transacciones


@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones


@app.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int
):
    # Consular si cliente_id existe; para consultar si tiene facturas con ese id y adicionar una transaccion o crear nueva factura.
    # cliente_encontrado = next((c for c in db_clientes if c.id == cliente_id), None)
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    # excepciones
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )

    # CONSULTAR FACTURA
    # factura_encontrada = next((f for f in lista_facturas if f.id == factura_id), None)
    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break

    # si la factura encontrada
    if factura_encontrada:
        # comprobar la factura con el id de cliente
        if factura_encontrada.cliente.id == cliente_id:
            # validar datos_transaccion
            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )
            transaccion_val.id = len(lista_transacciones) + 1
            transaccion_val.factura_id = factura_id
            lista_transacciones.append(transaccion_val)

            factura_encontrada.transacciones.append(transaccion_val)
            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            mensaje = f"Se encontro la factura de id: {factura_id}, pero es de otro cliente id: {cliente_id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura encontrada": factura_final}
    else:
        # si no se ha encontrado una factura,

        # validamos datos de la transaccion, y despues creamos la factura
        transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
        transaccion_val.id = len(lista_transacciones) + 1
        transaccion_val.factura_id = len(lista_facturas) + 1

        # creamos la factura(cliente, fecha, transacciones)
        factura = FacturaCrear(
            cliente=cliente_encontrado,
            fecha=str(datetime.now()),
            transacciones=[transaccion_val],
        )

        # datos_transaccion.vr_unitario * datos_transaccion.cantidad,
        factura_val = Factura.model_validate(factura.model_dump())
        factura_val.id = len(lista_facturas) + 1
        lista_facturas.append(factura_val)

        lista_transacciones.append(transaccion_val)

        return {
            "mensaje": f"Factura no existe con el id: {factura_id}, pero se creo la nueva factura",
            "facturas": transaccion_val,
        }