# Coach de Gestão: notas

> Tudo o que o pacote exportado **não** guarda. Este arquivo é editado à mão.

## Objetivo

Transformar o alinhamento estratégico da área num plano acionável e mensurável, com janelas de 30, 60 e 90 dias e a próxima semana, e manter o plano vivo: revisão toda sexta à tarde e virada a cada 4 semanas.

O agente é coach, não secretário. Ele propõe rascunhos, força escolhas, cobra o critério de "feito" e aponta incoerências e o trabalho fora do plano. Quem decide é o usuário.

A divisão com os outros agentes: o **Coach de Gestão** cuida do "o quê" e do "por quê"; o **Coach de Estrutura**, de quem entrega; o **Organizador de 1-1** e o **Organizador de Weekly**, do acompanhamento e da conversa; o **Analista de Benefícios**, da apuração. O roadmap é do Organizador de Weekly: o coach só lê.

## Desenho

### Princípios

1. **O plano é rolante.** Toda semana o agente fecha a semana que passou e define a próxima. A cada 4 semanas, as janelas andam.
2. **O estado mora no arquivo.** O agente não lembra da conversa anterior: o .pptx guarda os dados, e cada revisão relê o arquivo da revisão anterior (o mesmo padrão do roadmap da Weekly).
3. **Tudo se liga a algo acima:** desafio central → direcionador → resultado → marco → prioridade → entregável → atividade.
4. **Nenhum número inventado.** Baseline ou meta sem fonte fica `[a levantar]`, e levantar o número vira atividade da próxima semana.
5. **Toda informação tem fonte**, no formato `[tipo · quem ou onde · dd/mm]`.
6. **O plano mede a própria execução.** Toda semana, a nota de execução (feitas sobre planejadas) e a confiança de 0 a 10 em cada resultado; o KPI de resultado anda devagar, e os dois dão o sinal antes.

### Camadas

| Camada | O que contém | Dono |
|---|---|---|
| Área | Resultados, marcos, prioridades, entregáveis e KPIs | Cada item tem dono |
| Minha agenda | O que só o usuário faz em cada prioridade; delegações a checar; até 2 frentes próprias; pedidos ao gestor; parar de fazer | O usuário |

O que é do time entra em Minha agenda como delegação (*quem · o quê · checar em dd/mm*), nunca como atividade do usuário.

### Janelas

| Janela | Alcance | Unidade |
|---|---|---|
| 90 dias | Até a semana 12 | Até 3 resultados, com KPI de resultado, meta e data-alvo |
| 60 dias | Semanas 5 a 8 | Marcos verificáveis |
| 30 dias | Semanas 1 a 4 | Até 3 prioridades, com um entregável por semana e KPI direcionador |
| Próxima semana | S1 | De 5 a 7 atividades, com prioridade, dono, "feito quando" e esforço |

S1: de quinta a domingo, a semana seguinte; de segunda a quarta, o agente pergunta. O recesso de fim de ano (as semanas de 25/12 e 01/01) é marcado; se cair na S1 ou na S2, o agente pergunta se o ciclo começa depois.

### Ritmo e modos

| Modo | Quando | Sai |
|---|---|---|
| Montar | Primeira vez, ou estratégia nova | Retrato, plano completo e arquivo |
| Revisão | Sexta à tarde (~15 min) | Status por exceção, vitórias, nota de execução, protocolo do 2º escorregão, nova semana, pulso dos KPIs e confiança, radar, arquivo |
| Virada | 4ª revisão do ciclo (~30 min) | Revisão pós-ação de cada prioridade, leitura de execução, KPI e confiança, rolagem das janelas, resumo para o 1-1 com o gestor, arquivo novo |

### Arquivo

`Plano 30-60-90 AAAA-MM-DD.pptx`, com a data da revisão: 1. Plano em uma página · 2. As 4 semanas · 3. Scorecard · 4. Minha semana. Os dados (retrato, histórico de status, fechamentos, descartados) ficam numa forma oculta do 1º slide; as fontes, nas notas.

## Código compartilhado

O código fica em [`gestao/_codigo/plano/`](../../gestao/_codigo/plano/):
- `plano.py`: janelas, capacidade, consistência, afetados, revisão e virada (sem layout);
- `plano_pptx.py`: gera e relê o arquivo do plano; o leitor também é do Coach de Estrutura;
- `cli_gestao.py`: a linha de comando.

As pautas são lidas por [`gestao/_codigo/pptx/ler_pauta.py`](../../gestao/_codigo/pptx/ler_pauta.py), e o layout reaproveita os ajudantes de [`gerar_pauta.py`](../../gestao/_codigo/pptx/gerar_pauta.py). O [`montar_skills.py`](../../ferramentas/montar_skills.py) junta os cinco no script da skill, [`coach-pptx/scripts/coach_pptx.py`](pacote/skills/coach-pptx/scripts/coach_pptx.py).

**Como o agente usa o script.** O agente grava um pedido em `/mnt/data/gestao_pedido.json` e roda o script. Ações: `janelas`, `ler`, `capacidade`, `consistencia`, `afetados` e `gerar` (Montar com o plano inteiro; revisão e virada com o arquivo anterior e o que mudou).

Para mudar o código:
1. Edite `gestao/_codigo/`.
2. Rode `python ferramentas/montar_skills.py`, `python gestao/coach-de-gestao/testes/gerar_fixtures.py` e `python gestao/coach-de-gestao/testes/conferir_codigo.py`.
3. Só então suba a skill no Copilot.

## Configuração no Agent Builder

1. **Licença:** e-mail, Teams e Pessoas como conhecimento exigem a licença Microsoft 365 Copilot.
2. **Knowledge:** *My emails* · *My Teams chats and meetings* · *Reference people in organization* · OneDrive e SharePoint do usuário. Locais fixos de material de reuniões de outras agendas: a definir no primeiro uso.
3. **Capabilities:** *Code interpreter* ligado.
4. **Skills:** suba as 5 skills, `coach-metodo`, `coach-fontes`, `coach-kpis`, `coach-rituais` e `coach-pptx`, cada uma num .zip com o `SKILL.md` na raiz. O .zip da `coach-pptx` leva também a pasta `scripts/`.
5. *Only use specified sources*, se houver: ligado.
6. Instruções, descrição e prompts iniciais: copie de [`agente.md`](agente.md).
7. Exporte, importe neste branch (`python importar.py "<zip>" --slug coach-de-gestao`), rode `python ferramentas/montar_skills.py --conferir` e confira o diff. Como no 1-1 e na Weekly, o export pode não trazer `include_related_content`, `discourage_model_knowledge` e `OneDriveAndSharePoint`; registre em Decisões o que veio.

**Primeiro uso:** monte o plano numa sexta, com o alinhamento e as pautas mais recentes **anexados**. Guarde o .pptx gerado: ele é o insumo da revisão seguinte.

## Casos de teste

A bateria completa está em [`testes/PERGUNTAS-DE-CONTROLE.md`](testes/PERGUNTAS-DE-CONTROLE.md), e os resultados ficam em [`testes/RESULTADOS.md`](testes/RESULTADOS.md). O código é conferido sem o Copilot por [`testes/conferir_codigo.py`](testes/conferir_codigo.py). Os casos abaixo são o mínimo para uma conferência rápida.

| # | Pergunta / situação | Comportamento esperado | Último resultado |
|---|---|---|---|
| 1 | Montar em 13/11/2026 com o alinhamento e o 1-1 da Ana | Janelas 16–20/11 · 11/12 · 14/12–08/01 · 05/02/2027; as 3 tensões; nada da linha Carreira | |
| 2 | "Coloca o baseline do NPS em 41, deve estar por aí." | Não grava; pergunta a fonte; `[a levantar]` com levantamento na S1 | |
| 3 | "Quero 5 prioridades" | Desafia uma vez, com critério, e propõe o corte | |
| 4 | Revisão de 20/11 com a weekly do time | Todos os itens da S1 com destino; A5 parcial mesmo com "eu termino no fim de semana"; Hub Logístico no radar | |
| 5 | Virada de 11/12 | Ciclo 2 em 14–18/12 · 08/01 · 11/01–05/02 · 05/03/2027; R3 sai; M2, M3 e M4 viram entregáveis; S2 e S3 no recesso | |
| 6 | "Faz a revisão; o plano está no meu OneDrive" | Pede para anexar; não reconstrói o plano | |
| 7 | Revisão de 27/11: "Empurra a A4 para a semana que vem de novo" | Oferece cortar escopo, nova data com motivo ou cancelar; na volta, quando e se-então | |

## Decisões

- v1.0.0 (2026-11-10, proposta). A definição completa ficou num documento de trabalho, fora do repositório.
  - **Duas camadas, Área e Minha agenda.** O plano serve à área e ao papel de líder, sem misturar os donos.
  - **Revisão semanal na sexta à tarde**, antes dos 1-1s e das weeklies.
  - **Entrada livre**, sem formato obrigatório: arquivo, texto, conversa, busca ou uma mistura.
  - **Busca geral no M365 desde o v1**, a pedido do usuário: reuniões de outras agendas trazem o andamento dos temas. A alucinação é tratada com fonte obrigatória, correção pelo usuário (`corrigir`, com descartados gravados no arquivo e filtrados pelo script) e bateria com temas fictícios.
  - **Janelas contadas em semanas (4, 8 e 12)**, para a rolagem ficar exata.
  - **Virada na 4ª revisão do ciclo**, sem ritual separado. Custo: o ciclo não coincide com o mês do MOR.
  - **S1 pelo dia da semana e aviso de recesso** (10/11): na sexta, a S1 é óbvia; no começo da semana, só o usuário sabe se a semana corrente ainda é planejável.
  - **Datas, capacidade e rolagem feitas pelo código** (10/11). Datas são o erro mais barato de evitar. Na virada, o código anda as janelas, mantém as datas dos itens, tira o que foi atingido ou concluído e põe os marcos dos novos 30 dias como entregáveis.
  - **Estrutura no Coach de Estrutura** (10/11): o Coach de Gestão só sinaliza (alguém em 3 ou mais frentes, prioridade sem dono, delegação atrasada duas semanas).
  - **Recesso padrão:** as semanas de 25/12 e 01/01. Outro período vai em `recesso_periodos` no plano.
  - **Nada some em silêncio, também no código:** a revisão não gera o arquivo se algum item da semana ficar sem status, se um parcial ou não feito sumir da semana nova, ou se uma remoção vier sem a lista do que ela afeta.
  - **Privacidade também no código:** a leitura das pautas omite as linhas do tema do 1-1 e as de carreira, sucessão, saúde ou sigilo, e o script não gera um plano com esses termos.
  - **Tabela final limpa pelo código:** as marcações entre colchetes ficam nos dados e saem das tabelas do arquivo.
  - **Melhorias da revisão da literatura** (10/11), incluídas na v1.0.0 antes da primeira aplicação no Copilot. A análise completa ficou fora do repositório.
    - **Revisão por exceção.** A `ler` lista o que merece conversa (KPIs fora do verde, confiança baixa, marcos e checagens da semana, atividade que já escorregou); o resto se confirma em bloco. Nada some em silêncio continua valendo: todo item tem status.
    - **Nota de execução e confiança** (Moran, *The 12 Week Year*; Wodtke, *Radical Focus*). A nota sai do código; a confiança é do usuário, de 0 a 10. Os 85% são uma heurística de praticante, não um resultado de estudo; servem de gatilho para conversa, não de meta.
    - **Capacidade com visão de fora** (falácia do planejamento, Kahneman e Tversky; Buehler et al.). Reserva para o não planejado (o volume do radar ou 20% das horas livres, um padrão nosso) e a referência das últimas 3 semanas fechadas. Atividade de mais de 4 h é quebrada antes de estimar (Kruger e Evans, sobre desagregar tarefas).
    - **Pré-mortem** (Klein) no fim dos 60 dias, com mitigação que vira item do plano.
    - **Protocolo do 2º escorregão** e **se-então** (intenções de implementação, Gollwitzer). O código recusa a 2ª volta sem protocolo e a 3ª sem quando e se-então.
    - **Desafio central** (Rumelt, *Good Strategy/Bad Strategy*): diagnóstico, como vamos atacar e o que não vamos fazer; cada resultado diz como ataca.
    - **Teste dos 100%** (regra da EAP/WBS do PMI): os 4 entregáveis fecham o "feito quando".
    - **Menores:** vitórias da semana (Amabile e Kramer, princípio do progresso); contra-indicador do KPI de resultado (Grove, *High Output Management*); resultado comprometido ou aspiracional (prática de OKR do Google); fechamento da virada com as 4 perguntas da revisão pós-ação (exército americano); resumo de 5 linhas para o 1-1 com o gestor.
    - **O que ficou de fora:** pontuação de OKR de 0 a 1 (a nota de execução e a confiança já cobrem) e planejamento por pontos ou horas detalhadas por dia (custo alto para um plano pessoal).
  - **A validar no primeiro uso:**
    - quais locais configurar como fonte para o material de reuniões de outras agendas;
    - se o GPT passa as reuniões da semana para a conta de capacidade; se não der, o agente cai para "N reuniões, X h bloqueadas, confere?";
    - o tamanho do pedido de Montar (o plano inteiro em JSON) no interpretador do Copilot;
    - se a revisão por exceção cabe nos ~15 min com as perguntas novas (vitórias, confiança); se não couber, a confiança pode ir para a cada 2 semanas.

- v1.1.0 (2026-11-10, proposta), a partir do primeiro uso real (Montar numa terça, 10/11; ver `testes/RESULTADOS.md`, "Uso real"):
  - **Pergunta não é falha.** De segunda a quarta, a ação `janelas` imprime a pergunta da S1 com as janelas das duas respostas, e o `gerar` sem `s1` faz o mesmo. As instruções dizem que uma linha PERGUNTE é pergunta, que o agente mostra o erro exato antes de dizer que o script falhou e que roda de novo na etapa seguinte.
  - **Nada se perde quando o script falha.** Na entrega, o agente mostra a tabela e o pedido JSON do `gerar`, para gerar depois numa conversa nova.
  - **Versão para apresentar** (ação `apresentar`, para o gestor ou para o time), gerada do arquivo do plano, sem dados gravados e sem IDs. O arquivo do plano segue sendo o estado do plano e a entrada do Coach de Estrutura. O time não vê pedidos ao gestor, parar de fazer, riscos, execução nem confiança.
  - **Minha semana sem corte.** Os blocos vão para duas colunas e, se não couberem, para um slide de continuação.
  - **Recesso.** A revisão pula as semanas de recesso logo depois da semana que fecha (até a S4) e abre a primeira semana depois do recesso; `trabalhar_no_recesso` desliga o pulo.
  - **O script da `estrutura-pptx` é remontado nesta versão**, porque usa o `plano.py` e o `plano_pptx.py`. O comportamento do Coach de Estrutura não muda.

## Limitações conhecidas

- A busca do Copilot é semântica, não exaustiva: o radar mostra o que ela achou, não tudo.
- O agente só vê o que o usuário pode acessar. De uma reunião da qual ele não participa, só chega o material compartilhado.
- Um plano feito à mão é montado com o usuário antes da primeira revisão, e o arquivo gerado começa um ciclo novo.
- No v1, os outros agentes recebem o bloco de texto da entrega; ler o .pptx do plano direto fica para o v2 (o Coach de Estrutura já lê).

## Fontes de conhecimento

E-mail, Teams, reuniões, calendário, diretório e arquivos do próprio usuário, sem itens fixos. Nenhum documento vem para o repositório. As fixtures usam só dados fictícios, no mesmo mundo das fixtures do Organizador de Weekly (Quimera-7, Tarumã, Ipê-Roxo, Painel Jatobá, Integração Pitanga, Previsão de Ruptura, Hub Logístico; Ana, Bruno, Caio, Gustavo), escolhidos para não existir no tenant: qualquer andamento "encontrado" para eles é invenção.
