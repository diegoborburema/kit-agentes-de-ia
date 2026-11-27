---
name: prd-tecnico
description: 'Guia de preenchimento da etapa 04 (arquitetura, decisões, custos e business case; os canvas ficam em prd-canvas e os requisitos de IA em prd-ia), da etapa 05 (go-live, homologação, fases, go/no-go, cutover, contingência, rollback, comunicação e acordo de entrega) e dos anexos C e D do PRD: rótulos e colunas do template, "bom quando", regras de conta e perguntas. Use no refinamento técnico, nos custos, no business case e no go-live.'
---

## Como ler este guia

Igual a `prd-negocio`: **rótulos** vão em `campos`; **tabelas**, em `linhas` (`"04.5/custos"`); opções entre colchetes, pelo texto. Toda conta é feita só com dados das fontes ou do usuário, e mostrada na conversa.

## 04 · Refinamento técnico e custos

**04.1 · Arquitetura e componentes** · especialistas técnicos
- Rótulos: "Desenho" (fontes → ingestão → transformação → modelo → consumo, em linguagem simples) · "Aderência ao padrão".
- Tabela `componentes`: "Componente" · "Tecnologia" · "Novo ou reuso" · "Responsável".
- Bom quando: todo desvio do padrão da empresa tem uma decisão na 04.3; todo componente novo tem responsável.

**04.2 · Canvas por especialidade** · ver `prd-canvas`.

**04.3 · Decisões de arquitetura** · tabela `decisoes`: "ID" (DT-01…) · "Decisão" · "Alternativas" · "Racional". Obrigatório no porte G; recomendado no M.

**04.4 · Requisitos de IA** · rótulos: "Há IA na solução?" [Sim · Não] · "Onde está". Com "Sim", o detalhe vai no Anexo E (`prd-ia`).

**04.5 · Custos** · especialistas, com o PM · tabela `custos`, chave "Categoria" = Desenvolvimento – time interno · Desenvolvimento – fornecedor · Nuvem – processamento · Nuvem – armazenamento · Licenças · Aquisição de dados · Uso de IA (inferência ou tokens) · Sustentação · Evolução e retreino · Go-live e convivência · Adoção e mudança · TOTAL; colunas "Build" · "Run no ano 1" · "Run por ano depois" · "Total no horizonte" · "Premissa e fonte".
- Regras:
  - Total no horizonte = build + run no ano 1 + run por ano depois × (horizonte − 1).
  - "Desenvolvimento – time interno" = FTE-mês do Anexo D × custo por FTE-mês. O custo por FTE vem de uma fonte da empresa ou do usuário, que diz de onde veio. **Nunca** use valor "de mercado" ou suposto: sem fonte, a linha fica ○ e vira pergunta.
  - "Aquisição de dados" vem dos fornecedores com custo no Anexo C; "Uso de IA", do Anexo E (custo por uso); "Go-live e convivência", da 05.1 (manter a solução atual) e da 05.3 (operação assistida, hypercare).
  - O "esforço e custo" de cada canvas alimenta esta tabela.
- Bom quando: toda linha tem premissa e fonte, ou "R$ 0" com motivo; a linha TOTAL fecha com as outras.
- Se faltar: "Quantos FTE por especialidade e por quanto tempo? Qual o custo por FTE-mês usado na sua empresa, e de onde ele vem?"

**04.6 · Business case** · PM, com o revisor
- Tabela `bc`, chave "Linha" = Benefício (03.3), Build (04.5), Run (04.5), Resultado líquido; colunas "Ano 1" … "Ano 5" · "Total".
- Rótulos: "Payback" · "ROI no horizonte" · "Sensibilidade (benefício 30% menor)".
- Regras:
  - só monte quando 03.3 e 04.5 estiverem ✓; antes disso, diga o que falta e mostre só a parte com fonte;
  - resultado líquido = benefício − build − run, ano a ano;
  - ROI = (benefício total − custo total) ÷ custo total;
  - payback = mês em que o acumulado fica positivo; o build entra no início do ano 1 e o resto se distribui igualmente pelos meses;
  - sensibilidade (obrigatória no G, oferecida no M): o benefício 30% menor ainda paga o custo total?
- Mostre todas as contas na conversa, com os números de origem. Copie os totais para o painel (`painel_bc`).

## 05 · Go-live e transição

**05.1 · Estratégia de go-live** · sponsor, com o PM
- Rótulos: "Forma de lançamento" [Big bang · Por ondas · Piloto e expansão] · "O que a solução substitui" · "Convivência com a solução atual" · "Critério para desligar a solução atual" · "Time do negócio na transição" · "Operação assistida" · "Janelas a evitar" · "Dono da mudança".
- Bom quando: a convivência tem duração e critério de desligamento mensurável (ex.: 2 conferências seguidas dentro da tolerância), com quem decide; o time do negócio tem papéis, horas por semana e período ("o time apoia" é ◐); o dono da mudança é uma pessoa do negócio.
- Se faltar (sponsor): "A solução atual fica em paralelo? Por quanto tempo e até qual critério? Quem do seu time opera as duas nesse período, e quantas horas por semana?"

**05.2 · Homologação por release** · PM, com o sponsor
- Rótulos: "Quem dá o aceite" · "Homologadores" · "Período e ambiente" · "Critério de aceite da release".
- Tabela `roteiro`: "Caso" (H-01…) · "RF" · "Como testar" · "Resultado esperado" · "Release".
- Monte o roteiro a partir dos critérios de aceite da 02.1: um caso por RF da release, com o mesmo dado, caso e tolerância. RF sem critério não vira caso: vira lacuna na 02.1.
- Bom quando: o aceite é de uma pessoa nomeada; o roteiro cobre todo RF da release; o período e a base de teste estão definidos.

**05.3 · Fases da transição** · PM, com os especialistas · tabela `fases`, chave "Fase" = Homologação · Operação assistida · Go-live: onda 1 · Go-live: onda n · Convivência · Hypercare · Handover · Desligamento da solução atual; colunas "O que acontece" · "Início e fim" · "Participantes" · "Critério de saída" · "Responsável". Onda 2 ou mais: uma linha nova com a fase escrita ("Go-live: onda 2").
- Bom quando: toda fase que se aplica, conforme a 05.1, tem datas, participantes e critério de saída; a que não se aplica fica "N/A" em "O que acontece". Datas só da fonte ou do usuário.

**05.4 · Go/no-go** · PM · tabela `gonogo`, chave "Critério" = Homologação da release aceita · Dados reconciliados com a fonte · Acessos concedidos · Suporte e runbook prontos · Comunicação feita · Rollback ensaiado · Qualidade da IA atendida (quando houver); colunas "Como verificar" · "Responsável". Critério novo: linha nova. Rótulo: "Quem decide e quando".
- Bom quando: todo critério que se aplica tem como verificar e responsável; a decisão tem quem e quando. Sem IA, o último critério fica "N/A".

**05.5 · Cutover, contingência e rollback** · especialistas, com o PM
- Rótulos: "Cutover (sequência, janela e dono)" · "Contingência" · "Gatilhos de rollback" · "Como voltar" · "Tempo máximo para voltar" · "Quem decide e como comunica" · "Solução atual disponível até".
- **Contingência** é seguir sem voltar atrás (um plano B quando algo falha); **rollback** é voltar para a solução anterior. Não junte os dois, mesmo que o usuário peça: explique a diferença em uma linha e pergunte a contingência.
- Bom quando: os gatilhos são mensuráveis (horário, quantidade, percentual, dias seguidos); o tempo para voltar está definido; quem decide é uma pessoa; a solução atual fica disponível até uma data. "Se der errado, a gente volta" é ◐.

**05.6 · Comunicação, treinamento e adoção** · dono da mudança · tabela `publicos`, chave "Público" = Usuários finais · Gestores dos usuários · Áreas impactadas · Suporte; colunas "O que muda" · "Ação" · "Canal" · "Quando" · "Responsável". Rótulos: "Treinamento" · "Material de apoio" · "Canal de suporte" · "Métrica de adoção".
- Bom quando: todo público tem ação, data relativa ao go-live e responsável; a métrica de adoção é a premissa de adoção do benefício (03.3), com meta e data de medição. No P, bastam o comunicado, o canal de suporte e a métrica de adoção.

**05.7 · Acordo de entrega** · PM, com o revisor · rótulos: "Escopo da R1" · "Fora do escopo" · "Indicadores acordados" · "Aceite" · "Go-live" · "Critérios de handover" · "Quem conduz a execução" · "Datas".
- Bom quando: cita IDs e seções sem reescrever o conteúdo (ex.: "RF-01 a RF-04 (02.1)"; "Critérios de handover: canvas de Operação (04.2)").

## Anexos C e D

**Anexo C · Dados: origem, acesso e cuidados** · o negócio informa o que souber; a engenharia confirma · tabela `origem`: "ID" (D-nn da 02.5) · "Onde existe hoje" · "Disponível hoje" · "Forma de acesso" · "Classificação" (pública, interna, confidencial, restrita ou não sei) · "Dados pessoais" · "Dono do dado" · "Confirmado" ("☒" só quando a engenharia confirmar).
- Bom quando: nenhum dado da R1 com "não sei" em origem, acesso ou classificação; todo dado tem dono; fornecedor com custo aparece nos custos (04.5).

**Anexo D · Capacity e custos por especialidade** · especialistas
- Tabela `capacity`, chave "Período" (Mês 1, Mês 2… ou Sprint 1…; uma linha por período, antes da linha TOTAL); colunas "Engenharia" · "Ciência" · "Software" · "Segurança" · "Operação" · "Total", em FTE.
- Tabela `consolidacao`, chave "Especialidade"; colunas "Interno ou externo" · "Total FTE-mês" · "Custo por FTE-mês" · "Custo" · "Fonte".
- Bom quando: inclui operação assistida e hypercare; o custo por FTE tem fonte; o total bate com "Desenvolvimento – time interno" na 04.5.
- Peça a estimativa em FTE por especialidade e período, e não em horas soltas.
