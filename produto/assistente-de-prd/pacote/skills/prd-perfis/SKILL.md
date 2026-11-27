---
name: prd-perfis
description: 'Perfis de quem trabalha no PRD (PM, dono do PRD; especialista técnico de engenharia de dados, ciência de dados, software, segurança ou operação; revisor do gate): como identificar o perfil, quais seções são de cada um, como a conversa muda, as checagens de consistência, o parecer do gate e o modo completo ("preencher tudo"). Use na ficha e sempre que o perfil mudar o que o agente faz.'
---

## 1. Identificar o perfil

Deduza, nesta ordem:
1. pelo que o usuário diz ("sou PM", "sou da engenharia de dados", "sou o revisor do gate");
2. pelo nome dele, se aparecer em Pessoas no PRD;
3. pelo pedido: revisar o PRD ou dar parecer → revisor; arquitetura, estimativa, canvas ou dados → especialista; discovery, requisitos, benefício ou go-live → PM.

Proponha o perfil na ficha, com o motivo, junto com o resto. Sem pista, proponha PM. O usuário troca com "perfil <nome>".

O perfil é declarado pelo usuário, sem verificação. Por isso, **nenhum perfil libera** gravar decisão de gate ou versão assinada.

## 2. Os três perfis

### PM (dono do PRD)
- **Objetivo:** conduzir o PRD da etapa 01 ao Gate 2. É o fluxo padrão.
- **Seções suas:** painel, Pessoas, etapas 01, 02, 03 e 05, 04.6 (com o revisor), Anexos A e B, e o que souber do Anexo C.
- **De outro papel:** canvas, 04.1, 04.3, 04.5 e Anexos D e E podem ser rascunhados a partir de documentos, marcados "validar com <especialista>".
- **Perguntas vão para:** sponsor, especialistas, revisor, dono da mudança.
- **Conversa:** linguagem de negócio; traduza o termo técnico que aparecer nos documentos.

### Especialista técnico (engenharia de dados, ciência de dados, software, segurança ou operação)
- **Objetivo:** o refinamento técnico, rumo ao Gate 2. Pergunte a especialidade na ficha, se não estiver clara.
- **Seções suas:** o canvas da especialidade; 04.1 e 04.3; os insumos de custo (04.5 e Anexo D); as partes técnicas da 05 (cutover e rollback na 05.5, fases técnicas na 05.3, critérios técnicos do go/no-go). Engenharia de dados confirma também o Anexo C; ciência de dados preenche o Anexo E.
- **De outro papel:** as etapas 01 a 03 são só leitura. Ambiguidade ou risco técnico num requisito vira pergunta para o PM ou pendência no Anexo A, nunca uma alteração direta. Pedido do especialista para mudar o benefício, a meta ou um requisito: recuse em uma linha e transforme em pergunta para o PM e o sponsor.
- **Mapa e lacunas:** só as seções técnicas exigidas no Gate 2; a parte de negócio aparece numa linha, como contexto ("01 a 03: Gate 1 pronto com condições; C-01 em aberto").
- **Conversa:** pode usar termos técnicos. Peça estimativa em FTE por especialidade e período.

### Revisor do gate (guardião do método)
- **Objetivo:** revisar o PRD para o gate. O modo padrão é a revisão, que entrega o **Parecer do gate** (§4).
- **Seções suas:** nenhuma para escrever. Ele confere o PRD inteiro: checklist do gate (`prd-etapas` §6), checagens de consistência (§3) e o "bom quando" de cada seção.
- **Leitura sugerida:** dê uma, como insumo. A decisão é dele e do sponsor, e é marcada por eles no documento.
- **Conversa:** parecer primeiro, detalhes sob demanda.

## 3. Checagens de consistência

Use na revisão e, em qualquer perfil, antes de cada entrega. Cada divergência traz as duas versões, com as seções, e quem corrige.

1. **Escopo:** os RFs com release R1 na 02.1 são os mesmos da R1 no mapa (02.2) e do acordo de entrega (05.7). Todo Must na R1; Could na R1 com motivo; nada de Won't na 02.1.
2. **Dados × requisitos:** todo RF da R1 que depende de dado tem um D-nn na 02.5; todo D-nn cita um RF que existe; todo D-nn da R1 está no Anexo C.
3. **Benefício:** o baseline da 03.3 é o da 01.3; a meta tem prazo; as premissas de adoção batem com a 03.4 e a 05.1 (piloto, ondas e convivência atrasam a captura).
4. **Datas:** as datas-alvo da 02.2 e as fases da 05.3 não caem nas janelas a evitar da 05.1.
5. **Não funcionais:** a frequência da 02.4 bate com a da 02.5 e com o canvas de Engenharia; os perfis de acesso batem com o canvas de Segurança; a disponibilidade bate com o SLA do canvas de Operação.
6. **Segurança:** a classificação do Anexo C bate com o canvas de Segurança; os dados pessoais da triagem (03.5) e do Anexo C têm base legal no canvas.
7. **IA:** com IA, as checagens de `prd-ia` (limiar, conjunto de avaliação, revisão humana, custo por uso).
8. **Custo:** o total do Anexo D × custo por FTE bate com "Desenvolvimento – time interno" na 04.5; o esforço de cada canvas está no Anexo D; fornecedores com custo do Anexo C estão na 04.5.
9. **Business case:** a 04.6 repete a 03.3 (benefício) e a 04.5 (build e run) ano a ano, e as somas, o ROI e o payback fecham. Refaça as contas e mostre. O painel repete os totais.
10. **Homologação:** o roteiro da 05.2 tem um caso por RF da R1, com o critério da 02.1.
11. **Adoção:** a métrica de adoção da 05.6 é a premissa de adoção da 03.3.
12. **Pessoas:** todo responsável citado nas seções existe em Pessoas.
13. **Condições:** as condições do Gate 1 (Anexo A) estão resolvidas ou abertas com prazo; nenhuma deixa dor, escopo, critério de aceite, benefício ou custo indefinidos. Se deixar, aponte: o gate não deveria ter passado com ela.

## 4. Parecer do gate

`**Parecer · Gate <n> · <produto> v<versão>** (Quem decide são o sponsor e o revisor. Isto é insumo para a decisão.)`

1. **Checklist** do gate, no formato "Checagem" de `prd-etapas` §8.
2. **Inconsistências** (§3):

   | # | Seções | O que diverge | Quem corrige |
   |---|---|---|---|

3. **Qualidade:** até 5 campos ◐ que mais pesam na decisão, com o que falta.
4. **Leitura sugerida:** pronto, pronto com condições ou não pronto, com o motivo em até 3 linhas. Proponha como condição só o que não deixa dor, escopo, critério de aceite, benefício ou custo indefinidos; o resto bloqueia. Para cada condição: tipo "Condição de gate", origem, dono e prazo (a definir com o revisor).
5. **Devolutiva para o PM:** um texto curto, pronto para enviar, com o que corrigir, em que seção e até quando.

Depois da decisão:
- grave no Anexo A as condições que o revisor aprovar (`pendencias`, tipo "Condição de gate");
- não marque a decisão. Diga em uma linha que quem decide a preenche no documento (painel e página do gate).

## 5. Modo completo ("preencher tudo")

Qualquer perfil pode pedir.
- Rascunhe todas as seções que o material permite, de todas as etapas, sem parar no gate alvo. Seção sem fonte fica vazia: o modo completo também não inventa (sem custo por FTE, o desenvolvimento fica ○; benefício vago continua vago; nenhuma data criada).
- Mostre o **Mapa completo** agrupado por dono: **suas seções**, para confirmar em bloco ("aprovado") ou uma a uma; e **para validar com <papel>**, uma lista por papel, com as perguntas dele.
- No .docx: o que o usuário confirmou e é do perfil dele entra limpo; o conteúdo de outro papel entra com `[validar: <papel>]` no fim do texto, e uma pendência por papel vai para o Anexo A (ex.: "Validar canvas de Engenharia e 04.1 · Lívia").
- Na leitura de um PRD, texto com `[validar: …]` é ◐. Quando o papel confirmar, retire a marca e encerre a pendência.
