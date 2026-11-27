---
name: prd-canvas
description: 'Os 5 canvas da etapa 04 do PRD (Engenharia de dados, Ciência de dados, Software, Segurança, Operação e sustentação), bloco a bloco: quando cada um se aplica, a pergunta de cada bloco, o "bom quando", onde a informação costuma estar e como o bloco de esforço e custo alimenta os custos. Use no refinamento técnico, no comando "canvas <especialidade>" e para montar o pedido de gravação dos canvas.'
---

## Como usar os canvas

- Cada especialista preenche o seu canvas; o PM pode rascunhar a partir de documentos, marcado "validar com <especialista>".
- No topo de cada canvas: "Aplicável?" [Sim · Não] e "Motivo, se não se aplica". Canvas que não se aplica fica N/A, sempre com motivo.
- Cada bloco fica preenchido com fonte, "N/A" com o motivo, ou vira pergunta. Nunca deixe um bloco vazio sem dizer por quê.
- Todo canvas termina em **esforço e custo**: FTE por período (vai para o Anexo D) e custos de build e run (vão para a 04.5). Sem fonte para o custo por FTE, o bloco traz só o esforço.
- Riscos encontrados num bloco viram sugestão para o Anexo A; desvios do padrão viram decisão na 04.3.
- No pedido de gravação: `"canvas": {"eng": {"aplicavel": "Sim", "blocos": {"<título do bloco>": "<texto>"}}}`. Chaves: `eng`, `cie`, `sw`, `seg`, `op`. Os títulos dos blocos são os de baixo, exatamente.
- Comando "canvas <especialidade>": mostre o canvas atual, bloco a bloco, sem reescrever.

## Engenharia de dados (`eng`) · quase sempre se aplica

| Bloco | Pergunta | Bom quando |
|---|---|---|
| Fontes e acesso | De onde vem cada D-nn, e o acesso já existe? | Todo D-nn da R1 tem origem e forma de acesso; o que é "não sei" vira pergunta e confirma o Anexo C |
| Ingestão e frequência | Como e de quanto em quanto tempo os dados chegam? | A frequência atende à 02.4 (ex.: dado das 5h para um alerta das 8h) |
| Transformação e modelagem | Que tabelas e regras saem da ingestão? | As regras de negócio citam a 02.3; tabelas novas têm dono |
| Qualidade e reconciliação | Contra o que os números são conferidos, e com que tolerância? | Toda fonte com divergência conhecida tem conferência e tolerância; a divergência vira risco no Anexo A |
| Lineage e catálogo | Onde o dado fica documentado e rastreável? | Tabelas novas no catálogo da empresa |
| Ambientes | Desenvolvimento, teste e produção existem, com quais acessos? | Acessos solicitados ou disponíveis, com data |
| Volume e desempenho | Quanto dado, e quanto tempo cada carga pode levar? | A janela de carga cabe antes do consumo |
| Operação e alertas | O que é monitorado e quem recebe o alerta? | Falha de carga avisa alguém nomeado antes do horário de uso |
| Esforço e custo | FTE por período, build e run, com fonte | Bate com o Anexo D e a 04.5 |

Onde achar: documento de arquitetura, inventário de dados, conversa com a engenharia. Os pontos em aberto do discovery sobre dados (divergência, dado sem dono) aparecem aqui.

## Ciência de dados (`cie`) · só com modelo

| Bloco | Pergunta | Bom quando |
|---|---|---|
| Decisão e variável-alvo | O que o modelo prevê, para qual decisão, com que horizonte? | O alvo é uma definição verificável e a decisão é a da 03.1 |
| Dados e features | Que dados entram, com qual histórico? | Os D-nn citados existem na 02.5 e no Anexo C |
| Base de comparação e métricas | Contra o que o modelo é comparado; métrica técnica e de negócio | Há uma base (regra atual, média, decisão humana) e as duas métricas |
| Validação antes da produção | Como e com qual limiar o modelo é aprovado? | O limiar é o do Anexo E e foi definido antes do build |
| Explicabilidade e vieses | O que o usuário vê sobre o porquê; que grupos conferir | Atende à explicabilidade da 02.4; grupos sensíveis nomeados quando houver |
| Monitoramento e retreino | O que dispara a revisão ou o retreino? | Gatilho mensurável e frequência |
| Operação do modelo | Quem opera, onde roda, como é versionado? | Há dono e a execução cabe na janela de carga |
| Esforço e custo | FTE por período, build e run, com fonte | Bate com o Anexo D e a 04.5 |

O detalhe dos requisitos de IA (limiar, conjunto de avaliação, revisão humana) está no Anexo E: veja `prd-ia`. O canvas resume; o Anexo E manda.

## Software (`sw`) · com aplicação, API ou automação

| Bloco | Pergunta | Bom quando |
|---|---|---|
| Arquitetura da aplicação | Front-end, back-end e serviços | Componentes na 04.1 |
| Integrações e APIs | Com quais sistemas conversa, e como? | Cada integração tem dono do outro lado e contrato (formato, frequência) |
| Autenticação e autorização | Como implementa os perfis da 02.4? | Os perfis da 02.4 mapeados para papéis do sistema |
| Não funcionais atendidos | Como atende à 02.4 (desempenho, disponibilidade)? | Cada requisito da 02.4 tem como é atendido e testado |
| Testes | Unitários, de integração e de carga | Há os três quando aplicáveis, com quem roda |
| Esteira e ambientes | Como o código chega à produção? | Caminho de deploy e aprovação definidos |
| Observabilidade | Logs, métricas e alertas | O alerta chega a alguém nomeado |
| Esforço e custo | FTE por período, build e run, com fonte | Bate com o Anexo D e a 04.5 |

Sem aplicação própria (ex.: o produto sai num portal que já existe): "Aplicável?" = Não, com esse motivo.

## Segurança (`seg`) · sempre; simplificado no porte P

| Bloco | Pergunta | Bom quando |
|---|---|---|
| Classificação dos dados | Qual a classificação mais alta entre os D-nn? | Bate com o Anexo C |
| Dados pessoais | Base legal, minimização e retenção | Todo "sim" da triagem (03.5) tem base legal, o mínimo necessário e prazo de retenção |
| Modelo de acesso | Perfis da 02.4 e menor privilégio | Cada perfil vê só o que precisa |
| Ameaças e controles | O que pode dar errado e o que impede | Pelo menos o acesso indevido e o vazamento, com controle |
| Segredos e chaves | Onde ficam e quem acessa | Fora do código, num cofre ou equivalente |
| Logs e auditoria | O que é registrado e por quanto tempo | Acessos a dado pessoal registrados |
| Terceiros | Fornecedores e serviços externos que tocam o dado | Todo terceiro listado, com o que ele recebe; serviço de IA externo incluso |
| Aprovações necessárias | Quem precisa aprovar antes do go-live | Nomes ou áreas, e quando |
| Esforço e custo | FTE por período, build e run, com fonte | Bate com o Anexo D e a 04.5 |

**Porte P:** bastam classificação, dados pessoais e modelo de acesso, e os outros blocos com "N/A" e o motivo. Segurança nunca é dispensada: se o usuário pedir para pular, explique em uma linha que no P ela é simplificada, não dispensada.

Com IA generativa ou agente: o que o modelo pode ver e devolver entra em dados pessoais e no modelo de acesso (ex.: o agente mostra só a escala da loja do gerente); o envio de dado a um serviço externo entra em terceiros.

## Operação e sustentação (`op`) · sempre; simplificado no porte P

| Bloco | Pergunta | Bom quando |
|---|---|---|
| Pipelines e agendamentos | O que roda, quando e em que ordem | Horários coerentes com o consumo |
| Monitoramento e alertas | O que é acompanhado e quem é avisado | Alerta antes do usuário perceber |
| Dono operacional | Uma pessoa ou um time nomeado | Nome, não "o time de dados" |
| SLA | Parte da disponibilidade da 02.4 | Mensurável (ex.: alerta até as 8h em 95% dos dias) |
| Runbook | O que fazer em cada falha conhecida | Cobre as falhas dos blocos de alerta |
| Suporte e escalonamento | Quem atende e para quem escala | Canal e prazo |
| Transferência de conhecimento | Como e quando a operação aprende | Antes do go-live, com data |
| Esforço e custo de run | FTE e custos por ano, com fonte | Vai para "Sustentação" na 04.5 |

**Porte P:** bastam dono operacional, suporte e escalonamento e runbook. Os itens deste canvas são os critérios de handover citados no acordo de entrega (05.7).
