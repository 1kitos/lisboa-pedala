from fastapi import APIRouter
from lisboa_pedala.desbloqueio import service

router = APIRouter()


@router.post("/desbloquear")
def desbloquear(utilizador_id: str, bicicleta_id: str, doca_id: str):
    return service.desbloquear(utilizador_id, bicicleta_id, doca_id)