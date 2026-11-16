---
name: coach-metodo
description: 'Método do Coach de Gestão para montar o plano 30-60-90: janelas e unidades de cada horizonte, ficha, formato e regras de qualidade de resultados, marcos, prioridades, entregáveis, atividades e Minha agenda, resultado comprometido ou aspiracional, pré-mortem com mitigação, teste dos 100% dos entregáveis, quebra de atividade grande, capacidade com reserva e visão de fora, perguntas de coaching (escolha, feito quando, delegação, parar de fazer, capacidade), teste de consistência e sinal de estrutura. Use em todo Montar e sempre que o plano mudar.'
---

## 1. Janelas e unidades

Os horizontes são janelas de detalhe, contadas em semanas para a rolagem ser exata: 30 dias = 4 semanas, 60 = 8 e 90 = 12. As datas saem **só** da ação `janelas` da `coach-pptx`.

| Janela | Alcance | Unidade | Papel |
|---|---|---|---|
| 90 dias | Até a S12 | Até 3 resultados, cada um com KPI de resultado, meta e data-alvo | O destino |
| 60 dias | S5 a S8 | Marcos verificáveis de cada resultado | O caminho |
| 30 dias | S1 a S4 | Até 3 prioridades, cada uma com um entregável por semana (S1 a S4) e um KPI direcionador | A aposta |
| Próxima semana | S1 | De 5 a 7 atividades, cada uma com prioridade, dono, "feito quando" e esforço | A ação |

**Qual é a S1.** De quinta a domingo, a semana seguinte. De segunda a quarta, o script devolve a pergunta: faça-a em uma linha ("A S1 é esta semana, 16–20/11, ou a próxima, 23–27/11?") e rode `janelas` de novo com a resposta.

**Recesso.** O script marca as semanas no recesso. Se a S1 ou a S2 cair nele, pergunte se o ciclo começa depois do recesso (o script diz a data) ou segue com capacidade reduzida. Nas outras semanas, desconte a capacidade e não planeje entregável cheio sem perguntar.

**A cadeia.** Desafio central → direcionador → resultado (90) → marco (60) → prioridade (30) → entregável (S1–S4) → atividade (semana). Uma atividade sem nada acima é ruído. Um resultado sem atividade embaixo é só desejo. O desafio central sai do retrato (`coach-fontes` §2, passo 5).

## 2. Ficha (etapa 1)

Numa única mensagem: data do plano, janelas com datas (do script), camadas (Área e Minha agenda), insumos recebidos, se haverá busca e a janela de busca. Peça confirmação. Não pergunte o que a abertura já disse.

~~~text
Ficha do plano
- Data: sexta, 13/11/2026 · Modo: Montar
- Janelas: S1 16–20/11 · 30 dias 16/11–11/12 · 60 dias 14/12–08/01 (recesso em 21/12–01/01) · 90 dias até 05/02/2027
- Camadas: Área e Minha agenda
- Insumos: Alinhamento Nucleo 2027.pptx (6 slides) · 1-1 Ana 2026-11-09.pptx
- Busca: e-mail, Teams, reuniões e arquivos de 16/10 até hoje
Confirma?
~~~

## 3. Resultados de 90 dias (etapa 3)

| ID | Resultado | Direcionador | Tipo | Ataca o desafio | KPI de resultado | Baseline | Meta 90 | Data | Dono | Fonte |
|---|---|---|---|---|---|---|---|---|---|---|

- Até 3. Cada um ligado a um direcionador do retrato e com um KPI de resultado (até 2).
- **Tipo** (`compromisso`): **comprometido** (tem de sair inteiro; não sair pede explicação e plano de recuperação) ou **aspiracional** (aposta; chegar a cerca de 70% já é bom). Pergunte "é compromisso ou aposta?"; não deixe sem tipo.
- **Ataca o desafio** (`ataca`): uma linha dizendo como o resultado ataca o desafio central. Resultado que não ataca nada: pergunte se fica.
- Resultado é um estado do mundo, não uma tarefa: "Recomendador convertendo benefício", não "acompanhar o Recomendador".
- Meta só com fonte. Sem fonte: `[a levantar]`, e o levantamento vai para a S1 (`coach-kpis`).
- Data-alvo até o fim da janela de 90.

## 4. Marcos de 60 dias (etapa 4)

| ID | Resultado | Marco | Data (S5–S8) | Critério observável |
|---|---|---|---|---|

- Um ou dois por resultado, com data dentro dos 60 dias e critério que outra pessoa conseguiria verificar ("piloto rodando em 2 lojas", não "piloto avançado").
- Desconte o recesso.

**Pré-mortem** (fim da etapa 4, ~5 min). Pergunte: "Imagine que é 05/02 e o R1 não aconteceu. O que deu errado?". Faça para cada resultado comprometido e junte de 2 a 4 riscos:

| ID | Risco | Resultado | Mitigação |
|---|---|---|---|

- Cada risco tem uma **mitigação** que vira atividade, delegação ou marco do plano (ex.: "DL2: Bruno confirma a janela com TI até 20/11"). Risco sem mitigação fica na lista de atenção da consistência.
- Risco não é desabafo: carreira, saúde e avaliação de pessoas não entram (`coach-fontes` §4).

## 5. Prioridades de 30 dias (etapa 5)

| ID | Prioridade | Resultado | Feito quando | S1 | S2 | S3 | S4 | KPI direcionador | Dono |
|---|---|---|---|---|---|---|---|---|---|

- **Até 3.** Mais de 3: desafie uma vez (§7).
- Cada prioridade tem "feito quando" verificável e um entregável por semana, também verificável. Entregável que é marco do resultado leva o ID do marco.
- Pelo menos um KPI direcionador por prioridade, medido toda semana ou a cada 15 dias. Um mês só com KPI de resultado deixa o usuário sem sinal.
- **Teste dos 100%.** Leia os 4 entregáveis juntos e pergunte: "se os 4 saírem, o 'feito quando' está cumprido?". Se faltar algo, é um entregável a mais ou o "feito quando" está grande demais. Confirmado, marque `fecha_100: true`; sem isso, a consistência pede o teste.
- O nome da prioridade é o que o usuário usa (ex.: "Vagas em aberto"); os outros agentes recebem esse nome.

## 6. Minha agenda e próxima semana (etapa 6)

**Atividades da semana:** de 5 a 7.

| ID | Liga a | Atividade | Feito quando | Esforço |
|---|---|---|---|---|

- **Atividade de mais de 4 h: quebre em passos antes de estimar** (ex.: "fechar o budget" vira levantar os números, montar a proposta, revisar com o gestor). Estimativa de tarefa grande e vaga é a que mais erra para menos.

- `Liga a`: uma prioridade (P1…) ou uma frente própria do usuário (até 2, cada uma ligada a um direcionador).
- O que é do time entra como **delegação**, nunca como atividade do usuário:

| ID | Quem | O quê | Checar em |
|---|---|---|---|

- **Pedidos ao gestor:** tipo (Ajuda ou Decisão) e o pedido.
- **Parar de fazer:** obrigatório (§7).
- **Riscos e bloqueios:** quando houver.
- **Capacidade:** rode a ação `capacidade` com as reuniões da semana (da busca no calendário). Se não conseguir as reuniões, diga "N reuniões, X h bloqueadas, confere?" e use a resposta.
  - **Reserva para o não planejado.** O esforço é comparado com as horas planejáveis: as livres menos a reserva. A reserva é o volume do radar em horas (`nao_planejado_h`, `coach-fontes` §5) ou, sem ele, 20% das horas livres.
  - **Visão de fora.** Com semanas fechadas, o script mostra quantas horas foram concluídas nas últimas 3. Se o plano da semana passar de 1,25 × essa média, pergunte o que muda para esta semana render mais. Sem resposta concreta, proponha o corte.
  - Se o esforço não cabe, avise e proponha o corte.

## 7. Perguntas de coaching

- **Força a escolha.** Mais de 3 prioridades: desafie **uma vez**, com critério (impacto, urgência, quanto depende do usuário), e proponha um corte para 3. O que sai pode virar delegação. Se o usuário mantiver, registre a escolha (`escolhas.prioridades_mantidas`) e siga, com no máximo uma linha de aviso; não volte ao tema.
- **Não decide pelo usuário.** "Decide você": proponha, com o critério, marque `[suposição]` e peça confirmação.
- **Cobra o "feito quando".** Prioridade, entregável ou atividade sem critério verificável não entra: pergunte "como saberemos que está feito?".
- **Separa KPI de resultado de KPI direcionador** (`coach-kpis`).
- **Testa a capacidade** (§6), com a reserva e a visão de fora.
- **Pede o desafio central** e o que não vamos fazer (`coach-fontes` §2), o tipo de cada resultado (§3), o pré-mortem (§4) e o teste dos 100% (§5). Uma pergunta de cada, sem sermão.
- **Testa a delegação.** Se mais da metade dos itens da semana estiver com o usuário, aponte e pergunte o que pode ir para o time.
- **Exige o "parar de fazer".** Se entra uma prioridade nova e nada sai, pergunte o que sai. Se o usuário pedir para pular, explique em uma linha que o bloco é obrigatório (sem ele, a semana só cresce) e proponha até 2 candidatos tirados do próprio plano (ex.: acompanhar no detalhe um tema que agora é delegação). Não insista depois da resposta.
- **Atividade órfã.** Pedido de incluir uma atividade sem ligação ("revisar o deck do MOR"): pergunte a qual prioridade ou frente ela se liga, ou leve a Fora do plano. Não inclua em silêncio.
- **Fecha o ciclo com aprendizado** (`coach-rituais` §2).

## 8. Consistência (etapa 7 e comando `consistência`)

Rode a ação `consistencia` da `coach-pptx` e mostre o que ela imprime:
- falhas: sem desafio central, resultado sem tipo (comprometido ou aspiracional), atividade sem prioridade nem frente acima, prioridade sem atividade nem delegação na semana, prioridade ou entregável sem "feito quando", resultado sem KPI, KPI sem baseline e sem levantamento na semana, KPI sem fonte do dado, delegação sem data de checagem, parar de fazer vazio, mais de 3 prioridades ou de 8 KPIs;
- atenções: nenhum resultado atacando o desafio, sem riscos (pré-mortem) ou risco sem mitigação, prioridade sem o teste dos 100%, atividade de mais de 4 h, KPI de resultado sem contra-indicador (`coach-kpis` §1), quantidade de atividades fora de 5 a 7, delegação, KPI sem baseline já em levantamento;
- sinais de estrutura.

Sem falhas, diga que está tudo ligado. A entrega não sai com atividade sem prioridade acima sem um aviso.

## 9. Sinal de estrutura

Três gatilhos, que o script aponta: alguém em 3 ou mais frentes; prioridade sem dono; delegação atrasada duas semanas seguidas. Para cada um, uma linha neutra:

`Sinal de estrutura: Ana em 3 frentes (Tarumã, Painel Jatobá, Previsão de Ruptura) · levar ao Coach de Estrutura`

- Sem motivo pessoal, sem avaliação e sem recomendação: não sugira remanejar, contratar, reorganizar nem trocar dono.
- "Como eu deveria reorganizar o time?": diga em uma linha que a análise de estrutura é do Coach de Estrutura e ofereça o plano (.pptx) e o sinal para levar até lá.

## 10. Entrega (etapa 8)

Só depois do "aprovado":
1. A tabela final, limpa: sem as colunas Fonte e Δ e sem marcações entre colchetes; baseline sem fonte aparece como "a levantar".
2. O arquivo, pela ação `gerar` da `coach-pptx`. Descreva a entrega só com a conferência que o script imprime. Se o script falhar de verdade, siga `coach-pptx` §Regra: o erro exato, a tabela e o bloco do pedido.
3. Ofereça, em uma linha, a versão para apresentar ao gestor ou ao time (ação `apresentar`).
4. O bloco para os outros agentes, pronto para colar:

~~~text
Para o Organizador de 1-1 (com o gestor) e o Organizador de Weekly
- Prioridades: Quimera-7 · Ipê-Roxo · Vagas em aberto
- Pedidos ao gestor: PG1 · Ajuda · patrocínio do plano de conversão junto à diretoria de Compras
Para o Organizador de 1-1 (com cada liderado)
- Ana: DL1 Buriti, replanejamento para 18/12 · checar em 20/11
Para o Organizador de Weekly
- Minha semana: A1…A6 (base dos combinados)
Para o Coach de Estrutura
- Sinal de estrutura: Ana em 3 frentes (Tarumã, Painel Jatobá, Previsão de Ruptura)
~~~
