def sugerir_rotas() -> list:
    from lisboa_pedala.disponibilidade import service as disponibilidade

    mapa = disponibilidade.obter_mapa_completo()
    cheias, vazias = [], []

    for eid, estacao in mapa.items():
        total = estacao["docas_livres"] + estacao["docas_ocupadas"]
        if total == 0:
            continue
        ocup = estacao["docas_ocupadas"] / total
        entry = {"estacao_id": eid, "nome": estacao["nome"],
                 "ocupacao": round(ocup, 2)}
        if ocup >= 0.8:
            cheias.append(entry)
        elif ocup <= 0.2:
            vazias.append(entry)

    rotas = [
        {"origem": c, "destino": v,
         "acao": "mover bicicletas de estação cheia para estação vazia"}
        for c in cheias for v in vazias
    ]
    return rotas or [{"mensagem": "Sem redistribuição necessária"}]