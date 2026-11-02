# ARCHITECTURE.md — Lisboa Pedala

> Este ficheiro é a especificação de referência para geração
> de código com IA. Qualquer componente gerado tem de
> respeitar todas as regras aqui descritas. Ver também
> AGENTS.md se presente.

## 1. Componentes e responsabilidades

| Componente | Responsabilidade (uma frase) | Namespace |
|---|---|---|
| Desbloqueio | Valida o utilizador e autoriza a doca a libertar a bicicleta | `lisboa_pedala.desbloqueio` |
| Gateway de Docas | Recebe, deduplica por `evento_id` e encaminha eventos do hardware | `lisboa_pedala.gateway_docas` |
| Viagens | Abre, fecha e guarda o ciclo de vida de cada viagem | `lisboa_pedala.viagens` |
| Tarifário | Calcula o valor a cobrar dado o tipo de utilizador e a duração | `lisboa_pedala.tarifario` |
| Faturação | Emite, arquiva e comunica faturas à AT | `lisboa_pedala.faturacao` |
| Pagamentos | Processa pagamentos MB WAY / cartão de forma assíncrona (simulado) | `lisboa_pedala.pagamentos` |
| Disponibilidade | Mantém o estado em tempo real de docas e bicicletas livres | `lisboa_pedala.disponibilidade` |
| Manutenção | Cria e gere ordens de manutenção por avaria | `lisboa_pedala.manutencao` |
| Redistribuição | Sugere rotas às carrinhas com base na ocupação das estações | `lisboa_pedala.redistribuicao` |
| Relatórios | Produz o relatório mensal de utilização por freguesia e CO₂ evitado | `lisboa_pedala.relatorios` |
| Shared | Tipos partilhados entre componentes (sem lógica de negócio) | `lisboa_pedala.shared` |

## 2. Regras allowed-to-use (verificáveis por import-linter)

Cada linha é uma regra. Qualquer importação fora desta lista
é uma violação e deve ser rejeitada pelas fitness functions.

desbloqueio → viagens, disponibilidade, shared
gateway_docas → viagens, disponibilidade, manutencao, shared
viagens → tarifario, faturacao, shared
tarifario → shared
faturacao → pagamentos, shared
pagamentos → shared
disponibilidade → shared
manutencao → shared
redistribuicao → disponibilidade, shared
relatorios → viagens, shared


**Proibições absolutas:**
- Ciclos de dependência entre quaisquer dois componentes.
- Qualquer componente a importar de `gateway_docas`
  (o gateway só recebe, nunca é chamado).
- `faturacao` a importar de `viagens`
  (recebe um objeto `DadosFatura` completo, nunca chama de volta).
- `tarifario` a importar de qualquer componente de domínio.

## 3. Top 3 características e implicações para o código

### Tolerância a falhas / disponibilidade (ADR-002, ADR-003)
- O Gateway de Docas corre como processo separado do monólito.
- Todos os eventos de doca têm um campo `evento_id` (UUID).
- O Gateway mantém uma tabela `eventos_processados` com TTL 48h.
- Antes de encaminhar qualquer evento, verifica se `evento_id`
  já existe. Se existir, descarta sem erro.
- A doca pode reenviar o mesmo evento múltiplas vezes;
  o sistema tem de ser idempotente.

### Integridade de dados (ADR-003, ADR-004)
- O fecho de uma viagem e a emissão da fatura ocorrem na mesma
  transação de base de dados. Se a fatura não for criada,
  a transação faz rollback e a viagem não é fechada.
- O pagamento é processado de forma assíncrona após a fatura
  estar emitida (nunca bloqueia o fecho da viagem).
- Faturas têm estado: `pendente`, `pago`, `falhou`.
- O campo `evento_id` é UNIQUE na base de dados (constraint).

### Viabilidade / custo (ADR-001, ADR-005)
- Monólito modular: um único processo Python para todos os
  componentes exceto o Gateway.
- Persistência em SQLite (um ficheiro `lisboa_pedala.db`).
- Sem frameworks de filas de mensagens (sem Celery, RabbitMQ,
  Kafka). Pagamentos assíncronos são simulados com uma tabela
  `pagamentos_pendentes` e um loop de retentativa.
- Interface CLI ou REST (FastAPI). Sem frontend.

## 4. Acoplamento temporal — ordem obrigatória das operações

### Fluxo US-1 (desbloquear → devolver → cobrar)
Ordem estrita, cada passo depende do anterior:

1. Desbloqueio valida utilizador
2. Desbloqueio chama Viagens.abrir_viagem()
3. Gateway recebe evento “encaixe_confirmado” com evento_id
4. Gateway verifica duplicado — se duplicado, para aqui
5. Gateway chama Viagens.fechar_viagem() com timestamp de fim
6. Viagens chama Tarifario.calcular() com duração e tipo
7. Viagens constrói DadosFatura completo
8. Viagens chama Faturacao.emitir() com DadosFatura
↑ passos 6, 7, 8 numa só transação de base de dados
9. Faturacao chama Pagamentos.processar() de forma assíncrona


O passo 9 nunca bloqueia o passo 8.
O Tarifário nunca é chamado antes do timestamp de fim existir.

### Tipo partilhado DadosFatura (shared)
```python
@dataclass
class DadosFatura:
    viagem_id: str
    utilizador_id: str
    duracao_minutos: int
    tipo_utilizador: str  # "assinante" | "ocasional"
    valor_euros: float
    timestamp_inicio: datetime
    timestamp_fim: datetime
```

### Tipo partilhado DuracaoMinutos (shared)
```python
DuracaoMinutos = int  # sempre inteiro, arredondado para cima
```

## 5. Convenções de código

- Python 3.11+. Sem dependências externas além de
  `fastapi`, `uvicorn`, `sqlite3` (stdlib) e `pytest`.
- Cada componente é uma pasta com `__init__.py` e um
  `service.py` que expõe a lógica de negócio.
- Endpoints REST em `api.py` dentro de cada componente
  (router FastAPI incluído no main).
- Testes em `tests/` espelhando a estrutura de `src/`.
- Todos os `evento_id` são UUID4 gerados na doca (simulado:
  gerados no momento da chamada ao Gateway).
- Nomes em português para domínio, inglês para infraestrutura
  (ex: `viagem`, `fatura`, mas `router`, `service`, `db`).

## 6. O que a IA não pode fazer

- Criar importações fora das regras da secção 2.
- Criar componentes com nomes de entidades
  ("Bicicleta", "Estação", "Utilizador").
- Usar `faturacao` para chamar `viagens` ou vice-versa.
- Processar pagamentos de forma síncrona bloqueante.
- Usar qualquer base de dados que não SQLite.
- Criar ciclos de dependência entre componentes.
- Omitir o campo `evento_id` em qualquer evento de doca.
- Fechar uma viagem sem calcular o preço e emitir a fatura
  na mesma transação.

## 7. ADRs por componente

| Componente | ADRs relevantes |
|---|---|
| Gateway de Docas | ADR-002 (processo separado), ADR-003 (deduplicação) |
| Viagens | ADR-003 (integridade), ADR-004 (pagamentos assíncronos) |
| Tarifário | ADR-001 (monólito modular) |
| Faturação | ADR-004 (assíncrono), ADR-005 (SQLite) |
| Pagamentos | ADR-004 (assíncrono) |
| Todos | ADR-001 (monólito), ADR-005 (SQLite) |