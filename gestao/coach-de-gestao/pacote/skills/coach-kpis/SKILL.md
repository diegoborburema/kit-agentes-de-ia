---
name: coach-kpis
description: 'KPIs do Coach de Gestão: o cartão do KPI, os tipos (resultado, direcionador e saúde), as regras de baseline e meta (sem fonte fica a levantar, sem interpolação sem baseline), os limites por resultado e prioridade, o contra-indicador, a confiança de 0 a 10 por resultado, o pulso semanal com a nota de execução e o banco de sugestões. Use ao definir os KPIs no Montar, no comando kpis e no pulso da revisão.'
---

## 1. Cartão

Nome · Tipo · Definição ou fórmula · Fonte do dado · Baseline · Meta 30/60/90 · Frequência · Dono · Status (🟢 🟡 🔴 ⚪ sem dado) · Par

| Tipo | Para que serve | Onde aparece |
|---|---|---|
| Resultado | Mostra se o resultado foi atingido | Janela de 90 (até 2 por resultado) |
| Direcionador | Dá sinal antecipado, medido toda semana ou a cada 15 dias | Prioridades de 30 (pelo menos 1 por prioridade) |
| Saúde | Alarme do time ou do processo; não é meta | Scorecard |

Até 8 KPIs no scorecard.

**Par (contra-indicador).** Todo KPI de resultado ganha um par que mostra o efeito colateral de persegui-lo (Grove): quantidade com qualidade, velocidade com retrabalho, benefício com carga do time. Ex.: "% de chamados resolvidos pela Triagem" com "% de chamados reabertos depois da Triagem". O par pode ser outro KPI do scorecard (`"par": "K5"`) ou só um nome, acompanhado no pulso sem meta. Sem par, a consistência dá atenção.

## 2. Baseline e meta

- **Só com fonte.** Baseline e meta vêm de um arquivo, do usuário com a origem do número, ou da busca com a data da fonte e `[a confirmar]`.
- **Sem fonte: `[a levantar]`**, e o levantamento vira uma atividade ou delegação na S1, com o KPI em `levanta` (ex.: `"levanta": ["K2"]`). O script cobra isso na consistência.
- **Número "de cabeça" não entra.** "Coloca 41, deve estar por aí": não grave; pergunte de onde vem o número e mantenha `[a levantar]` com o levantamento na S1.
- **Sem baseline, sem interpolação.** Não calcule meta de 30 ou 60 dias a partir da meta final sem um ponto de partida medido. Diga isso em uma linha e deixe a meta intermediária em aberto.
- **Meta de 2027 não é meta de 90 dias.** Uma meta anual (ex.: NPS 40 em 2027) entra como referência; a meta de 90 só com base e fonte.
- **KPI do Analista de Benefícios** usa o número da última análise, com a data (ex.: "R$ 0,3 MM/mês (nov) · [Painel do Recomendador · 10/12]"). Não projete dezembro nem janeiro.

## 3. Pulso (revisão semanal)

- Para cada KPI: o valor novo, com a data e a fonte, ou "sem dado novo".
- Sem dado novo, o KPI fica com o último valor e a data, ou ⚪. Nunca um número fora dos anexos, da busca com fonte e do que o usuário disse.
- O status (🟢 🟡 🔴) muda só com evidência.
- Mande os valores novos em `kpis` no pedido da revisão (`coach-pptx`).
- **Confiança, de 0 a 10, em cada resultado** (Wodtke): "de 0 a 10, quanto você acredita que o R1 sai até 05/02?". Uma pergunta para todos os resultados, numa linha. Comece o ciclo perto de 5. Mande em `confianca`. O script avisa queda de 2 pontos ou mais (pergunte o porquê e o risco) e nota de 3 ou menos (pergunte o que mudaria a nota). Confiança é opinião do usuário: não proponha a nota.
- **Nota de execução** (Moran): o script calcula as atividades feitas sobre as planejadas (canceladas com motivo ficam fora). Abaixo de 85%, pergunte se o plano estava grande demais ou se algo travou, e não aumente a carga da semana nova.

## 3a. Leitura conjunta

O KPI de resultado anda devagar; a execução e a confiança dão o sinal antes. Leia os três juntos:

| Execução | KPI e confiança | Leitura |
|---|---|---|
| Alta (85% ou mais) | Parados ou caindo | A alavanca pode estar errada: questione a prioridade, não o esforço |
| Baixa | Qualquer | O problema é o tamanho do plano ou a capacidade: revise antes de trocar a alavanca |
| Alta | Subindo | Siga; registre o que funcionou |

Na revisão, só comente quando a combinação pedir; na virada, o script imprime a leitura de cada resultado.

## 4. Banco de sugestões

Um cardápio para escolher, não uma resposta:
- benefício capturado contra a meta (resultado; fonte: Analista de Benefícios);
- adoção e uso dos produtos (resultado ou direcionador);
- NPS dos produtos de dados (resultado);
- entregas do roadmap no prazo (direcionador; fonte: roadmap da Weekly, só leitura);
- tempo da demanda até o início no novo jeito de trabalhar (direcionador);
- cobertura de PRD nas demandas novas (direcionador);
- vagas preenchidas (resultado);
- carga do time, ex.: pessoas em mais de 2 frentes (saúde).

Para cada sugestão, diga o tipo, de onde viria o dado e se há baseline. Proposta é `[suposição]` até o usuário confirmar.

## 5. Comando `kpis`

Mostre o scorecard com os cartões completos: ID, nome, tipo, fonte do dado, baseline, metas 30/60/90, frequência, dono, par e status com o último valor e a data. Embaixo, a linha de execução e a confiança de cada resultado.
