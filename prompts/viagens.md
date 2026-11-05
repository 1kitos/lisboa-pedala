# Prompt — Viagens

## Pedido
"Lê ARCHITECTURE.md secção 4 e ADR-004. Gera o componente Viagens
com as funções abrir_viagem e fechar_viagem. fechar_viagem tem de
chamar Tarifário e Faturação numa só transação atómica."

## Contexto fornecido
- ARCHITECTURE.md
- docs/adr/ADR-004.md
- docs/02-componentes.md (secção acoplamento temporal)

## Resultado
A IA gerou fechar_viagem a chamar faturacao.emitir() e, dentro de
emitir(), tentou chamar viagens.obter_detalhes() para obter a duração.
Criou o ciclo Viagens → Faturação → Viagens que ADR-004 proíbe.

## Violação detectada por
Fitness function (lint-imports) — reportou ciclo de dependência
imediatamente ao correr lint-imports.

## Decisão
Rejeitado. Novo pedido com instrução explícita: "Faturação recebe
um objeto DadosFatura completo e nunca chama Viagens de volta."
Segunda geração passou nas fitness functions.