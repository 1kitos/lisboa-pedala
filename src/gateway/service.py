"""
VIOLAÇÃO DOCUMENTADA (ver prompts/gateway.md):
Em produção, este módulo correria como processo separado (ADR-002).
No protótipo corre como módulo dentro do monólito para simplificar.
"""
from datetime import datetime
from typing import Set

_eventos_processados: Set[str] = set()


def processar_evento_encaixe(evento_id: str, bicicleta_id: str,
                              doca_id: str, timestamp_str: str) -> dict:
    if evento_id in _eventos_processados:
        return {"status": "duplicado_ignorado", "evento_id": evento_id}

    _eventos_processados.add(evento_id)

    from lisboa_pedala.viagens import service as viagens
    from lisboa_pedala.disponibilidade import service as disponibilidade

    viagem = viagens.obter_por_bicicleta(bicicleta_id, estado="aberta")
    if not viagem:
        return {"status": "erro",
                "mensagem": f"Nenhuma viagem aberta para {bicicleta_id}"}

    timestamp_fim = datetime.fromisoformat(timestamp_str)
    dados = viagens.fechar_viagem(viagem["viagem_id"], evento_id, timestamp_fim)
    disponibilidade.atualizar_estado_doca(doca_id, "ocupada", bicicleta_id)

    return {
        "status":          "processado",
        "evento_id":       evento_id,
        "viagem_id":       viagem["viagem_id"],
        "duracao_minutos": dados.duracao_minutos,
        "valor_euros":     dados.valor_euros,
    }


def processar_evento_avaria(evento_id: str, bicicleta_id: str,
                             motivo: str) -> dict:
    if evento_id in _eventos_processados:
        return {"status": "duplicado_ignorado", "evento_id": evento_id}

    _eventos_processados.add(evento_id)

    from lisboa_pedala.manutencao import service as manutencao

    ordem_id = manutencao.abrir_ordem(bicicleta_id, motivo, "bicicleta")
    return {"status": "processado", "evento_id": evento_id,
            "ordem_id": ordem_id}


def processar_reenvio_offline(eventos: list) -> dict:
    """US-3: processa lista de eventos offline, deduplicando."""
    processados = ignorados = 0

    for ev in eventos:
        tipo = ev.get("tipo")
        evento_id = ev.get("evento_id")
        if not evento_id:
            continue

        if tipo == "encaixe":
            r = processar_evento_encaixe(
                evento_id, ev["bicicleta_id"],
                ev["doca_id"], ev["timestamp"])
        elif tipo == "avaria":
            r = processar_evento_avaria(
                evento_id, ev["bicicleta_id"],
                ev.get("motivo", "desconhecido"))
        else:
            continue

        if r["status"] == "duplicado_ignorado":
            ignorados += 1
        else:
            processados += 1

    return {"processados": processados, "ignorados": ignorados}