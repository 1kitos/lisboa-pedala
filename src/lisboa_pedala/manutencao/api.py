from fastapi import APIRouter
from lisboa_pedala.manutencao import service

router = APIRouter()


@router.post("/ordem")
def abrir_ordem(bicicleta_id: str, motivo: str, origem: str):
    """origem: 'bicicleta' | 'utilizador'"""
    return service.abrir_ordem(bicicleta_id, motivo, origem)


@router.get("/ordens")
def listar_ordens():
    return service.listar_ordens()