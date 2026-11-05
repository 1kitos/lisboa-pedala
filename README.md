# Lisboa Pedala

Trabalho Prático 1 — Design de Software
Especificação de Arquitetura + Esqueleto Funcional

## Sobre o projecto

Sistema de bicicletas partilhadas para Lisboa. Plataforma para
desbloquear e devolver bicicletas, cobrar viagens, manter a frota
e reportar à Câmara Municipal.

Trabalho individual.

## Estrutura do repositório

docs/
01-caracteristicas.md
02-componentes.md
03-particionamento-e-vistas.md
reflexao.md
adr/ # ADR-001 a ADR-005
diagramas/ # C4 níveis 1-3
src/
gateway/ # Gateway de Docas (namespace separado, ADR-002)
lisboa_pedala/
desbloqueio/, viagens/, tarifario/, faturacao/, pagamentos/
disponibilidade/, manutencao/, redistribuicao/, relatorios/
shared/ # tipos partilhados: DuracaoMinutos, DadosFatura
main.py
tests/
architecture/ # fitness functions (import-linter)
prompts/ # registo de uso de IA por componente
ARCHITECTURE.md # especificação de referência para geração de código
CODEOWNERS


## Como correr

```bash
cd src
pip install fastapi uvicorn import-linter pytest
python -m pip install --user import-linter


python uvicorn lisboa_pedala.main:app --reload
```

Swagger disponível em `http://localhost:8000/docs`.

## Fitness functions

```bash
# na raiz do projecto
$env:PATH += ";$env:APPDATA\Python\Python314\Scripts"
lint-imports
```

Todos os contratos devem estar `KEPT` antes de qualquer commit de código.

## User Stories implementadas

- **US-1:** desbloquear e devolver bicicleta, viagem registada e cobrada
- **US-2:** ordem de manutenção aberta quando bicicleta reporta avaria
- **US-3:** doca reenvia eventos offline sem criar viagens duplicadas

## Uso de IA

Todo o código foi gerado com assistência de IA e validado por mim. 
Cada componente temum ficheiro de registo em `prompts/` com o pedido feito, o contexto fornecido, o resultado aceite ou rejeitado e as violações detectadas.

| Ferramenta | Modelo | Utilização |
|---|---|---|
| Claude (claude.ai) | Claude Sonnet 4.6 | Geração de código, revisão da especificação, crítica de decisões arquitecturais |

A análise de características, os componentes lógicos e as decisões
dos ADRs são do autor. A IA foi usada como revisor crítico e gerador
de código a partir da especificação.

Foram identificados pelo menos 3 casos em que o código gerado violou
a especificação — ver `docs/reflexao.md`.