from lisboa_pedala.shared.types import DadosFatura


def emitir(dados: DadosFatura) -> str:
    """
    Emite e arquiva a fatura.
    Recebe DadosFatura completo — nunca chama Viagens.
    Ver ADR-004 e ARCHITECTURE.md secção 4.
    """
    raise NotImplementedError

def listar_faturas(utilizador_id: str) -> list:
    raise NotImplementedError