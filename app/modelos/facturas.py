from sqlmodel import SQLModel, Field
from pydantic import computed_field


class FacturaBase(SQLModel):

    fecha: str

    cliente_id: int

    @computed_field
    @property
    def valor_total(self) -> float:
        return 0.0


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )