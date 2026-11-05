import threading
import time
from typing import Dict

_pagamentos: Dict[str, Dict] = {}


def processar_assincrono(fatura_id: str, valor: float, metodo: str) -> None:
    """Não bloqueia — regista e lança thread. Ver ADR-004."""
    _pagamentos[fatura_id] = {
        "fatura_id":  fatura_id,
        "valor":      valor,
        "metodo":     metodo,
        "estado":     "pendente",
        "tentativas": 0,
    }
    threading.Thread(target=_tentar, args=(fatura_id,), daemon=True).start()


def _tentar(fatura_id: str) -> None:
    time.sleep(0.5)  # simula latência de rede
    if fatura_id in _pagamentos:
        _pagamentos[fatura_id]["estado"]     = "pago"
        _pagamentos[fatura_id]["tentativas"] = 1


def listar_pendentes() -> list:
    return [p for p in _pagamentos.values() if p["estado"] == "pendente"]