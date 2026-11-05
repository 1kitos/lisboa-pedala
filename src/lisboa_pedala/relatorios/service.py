CO2_POR_VIAGEM_KG = 0.45  # estimativa: 150g/km * 3km médios


def relatorio_mensal(ano: int, mes: int) -> dict:
    from lisboa_pedala.viagens import service as viagens

    todas = viagens.listar_todas()
    prefixo = f"{ano:04d}-{mes:02d}"

    viagens_mes = [
        v for v in todas
        if v["timestamp_fim"] and v["timestamp_fim"].startswith(prefixo)
    ]

    return {
        "ano":            ano,
        "mes":            mes,
        "total_viagens":  len(viagens_mes),
        "co2_evitado_kg": round(len(viagens_mes) * CO2_POR_VIAGEM_KG, 2),
        "nota":           "Dados por freguesia não disponíveis no protótipo",
        "viagens":        viagens_mes,
    }