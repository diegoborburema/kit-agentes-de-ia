---
name: coach-rituais
description: 'Rituais do Coach de Gestão: a revisão semanal de sexta por exceção (status de cada item, vitórias, nota de execução, protocolo do 2º escorregão, delegações checadas com fonte, nova semana, pulso dos KPIs e confiança, radar), a virada a cada 4 semanas (revisão pós-ação de cada prioridade, comprometido x aspiracional, rolagem das janelas, resultados e marcos, resumo para o 1-1 com o gestor) e o plano feito à mão, sem dados gravados. Use em toda revisão e virada.'
---

## 0. Antes de tudo

- O .pptx do plano anterior precisa estar **anexado**. Sem ele, peça para anexar; não reconstrua o plano de memória, pela busca nem a partir de um arquivo só citado ("está no meu OneDrive").
- Leia o plano com a ação `ler` da `coach-pptx`. Ela mostra o ciclo, a semana (N de 4), as janelas, os itens da semana, os KPIs, os descartados, a execução do ciclo e a lista da **revisão por exceção**.
- Na 4ª revisão do ciclo (semana 4 de 4), é a **virada** (§2). Nas outras, a **revisão** (§1).
- As janelas do ciclo não mudam na revisão. Só a virada anda as janelas.

## 1. Revisão semanal (sexta à tarde, ~15 min)

1. **Ficha.** Plano lido (data, ciclo, semana N de 4), as janelas mantidas, a semana que fecha e a que abre, a janela de busca (da revisão anterior até hoje), os anexos. Peça confirmação.
2. **Fechamento da semana, por exceção.** Não percorra item a item. Pergunte de uma vez: "o que **não** saiu como planejado?", e mostre a lista de exceções que a `ler` imprimiu (KPIs fora do verde, resultados com confiança baixa, marcos e checagens da semana, atividades que já escorregaram uma vez). Cruze com os anexos e a busca. O resto, proponha como feito, com a evidência que houver, e peça confirmação em bloco. A tabela final mostra todos os itens da semana, sem exceção:

| ID | Item | Status | Evidência | Destino |
|---|---|---|---|---|

   - Atividades: **feito**, **parcial**, **não feito**, **replanejado** (com a nova data), **cancelado** (com motivo) ou **a confirmar**.
   - Delegações: **em dia**, **atrasada**, **concluída**, **checar depois** (com a nova data) ou **cancelada**, com a fonte da checagem (ex.: `[Anotações weekly do time · 18/11]`). Delegação com data de checagem futura fica para essa data.
   - Pedidos ao gestor: **aberto**, **atendido** ou **cancelado**. Aberto segue para a próxima semana e para o 1-1 com o gestor.
   - Parar de fazer: **mantido** ou **retomado**.
   - **Status sem evidência não melhora.** "Marca como feita, eu termino no fim de semana": mantenha parcial e diga em uma linha que vira feito quando o critério do "feito quando" for cumprido.
   - "Não sei" vira **a confirmar**; não vira feito.
   - Parcial e não feito vão para a nova semana com o mesmo ID, ou o usuário diz o destino. A confirmar só entra na nova semana se o usuário confirmar.
   - **2º escorregão seguido** (a atividade já tinha ficado parcial, não feita ou replanejada na semana anterior): não a empurre de novo. Ofereça, nesta ordem: **cortar escopo** (o que sai, em `corte`), **nova data com motivo** ou **cancelar** (com motivo). Mande a escolha em `protocolo` no status. Se ela volta à semana, combine **quando** (dia e hora) e um **se-então** ("se o RH não mandar o modelo até segunda, então uso a vaga do Analista Pleno como base"), em `quando` e `se_entao`. O script recusa sem isso.
   - **Vitórias:** peça de 1 a 3 da semana, do usuário ou do time (o que andou, não só o que fechou). Vão em `vitorias` e aparecem em Minha semana. Se o usuário não lembrar, proponha a partir dos itens feitos, como `[suposição]`.
   - A conferência mostra a **nota de execução** da semana. Mostre a linha; abaixo de 85%, siga `coach-kpis` §3.
3. **Nova semana.** Parta da coluna da semana nova de cada prioridade (S2, S3 ou S4), mais o que veio da semana anterior. De 5 a 7 atividades, com "feito quando" e esforço; delegações com data; pedidos; parar de fazer. Rode `capacidade` com o plano lido (para a referência das semanas fechadas) e, se houver, o volume do radar em `nao_planejado_h`.
4. **Pulso dos KPIs e confiança** (`coach-kpis` §3): os KPIs com dado novo e a confiança de 0 a 10 em cada resultado, numa pergunta só.
5. **Radar** (`coach-fontes` §5).
6. **Mudanças no plano**, só com pedido do usuário:
   - replanejar um marco ou entregável: nova data e motivo;
   - concluir um marco: data e fonte;
   - cortar o escopo de um entregável ou de uma atividade, mantendo a data: `cortar_escopo` com o texto novo e o que sai (`corte`);
   - remover uma prioridade ou um resultado: rode `afetados`, mostre a lista (ex.: R3, M5, M6, P3, K3, K7 e as atividades ligadas) e pergunte se cancela, com motivo. Nada sai antes da resposta. Se o usuário desistir, mantenha tudo.
7. **Entrega.** Depois do "aprovado", gere o arquivo com a ação `gerar` (pedido com `partida` e `revisao`). Nome: `Plano 30-60-90 <data da revisão>.pptx`. Mostre a semana nova, o radar e o bloco para os outros agentes (`coach-metodo` §10). Se a semana seguinte cair no recesso, o script abre a primeira semana depois dele: diga a data da próxima revisão.

## 2. Virada (4ª revisão do ciclo, ~30 min)

1. **Ficha.** Plano lido, "4ª revisão do ciclo N", as janelas novas (as atuais andam 4 semanas; o script calcula), o recesso que cair nelas.
2. **Fechamento da última semana**, como na revisão (§1, passo 2).
3. **Fechamento do ciclo: revisão pós-ação** (as 4 perguntas do exército americano), uma linha cada, por prioridade:
   1. **O que esperávamos?** O "feito quando" (o script grava).
   2. **O que aconteceu?** **Atingida**, **parcial** ou **não atingida**, pela evidência.
   3. **Por que a diferença?** Obrigatório quando não foi atingida (`porque`).
   4. **O que repetir ou mudar?** O aprendizado (`aprendizado`).

   Peça as linhas ao usuário ou proponha como `[suposição]`. Leia o tipo do resultado: prioridade não atingida num resultado **comprometido** pede explicação e plano de recuperação; parcial num **aspiracional** está dentro do esperado (o script diz). O script também imprime, por resultado, a leitura conjunta de execução do ciclo, KPI e confiança (`coach-kpis` §3a): use-a para decidir se a prioridade segue, muda de alavanca ou diminui de tamanho.
4. **Rolagem** (o script faz, na ação `gerar` com `virada`):
   - **Os itens mantêm as datas.** Nada é empurrado em bloco. "Empurra todas as datas 4 semanas": diga em uma linha que as datas ficam e só o que atrasou é replanejado, com motivo; pergunte o que atrasou.
   - Marcos concluídos e resultados atingidos saem, com registro no fechamento do ciclo.
   - Os marcos que caem nas novas S1 a S4 viram entregáveis da prioridade do mesmo resultado, na semana da data.
   - Resultado que segue sem marco nas novas S5 a S8 ganha marco proposto, como `[suposição]`, sem data sem base.
   - Com resultado a menos, há espaço para um novo (até 3): proponha a partir do retrato (ex.: um desafio ainda sem movimento), como `[suposição]`. Se não for aprovado, lembre em uma linha o desafio que segue descoberto.
   - Os descartados continuam descartados.
5. **Prioridades e semana do novo ciclo**, como no Montar (`coach-metodo` §5 e §6), com o recesso descontado.
6. **Entrega.** Arquivo novo, `Plano 30-60-90 <data da virada>.pptx`, com o ciclo novo, o histórico do ciclo anterior e o fechamento. Depois do bloco para os outros agentes, mostre o **resumo para o 1-1 com o gestor** que a conferência imprime (5 linhas: o ciclo que fechou, o que sai, o ciclo novo com o desafio central, os pedidos em aberto, execução e confiança), pronto para colar. Ofereça a versão para apresentar ao gestor (ação `apresentar`).

## 3. Plano feito à mão, sem dados gravados

O script avisa e mostra os textos por coluna (30, 60 e 90 dias), de cima para baixo, com a cor do ponto de status.
1. Diga que o plano não tem os dados gravados e que você vai montá-los com o usuário antes de revisar.
2. Monte a tabela de dados: resultados, marcos, prioridades, entregáveis, atividades e KPIs, a partir dos textos.
3. **Não chute o que só está no desenho:** status só pela cor (verde, amarelo, vermelho; sem cor, `[a confirmar]`); data só se estiver escrita; dono ausente fica `[a confirmar]`; resultado sem KPI fica sem KPI.
4. Nenhum status de revisão e nenhuma semana nova antes de a tabela ser confirmada.
5. Depois da confirmação, siga a revisão (§1) e gere o arquivo com o `plano` completo (não com `partida`), já com a semana nova. O arquivo começa um ciclo novo a partir da data da revisão: diga isso em uma linha.
