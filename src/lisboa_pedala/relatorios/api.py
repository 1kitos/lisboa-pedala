from fastapi import APIRouter
from lisboa_pedala.relatorios import service

router = APIRouter()


@router.get("/mensal/{ano}/{mes}")
def relatorio_mensal(ano: int, mes: int):
    return service.relatorio_mensal(ano, mes)