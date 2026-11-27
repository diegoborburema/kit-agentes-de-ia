---
name: prd-negocio
description: 'Guia de preenchimento das etapas 01 (Dor), 02 (Requisitos e critérios de aceite por release) e 03 (Solução e benefícios) do PRD, seção por seção: quem preenche, os rótulos e colunas do template, o critério de qualidade ("bom quando"), onde a informação costuma estar e a pergunta a fazer quando faltar. Use para ler o material do usuário, dar o status das seções, propor rascunhos e montar o pedido de gravação dessas etapas.'
---

## Como ler este guia

- **Rótulos** são os campos de 2 colunas do template (vão em `campos` no pedido de gravação). **Tabela** traz o nome da tabela e as colunas (vão em `linhas`, como `"02.1/rfs"`). Opções entre colchetes são caixas ☐: mande o texto da opção.
- **Bom quando** é o critério de ✓. O que não atende é ◐, mesmo preenchido.
- Escreva no estilo do template: frases curtas, fato antes de opinião, números com unidade e fonte.

## Painel e pessoas

**Painel** · rótulos: "Produto" · "Tipo" [Produto novo · Evolução] · "Porte" [P · M · G] · "Horizonte do business case" · "Etapa atual" · "Versão vigente" (o script atualiza). **Nunca** "Versão assinada".
**Pessoas** · tabela com chave = papel: Sponsor, PM, Engenharia de dados, Ciência de dados, Software, Segurança, Operação, Revisor do gate, Dono da mudança; colunas "Nome" e "Área". Bom quando: o sponsor é uma pessoa com nome, e não uma área. Só nomes das fontes ou ditos pelo usuário.

## 01 · Dor

**01.1 · Problema e contexto** · PM, com o sponsor
- Rótulos: "Problema ou oportunidade" · "Por que agora" · "Prioridade estratégica" · "Quem sente a dor".
- Bom quando: o problema descreve a dor e quem a sente, sem citar a solução ("os 38 gerentes levam 3 h por semana para montar a lista de faltas", e não "precisamos de um painel"); "por que agora" tem um gatilho com data ou evento; quem sente tem área e volume.
- Problema escrito como solução é ◐: proponha a reescrita, marcada `[suposição]`, e peça confirmação.
- Onde achar: abertura do discovery, e-mail ou ata do pedido, apresentação para a liderança.
- Se faltar: "Qual problema existe hoje, sem falar da solução? O que acontece se nada for feito até <data>?"

**01.2 · Como é hoje** · PM · tabela `personas`: "Persona" · "Volume" · "Como faz hoje" · "Principal dor" · "Evidência".
- Bom quando: cada persona tem volume, o passo a passo atual em uma frase e uma evidência (entrevista com data, dado, observação). Na evolução: como o produto atual é usado e o que falta nele.
- Se faltar: "Quem faz isso hoje, quantos são e como fazem, passo a passo? De onde vem essa informação?"

**01.3 · Tamanho da dor** · PM, com o sponsor · tabela `dimensoes`, chave "Dimensão" = Financeira, Operacional ou Risco ou compliance; colunas "Indicador atual" · "Ordem de grandeza" · "Fonte".
- Bom quando: pelo menos uma dimensão tem baseline numérico, com unidade e fonte. É o tamanho do problema hoje, não o benefício (que vai na 03.3). No porte P, a ordem de grandeza pode vir de quem informou.
- Se faltar: "Quanto a dor custa hoje (horas, R$, retrabalho, risco)? Quem confirma esse número?"

**01.4 · Hipótese e alternativas** · PM · rótulos: "Hipótese" · "Alternativas consideradas".
- Bom quando: a hipótese segue "Se [capacidade], [usuário] conseguirá [resultado], reduzindo [dor]". No porte G, as alternativas incluem processo, ferramenta de mercado e não fazer, com o motivo do descarte.

## 02 · Requisitos e critérios de aceite por release

Primeiro os requisitos (02.1), depois o mapa que os agrupa em releases (02.2).

**02.1 · Requisitos funcionais e critérios de aceite** · PM, com o negócio · tabela `rfs`: "ID" (RF-01…) · "A solução deverá" · "Prioridade" (Must, Should ou Could) · "Release" · "Critério de aceite".
- Bom quando:
  - cada RF descreve uma capacidade observável, sem detalhe de implementação;
  - todo RF tem prioridade, e a prioridade orienta a release: todo Must na R1; Could na R1 só com motivo dito pelo usuário;
  - Won't não fica aqui: vai para a 02.6;
  - todo RF da release que vai ser construída (a R1, até o Gate 2) tem critério verificável: "pronto quando…", com dado, caso ou tolerância concretos. RF de outra release pode ficar sem critério.
- Fraco: "funcionar bem", "ser rápido", "ter boa usabilidade", "dados corretos" sem referência. Aponte em uma linha o que falta (dado, caso, tolerância) e proponha uma versão melhor, marcada `[suposição]`.
- Ao propor um critério, use o relatório e a tolerância das fontes; o resto é suposição.
- Se faltar: "Sem qual RF a R1 não faz sentido (Must)? Qual é importante mas pode esperar (Should)? Qual é desejável (Could)?" e "Para dizer que RF-nn está pronto, o que o homologador confere, com qual dado e qual tolerância?"

**02.2 · Mapa de releases** · PM, com o sponsor · tabela `releases`: "Release" · "Objetivo" · "RFs incluídos" · "Critério de saída" · "Data-alvo".
- Bom quando: as releases são as que o produto precisar (R1 = MVP); cada uma entrega valor sozinha, tem objetivo e critério de saída; os RFs incluídos batem com a coluna "Release" da 02.1. Data-alvo só da fonte ou do usuário.

**02.3 · Indicadores e regras de negócio** · PM, com o sponsor · só se o produto calcula ou mostra indicador · tabela `indicadores`: "Indicador" · "Fórmula e janela" · "Referência para conferir" · "Dono".
- Bom quando: a fórmula tem numerador, denominador e janela; há um relatório ou total contra o qual conferir; o dono é uma pessoa.

**02.4 · Requisitos não funcionais** · PM · tabela `nfr`, chave "Requisito" = Frequência de atualização, Disponibilidade, Perfis de acesso, Desempenho, Explicabilidade; colunas "Esperado" · "Release" · "Como verificar".
- Bom quando: frequência e perfis de acesso definidos em todo porte; no G, toda categoria com forma de verificação. Os perfis de acesso viram o modelo de acesso do canvas de Segurança; a disponibilidade vira o SLA do canvas de Operação.

**02.5 · Dados necessários** · PM, com o negócio · tabela `dados`: "ID" (D-01…) · "Informação" · "Para qual RF" · "Principais campos" · "Frequência" · "Histórico" · "Release".
- Bom quando: todo RF da R1 que depende de dado tem pelo menos um D-nn; frequência e histórico definidos. Origem, acesso e cuidados vão no Anexo C (o negócio informa o que souber; a engenharia confirma).

**02.6 · Fora do escopo** · PM, com o sponsor · tabela `fora`: "Item" · "Motivo" · "Reavaliar quando".
- Bom quando: tem pelo menos os pedidos que apareceram e não entraram, cada um com motivo. Vazio é ◐: o que não está escrito vira discussão depois.
- Onde achar: discovery ("ideias", "próximas fases", "não agora"), atas de priorização.

## 03 · Solução e benefícios

**03.1 · Visão da solução** · PM · rótulos: "O que a solução faz" · "Tipo de produto" [Dashboard · Modelo · Data product · API · Aplicação · Automação · Agente] (pode marcar mais de um) · "Decisão ou processo apoiado" · "Onde e como é consumida".
- Bom quando: a saída em linguagem de negócio; a decisão apoiada é específica ("o que repor primeiro na loja, a cada manhã"); o consumo tem ferramenta, frequência e momento do processo.
- Tipo Modelo ou Agente, ou IA na solução: abra o Anexo E (`prd-ia`) e responda "sim" na triagem (03.5).

**03.2 · Jornada e protótipo** · PM · rótulos: "Jornada TO-BE" · "Protótipo" · "Teste com usuários" [Sim · Não · N/A] · "Aprendizados".
- Bom quando: no porte G, protótipo testado com usuários e aprendizados registrados.

**03.3 · Benefícios por release** · sponsor (dono), com o PM
- Tabela `kpis`: "KPI" · "Tipo" (receita, custo, produtividade ou risco) · "Baseline" · "Meta e prazo" · "Método e responsável" · "Release".
- Tabela `valores` (por ano, no horizonte da ficha): "KPI" · "Ano 1" … "Ano 5" · "Total"; a linha "TOTAL" soma as outras.
- Rótulos: "Premissas do benefício" · "Benefícios não financeiros" · "Validação do sponsor" (nome e data).
- Bom quando:
  - todo KPI tem baseline (o mesmo da 01.3), meta com prazo e método com responsável;
  - os valores por ano vêm do sponsor ou de uma fonte, nunca de estimativa do agente; ano sem valor fica em branco e vira pergunta;
  - as premissas de adoção batem com a 03.4: piloto, ondas e convivência atrasam a captura.
- Com IA, o benefício esperado depende do limiar do Anexo E: diga isso na premissa.
- Fraco: "ganho de produtividade" sem número; meta sem baseline; horas convertidas em R$ sem o custo-hora de uma fonte.
- Se faltar (sponsor): "Qual indicador vai provar o benefício, qual o valor hoje, qual a meta, quando e quem mede? Quanto isso vale por ano?"

**03.4 · Estratégia de lançamento (preliminar)** · sponsor, com o PM · rótulos: "Forma de lançamento" [Big bang · Por ondas · Piloto e expansão] · "Convivência com a solução atual" · "Dono da mudança".
- Bom quando: a forma está escolhida, a convivência tem duração e o dono da mudança é uma pessoa do negócio. O detalhe vai na 05.1.

**03.5 · Triagem de governança** · PM · tabela `triagem`, chave "Pergunta" = "Envolve dados pessoais?", "Todo dado tem um dono?", "Cria ou muda um indicador?", "Usa IA (modelo, IA generativa ou agente)?"; colunas "Resposta" (Sim, Não ou Não sei) · "Ação" · "Responsável".
- Bom quando: todo "sim" ou "não sei" tem ação e responsável. Dados pessoais vão para o canvas de Segurança; IA abre o Anexo E; dado sem dono vira pergunta e pendência.
- Um dado pessoal pode aparecer de lado (um telefone para aviso, um nome num relatório): pergunte quando um RF tocar pessoas.

## Riscos e pendências (Anexo A)

Tabela `pendencias` (vai em `pendencias` no pedido): "ID" (P-nn, R-nn, C-nn) · "Tipo" (Risco, Dependência, Pendência ou Condição de gate) · "Descrição" · "Origem" (seção ou ID) · "Gate" · "Bloqueante" (Sim ou Não) · "Dono" · "Prazo". Só o que o usuário aceitar; dono e prazo quando ele informar. Os pontos em aberto do discovery viram sugestão de risco ou dependência.
