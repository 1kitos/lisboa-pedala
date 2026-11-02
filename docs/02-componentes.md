# Componentes lógicos

## 1. Abordagem

Abordagem **workflow**: seguimos o fluxo principal do negócio
(desbloquear → viajar → devolver → cobrar) e cada passo 
relevante origina um componente. Esta abordagem é preferível
à actor/action porque o sistema é orientado a eventos 
sequenciais com regras de negócio claras em cada passo.

## 2. Componentes lógicos

### Desbloqueio
Autoriza e inicia o processo de desbloqueio de uma bicicleta,
validando o assinante ou utilizador ocasional e comunicando
à doca para libertar a bicicleta.
- **Namespace:** `lisboa_pedala.desbloqueio`

### Gateway de Docas
Recebe, normaliza e deduplica os eventos enviados pelas docas
(desbloqueio confirmado, encaixe confirmado, avaria reportada).
É o único componente que fala diretamente com o hardware.
- **Namespace:** `lisboa_pedala.gateway_docas`

### Viagens
Gere o ciclo de vida de uma viagem: abertura quando a bicicleta
é desbloqueada, fecho quando a doca confirma o encaixe, 
cálculo da duração.
- **Namespace:** `lisboa_pedala.viagens`

### Tarifário
Calcula o valor a cobrar com base no tipo de utilizador
(assinante com 45 min grátis + blocos de 15 min, ou ocasional
por viagem) e na duração da viagem.
- **Namespace:** `lisboa_pedala.tarifario`

### Faturação
Emite, arquiva e comunica faturas à Autoridade Tributária.
Guarda faturas durante 10 anos.
- **Namespace:** `lisboa_pedala.faturacao`

### Pagamentos
Processa pagamentos via MB WAY ou cartão (simulado).
Tentativas assíncronas em caso de falha transitória.
- **Namespace:** `lisboa_pedala.pagamentos`

### Disponibilidade
Mantém e expõe o estado em tempo real de bicicletas e docas
livres por estação (alimenta o mapa).
- **Namespace:** `lisboa_pedala.disponibilidade`

### Manutenção
Recebe e gere ordens de manutenção abertas por avaria
reportada pela bicicleta ou pelo utilizador.
- **Namespace:** `lisboa_pedala.manutencao`

### Redistribuição
Sugere rotas às carrinhas para equilibrar a ocupação
das estações, com base no estado atual da disponibilidade.
- **Namespace:** `lisboa_pedala.redistribuicao`

### Relatórios
Produz o relatório mensal de utilização por freguesia
e CO₂ evitado para a Câmara Municipal.
- **Namespace:** `lisboa_pedala.relatorios`

## 3. Mapeamento user story → componente

- **US-1** (desbloquear, devolver, registar e cobrar):
  Desbloqueio → Gateway de Docas → Viagens → Tarifário
  → Faturação → Pagamentos
- **US-2** (ordem de manutenção por avaria):
  Gateway de Docas → Manutenção
- **US-3** (doca sem rede reenvia eventos sem duplicar):
  Gateway de Docas → Viagens
- **US-4** (relatório de utilização por freguesia):
  Relatórios → Viagens

A US-1 envolve 6 componentes, cumprindo o requisito de
pelo menos uma user story com 3 ou mais componentes.

## 4. Nota sobre a entity trap

Não existem componentes "Bicicleta", "Estação" ou "Utilizador".
Esses são entidades de dados, não comportamentos. Os dados de 
uma bicicleta vivem nos componentes que precisam deles 
(Disponibilidade guarda o estado da doca; Manutenção guarda
o histórico de avarias). Um componente "Bicicleta" seria 
apenas CRUD sem lógica de negócio própria.

## 5. Análise de acoplamento e instabilidade

As dependências seguem o sentido do fluxo de negócio:

- **Desbloqueio**
  - Ce (usa): Viagens, Disponibilidade → Ce = 2
  - Ca (usado por): ninguém → Ca = 0
  - I = 2 / (0 + 2) = **1.0** — instável, é ponto de entrada

- **Gateway de Docas**
  - Ce (usa): Viagens, Disponibilidade, Manutenção → Ce = 3
  - Ca (usado por): ninguém (recebe eventos do hardware) → Ca = 0
  - I = 3 / (0 + 3) = **1.0** — instável, é ponto de entrada

- **Viagens**
  - Ce (usa): Tarifário, Faturação → Ce = 2
  - Ca (usado por): Desbloqueio, Gateway de Docas, Relatórios → Ca = 3
  - I = 2 / (3 + 2) = **0.4** — relativamente estável, correto

- **Tarifário**
  - Ce (usa): ninguém → Ce = 0
  - Ca (usado por): Viagens → Ca = 1
  - I = 0 / (1 + 0) = **0.0** — maximamente estável, correto
  (as regras de negócio do tarifário mudam raramente e
  muitos dependem delas)

- **Faturação**
  - Ce (usa): Pagamentos → Ce = 1
  - Ca (usado por): Viagens → Ca = 1
  - I = 1 / (1 + 1) = **0.5** — neutro, aceitável

- **Pagamentos**
  - Ce (usa): ninguém (sistema externo simulado) → Ce = 0
  - Ca (usado por): Faturação → Ca = 1
  - I = 0 / (1 + 0) = **0.0** — estável, correto

- **Disponibilidade**
  - Ce (usa): ninguém → Ce = 0
  - Ca (usado por): Desbloqueio, Gateway de Docas,
    Redistribuição → Ca = 3
  - I = 0 / (3 + 0) = **0.0** — muito estável, correto

- **Manutenção**
  - Ce (usa): ninguém → Ce = 0
  - Ca (usado por): Gateway de Docas → Ca = 1
  - I = 0 / (1 + 0) = **0.0** — estável

- **Redistribuição**
  - Ce (usa): Disponibilidade → Ce = 1
  - Ca (usado por): ninguém → Ca = 0
  - I = 1 / (0 + 1) = **1.0** — instável, é folha do grafo

- **Relatórios**
  - Ce (usa): Viagens → Ce = 1
  - Ca (usado por): ninguém → Ca = 0
  - I = 1 / (0 + 1) = **1.0** — instável, é folha do grafo

## 6. Análise de coesão

Cada componente tem coesão funcional: todas as suas 
operações servem um único propósito de negócio bem definido.

- **Tarifário** — só calcula preços. Não emite faturas,
  não cobra.
- **Gateway de Docas** — só recebe e normaliza eventos do
  hardware. Não decide o que fazer com eles além de os 
  encaminhar.
- **Viagens** — só gere o ciclo de vida da viagem. Não calcula
  preços nem emite faturas.

O risco de coesão mais baixa está no **Gateway de Docas**, 
que agrega eventos de natureza diferente (desbloqueio,
devolução, avaria). Mantém-se assim por coesão comunicacional:
todos os eventos vêm da mesma fonte (hardware das docas) e 
partilham o mesmo mecanismo de deduplicação.

## 7. Conascência

### Conascência de tipo — Viagens e Tarifário
Viagens passa a duração da viagem ao Tarifário como um 
inteiro de minutos. Ambos têm de concordar nesta representação:
se Viagens passar segundos ou um timedelta, o Tarifário calcula
mal. Esta conascência é de tipo/significado (connascence of
meaning) e é mitigada por um tipo explícito partilhado
`DuracaoMinutos` definido num módulo comum.

### Conascência de algoritmo — Gateway de Docas e Viagens
O Gateway deduplica eventos pelo campo `evento_id` antes
de os passar a Viagens. Viagens assume que não recebe 
duplicados. Se o algoritmo de deduplicação mudar (por exemplo,
passar a usar `evento_id + timestamp`), Viagens pode começar
a receber duplicados silenciosamente. Esta conascência de
algoritmo é documentada e mitigada por um contrato de 
interface explícito.

## 8. Acoplamento temporal

### Exemplo 1 — fecho de viagem e emissão de fatura
O fecho da viagem em Viagens e a emissão da fatura em 
Faturação têm de ocorrer na mesma unidade de trabalho
(transação). Se a viagem fechar mas a fatura não for emitida
(falha entre os dois passos), o utilizador viajou sem ser
cobrado e não há registo para a AT. Esta ordem é obrigatória
e não pode ser invertida nem omitida.

### Exemplo 2 — confirmação de encaixe antes do cálculo de preço
O evento "encaixe confirmado" da doca tem de ser processado
pelo Gateway de Docas e registado em Viagens (com o timestamp
de fim) antes de Tarifário calcular o preço. O Tarifário 
depende da duração real, que só existe depois do encaixe.
Chamar Tarifário antes viola este acoplamento temporal e
produz um preço errado.

## 9. Reestruturação (iteração 1)

### Problema identificado
No desenho inicial, Viagens chamava Faturação para emitir a
fatura, e Faturação chamava Viagens de volta para obter os
detalhes da viagem (duração, utilizador, tarifário aplicado).
Isto criava um ciclo de dependência:
`Viagens → Faturação → Viagens`

Um ciclo entre componentes viola as regras de allowed-to-use
e é detetado pelas fitness functions como erro.

### Solução aplicada
Viagens passou a ser responsável por recolher toda a 
informação necessária (duração, tipo de utilizador, valor
calculado pelo Tarifário) e passa-a como um objeto
`DadosFatura` completo para Faturação. Faturação nunca
chama Viagens. O ciclo foi eliminado.

### Resultado
`Viagens → Faturação` (unidirecional)
`Viagens → Tarifário` (unidirecional)
`Faturação` não depende de nenhum outro componente de domínio.