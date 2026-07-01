from sqlmodel import SQLModel, Field


class TransaccionesBase(SQLModel):

    cantidad: int

    vr_unitario: float

    descripcion: str


class TransaccionesCrear(
    TransaccionesBase
):
    pass


class TransaccionesEditar(
    TransaccionesBase
):
    pass


class Transacciones(
    TransaccionesBase,
    table=True
):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    factura_id: int | None = None