import math
from lisboa_pedala.shared.types import DuracaoMinutos

MINUTOS_GRATIS_ASSINANTE = 45
PRECO_BLOCO_ASSINANTE = 0.50   # euros por bloco de 15 min
PRECO_BASE_OCASIONAL = 2.00    # euros base por viagem
PRECO_BLOCO_OCASIONAL = 1.00   # euros por bloco de 15 min


def calcular(duracao: DuracaoMinutos, tipo_utilizador: str) -> float:
    if tipo_utilizador == "assinante":
        minutos_cobrados = max(0, duracao - MINUTOS_GRATIS_ASSINANTE)
        blocos = math.ceil(minutos_cobrados / 15) if minutos_cobrados > 0 else 0
        return round(blocos * PRECO_BLOCO_ASSINANTE, 2)
    else:
        blocos = math.ceil(duracao / 15)
        return round(PRECO_BASE_OCASIONAL + blocos * PRECO_BLOCO_OCASIONAL, 2)