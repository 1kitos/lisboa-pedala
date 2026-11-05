from typing import Dict, Optional

# Estado em memória — dados de seed para o protótipo
_docas: Dict[str, Dict] = {
    "DOCA-001": {"estacao_id": "EST-001", "estado": "ocupada", "bicicleta_id": "BIC-001"},
    "DOCA-002": {"estacao_id": "EST-001", "estado": "ocupada", "bicicleta_id": "BIC-002"},
    "DOCA-003": {"estacao_id": "EST-001", "estado": "livre",   "bicicleta_id": None},
    "DOCA-004": {"estacao_id": "EST-002", "estado": "ocupada", "bicicleta_id": "BIC-003"},
    "DOCA-005": {"estacao_id": "EST-002", "estado": "livre",   "bicicleta_id": None},
}

_estacoes: Dict[str, Dict] = {
    "EST-001": {"nome": "Marquês de Pombal", "docas": ["DOCA-001", "DOCA-002", "DOCA-003"]},
    "EST-002": {"nome": "Rossio",            "docas": ["DOCA-004", "DOCA-005"]},
}


def atualizar_estado_doca(doca_id: str, estado: str,
                           bicicleta_id: Optional[str] = None) -> None:
    if doca_id not in _docas:
        raise ValueError(f"Doca {doca_id} não existe")
    _docas[doca_id]["estado"] = estado
    _docas[doca_id]["bicicleta_id"] = bicicleta_id


def obter_estado_estacao(estacao_id: str) -> dict:
    if estacao_id not in _estacoes:
        raise ValueError(f"Estação {estacao_id} não existe")
    estacao = dict(_estacoes[estacao_id])
    docas = {d: _docas[d] for d in estacao["docas"]}
    estacao["docas"] = docas
    estacao["docas_livres"]   = sum(1 for d in docas.values() if d["estado"] == "livre")
    estacao["docas_ocupadas"] = sum(1 for d in docas.values() if d["estado"] == "ocupada")
    return estacao


def obter_mapa_completo() -> dict:
    return {eid: obter_estado_estacao(eid) for eid in _estacoes}