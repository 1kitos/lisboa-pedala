from fastapi import APIRouter
from lisboa_pedala.redistribuicao import service

router = APIRouter()


@router.get("/rotas")
def sugerir_rotas():
    return service.sugerir_rotas()