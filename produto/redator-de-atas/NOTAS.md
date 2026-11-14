# Redator de Atas: notas

> Tudo o que o pacote exportado **não** guarda. Este arquivo é editado à mão.

## Objetivo

Transformar a transcrição e os materiais de uma reunião numa ata pronta para enviar: objetiva, fiel à fonte e adaptada ao tipo (homologação, discovery, refinamento, alinhamento ou outro). O público mistura Dados, Produto, Engenharia, Ciência de Dados, áreas de negócio e parceiros. A ata deve parecer uma comunicação final, não uma transcrição reorganizada.

O valor está em três coisas:
1. **Leitura completa.** O script lê a transcrição inteira, em blocos, e lista quem falou. O modelo não escreve a partir de uma leitura parcial.
2. **Fidelidade conferida por código.** Antes de mostrar a ata, o script a confere contra a fonte:
   - participantes sem prova de presença e quem falou e ficou de fora;
   - responsáveis que não aparecem na fonte;
   - números e datas que não estão na fonte, ou que foram corrigidos na reunião;
   - seções fora do tipo;
   - restos de formatação.
3. **Ata enxuta, com a dúvida à parte.** A ata sai limpa. O que só o usuário resolve vai para um bloco de conferência abaixo dela, com no máximo 6 pontos: convidado sem fala, ação sem dono, prazo convertido.

## De onde vem

O usuário tinha um agente de atas só com instruções, sem skills, sem código e fora deste repositório. O texto ficou fora da versão pública porque usava exemplos de um caso real. A ideia continua a mesma; o v1 muda a forma.

**Mantido do v0.** Todas as regras de conteúdo continuam, agora nas skills:
- a pergunta do tipo, com as 5 opções, e o tipo do usuário prevalecendo;
- a fonte única e o "não infira" (presença, papel, área, responsável, prazo, status, risco);
- a diferença entre discussão, alinhamento, decisão, hipótese, dúvida e próximo passo;
- "convite não é presença", nomes em ordem natural e a tabela Participante · Área;
- as estruturas por tipo e as regras do Refinamento (direcional junto do tema, insumos com origem, solução consolidada, sem seção para alternativa só avaliada);
- as seções proibidas sem pedido, o estilo e o Markdown para Loop, Teams e e-mail;
- a verificação final.

**O que não funcionava, e o que o v1 faz**

| No v0 | Efeito provável | No v1 |
|---|---|---|
| Tudo nas instruções, perto do limite de 8.000 caracteres. O texto colado termina cortado em "releva", no meio da verificação final | Parte das regras pode não ter chegado ao modelo. Não havia espaço para detalhar os tipos | Instruções com 5.350 caracteres, só com as regras críticas. O detalhe vai para 4 skills (7 a 10 mil caracteres cada), com espaço para crescer |
| Só o Refinamento tinha regras detalhadas, com exemplos de um caso real | Os outros tipos saíam genéricos. Os exemplos reais puxavam a ata para o caso original | Os 5 tipos com estrutura, ordem e regras próprias (`ata-tipos`). Exemplos fictícios |
| "Leia todo o conteúdo antes de selecionar participantes" dependia da memória do modelo | Em transcrição longa, o GPT tende a ler por amostragem e a perder quem falou pouco e as ações do fim da reunião | O script lê tudo e divide em blocos de 8.000 caracteres. O agente lê todos antes de escrever, e a linha de status mostra `Leitura k/n blocos` |
| "Não trate convidados como presentes" e "não atribua ação a quem só comentou" eram só regras de texto | Sem checagem, o erro só aparecia depois do envio | O script lista os falantes, separa convidados sem fala, reconhece dispositivo de sala e falante sem nome, e confere a ata. Os casos de responsável viram uma tabela de exemplos (`ata-fidelidade` §4) |
| A verificação final era um checklist do próprio modelo | O modelo confere o próprio texto com o mesmo viés com que o escreveu | `conferir` aponta o que não bate com a fonte. O checklist continua para o que só o modelo julga (decisão ou hipótese, tema lateral) |
| Uma resposta só, já como final | Dúvidas (dono, presença, prazo relativo) eram resolvidas por omissão silenciosa ou por inferência | Rascunho com Conferência à parte, revisão só do que mudou e entrega limpa com "aprovado" |
| O usuário colava ou anexava a transcrição | Transcrição de 1 hora passa do que cabe numa mensagem | Anexo do .docx ou .vtt do Teams lido pelo script. Sem anexo, a busca da reunião no Teams, com a cobertura marcada como parcial |
| Sem bateria de testes nem histórico | Uma mudança de instrução não tinha como ser conferida | Bateria com 4 reuniões fictícias e armadilhas plantadas, `conferir_codigo.py` e versão no repositório, como os outros agentes |

**O que o v1 acrescenta**
- **Correção vale a última:** o número ou a regra corrigidos na reunião ("na verdade é 12%") entram só na versão final. O script aponta quando a ata usa o valor antigo.
- **Prazo relativo:** "até quinta" vira data pela data da reunião, e a conversão vai para a conferência.
- **Fora da ata:** saúde, vida pessoal, avaliação de pessoas, salário, conflito pessoal e recados sociais.
- **Comandos:** `evidência <item>` (as falas que sustentam um item), `omitidos` / `incluir`, `tipo`, `conferência`, `versão atual` e `markdown`.
- **Data e link** numa linha abaixo do título. O v0 só pedia o link; a data entra porque a ata costuma circular dias depois da reunião.

## Desenho

### Princípios

1. **Fonte única.** A reunião escolhida e o que o usuário diz. Outra reunião, o convite e o recap gerado por IA não são fonte de fato.
2. **Leitura completa antes de escrever.** Pelo script, em blocos. Sem anexo, a cobertura é declarada parcial.
3. **Cada coisa no seu nome.** Decisão, alinhamento, hipótese, recomendação, dúvida, risco, próximo passo e lateral (`ata-fidelidade` §3).
4. **Nada sem fala que sustente.** Responsável e prazo só ditos. Na dúvida, a conferência pergunta; a ata não inventa.
5. **Conferência por código antes do usuário.** O que o script aponta como "Corrija" é corrigido antes de a ata aparecer.
6. **Enxuta.** Só os temas com detalhamento, direcional ou ação, consolidados. O que ficou de fora pode voltar com `omitidos`.
7. **O usuário envia.** O agente não envia nem publica.

### Fluxo

1. **Ficha:** reunião, fonte, cobertura e tipo. Só para aqui se faltar o tipo ou a fonte.
2. **Rascunho:** ler, ler os blocos, extrair, escrever, conferir, corrigir e mostrar com a Conferência.
3. **Revisão:** só o que foi pedido; só as seções que mudaram.
4. **Entrega:** a ata limpa, com "aprovado".

### Arquitetura

| Peça | Conteúdo | Caracteres |
|---|---|---|
| Instruções | Papel, fontes, fluxo, linha de status, regras críticas e comandos | 5.350 de 8.000 |
| `ata-fidelidade` | Fonte, leitura, tipos de fala, responsável e prazo, participantes e área, números, trecho não identificado, o que fica fora, conferência e verificação final | 9.853 |
| `ata-tipos` | Pergunta e sinais do tipo, estrutura e regras de Homologação, Discovery, Refinamento, Alinhamento e Outro | 7.735 |
| `ata-formato` | Cabeçalho, tabelas, seleção e síntese, linguagem, Markdown, conferência, omitidos, revisão, entrega e um exemplo | 7.217 |
| `ata-transcricao` | Como rodar o script: `ler`, `trecho`, `buscar` e `conferir` | 7.524 |

As regras críticas (fonte única, convite não é presença, responsável e prazo só ditos, correção vale a última, fora da ata) estão nas instruções **e** nas skills. Assim, valem mesmo se o modelo não abrir a skill.

## Código

O código só deste agente fica em [`codigo/`](codigo/). O [`montar_skills.py`](../../ferramentas/montar_skills.py) junta os três arquivos no script da skill, [`ata-transcricao/scripts/atas_transcricao.py`](pacote/skills/ata-transcricao/scripts/atas_transcricao.py).

- `transcricao.py`: lê sem bibliotecas externas, só com zip e XML da biblioteca padrão:
  - os formatos aceitos: .docx do Teams (nome e hora numa linha, fala na seguinte), .vtt do Teams (`<v Nome>`, com id de deixa e deixas partidas), texto com hora ou com "Nome: fala", notas sem falantes e .docx/.pptx de apoio;
  - o nome em ordem natural, com as marcas externo, sala e não identificado;
  - as listas "Presentes" e "Convidados" das notas e os eventos de transcrição;
  - a limpeza de HTML, `[Event]` e referências automáticas;
  - os blocos de leitura e a busca.
- `conferencia.py`: a conferência da ata contra a leitura. Confere:
  - participantes, responsáveis, números e datas, com os números por extenso ("cem por cento", "cinco mil");
  - correções na reunião e datas ditas por dia da semana;
  - seções por tipo, título e formato.
- `cli_atas.py`: a linha de comando (pedido em `/mnt/data/ata_pedido.json`; leitura guardada em `/mnt/data/ata_leitura.json`).

Para mudar o código:
1. Edite `codigo/`.
2. Rode `python ferramentas/montar_skills.py` e `python produto/redator-de-atas/testes/conferir_codigo.py`.
3. Só então suba a skill no Copilot.

As fixtures são geradas por `testes/gerar_fixtures.py` (precisa de python-docx só para gerar os .docx). As atas esperadas são escritas à mão.

## Configuração no Agent Builder

Os nomes abaixo seguem a documentação em inglês; na interface em português podem variar.

1. **Licença.** Teams, reuniões e Pessoas só aparecem como conhecimento com a licença Microsoft 365 Copilot. Sem elas, o agente funciona só com anexo.
2. **Knowledge:**
   - *My Teams chats and meetings*: inclui calendário, chat e transcrições, para achar a reunião, os convidados e o link;
   - *Reference people in organization*: a área pelo diretório.
   Não fixe reuniões específicas, nem ligue e-mail ou arquivos. Outra fonte só aumenta o risco de trazer fato de outra reunião.
3. **Capabilities:** *Code interpreter* ligado.
4. **Skills:** suba as 4 skills, cada uma num .zip com o `SKILL.md` na raiz. O .zip da `ata-transcricao` leva também a pasta `scripts/`.
5. Se houver a opção *Only use specified sources*, ligue.
6. Instruções, descrição e prompts iniciais: copie de [`agente.md`](agente.md).
7. Exporte, importe neste branch (`python ferramentas/importar.py "<zip>"`), rode `python ferramentas/montar_skills.py --conferir` e confira o diff. Registre em Decisões o que o export trouxe de diferente. É esperado que ele não traga `discourage_model_knowledge`, se a interface não expuser a opção.

**Uso:** anexe a transcrição baixada do Teams (na reunião: Recap → Transcrição → Baixar, em .docx ou .vtt) e o material apresentado, se houver. Diga o tipo e cole o convite ou o link, se quiser que eles entrem na conferência e no cabeçalho.

## Casos de teste

A bateria completa está em [`testes/PERGUNTAS-DE-CONTROLE.md`](testes/PERGUNTAS-DE-CONTROLE.md), e os resultados ficam em [`testes/RESULTADOS.md`](testes/RESULTADOS.md). O código é conferido sem o Copilot por [`testes/conferir_codigo.py`](testes/conferir_codigo.py). Os casos abaixo são o mínimo para uma conferência rápida.

| # | Pergunta / situação | Comportamento esperado | Último resultado |
|---|---|---|---|
| 1 | Refinamento do Jatobá, com o convite colado | 7 participantes (com o Marcos, pela fala da sala); Gustavo e Helena só na conferência | |
| 2 | Tolerância de revisão | 12% (o valor corrigido); 15% não aparece | |
| 3 | Pendência do jurídico | Sem responsável inventado; em Riscos, com a pergunta na conferência | |
| 4 | Última ação da reunião (Bruno e Caio até segunda) | Está na tabela, com os dois na mesma linha e 16/11; leitura 2/2 blocos | |
| 5 | Homologação sem tipo dito | Pergunta o tipo e sugere Homologação; alerta "sem status declarado" | |
| 6 | "Complete os prazos que faltaram" | Não inventa; pergunta ou deixa a célula vazia | |

## Decisões

- v1.0.0 (2026-11-12, proposta). Reconstrução do agente de atas do usuário (v0, fora da versão pública), no padrão dos outros agentes. A comparação completa está em [De onde vem](#de-onde-vem).
  - **Nome:** Redator de Atas, no padrão de função dos outros agentes (Organizador, Assistente, Analista).
  - **Regras críticas nas instruções, detalhe nas skills**, como no Coach de Pessoas: o que não pode falhar fica nos dois lugares.
  - **Leitura e conferência por código.** Ler tudo e conferir participantes, números e datas é trabalho mecânico, e o modelo erra nesse tipo de trabalho. O julgamento (decisão ou hipótese, tema lateral, área) continua com o modelo e com o usuário.
  - **Leitor sem bibliotecas externas.** O .docx e o .pptx são lidos por zip e XML da biblioteca padrão. Assim, o leitor não depende de o python-docx existir no ambiente das skills; a sonda de 09/11 só registrou o python-pptx.
  - **Blocos de 8.000 caracteres**, menores que o normal, para a saída do interpretador não ser cortada. O fim de cada bloco ("Fim do bloco k/n") serve de prova de leitura completa. Se faltar, o agente lê de novo com `"tamanho": 5000`.
  - **Rascunho com conferência à parte, em vez de uma resposta final direta.** A ata continua com cara de comunicação final; a dúvida fica fora dela. Com o tipo dito e a fonte em mãos, o agente não para na ficha.
  - **Data abaixo do título**, junto com o link. É uma mudança em relação ao v0, que não pedia a data. Se não quiser, tire de `ata-formato` §1.
  - **Participantes sem área comprovada viram lista**, não tabela com a coluna Área vazia.
  - **Homologação:** o status por funcionalidade fica numa tabela; "Status de Homologação" vira seção só quando há um status geral declarado à parte. Assim, o mesmo status não se repete.
  - **Fora da ata:** saúde, vida pessoal, avaliação de pessoas, salário, conflito pessoal e recados. O v0 não tratava isso. A ata circula para um público grande, e o padrão dos outros agentes já é esse.
  - **Fontes:** Teams (reuniões e chats) e Pessoas, sem e-mail e sem arquivos. Com `discourage_model_knowledge`. A busca serve para achar a reunião; o anexo é o caminho para a versão final.
  - **Exemplos reais do v0 trocados por fictícios** (Portal Araçá, Base Cambuci, nível N3). Mesma lógica, sem puxar a ata para o caso original.
  - **A validar no primeiro uso:**
    - se a busca do Teams traz a transcrição inteira ou só trechos;
    - se a saída de 8.000 caracteres do interpretador chega inteira;
    - o formato exato do .docx que o Teams do tenant baixa (o leitor aceita os três formatos conhecidos);
    - se o agente lê todos os blocos sem ser lembrado.

## Limitações conhecidas

- A conferência por código não sabe se uma decisão foi decisão nem se o responsável assumiu a ação: ela confere nomes, números, datas, seções e formato. O resto é das regras e da bateria.
- Número dito por extenso fora de "por cento" e "mil" ("duas semanas") não é conferido.
- A conferência compara valores, não contexto. Um número da fonte usado no lugar errado passa.
- Pela busca do Teams, sem anexo, a conferência é só de formato.
- Falante não identificado e dispositivo de sala dependem do usuário ou de alguém se identificar na fala.

## Fontes de conhecimento

Teams (reuniões, calendário, chats e transcrições) e o diretório de Pessoas do próprio usuário, sem itens fixos. Nenhum documento vem para o repositório. As fixtures usam só dados fictícios, no mesmo mundo das fixtures dos outros agentes:
- Projetos e sistemas: Painel Jatobá, Tarumã, Quimera-7, Previsão de Ruptura, Hub Logístico, Base Cambuci, Portal Araçá, Parceiro+.
- Pessoas: Ana, Bruno, Caio, Gustavo, Renata, Paula, Marcos, Fernanda, Otavio, Jorge, Fabio, Helena.

Os nomes foram escolhidos para não existir no tenant: qualquer fato "encontrado" para eles é invenção.
