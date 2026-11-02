from fastapi import APIRouter
from lisboa_pedala.viagens import service

router = APIRouter()


@router.post("/abrir")
def abrir_viagem(utilizador_id: str, bicicleta_id: str, doca_id: str):
    return service.abrir_viagem(utilizador_id, bicicleta_id, doca_id)


@router.get("/{utilizador_id}/historico")
def historico(utilizador_id: str):
    return service.historico_utilizador(utilizador_id)