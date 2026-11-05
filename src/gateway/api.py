from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from gateway import service

router = APIRouter()


class EventoEncaixe(BaseModel):
    evento_id: str
    bicicleta_id: str
    doca_id: str
    timestamp: str


class EventoAvaria(BaseModel):
    evento_id: str
    bicicleta_id: str
    motivo: str


class EventoOffline(BaseModel):
    tipo: str
    evento_id: str
    bicicleta_id: str
    doca_id: Optional[str] = None
    timestamp: Optional[str] = None
    motivo: Optional[str] = None


class ReenvioOffline(BaseModel):
    eventos: List[EventoOffline]


@router.post("/encaixe")
def receber_encaixe(evento: EventoEncaixe):
    return service.processar_evento_encaixe(
        evento.evento_id, evento.bicicleta_id,
        evento.doca_id, evento.timestamp)


@router.post("/avaria")
def receber_avaria(evento: EventoAvaria):
    return service.processar_evento_avaria(
        evento.evento_id, evento.bicicleta_id, evento.motivo)


@router.post("/reenvio-offline")
def reenvio_offline(payload: ReenvioOffline):
    """US-3: doca reenvia eventos acumulados offline."""
    return service.processar_reenvio_offline(
        [e.dict() for e in payload.eventos])