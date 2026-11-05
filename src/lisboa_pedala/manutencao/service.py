import uuid
from datetime import datetime
from typing import Dict

_ordens: Dict[str, Dict] = {}


def abrir_ordem(bicicleta_id: str, motivo: str, origem: str) -> str:
    """origem: 'bicicleta' | 'utilizador'"""
    ordem_id = str(uuid.uuid4())
    _ordens[ordem_id] = {
        "ordem_id":     ordem_id,
        "bicicleta_id": bicicleta_id,
        "motivo":       motivo,
        "origem":       origem,
        "timestamp":    datetime.now().isoformat(),
        "estado":       "aberta",
    }
    return ordem_id


def listar_ordens() -> list:
    return list(_ordens.values())