from fastapi import APIRouter
from pydantic import BaseModel
from lisboa_pedala.desbloqueio import service

router = APIRouter()


class PedidoDesbloqueio(BaseModel):
    utilizador_id: str
    bicicleta_id: str
    doca_id: str


@router.post("/desbloquear")
def desbloquear(pedido: PedidoDesbloqueio):
    return service.desbloquear(
        pedido.utilizador_id,
        pedido.bicicleta_id,
        pedido.doca_id
    )