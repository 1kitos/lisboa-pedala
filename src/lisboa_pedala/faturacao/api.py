from fastapi import APIRouter
from lisboa_pedala.faturacao import service

router = APIRouter()


@router.get("/{utilizador_id}/faturas")
def listar_faturas(utilizador_id: str):
    return service.listar_faturas(utilizador_id)