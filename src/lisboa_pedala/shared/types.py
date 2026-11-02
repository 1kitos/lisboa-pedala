from dataclasses import dataclass
from datetime import datetime

# Tipo canónico para duração — sempre inteiros de minutos,
# arredondados para cima. Ambos os lados do contrato
# (Viagens e Tarifário) usam este tipo.
DuracaoMinutos = int


@dataclass
class DadosFatura:
    """
    Objeto completo que Viagens passa a Faturação.
    Faturação nunca chama Viagens de volta.
    Ver ARCHITECTURE.md secção 4 e ADR-004.
    """
    viagem_id: str
    utilizador_id: str
    duracao_minutos: DuracaoMinutos
    tipo_utilizador: str  # "assinante" | "ocasional"
    valor_euros: float
    timestamp_inicio: datetime
    timestamp_fim: datetime