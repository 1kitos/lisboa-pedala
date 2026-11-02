from fastapi import APIRouter
from lisboa_pedala.pagamentos import service

router = APIRouter()


@router.get("/pendentes")
def listar_pendentes():
    return service.listar_pendentes()