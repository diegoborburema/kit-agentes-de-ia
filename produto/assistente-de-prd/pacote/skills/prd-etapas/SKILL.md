---
name: prd-etapas
description: 'Método do PRD em 5 etapas: classificar a demanda (tipo, porte, etapa atual, gate alvo), saber o que cada etapa exige por porte, dar o status das seções, conduzir os checkpoints, priorizar as lacunas, aplicar os checklists do Gate 1 e do Gate 2 e montar as saídas da conversa (ficha, mapa, lacunas, checkpoint, checagem, pedido de mudança). Use na ficha, no mapa, em todo checkpoint e sempre que perguntarem o que falta.'
---

## 1. Classificação

**Tipo.** Produto novo ou evolução de um produto que já existe. Na evolução, peça o PRD de origem, se existir: ele é a fonte do "como é hoje" (01.2), dos indicadores (02.3) e da arquitetura atual, e o PRD novo trata só o que muda.

**Ajuste pequeno.** Um pedido que não cria dado novo, não muda regra de negócio nem indicador e cabe em poucos dias pode não precisar de PRD. Diga isso em uma linha, diga que quem decide é o revisor do gate e pergunte se o usuário quer seguir. Nunca classifique sozinho.

**Porte.** Pelo critério mais alto atendido. Na ficha, o porte é preliminar: diga qual critério ainda é estimativa. As faixas são um ponto de partida; se o usuário disser que a empresa dele usa outras, use as dele.

| Critério | P | M | G |
|---|---|---|---|
| Esforço | Até 1 sprint | Até 3 meses | Mais de 3 meses |
| Plataforma | Sem componente novo | Componente novo dentro do padrão | Padrão novo ou ferramenta nova |
| Impacto | Uma área, decisão local | Uma área, processo recorrente | Várias áreas ou processo crítico |

**Etapa atual e gate alvo.** Deduza do PRD em andamento (painel: "Etapa atual"; checkpoints; decisões de gate) e confirme:
- sem PRD ou só com a 01 começada → etapa 01, alvo Gate 1;
- checkpoints 01 e 02 cumpridos → etapa 03, alvo Gate 1;
- Gate 1 decidido ("Pronto" ou "Pronto com condições") → etapa 04, alvo Gate 2; as condições do Gate 1 (Anexo A) entram nas lacunas;
- "Versão assinada" preenchida → PRD assinado: só pedidos de mudança (§6).
No perfil técnico, o alvo é o Gate 2; no revisor, o gate que ele vai revisar.

## 2. O que cada etapa exige

● exigido · ◐ simplificado · ○ recomendado · – não cobrar. Um gate exige tudo o que as etapas anteriores exigem.

| Seção | P | M | G |
|---|---|---|---|
| Painel (produto, tipo, porte, horizonte) e Pessoas (sponsor, PM) | ● | ● | ● |
| 01.1 Problema e contexto | ● | ● | ● |
| 01.2 Como é hoje · 01.3 Tamanho da dor | ◐ | ● | ● |
| 01.4 Hipótese e alternativas | – | ● | ● |
| 02.1 Requisitos funcionais e critérios de aceite · 02.2 Mapa de releases | ● | ● | ● |
| 02.3 Indicadores e regras | ● se o produto calcula ou mostra indicador; senão N/A | | |
| 02.4 Não funcionais | ◐ (frequência e perfis de acesso) | ● | ● |
| 02.5 Dados necessários · 02.6 Fora do escopo | ● | ● | ● |
| 03.1 Visão da solução · 03.3 Benefícios · 03.5 Triagem de governança | ● | ● | ● |
| 03.2 Jornada e protótipo | – | ○ | ● |
| 03.4 Estratégia de lançamento | ◐ (forma, convivência, dono da mudança) | ● | ● |
| Anexo A: riscos e dependências conhecidos | ● | ● | ● |
| **Gate 1** | | | |
| 04.1 Arquitetura e componentes | ◐ | ● | ● |
| 04.2 Canvas: Engenharia de dados (quando houver dado), Segurança e Operação | ◐ | ● | ● |
| 04.2 Canvas: Ciência de dados (com modelo) · Software (com aplicação, API ou automação) | ◐ | ● | ● |
| 04.3 Decisões de arquitetura | – | ○ | ● |
| 04.4 e Anexo E · Requisitos de IA (com modelo, IA generativa ou agente) | ● | ● | ● |
| 04.5 Custos · Anexo D | ● | ● | ● |
| 04.6 Business case (sensibilidade de −30% só no G) | ● | ● | ● |
| Anexo C: origem, acesso e cuidados dos D-nn | ● | ● | ● |
| 05.1 Estratégia de go-live · 05.2 Homologação | ◐ | ● | ● |
| 05.3 Fases · 05.4 Go/no-go · 05.6 Comunicação e adoção | ◐ | ● | ● |
| 05.5 Cutover, contingência e rollback | ◐ (gatilhos e como voltar) | ● | ● |
| 05.7 Acordo de entrega · Pessoas completas | ● | ● | ● |
| **Gate 2** | | | |

Canvas que não se aplica: "Aplicável?" = Não, com o motivo; fica N/A. No porte P, Segurança e Operação nunca ficam N/A: são simplificadas (classificação, dados pessoais, modelo de acesso; dono operacional, suporte, runbook).

## 3. Status de seção

| Status | Quando |
|---|---|
| ✓ | Todo campo exigido no porte está preenchido, com fonte, e atende ao "bom quando" |
| ◐ | Algum campo exigido está vazio ou fraco, ou o conteúdo está marcado "validar com <papel>" |
| ○ | Nada preenchido |
| N/A | Não se aplica no porte ou no tipo, ou "Aplicável?" = Não |
| P-nn | A lacuna virou pendência aceita no Anexo A. O status continua ◐ ou ○ |

## 4. Checkpoints

No fim de cada etapa, mostre o **Checkpoint** (§8): as seções exigidas da etapa, o status e o que falta.
- **Passa** quando toda seção exigida no porte está ✓ ou N/A. Registre no painel ("Situação": Cumprido, com a data) na próxima gravação.
- **Não passa:** diga o que falta e não avance sozinho. Se o usuário quiser avançar assim mesmo, avance, registre a situação como "Cumprido com pendências" e proponha cada lacuna como pendência no Anexo A, com dono e prazo.
- Critérios que seguram cada checkpoint, além do status:
  - **01:** o problema não descreve a solução; existe pelo menos um baseline com fonte (no P, pode vir de quem informou).
  - **02:** todo RF da R1 tem prioridade e critério de aceite verificável; o mapa de releases tem objetivo e critério de saída; o fora do escopo não está vazio.
  - **03:** benefício com baseline, meta, prazo, método e responsável; triagem de governança com ação para todo "sim" ou "não sei".
  - **04:** canvas aplicáveis completos; Anexo E com limiar e conjunto de avaliação, quando houver IA; todo custo com premissa e fonte; business case fechado.
  - **05:** rollback com gatilho mensurável e data até quando a solução atual fica disponível; go/no-go com responsáveis e quem decide; homologação com aceite nomeado.

## 5. Lacunas

Liste só lacunas exigidas até o gate alvo, no máximo 7, nesta ordem:
1. **O que segura o checkpoint da etapa atual.**
2. **Bloqueantes do gate alvo:** o que deixa indefinido um destes pontos, que nenhuma condição de gate pode deixar em aberto.
   - Gate 1: a dor (01.1, 01.3), o escopo (02.1, 02.2, 02.6), o critério de aceite da R1 (02.1), o benefício (03.3).
   - Gate 2: o custo (04.5), o business case (04.6), os dados da R1 com "não sei" (Anexo C), o limiar da IA (Anexo E), o rollback (05.5), o go/no-go (05.4), o acordo de entrega (05.7).
3. **Desbloqueadores:** 01.3 → 03.3 (baseline) · 02.1 → 02.2, 02.5, 05.2 (roteiro) · 02.5 → canvas de Engenharia e Anexo C · 03.4 → 03.3 (premissas de adoção) e 05.1 · canvas (esforço e custo) → 04.5 → 04.6 · 02.4 → canvas de Segurança (perfis) e de Operação (SLA).
4. **Demais exigidos** no gate alvo.

Dentro de cada nível, primeiro o que o usuário responde sozinho, depois o que depende de outro papel. Agrupe as perguntas por quem responde (PM, sponsor, cada especialista, revisor), até 3 por papel. As lacunas das etapas seguintes vão numa linha no fim ("Depois do Gate 1: …").

## 6. Gates e situações especiais

**Checklist.** A coluna "Atende?" sai do status: **Sim** quando todas as seções do critério estão ✓ ou N/A; **Parcial** com alguma ◐; **Não** com alguma ○.

Gate 1 · Vale construir? (decidem: sponsor e revisor do gate)
1. Problema sem solução embutida, com quem sente e volume (01.1)
2. Tamanho da dor com baseline e fonte (01.3)
3. Todo RF da R1 com prioridade e critério de aceite verificável (02.1)
4. Mapa de releases com objetivo e critério de saída (02.2)
5. Dados da R1 mapeados (02.5) · 6. Fora do escopo preenchido (02.6)
7. Visão da solução com decisão apoiada e consumo (03.1)
8. Benefício com baseline, meta, prazo, método e responsável (03.3)
9. Estratégia de lançamento preliminar e dono da mudança (03.4)
10. Triagem de governança com ações (03.5) · 11. Riscos e dependências no Anexo A

Gate 2 · PRD assinado (decidem: sponsor e revisor, com os especialistas)
1. Condições do Gate 1 resolvidas · 2. Arquitetura, com os desvios decididos (04.1, 04.3)
3. Canvas aplicáveis completos (04.2) · 4. Anexo E com limiar e conjunto de avaliação, quando há IA
5. Custos com premissa e fonte (04.5) · 6. Business case fechado (04.6; no G, também com −30%)
7. Go-live e fases com critério de saída (05.1, 05.3) · 8. Homologação da R1 com roteiro e aceite nomeado (05.2)
9. Go/no-go com responsáveis e quem decide (05.4) · 10. Cutover, contingência e rollback mensuráveis (05.5)
11. Comunicação e métrica de adoção (05.6) · 12. Acordo de entrega (05.7) · 13. Pessoas completas

**Leitura do resultado.** Diga só se, pelo checklist, o PRD está em condições de ir ao gate: com "Não" em algum bloqueante (§5), não está; com "Parcial", pode ir como "pronto com condições", se cada parcial virar pendência com dono e prazo e nenhuma deixar dor, escopo, critério de aceite, benefício ou custo indefinidos. Nunca marque a decisão: no documento, ela é preenchida por quem decide.

**PRD assinado.** É mudança alterar RF ou critério de aceite da R1, item fora do escopo, data-alvo, custo ou benefício. Monte o **Pedido de mudança** (§8) e grave só ele, em `mudancas` (Anexo B). O conteúdo muda depois da decisão, numa versão nova, que o sponsor e o revisor assinam de novo.

**Fontes divergentes:** mostre as duas versões, com as fontes, e pergunte qual vale. Não escolha.

**Planilha de business case:** use só os números da planilha, com a aba e a célula como fonte. Para o horizonte da ficha, só com o dado de cada ano; se faltar um ano, pergunte.

**Material longo:** extraia só o que serve às seções exigidas até o gate alvo. Não resuma o documento.

## 7. Releases

As releases são livres (R1 = MVP, R2, R3…). Os requisitos vêm primeiro (02.1) e o mapa os agrupa (02.2). A prioridade orienta a release: todo Must na R1; Should na R1 ou depois; Could na R1 só com motivo dito pelo usuário. Won't não fica em 02.1: vai para 02.6. O critério de aceite é cobrado da release que vai ser construída: no Gate 2, da R1. As outras ganham critério no próprio refinamento.

## 8. Formatos

**Ficha**
| Campo | Valor | Fonte |
|---|---|---|
| Perfil | PM / especialista (qual) / revisor, com o motivo | |
| Produto | | |
| Tipo | Novo / Evolução (de: <produto>) | |
| Porte | P / M / G, com o critério que define e o que é estimativa | |
| Etapa atual · gate alvo | | |
| Horizonte do business case | 5 anos (padrão) ou o da empresa | |
| PRD em andamento | v<x.y> · ou "não há" | |
| Material | arquivos | |
Termine com "Confirma?" e as perguntas do que faltar, numa mensagem só.

**Mapa** (uma linha por seção exigida até o gate alvo)
| Seção | Status | O que já tem | Fonte | O que falta |
|---|---|---|---|---|

**Lacunas**: lista numerada (§5), depois as perguntas agrupadas por papel.

**Checkpoint · Etapa <nn>**: as seções da etapa com status, o resultado (passa / não passa) e o que falta, em até 5 linhas.

**Rascunho de seção**: os campos, cada um com o texto proposto e a fonte; suposições marcadas; no fim, até 3 perguntas.

**Checagem · Gate <n>**
| # | Critério | Seções | Atende? | O que falta |
|---|---|---|---|---|
Depois, a leitura do resultado, em até 3 linhas.

**Pedido de mudança**: ID (M-nn), data, pedido, impacto (seções, RFs, critérios de aceite, homologação, custo, benefício, datas) e "decisão: a tomar por sponsor e revisor".
