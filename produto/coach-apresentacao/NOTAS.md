# Coach Apresentação: notas

> Tudo o que o pacote exportado **não** guarda. Este arquivo é editado à mão.

## Objetivo

Transformar um canvas de storytelling para apresentações (o Canvas de Apresentação, descrito em texto na skill [`canvas-storytelling`](pacote/skills/canvas-storytelling/SKILL.md)) em um coach que:

1. identifica o tipo de atividade;
2. decide quais caixas são necessárias no caso, porque preencher todas sempre é penoso;
3. conduz pelas caixas obrigatórias respeitando as dependências;
4. gera um prompt robusto para o **Claude** criar o storytelling e montar a apresentação.

O agente roda no Microsoft 365 Copilot. O prompt final é para o Claude, porque a apresentação gerada pelo próprio Copilot não atendia.

## Perguntas de controle

Ficam em [`testes/PERGUNTAS-DE-CONTROLE.md`](testes/PERGUNTAS-DE-CONTROLE.md), e os resultados por versão em [`testes/RESULTADOS.md`](testes/RESULTADOS.md).

## Decisões

- v1.0.6 (2026-10-30): primeira versão registrada no repositório (baseline).
- v1.0.7 (2026-10-30, proposta):
  - Canvas de Apresentação incorporado à skill: 15 caixas, dependências em 3 trilhas e critérios de qualidade tirados das dicas do canvas. Substitui a lista genérica de briefing.
  - Exceção na regra de dependências: o vd 1 da Introdução pessoal não bloqueia as caixas verdes seguintes. A regra literal gera um ciclo (Introdução ↔ Tópicos-chave), então a Introdução vai para o nível 6.
  - 9 caixas no núcleo, sempre obrigatórias; as outras 6 são classificadas pela triagem, ajustada por tipo de atividade e duração.
  - O agente propõe rascunhos em vez de só perguntar.
  - Barra de progresso: atividade 5%, triagem 15%, canvas 70% (só obrigatórias), síntese 5%, prompt 5%.
  - Prompt final destinado ao Claude, com pausa para aprovação do roteiro por padrão.
  - Perguntas de controle: 55 perguntas em 5 cenários, sondas e execução no Claude (21 Críticas). O que rodar depende do que mudou (matriz de impacto); execução rápida com aberturas prontas, abas paralelas e correção em lote pelo Claude.
  - Prompts iniciais passam a ser os tipos de atividade; saem "Prompt para mudança" (caso específico) e "Gerar prompt do canvas" (pressupunha canvas preenchido fora do agente).

## Fontes de conhecimento

Nenhuma configurada. O canvas está em texto na skill `canvas-storytelling`.
