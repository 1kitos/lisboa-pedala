from fastapi import APIRouter
from lisboa_pedala.tarifario import service

router = APIRouter()


@router.get("/calcular")
def calcular(duracao: int, tipo_utilizador: str):
    return service.calcular(duracao, tipo_utilizador)