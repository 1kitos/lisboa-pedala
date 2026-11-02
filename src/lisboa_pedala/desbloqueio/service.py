from lisboa_pedala.viagens import service as viagens
from lisboa_pedala.disponibilidade import service as disponibilidade


def desbloquear(utilizador_id: str, bicicleta_id: str,
                doca_id: str) -> dict:
    raise NotImplementedError