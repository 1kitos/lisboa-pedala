from fastapi import FastAPI

app = FastAPI(title="Lisboa Pedala")

from lisboa_pedala.desbloqueio import api as desbloqueio_api
from lisboa_pedala.viagens import api as viagens_api
from lisboa_pedala.tarifario import api as tarifario_api
from lisboa_pedala.faturacao import api as faturacao_api
from lisboa_pedala.pagamentos import api as pagamentos_api
from lisboa_pedala.disponibilidade import api as disponibilidade_api
from lisboa_pedala.manutencao import api as manutencao_api
from lisboa_pedala.redistribuicao import api as redistribuicao_api
from lisboa_pedala.relatorios import api as relatorios_api
from gateway import api as gateway_api  # VIOLAÇÃO DOCUMENTADA: ver prompts/gateway.md

app.include_router(desbloqueio_api.router,    prefix="/desbloqueio")
app.include_router(viagens_api.router,         prefix="/viagens")
app.include_router(tarifario_api.router,       prefix="/tarifario")
app.include_router(faturacao_api.router,       prefix="/faturacao")
app.include_router(pagamentos_api.router,      prefix="/pagamentos")
app.include_router(disponibilidade_api.router, prefix="/disponibilidade")
app.include_router(manutencao_api.router,      prefix="/manutencao")
app.include_router(redistribuicao_api.router,  prefix="/redistribuicao")
app.include_router(relatorios_api.router,      prefix="/relatorios")
app.include_router(gateway_api.router,         prefix="/gateway")