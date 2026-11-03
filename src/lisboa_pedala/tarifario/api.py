
from fastapi import APIRouter
from pydantic import BaseModel
from lisboa_pedala.tarifario import service

router = APIRouter()


class PedidoCalculo(BaseModel):
    duracao: int
    tipo_utilizador: str


@router.post("/calcular")
def calcular(pedido: PedidoCalculo):
    return service.calcular(
        pedido.duracao,
        pedido.tipo_utilizador
    )
