# Prompt — Gateway de Docas

## Pedido
"Lê ARCHITECTURE.md e ADR-002. Gera o componente Gateway de Docas
como processo separado que recebe eventos de docas, deduplica por
evento_id e encaminha para o monólito via HTTP."

## Contexto fornecido
- ARCHITECTURE.md
- docs/adr/ADR-002.md
- docs/adr/ADR-003.md

## Resultado
A IA gerou o gateway como router FastAPI dentro do main.py do monólito,
ignorando ADR-002 que o define como processo separado.

## Violação detectada por
Revisão humana — a fitness function não apanha esta violação porque
é semântica (onde corre o processo), não estrutural (quem importa quem).

## Decisão
Aceite com documentação. ARCHITECTURE.md secção 6 actualizada com a
regra "o Gateway não pode ser incluído como router no monólito".
Registado na reflexão como violação que passou às fitness functions.