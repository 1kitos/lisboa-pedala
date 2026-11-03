
def processar_assincrono(fatura_id: str, valor: float,
                         metodo: str) -> None:
    """
    Assíncrono: não bloqueia o fecho da viagem.
    Ver ADR-004 e ARCHITECTURE.md secção 3.
    """
    raise NotImplementedError


def listar_pendentes() -> list:
    raise NotImplementedError
