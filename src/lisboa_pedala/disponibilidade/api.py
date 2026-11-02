from fastapi import APIRouter
from lisboa_pedala.disponibilidade import service

router = APIRouter()


@router.get("/estacao/{estacao_id}")
def estado_estacao(estacao_id: str):
    return service.obter_estado_estacao(estacao_id)


@router.get("/mapa")
def mapa():
    return service.obter_mapa_completo()