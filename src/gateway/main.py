"""
Gateway de Docas — processo separado.
Recebe eventos das docas, deduplica por evento_id
e encaminha para o monólito via HTTP.
Ver ADR-002 e ADR-003.
"""
import uuid
from fastapi import FastAPI

app = FastAPI(title="Gateway de Docas")

# Tabela de eventos já processados (em memória para o esqueleto;
# em SQLite na implementação real — TTL 48h)
_eventos_processados: set[str] = set()


@app.post("/eventos/desbloqueio")
def receber_desbloqueio(evento_id: str, bicicleta_id: str,
                         doca_id: str, timestamp: str):
    if evento_id in _eventos_processados:
        return {"status": "duplicado_ignorado"}
    _eventos_processados.add(evento_id)
    raise NotImplementedError


@app.post("/eventos/encaixe")
def receber_encaixe(evento_id: str, bicicleta_id: str,
                     doca_id: str, timestamp: str):
    if evento_id in _eventos_processados:
        return {"status": "duplicado_ignorado"}
    _eventos_processados.add(evento_id)
    raise NotImplementedError


@app.post("/eventos/avaria")
def receber_avaria(evento_id: str, bicicleta_id: str,
                    motivo: str):
    if evento_id in _eventos_processados:
        return {"status": "duplicado_ignorado"}
    _eventos_processados.add(evento_id)
    raise NotImplementedError