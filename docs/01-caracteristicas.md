# Características arquiteturais

## 1. Worksheet de candidatas

### 1. Integridade de dados
- **Tipo:** implícita
- **Frase do enunciado:** "Cada doca guarda até 24 h de eventos localmente." / "a viagem fecha quando a doca confirma o encaixe" / faturas "guardadas durante 10 anos"
- **Porque importa aqui:** As docas enviam eventos offline que chegam desfasados; sem garantia de consistência, a mesma viagem pode ser registada duas vezes ou o valor cobrado pode estar errado. As faturas têm obrigação legal de arquivo por 10 anos, pelo que um erro de dados não é recuperável.

### 2. Tolerância a falhas / disponibilidade
- **Tipo:** implícita
- **Frase do enunciado:** "O contrato de concessão aplica uma multa por cada hora em que mais de 10% das estações não conseguem desbloquear bicicletas." / "há zonas onde a rede falha com frequência"
- **Porque importa aqui:** 10% de 180 estações são 18. Se 18 estações ficarem inoperacionais durante 1 hora, há multa. A rede falha com frequência em certas zonas, o que significa que a disponibilidade não pode depender de conectividade contínua.

### 3. Privacidade
- **Tipo:** quase explícita
- **Frase do enunciado:** "O percurso de cada viagem é dado pessoal (RGPD)."
- **Porque importa aqui:** O percurso revela padrões de movimento dos utilizadores. O RGPD obriga a controlar quem acede, por quanto tempo os dados são guardados e como são eliminados. Uma violação tem consequências legais e reputacionais.

### 4. Viabilidade / custo
- **Tipo:** explícita
- **Frase do enunciado:** "Equipa de desenvolvimento de 6 pessoas e orçamento fixo."
- **Porque importa aqui:** Com 6 pessoas, uma arquitetura distribuída complexa (microserviços, filas de mensagens dedicadas, múltiplos deploys) é impossível de manter. A escolha de arquitetura tem de caber na capacidade da equipa.

### 5. Elasticidade
- **Tipo:** implícita
- **Frase do enunciado:** "Cerca de 70% dos desbloqueios acontecem entre as 8h00–9h30 e as 17h30–19h00." / "a procura em algumas estações multiplica por 4"
- **Porque importa aqui:** Os picos são previsíveis (hora de ponta) e pontuais (eventos). A telemetria das elétricas gera ~35 msg/s em pico (1 050 bicicletas × 1/30s), o que é um volume baixo e não justifica uma arquitetura de elasticidade automática.

### 6. Configurabilidade / extensibilidade
- **Tipo:** implícita
- **Frase do enunciado:** "Duas câmaras vizinhas mostraram interesse em usar a plataforma com tarifários próprios."
- **Porque importa aqui:** Se o tarifário estiver hardcoded, suportar outra câmara obriga a duplicar o sistema. Se estiver parametrizado, é uma configuração. O interesse ainda não é compromisso, por isso não conduz a arquitetura mas deve influenciar o desenho do módulo de tarifário.

### 7. Interoperabilidade
- **Tipo:** implícita
- **Frase do enunciado:** "As faturas são comunicadas à Autoridade Tributária" / "publicar a ocupação das estações como dados abertos" / MB WAY e cartão Navegante
- **Porque importa aqui:** O sistema tem três integrações externas obrigatórias com protocolos distintos. Cada uma pode mudar independentemente, por isso os pontos de integração têm de ser isolados do núcleo.

## 2. Top 3 (sem ordenar)

- **Integridade de dados.** É o único requisito com consequência legal direta (faturas 10 anos, AT) e operacional imediata (viagens duplicadas geram cobranças erradas). Se falhar, o sistema produz resultados incorretos que não se conseguem recuperar facilmente.
- **Tolerância a falhas / disponibilidade.** É o único requisito com penalização financeira explícita no contrato. A rede falha por design (zonas sem cobertura), por isso a falha não é um caso extremo, é o funcionamento normal.
- **Viabilidade / custo.** Com 6 pessoas e orçamento fixo, qualquer decisão de arquitetura que exija mais do que um monólito modular é inviável de implementar e manter. Esta característica é um filtro que elimina soluções tecnicamente elegantes mas irrealistas para esta equipa.

**Conflito entre as três:** Tolerância a falhas exige que as docas aceitem desbloqueios offline e guardem eventos localmente. Isso cria o risco de eventos duplicados ou fora de ordem quando a rede volta, atacando diretamente a Integridade. Resolver este conflito (deduplicação, ordenação de eventos) tem custo de implementação que pressiona a Viabilidade.

## 3. Outras consideradas

- **Elasticidade:** O volume de telemetria em pico é de aproximadamente 35 msg/s, e os picos de utilização são previsíveis e de curta duração. Não justifica uma arquitetura elástica automática; um servidor bem dimensionado chega.
- **Configurabilidade / extensibilidade:** O interesse das câmaras vizinhas ainda não é um requisito confirmado. Influencia o design do módulo de tarifário (que deve ser parametrizável) mas não conduz a arquitetura global.
- **Interoperabilidade:** As integrações externas (AT, MB WAY, Navegante) são pontos de contacto isoláveis com adaptadores. Importante mas não molda a estrutura interna do sistema.
- **Desempenho:** Não há requisitos de latência ou débito definidos. O volume é baixo para um sistema moderno.
- **Privacidade:** Resolve-se com boas práticas dentro de qualquer arquitetura (cifrar em repouso, controlo de acesso, retenção limitada). Não molda a estrutura do sistema.
- **Usabilidade:** Fora do âmbito da arquitetura de backend; não é pedida interface gráfica.
- **Testabilidade:** Importante mas consequência das outras escolhas, não um driver independente.

## 4. Característica composta decomposta

**Tolerância a falhas / disponibilidade**, decomposta em:

- **Operação offline na doca:** a doca consegue autorizar desbloqueios e registar eventos sem rede, durante pelo menos 24 horas.
- **Recuperação sem duplicação:** quando a rede volta, os eventos guardados localmente são reenviados e processados exatamente uma vez, sem criar viagens duplicadas.
- **Degradação graciosa do pagamento:** se o sistema de pagamentos externo (MB WAY) estiver indisponível, a viagem fica registada e o pagamento é tentado de forma assíncrona, sem bloquear o utilizador na doca.

## 5. Cenários das top 3

- **Cenário 1 — Tolerância a falhas:** Às 8h30, a cobertura móvel de 25 estações (14% do total) cai durante 40 minutos. Durante esse período, as docas continuam a autorizar desbloqueios com a lista de assinantes em cache local e a registar os eventos internamente. Ao fim de 40 minutos, a rede é reposta e todos os eventos são enviados para o servidor central. Nenhuma viagem é duplicada. A multa contratual não é aplicada porque a interrupção ficou abaixo de 1 hora e as estações nunca deixaram de desbloquear.

- **Cenário 2 — Integridade de dados:** Uma doca perde a ligação durante uma devolução e regista o evento "encaixe confirmado" localmente. Quando a rede volta, o evento é reenviado duas vezes por um bug no firmware. O sistema deteta o duplicado pelo identificador único do evento e processa-o apenas uma vez. A viagem é fechada com a duração correta e o valor cobrado é o certo.

- **Cenário 3 — Viabilidade / custo:** Um programador novo junta-se à equipa e precisa de acrescentar o tarifário de uma câmara vizinha. Encontra um módulo de tarifário isolado com uma interface clara, altera um ficheiro de configuração e escreve um teste. Não toca em código de faturação, pagamentos ou viagens. A alteração fica feita num dia.