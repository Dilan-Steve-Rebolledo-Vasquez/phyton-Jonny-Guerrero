from pydantic import BaseModel, computed_field

from ..modelos.clientes import Cliente
from ..modelos.transacciones import Transacciones


class FacturaBase(BaseModel):
    # atributos
    fecha: str
    cliente: Cliente
    transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        # consultar el id actual y poder filtra trasacciones
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None or not self.transacciones:
            return 0.0
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
            if t.factura_id == factura_id_actual
        )


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None