# Reflexão

## O que a especificação não previu

### Persistência em memória vs. SQLite
A especificação original (ARCHITECTURE.md e ADR-005) definia
SQLite como mecanismo de persistência. A implementação usou
dicionários Python em memória por ser mais simples para o
âmbito do protótipo. A especificação teve de ser revista
(ADR-005 revisto) para reflectir a decisão real. A IA seguiu
a spec original literalmente e gerou código com SQLite, que
foi rejeitado e substituído.

### Importações transitivas não previstas
O `.importlinter` com contratos `forbidden` verifica também
importações transitivas por omissão. Por exemplo, `desbloqueio`
importa `viagens`, que importa `faturacao` — o linter reportou
que `desbloqueio` estava a importar `faturacao` indiretamente.
A especificação não previa este comportamento do linter.
Resolvido adicionando `allow_indirect_imports = True` aos
contratos relevantes.

### Formato dos identificadores
ARCHITECTURE.md especifica `evento_id` como UUID mas não define
o formato dos restantes identificadores (`viagem_id`,
`utilizador_id`, `fatura_id`). No protótipo todos são UUIDs
gerados com `uuid.uuid4()`, mas a spec devia ter explicitado
este contrato para todos os IDs.

### Gateway como módulo vs. processo separado
ADR-002 define o Gateway como processo separado a comunicar
via HTTP. No protótipo, o Gateway vive em `gateway/` mas corre
no mesmo processo que o monólito. A spec não definia
claramente o comportamento esperado no contexto de um
protótipo, o que causou ambiguidade na geração de código.

## Violações que a IA cometeu

### Violação 1 — `gateway/service.py` em falta (detectada em runtime)
Quando foi pedido à IA para gerar o Gateway, gerou
`gateway/main.py` com os endpoints mas não criou
`gateway/service.py` com a lógica de negócio. O `gateway/api.py`
tentou importar `from . import service` e falhou com
`ImportError` no arranque do servidor. A fitness function não
detectou porque verifica importações entre módulos existentes,
não a ausência de módulos. Foi detectada ao tentar arrancar
o servidor com `uvicorn`.

### Violação 2 — Gateway incluído no namespace errado (detectada por revisão humana)
A IA gerou o Gateway como router FastAPI dentro de
`lisboa_pedala/main.py`, ignorando ADR-002 e a separação de
namespaces. ARCHITECTURE.md não tinha a regra explícita
"o Gateway não pode ser sub-módulo de `lisboa_pedala/`".
A violação foi detectada por revisão humana e a regra foi
adicionada à secção 6 do ARCHITECTURE.md após a ocorrência.

### Violação 3 — Parâmetro de path declarado como Query (detectada em runtime)
No `relatorios/api.py`, o endpoint `GET /mensal/{ano}/{mes}`
foi gerado com `mes: int = Query(ge=1, le=12)`. O FastAPI
não permite usar `Query` para parâmetros que estão na path
— causou `AssertionError` no arranque. A fitness function
não detectou porque é uma violação semântica de uso do
framework, não estrutural. Foi detectada ao arrancar o
servidor.

## O que as fitness functions apanharam

- Importações proibidas entre componentes (`lint-imports`,
  contrato `forbidden`) — validado com `lint-imports` a verde
  antes de qualquer commit de código.
- Importações transitivas não intencionais — o linter reportou
  cadeias como `desbloqueio → viagens → faturacao`, que levaram
  à adição de `allow_indirect_imports = True`.

## O que passou despercebido às fitness functions

- Ausência de ficheiros obrigatórios (`gateway/service.py`).
- Violações semânticas de framework (Query vs. Path).
- Inconsistência entre spec (SQLite) e implementação (memória).
- Ambiguidade na separação Gateway/monólito em contexto de protótipo.

As fitness functions verificam *estrutura* (quem importa quem)
mas não *comportamento* nem *completude*. As três violações
acima foram todas detectadas em runtime ou por revisão humana,
não pelo linter. Testes de integração das user stories são
necessários para cobrir o segundo tipo de violação — um teste
que arranca o servidor e chama os endpoints teria apanhado
as violações 1 e 3 automaticamente.