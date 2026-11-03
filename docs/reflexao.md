# Reflexão

## O que a especificação não previu

### Inicialização da base de dados
A especificação define o esquema conceptual mas não especifica
quando e como as tabelas SQLite são criadas. A IA gerou código
que assumia tabelas já existentes, causando erros na primeira
execução. Foi necessário adicionar um passo de inicialização
(`CREATE TABLE IF NOT EXISTS`) não previsto em ARCHITECTURE.md.

### Formato dos identificadores
ARCHITECTURE.md diz que `evento_id` é UUID mas não especifica
o formato dos restantes identificadores (`viagem_id`,
`utilizador_id`, `fatura_id`). A IA usou formatos
inconsistentes entre componentes (inteiros em Viagens,
strings em Faturação), o que causou erros de tipo na
integração. A especificação devia ter definido um tipo
canónico para todos os IDs.

### Autenticação simulada
A especificação diz "valida o assinante" mas não define o
que isso significa num protótipo simulado. A IA inventou
um mecanismo de autenticação diferente do esperado.

## Violações que a IA cometeu

### Violação 1 — Faturação a importar Viagens (detectada pela fitness function)
Na primeira geração do componente Faturação, a IA importou
`lisboa_pedala.viagens.service` para obter os detalhes da
viagem dentro de `emitir()`. Esta importação viola
directamente a regra de ARCHITECTURE.md ("faturacao não pode
importar de viagens") e cria o ciclo que ADR-004 proibiu.
O `lint-imports` detectou e rejeitou o código antes de entrar
no repositório.

### Violação 2 — Pagamento síncrono (detectada por revisão humana)
Na primeira geração de Faturação, o pagamento era processado
de forma síncrona dentro de `emitir()`, bloqueando o retorno
ao utilizador até o pagamento ser confirmado. ARCHITECTURE.md
secção 3 e ADR-004 proíbem explicitamente este padrão.
A fitness function não detectou porque é uma violação
semântica, não estrutural. Foi detectada por revisão do código
gerado antes do commit.

### Violação 3 — Gateway dentro do monólito (detectada por revisão humana)
Quando foi pedido à IA para gerar o ponto de entrada da
aplicação, colocou o Gateway de Docas como router FastAPI
dentro do `main.py` do monólito, ignorando ADR-002 que o
define como processo separado. ARCHITECTURE.md menciona a
separação mas a secção 6 ("o que a IA não pode fazer") não
tinha esta regra explícita. Foi adicionada após a violação.

## O que as fitness functions apanharam

- Importações proibidas entre componentes (lint-imports,
  contrato `forbidden`)
- Ciclos de dependência (lint-imports, contrato `independence`)

## O que passou despercebido às fitness functions

- Violações semânticas: pagamento síncrono, autenticação
  inventada, formato de IDs inconsistente
- Ausência de campos obrigatórios (ex: `evento_id` em eventos)
- Ordem errada de operações dentro de uma função
  (acoplamento temporal)

As fitness functions verificam *estrutura* (quem importa quem)
mas não *comportamento* (o que o código faz). Testes de
integração das user stories são necessários para cobrir
o segundo tipo de violação.