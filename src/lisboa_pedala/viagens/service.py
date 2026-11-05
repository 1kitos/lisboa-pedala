import uuid
import math
from datetime import datetime
from typing import Dict, Optional
from lisboa_pedala.shared.types import DadosFatura, DuracaoMinutos
from lisboa_pedala.tarifario import service as tarifario
from lisboa_pedala.faturacao import service as faturacao

_viagens: Dict[str, Dict] = {}

# Registo de utilizadores (protótipo)
_utilizadores = {
    "U001": {"nome": "João Silva",    "tipo": "assinante"},
    "U002": {"nome": "Maria Santos",  "tipo": "ocasional"},
}


def abrir_viagem(utilizador_id: str, bicicleta_id: str, doca_id: str) -> str:
    for v in _viagens.values():
        if v["utilizador_id"] == utilizador_id and v["estado"] == "aberta":
            raise ValueError(f"Utilizador {utilizador_id} já tem uma viagem aberta")

    viagem_id = str(uuid.uuid4())
    tipo = _utilizadores.get(utilizador_id, {}).get("tipo", "ocasional")
    _viagens[viagem_id] = {
        "viagem_id":        viagem_id,
        "utilizador_id":    utilizador_id,
        "bicicleta_id":     bicicleta_id,
        "doca_inicio_id":   doca_id,
        "timestamp_inicio": datetime.now().isoformat(),
        "timestamp_fim":    None,
        "estado":           "aberta",
        "tipo_utilizador":  tipo,
        "fatura_id":        None,
    }
    return viagem_id


def fechar_viagem(viagem_id: str, evento_id: str,
                  timestamp_fim: datetime) -> DadosFatura:
    """
    Fecha a viagem, calcula o preço e emite a fatura
    numa só operação atómica. Ver ARCHITECTURE.md secção 4.
    """
    if viagem_id not in _viagens:
        raise ValueError(f"Viagem {viagem_id} não existe")

    viagem = _viagens[viagem_id]
    if viagem["estado"] == "fechada":
        raise ValueError(f"Viagem {viagem_id} já está fechada")

    timestamp_inicio = datetime.fromisoformat(viagem["timestamp_inicio"])
    duracao_seg = (timestamp_fim - timestamp_inicio).total_seconds()
    duracao: DuracaoMinutos = max(1, math.ceil(duracao_seg / 60))

    valor = tarifario.calcular(duracao, viagem["tipo_utilizador"])

    dados = DadosFatura(
        viagem_id=viagem_id,
        utilizador_id=viagem["utilizador_id"],
        duracao_minutos=duracao,
        tipo_utilizador=viagem["tipo_utilizador"],
        valor_euros=valor,
        timestamp_inicio=timestamp_inicio,
        timestamp_fim=timestamp_fim,
    )

    # Atómico: fatura emitida e viagem fechada juntas
    fatura_id = faturacao.emitir(dados)
    viagem["estado"]        = "fechada"
    viagem["timestamp_fim"] = timestamp_fim.isoformat()
    viagem["fatura_id"]     = fatura_id

    return dados


def historico_utilizador(utilizador_id: str) -> list:
    return [v for v in _viagens.values() if v["utilizador_id"] == utilizador_id]


def listar_todas() -> list:
    return list(_viagens.values())


def obter_por_bicicleta(bicicleta_id: str,
                         estado: str = "aberta") -> Optional[Dict]:
    for v in _viagens.values():
        if v["bicicleta_id"] == bicicleta_id and v["estado"] == estado:
            return v
    return None