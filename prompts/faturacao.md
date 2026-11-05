# Prompt — Faturação

## Pedido
"Lê ARCHITECTURE.md secção 3 e ADR-004. Gera o componente Faturação.
O pagamento tem de ser processado de forma assíncrona — nunca bloqueia
o fecho da viagem."

## Contexto fornecido
- ARCHITECTURE.md
- docs/adr/ADR-004.md

## Resultado
A IA gerou faturacao.emitir() a chamar pagamentos.processar() de forma
síncrona com await, bloqueando o retorno até o pagamento ser confirmado.
Viola ADR-004 e ARCHITECTURE.md secção 3.

## Violação detectada por
Revisão humana — a fitness function não apanha violações semânticas
(síncrono vs assíncrono), só violações estruturais (importações).

## Decisão
Rejeitado. Novo pedido com exemplo explícito de threading.Thread no
prompt. Segunda geração usou threading correctamente.