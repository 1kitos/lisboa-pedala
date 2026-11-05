from lisboa_pedala.viagens import service as viagens
from lisboa_pedala.disponibilidade import service as disponibilidade


def desbloquear(utilizador_id: str, bicicleta_id: str, doca_id: str) -> dict:
    viagem_id = viagens.abrir_viagem(utilizador_id, bicicleta_id, doca_id)
    disponibilidade.atualizar_estado_doca(doca_id, "livre", None)
    return {
        "viagem_id":   viagem_id,
        "bicicleta_id": bicicleta_id,
        "doca_id":     doca_id,
        "estado":      "desbloqueado",
        "mensagem":    "Bicicleta desbloqueada. Boa viagem!",
    }