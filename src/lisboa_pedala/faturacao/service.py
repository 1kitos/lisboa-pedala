import uuid
from typing import Dict
from lisboa_pedala.shared.types import DadosFatura
from lisboa_pedala.pagamentos import service as pagamentos

_faturas: Dict[str, Dict] = {}


def emitir(dados: DadosFatura) -> str:
    """
    Recebe DadosFatura completo — nunca chama Viagens.
    Ver ADR-004 e ARCHITECTURE.md secção 4.
    """
    fatura_id = str(uuid.uuid4())
    _faturas[fatura_id] = {
        "fatura_id":        fatura_id,
        "viagem_id":        dados.viagem_id,
        "utilizador_id":    dados.utilizador_id,
        "duracao_minutos":  dados.duracao_minutos,
        "tipo_utilizador":  dados.tipo_utilizador,
        "valor_euros":      dados.valor_euros,
        "timestamp_inicio": dados.timestamp_inicio.isoformat(),
        "timestamp_fim":    dados.timestamp_fim.isoformat(),
        "estado_pagamento": "pendente",
    }
    metodo = "passe" if dados.tipo_utilizador == "assinante" else "mbway"
    pagamentos.processar_assincrono(fatura_id, dados.valor_euros, metodo)
    return fatura_id


def listar_faturas(utilizador_id: str) -> list:
    return [f for f in _faturas.values() if f["utilizador_id"] == utilizador_id]