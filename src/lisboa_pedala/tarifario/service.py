
from lisboa_pedala.shared.types import DuracaoMinutos
import math


MINUTOS_GRATIS_ASSINANTE = 45
PRECO_BLOCO_15MIN_ASSINANTE = 0.50
PRECO_POR_VIAGEM_OCASIONAL = 2.00
PRECO_BLOCO_15MIN_OCASIONAL = 1.00


def calcular(duracao: DuracaoMinutos, tipo_utilizador: str) -> float:
    """
    Calcula o valor a cobrar.
    Tarifário não importa nenhum outro componente de domínio.
    Ver ARCHITECTURE.md secção 2 (regras allowed-to-use).
    """
    raise NotImplementedError("A implementar no Bloco F")
