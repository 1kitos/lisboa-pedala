
from fastapi import APIRouter
from pydantic import BaseModel
from lisboa_pedala.viagens import service

router = APIRouter()


class PedidoAberturaViagem(BaseModel):
    utilizador_id: str
    bicicleta_id: str
    doca_id: str


@router.post("/abrir")
def abrir_viagem(pedido: PedidoAberturaViagem):
    return service.abrir_viagem(
        pedido.utilizador_id,
        pedido.bicicleta_id,
        pedido.doca_id
    )


@router.get("/{utilizador_id}/historico")
def historico(utilizador_id: str):
    return service.historico_utilizador(utilizador_id)
