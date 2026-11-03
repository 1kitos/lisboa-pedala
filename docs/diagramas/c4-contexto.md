# C4 Nível 1 — Contexto

```mermaid
C4Context
    title Sistema Lisboa Pedala — Contexto

    Person(assinante, "Assinante", "60 000; passe anual")
    Person(ocasional, "Utilizador Ocasional", "15 000/mês")
    Person(tecnico, "Técnico de Manutenção", "25 técnicos")
    Person(redistribuicao, "Equipa de Redistribuição", "6 carrinhas")
    Person(gestor, "Gestor Municipal", "~10 gestores")

    System(lp, "Lisboa Pedala", "Plataforma de bicicletas partilhadas: desbloqueio, cobrança, manutenção, relatórios")

    System_Ext(at, "Autoridade Tributária", "Recebe faturas mensalmente")
    System_Ext(mbway, "MB WAY / Cartão", "Processamento de pagamentos")
    System_Ext(navegante, "Cartão Navegante", "Autenticação de assinantes")
    System_Ext(docas, "Docas e Bicicletas", "Hardware IoT; enviam telemetria e eventos")

    Rel(assinante, lp, "Desbloqueia e devolve bicicletas, consulta histórico")
    Rel(ocasional, lp, "Paga e usa bicicletas")
    Rel(tecnico, lp, "Gere ordens de manutenção")
    Rel(redistribuicao, lp, "Consulta rotas de redistribuição")
    Rel(gestor, lp, "Consulta relatórios mensais")
    Rel(lp, at, "Envia faturas", "HTTP")
    Rel(lp, mbway, "Processa pagamentos", "HTTP/simulado")
    Rel(navegante, lp, "Autentica assinantes", "HTTP/simulado")
    Rel(docas, lp, "Envia eventos e telemetria", "HTTP/simulado")
```

## Legenda

| Elemento | Descrição |
|---|---|
| 🧍 Pessoa (azul) | Utilizador humano do sistema |
| ▭ Sistema (azul escuro) | O sistema Lisboa Pedala |
| ▭ Sistema externo (cinzento) | Sistema fora do âmbito da solução |
| → Relação | Interação entre elementos; etiqueta indica protocolo |