
from fastapi import APIRouter, Query
from lisboa_pedala.relatorios import service

router = APIRouter()


@router.get("/mensal/{ano}/{mes}")
def relatorio_mensal(
    ano: int,
    mes: int = Query(ge=1, le=12)
):
    return service.relatorio_mensal(ano, mes)
