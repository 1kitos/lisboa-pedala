from fastapi import APIRouter, Path
from lisboa_pedala.relatorios import service

router = APIRouter()


@router.get("/mensal/{ano}/{mes}")
def relatorio_mensal(
    ano: int = Path(...),
    mes: int = Path(..., ge=1, le=12)
):
    return service.relatorio_mensal(ano, mes)