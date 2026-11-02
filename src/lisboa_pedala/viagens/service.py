from datetime import datetime
from lisboa_pedala.shared.types import DadosFatura, DuracaoMinutos
from lisboa_pedala.tarifario import service as tarifario
from lisboa_pedala.faturacao import service as faturacao
import math


def abrir_viagem(utilizador_id: str, bicicleta_id: str,
                 doca_id: str) -> str:
    raise NotImplementedError


def fechar_viagem(viagem_id: str, evento_id: str,
                  timestamp_fim: datetime) -> DadosFatura:
    """
    Fecha a viagem, calcula o preço e emite a fatura
    numa só transação. Ver ARCHITECTURE.md secção 4.
    """
    raise NotImplementedError

def historico_utilizador(utilizador_id: str) -> list:
    raise NotImplementedError