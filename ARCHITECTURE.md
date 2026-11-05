# ARCHITECTURE.md — Lisboa Pedala

> Este ficheiro é a especificação de referência para geração
> de código com IA. Qualquer componente gerado tem de
> respeitar todas as regras aqui descritas. Ver também
> AGENTS.md se presente.

## 1. Componentes e responsabilidades

| Componente | Responsabilidade (uma frase) | Namespace |
|---|---|---|
| Desbloqueio | Valida o utilizador e autoriza a doca a libertar a bicicleta | `lisboa_pedala.desbloqueio` |
| Gateway de Docas | Recebe, deduplica por `evento_id` e encaminha eventos do hardware | `gateway` |
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

```
desbloqueio    → viagens, disponibilidade, shared
gateway        → viagens, disponibilidade, manutencao, shared
viagens        → tarifario, faturacao, shared
tarifario      → shared
faturacao      → pagamentos, shared
pagamentos     → shared
disponibilidade → shared
manutencao     → shared
redistribuicao → disponibilidade, shared
relatorios     → viagens, shared
```

**Proibições absolutas:**
- Ciclos de dependência entre quaisquer dois componentes.
- Qualquer componente a importar de `gateway`
  (o gateway só recebe, nunca é chamado).
- `faturacao` a importar de `viagens`
  (recebe um objeto `DadosFatura` completo, nunca chama de volta).
- `tarifario` a importar de qualquer componente de domínio.

## 3. Top 3 características e implicações para o código

### Tolerância a falhas / disponibilidade (ADR-002, ADR-003)
- O Gateway de Docas vive no namespace `gateway/`, separado de
  `lisboa_pedala/`. É importado no `main.py` mas nunca deve ser
  movido para dentro de nenhum sub-módulo de `lisboa_pedala/`.
- Todos os eventos de doca têm um campo `evento_id` (UUID).
- O Gateway mantém um `set` Python `_eventos_processados` em memória.
- Antes de encaminhar qualquer evento, verifica se `evento_id`
  já existe no set. Se existir, descarta sem erro.
- A doca pode reenviar o mesmo evento múltiplas vezes;
  o sistema tem de ser idempotente.

### Integridade de dados (ADR-003, ADR-004)
- O fecho de uma viagem e a emissão da fatura ocorrem em sequência
  atómica: primeiro `faturacao.emitir()`, depois atualiza o estado
  da viagem. Se `emitir()` lançar excepção, o estado da viagem
  não é alterado.
- O pagamento é processado de forma assíncrona após a fatura
  estar emitida (nunca bloqueia o fecho da viagem).
- Faturas têm estado: `pendente`, `pago`, `falhou`.
- O `evento_id` é guardado num `set` Python — duplicados são
  detectados por `evento_id in _eventos_processados`.

### Viabilidade / custo (ADR-001, ADR-005)
- Monólito modular: um único processo Python para todos os
  componentes. O Gateway vive em `gateway/` mas é incluído
  no mesmo processo via router FastAPI.
- Persistência em memória: dicionários Python por componente.
  Não há base de dados — os dados não sobrevivem a um restart.
- Sem frameworks de filas de mensagens (sem Celery, RabbitMQ,
  Kafka). Pagamentos assíncronos são simulados com `threading.Thread`.
- Interface REST (FastAPI). Sem frontend.

## 4. Acoplamento temporal — ordem obrigatória das operações

### Fluxo US-1 (desbloquear → devolver → cobrar)
Ordem estrita, cada passo depende do anterior:

```
1. Desbloqueio valida utilizador
2. Desbloqueio chama Viagens.abrir_viagem()
3. Gateway recebe evento "encaixe_confirmado" com evento_id
4. Gateway verifica duplicado — se evento_id já no set, para aqui
5. Gateway chama Viagens.fechar_viagem() com timestamp de fim
6. Viagens chama Tarifario.calcular() com duração e tipo
7. Viagens constrói DadosFatura completo
8. Viagens chama Faturacao.emitir() com DadosFatura
   ↑ passos 6, 7, 8 são uma sequência atómica em memória:
     se qualquer passo falhar, nenhum estado é persistido
9. Faturacao lança threading.Thread para Pagamentos.processar()
```

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
  `fastapi`, `uvicorn` e `pytest`.
- Cada componente é uma pasta com `__init__.py` e um
  `service.py` que expõe a lógica de negócio.
- Endpoints REST em `api.py` dentro de cada componente
  (router FastAPI incluído no main).
- Persistência: dicionários Python no topo de cada `service.py`
  (module-level). Não usar SQLite, ficheiros ou qualquer outra
  forma de persistência externa.
- Pagamentos assíncronos: usar `threading.Thread` com `daemon=True`.
- Todos os `evento_id` são UUID4 gerados na doca (simulado:
  gerados no momento da chamada ao Gateway).
- Nomes em português para domínio, inglês para infraestrutura
  (ex: `viagem`, `fatura`, mas `router`, `service`).

## 6. O que a IA não pode fazer

- Criar importações fora das regras da secção 2.
- Criar componentes com nomes de entidades
  ("Bicicleta", "Estação", "Utilizador").
- Usar `faturacao` para chamar `viagens` ou vice-versa.
- Processar pagamentos de forma síncrona bloqueante.
- Usar qualquer forma de persistência que não dicionários Python
  em memória (proibido: SQLite, ficheiros, Redis, PostgreSQL).
- Criar ciclos de dependência entre componentes.
- Omitir o campo `evento_id` em qualquer evento de doca.
- Fechar uma viagem sem chamar `faturacao.emitir()` primeiro.
- Incluir o Gateway como sub-módulo de `lisboa_pedala/` —
  o Gateway vive exclusivamente em `gateway/`.
- Mover lógica de deduplicação para fora do Gateway.

## 7. ADRs por componente

| Componente | ADRs relevantes |
|---|---|
| Gateway de Docas | ADR-002 (separação de namespace), ADR-003 (deduplicação) |
| Viagens | ADR-003 (integridade), ADR-004 (pagamentos assíncronos) |
| Tarifário | ADR-001 (monólito modular) |
| Faturação | ADR-004 (assíncrono) |
| Pagamentos | ADR-004 (assíncrono) |
| Todos | ADR-001 (monólito), ADR-005 (in-memory) |
