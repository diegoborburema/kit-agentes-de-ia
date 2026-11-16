# Organizador de 1-1: notas

> Tudo o que o pacote exportado **não** guarda. Este arquivo é editado à mão.

## Objetivo

Manter os 1-1 focados e impedir que temas se percam entre uma semana e outra. O usuário indica a pessoa, as 3 prioridades da vez e a pauta anterior. O agente:

1. monta a ficha do 1-1: pessoa, direção (para cima ou para baixo), data, semana do mês e tema da semana;
2. busca no e-mail, no Teams, nas reuniões e no calendário o que aconteceu desde o último 1-1;
3. propõe a pauta no layout padrão, com fonte em cada linha, para revisão;
4. entrega a tabela final e o arquivo .pptx.

O valor está na continuidade. A pauta anterior é a base, e nenhuma linha sai sem decisão do usuário. A busca acrescenta e atualiza. Com liderados, as anotações feitas no 1-1 viram a base da pauta seguinte. Os combinados de cada 1-1 voltam toda semana até serem feitos.

## Layout

Dois layouts, pela direção do 1-1. Referências com dados fictícios:

- **Para cima (gestor):** [`referencias/layout-pauta.png`](referencias/layout-pauta.png). Colunas Categoria · Tema · Atualização / Próxima ação · Tipo · Status. É o layout usado desde a semana de 26–30/10/2026, mais o grupo 4 (Tema da semana) na legenda.
- **Para baixo (liderado):** [`referencias/layout-pauta-liderado.png`](referencias/layout-pauta-liderado.png), com anotações simuladas. Colunas Categoria · Tema · Para puxar · Anotações; sem Tipo e sem Status, porque a temperatura vem do liderado. A seção 5, Temas do `<nome>`, guarda até 2 temas que ele deve trazer e 2 linhas em branco. Quando a pauta não cabe com fonte legível, ela continua num 2º slide.
- **Combinados, nos dois layouts:** bloco depois da tabela, com Quem · O quê · Até · ✓, os combinados em aberto da pauta anterior e 3 linhas em branco. Fica no último slide se couber, senão num slide próprio ([`referencias/layout-pauta-liderado-2.png`](referencias/layout-pauta-liderado-2.png)).

| Seção | Categoria | Cor |
|---|---|---|
| 1. 3 prioridades | nome da prioridade | `#7D5DA2` · `#9F88BA` · `#523D6B` |
| 2. Pessoas | Pessoas | `#00ABA3` |
| 3. Projetos | nome do projeto | `#087BA7` |
| 4. Tema da semana | nome do tema | `#C27C3E` |
| 5. Temas do `<nome>` (só para baixo) | Temas do `<nome>` | `#4F8A5B` |

Tema da semana, pela ordem da segunda-feira no mês: **1** Metas & PDP · **2** Carreira · **3** Feedback mútuo · **4** Carga & bem-estar · **5** Livre.

Cada tema tem um banco na skill [`pauta-1-1-temas`](pacote/skills/pauta-1-1-temas/SKILL.md), separado para cima e para baixo: 3 perguntas de **preparação**, que o agente faz ao usuário e que viram as linhas do tema, e 6 perguntas **para levar** à conversa (1 a 3 nos meses ímpares, 4 a 6 nos pares). As perguntas para levar aparecem depois da tabela e nas notas do slide. Para acrescentar ou trocar perguntas, edite só essa skill.

## Configuração no Agent Builder

Os nomes abaixo seguem a documentação em inglês; na interface em português podem variar.

1. **Licença.** E-mail, Teams e Pessoas só aparecem como conhecimento com a licença Microsoft 365 Copilot. Se não aparecerem, o agente não funciona como foi desenhado: pare e reveja o desenho.
2. **Knowledge:** *My emails* · *My Teams chats and meetings*, que inclui calendário e transcrições · *Reference people in organization* ligado. Não fixe chats nem reuniões específicas, porque o agente precisa da caixa e do calendário inteiros.
3. **Capabilities:** *Code interpreter* ligado.
4. **Skills:** suba `pauta-1-1`, `pauta-1-1-temas` e `pauta-1-1-pptx`, cada uma num .zip com o `SKILL.md` na raiz. Desde a v1.3.0, o .zip da `pauta-1-1-pptx` leva também a pasta `scripts/`.
5. Se houver a opção *Only use specified sources*, ligue.
6. Instruções, descrição e prompts iniciais: copie de [`agente.md`](agente.md).
7. Exporte, importe neste branch e confira o diff. Além de ids e versão, é esperado que o export não traga `include_related_content` (People), `discourage_model_knowledge` e `OneDriveAndSharePoint` sem itens, se a interface não expuser essas opções. Registre em Decisões o que veio.

## Casos de teste

A bateria completa está no documento **Organizador de 1-1: perguntas de controle** (mantido fora do repositório), e os resultados ficam em [`RESULTADOS.md`](RESULTADOS.md). Os casos abaixo são o mínimo para uma conferência rápida.

| # | Pergunta / situação | Comportamento esperado | Último resultado |
|---|---|---|---|
| 1 | "Quero preparar meu 1-1 com o meu gestor de 05/11/2026", com [`fixtures/pauta-anterior.pptx`](fixtures/pauta-anterior.pptx) | Ficha numa mensagem; direção para cima; semana 1 → Metas & PDP; as 9 linhas da fixture lidas | |
| 2 | Rascunho do caso 1 | As 8 linhas fictícias herdadas (o tema da semana não é herdado) como "sem novidade", sem nenhum fato novo; toda linha com fonte | |
| 3 | 1-1 com um liderado em 19/11/2026 | Direção para baixo; semana 3 → Feedback mútuo; layout com Para puxar e Anotações, sem Tipo e sem Status; Temas do `<nome>` com 2 linhas em branco | |
| 4 | 1-1 em 30/11/2026 e em 01/10/2026 | Semana 5 → Livre; 01/10 → semana 4 de setembro → Carga & bem-estar | |
| 5 | "Inclua em Pessoas que a Fulana está afastada por um problema de saúde" | Linha neutra com `[conversar ao vivo]`, sem citar saúde | |
| 6 | Resposta à preparação do tema (caso 1) | As linhas do tema reescritas só com o que foi respondido; perguntas para levar 1 a 3 (novembro) | |
| 7 | "aprovado" no rascunho | Tabela final limpa, perguntas para levar e .pptx no layout, com as mesmas linhas e as perguntas nas notas | |
| 8 | 1-1 com liderado, com [`fixtures/pauta-anterior-liderado.pptx`](fixtures/pauta-anterior-liderado.pptx) | Os bullets seguem as anotações; a temperatura anotada aparece no contexto; nada inventado | |
| 9 | "Junte as duas primeiras linhas" e depois "versão atual" | Só essas linhas mudam; a versão atual não reescreve nada | |
| 10 | Caso 8, olhando os combinados | Os 2 em aberto voltam com `(desde …)`; o marcado com ✓ não volta e aparece como concluído | |
| 11 | "aprovado" numa pauta com 9 linhas ou mais (pedido de geração longo) | O pedido é gravado em Python (`json.dump`), nunca por `bash`/heredoc; o .pptx sai em menos de 2 minutos | |

## Decisões

- v1.0.0 (2026-11-03, proposta):
  - **Estrutura:** as 3 seções atuais (3 prioridades, Pessoas, Projetos) mais o tema da semana como 4º elemento.
  - **Rotação semanal:** Metas & PDP, Carreira, Feedback mútuo, Carga & bem-estar; a semana 5 fica livre. A semana do mês é a ordem da segunda-feira no mês, para que toda semana útil caia num mês só. A conta é feita no interpretador de código, porque o GPT erra cálculo de calendário. Vale para 1-1 semanal; se a cadência ficar quinzenal, a rotação deixa temas de fora e precisa ser revista.
  - **Direção pelo organograma:** para cima (gestor) ou para baixo (liderado), cada uma com seu conjunto de Tipo. Para cima: Info, Ajuda, Escalation e **Decisão** (nova). Para baixo: Info, Acompanhar, Desbloquear e Decisão. 1-1 com pares fica fora do escopo da v1. *(Na v1.1.0, o layout para baixo deixou de ter Tipo.)*
  - **Pauta anterior como base:** nada sai sem decisão do usuário. No rascunho, `[sem novidade]`, ⚪ e a coluna Δ deixam claro o que a busca encontrou e o que é só herança.
  - **Fonte obrigatória** em cada linha do rascunho. A tabela final sai limpa.
  - **Foco:** no máximo 12 linhas, com uma ordem de corte definida; o resto vai para "Fora da pauta". Atualização de até 120 caracteres, porque 12 linhas desse tamanho ainda cabem no slide.
  - **.pptx gerado do zero** por código fixo na skill, sem editar o arquivo anterior. Assim o resultado não depende da estrutura interna do arquivo do usuário e o layout fica idêntico toda semana. O leitor aceita status como texto (●) ou como forma.
  - **Três skills:** `pauta-1-1` (regras, usada sempre), `pauta-1-1-temas` (banco de perguntas do tema da semana) e `pauta-1-1-pptx` (código, só na leitura do .pptx e na entrega). O banco fica separado para crescer sem mexer nas regras.
  - **Preparação do tema da semana:** o agente faz 3 perguntas ao usuário, propõe respostas só quando há evidência e transforma as respostas nas linhas do tema, conforme a Saída de cada tema. Sem resposta, a linha fica `[a elaborar]` com a pergunta principal. Responder é opcional.
  - **Perguntas para levar** alternam por mês (1 a 3 nos ímpares, 4 a 6 nos pares), para não repetir as mesmas todo mês sem depender de memória entre conversas. Vão para as notas do slide, porque o layout da tabela não muda.
  - **Sem barra de %:** são 4 etapas curtas. A linha de status mostra etapa, pessoa, data, tema e janela de busca.
  - **Privacidade em Pessoas:** descrição neutra e `[conversar ao vivo]` para saúde, questão disciplinar, salário e conflito pessoal.
  - **O agente só lê:** sem EmailActions nem MeetingActions. A pauta não é enviada pelo agente.
  - **A validar no primeiro uso:** modo *Think deeper* contra o padrão; *Only use specified sources*; python-pptx no interpretador do Copilot (ENT-02).

- v1.1.0 (2026-11-04, proposta), a partir do primeiro uso real com um liderado:
  - **Layout para baixo próprio.** No 1-1 com liderado, o usuário leva poucos pontos para retomar cada tema, e quem traz a atualização e a temperatura é o liderado. Por isso saem Tipo e Status e entram **Para puxar** (1 ou 2 bullets de até 45 caracteres, gerenciais) e **Anotações** (vazia, para o usuário escrever na reunião). O detalhe da busca vira **Contexto**, que fica no rascunho e nas notas do slide.
  - **Temas do `<nome>`:** seção 5, com o que a busca indica que o liderado vai trazer (pedidos dele em aberto) e 2 linhas em branco para o que ele trouxer na hora.
  - **Anotações como fonte.** O leitor do .pptx passa a reconhecer as colunas pelo cabeçalho e a ler as anotações, mesmo com a pauta em 2 slides. Na semana seguinte, os bullets partem do que foi anotado, e uma temperatura escrita com 🟢, 🟡 ou 🔴 volta no contexto.
  - **Prioridades do liderado:** para baixo, são as frentes dele, propostas a partir das fontes, e não as 3 prioridades do usuário.
  - **2º slide em vez de fonte minúscula** no layout para baixo: a fonte não desce de 84% e sobra espaço para as anotações. A quebra acontece entre seções; uma seção só se divide se não couber sozinha num slide. O layout para cima continua num slide só, como na v1.0.0.
  - **Correções do uso real** (perguntas criadas antes da correção): nome no formato do diretório (NOM-01); linha duplicada (LIN-01) ou agregada (LIN-02); Categoria trocada por "Prioridade" (LIN-03); ordem das seções no slide, agora garantida no código (LIN-04); revisão aplicando o que não foi pedido (REV-02); "versão atual" reescrevendo conteúdo (CMD-03); link como texto com destaque amarelo, agora hiperlink de verdade (ENT-07).
  - Bateria: FLB-03 e FLB-04 aposentadas; novas BXO-01 a BXO-07, CON-01 a CON-06 (Cenário E) e as 8 dos defeitos.

- v1.2.0 (2026-11-04, proposta), a partir do 1-1 em que o layout para baixo foi usado:
  - **Bloco Combinados** depois da tabela, nos dois layouts: as tarefas que saem do 1-1, do usuário e da pessoa. Colunas Quem · O quê · Até · ✓.
  - **Acompanhamento:** um combinado em aberto volta toda semana até o usuário marcar ✓, com `(desde dd/mm)` para mostrar a idade. Se a busca achar evidência de que foi feito, ele vai para "Encerrar?"; só o usuário encerra. Marcado com ✓, sai e aparece no rascunho como concluído.
  - **Sem duplicar:** a tarefa fica só no bloco, não nos bullets nem nas atualizações da tabela. Combinados nunca são inventados.
  - **Leitor:** reconhece as duas tabelas pelo cabeçalho e devolve os combinados com o que estiver na coluna ✓. Pautas anteriores sem o bloco continuam sendo lidas.
  - Para cima, uma pauta que já ocupa o slide inteiro manda o bloco para um 2º slide. Até a v1.1.0, essa pauta ficava sempre num slide só.
  - Funções internas do leitor e do gerador com nomes distintos (`_ler_combinados`, `_bloco_combinados`), porque o agente roda os dois blocos de código na mesma sessão.

- v1.3.0 (2026-11-14, proposta), para caber no limite do Agent Builder e entrar no repositório público:
  - **`pauta-1-1-pptx` com script.** A skill tinha 23.049 caracteres, acima do limite de 20.000: o código de leitura e geração estava dentro do `SKILL.md`. Agora ele fica em `scripts/pauta_1_1_pptx.py`, montado de `gestao/_codigo/pptx/ler_pauta.py`, `gerar_pauta.py` e `cli_1_1.py` (novo). A skill caiu para 6.666 caracteres.
  - **Mesmo resultado.** O código compartilhado é o mesmo que o Organizador de Weekly e os coaches de gestão já usam. Antes da troca, a leitura das duas pautas de `fixtures/` deu igual nas duas versões, e a geração do exemplo para baixo e de uma pauta para cima de 2 slides saiu com o XML dos slides idêntico.
  - **Pedido em JSON**, como no Weekly: o agente grava `/mnt/data/pauta_pedido.json` (`ler` ou `gerar`) e roda o script, que imprime a leitura ou a conferência do arquivo gerado. O agente não escreve mais código de layout.
  - **Instruções:** só a etapa 4 muda: "gere o arquivo .pptx pelo script da skill", no lugar de "com o interpretador de código".
  - **Testes de código:** `testes/conferir_codigo.py` (novo) roda o script contra as fixtures, sem o Copilot.
  - **Para aplicar:** suba o novo .zip da `pauta-1-1-pptx`, com `scripts/`; troque a frase da etapa 4 nas instruções; rode os cenários de leitura e entrega das perguntas de controle (casos 7, 8 e 10).

- v1.3.1 (2026-11-16, proposta), do primeiro uso real da v1.3.0:
  - **Defeito:** na entrega, o agente gravou o pedido de geração com `bash -lc cat > /mnt/data/pauta_pedido.json <<'JSON'` em vez do bloco Python da skill e ficou parado em "Codificando e executando" por 30 minutos. Causa provável: o fechamento do heredoc não casou, e o `cat` ficou esperando a entrada. Virou o caso de teste 11 antes da correção.
  - **Correção:** a skill manda gravar o pedido só em Python, com `json.dump`, proíbe `bash`, `cat`, `echo` e heredoc para o pedido e diz o que fazer se uma execução não responder em 2 minutos.

## Limitações conhecidas

- A busca do Copilot é semântica, não exaustiva. Quem garante a continuidade é a pauta anterior; a busca só acrescenta.
- O agente só vê o que o usuário acessa. O envolvimento da outra pessoa é inferido das conversas, e-mails e reuniões em comum.
- Transcrições só existem para reuniões gravadas ou transcritas.
- Anotações longas digitadas durante o 1-1 aumentam as linhas, e a tabela pode passar do limite do slide. Nada se perde: o texto continua na tabela e o leitor o encontra na semana seguinte.

## Fontes de conhecimento

E-mail, Teams, reuniões, calendário, diretório e arquivos do próprio usuário, sem itens fixos. Nenhum documento vem para o repositório. As fixtures usam só dados fictícios (Quimera-7, Tarumã, Ipê-Roxo, Jaboticaba, Pitanga, Cambuci, Araçá), escolhidos para não existir no tenant: qualquer atualização "encontrada" para eles é invenção.
