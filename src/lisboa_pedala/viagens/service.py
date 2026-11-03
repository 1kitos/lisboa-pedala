
from datetime import datetime
from lisboa_pedala.shared.types import DadosFatura, DuracaoMinutos
from lisboa_pedala.tarifario import service as tarifario
from lisboa_pedala.faturacao import service as faturacao


def abrir_viagem(utilizador_id: str, bicicleta_id: str,
                 doca_id: str) -> str:
    raise NotImplementedError


def fechar_viagem(viagem_id: str, evento_id: str,
                  timestamp_fim: datetime) -> None:
    """
    Fecha a viagem, calcula o preço e emite a fatura
    numa só transação.

    Fluxo:
    1. Obtém os dados da viagem.
    2. Calcula a duração.
    3. Chama tarifario.calcular().
    4. Constrói DadosFatura.
    5. Chama faturacao.emitir().

    Os passos 2 a 5 devem respeitar a mesma transação
    de base de dados.

    Ver ARCHITECTURE.md secção 4.
    """
    raise NotImplementedError


def historico_utilizador(utilizador_id: str) -> list:
    raise NotImplementedError
