
from fastapi import APIRouter
from pydantic import BaseModel
from lisboa_pedala.manutencao import service

router = APIRouter()


class PedidoOrdem(BaseModel):
    bicicleta_id: str
    motivo: str
    origem: str


@router.post("/ordem")
def abrir_ordem(pedido: PedidoOrdem):
    return service.abrir_ordem(
        pedido.bicicleta_id,
        pedido.motivo,
        pedido.origem
    )


@router.get("/ordens")
def listar_ordens():
    return service.listar_ordens()
