# Assistente de PRD: notas

> Tudo o que o pacote exportado **não** guarda. Este arquivo é editado à mão.

## Objetivo

Conduz o PRD (Product Requirements Document) de um produto de dados ou de IA em 5 etapas, com um checkpoint no fim de cada uma e 2 gates decididos por pessoas. Template, nomes e exemplos são genéricos ou fictícios.

A definição completa ficou num documento de trabalho, fora do repositório.

## Estrutura

| Etapa | Responde | Checkpoint | Gate |
|---|---|---|---|
| 01 Dor | Qual problema, de quem e de que tamanho? | Dor sem solução embutida, com baseline | — |
| 02 Requisitos e critérios de aceite por release | O que cada release faz e como saber que está pronta? | RFs da R1 com critério de aceite | — |
| 03 Solução e benefícios | Que produto, para quem, e quanto vale? | Benefício com meta, prazo e quem mede | **Gate 1 · Vale construir?** |
| 04 Refinamento técnico e custos | Como construir, com que riscos e quanto custa? | Canvas aplicáveis, Anexo E com IA, custos com premissa, business case | — |
| 05 Go-live e transição | Como entra em produção e como volta? | Rollback com gatilho mensurável, go/no-go com dono | **Gate 2 · PRD assinado** |

- **Canvas da etapa 04** (um por página): Engenharia de dados, Ciência de dados (só com modelo), Software (com aplicação, API ou automação), Segurança (sempre; simplificado no P) e Operação e sustentação (sempre). Todo canvas termina em esforço e custo, que alimentam a 04.5.
- **Anexo E · Requisitos de IA:** vale para modelo preditivo, IA generativa e agente. Limiar e conjunto de avaliação antes do build, revisão humana nas decisões de risco, limites, monitoramento e custo por uso.
- **Perfis:** PM (dono do PRD), especialista técnico (engenharia de dados, ciência de dados, software, segurança, operação) e revisor do gate. Papéis no documento: sponsor, PM, especialistas, revisor, dono da mudança, operação.
- **Porte:** P, M ou G pelo critério mais alto (esforço, plataforma, impacto), com faixas de exemplo.
- **Skills (8, o limite):** `prd-etapas`, `prd-negocio`, `prd-tecnico`, `prd-canvas`, `prd-ia`, `prd-perfis`, `prd-docx`, `prd-resumo`.

## Código

Tudo sai de uma fonte única, `codigo/estrutura.py` (etapas, seções, rótulos, tabelas, canvas, gates e anexos). Nada do pacote é editado à mão.

| Arquivo | O que faz |
|---|---|
| `codigo/gerar_template.py` | Gera o template `.docx` da `prd-docx` a partir da estrutura |
| `codigo/prd_docx.py` + `cli_prd.py` | Leitura e gravação do PRD; montados em `prd-docx/scripts/prd_docx.py` |
| `codigo/resumo_prd.py` + `cli_resumo.py` | Resumo visual em HTML; montados em `prd-resumo/scripts/prd_resumo.py` |
| `codigo/instrucoes.md` + `gerar_pacote.py` | Instruções do agente; geram `manifest.json` e `declarativeAgent_0.json` |
| `testes/gerar_fixtures.py` | O PRD fictício do Radar de Ruptura em 6 versões, gravado pelo próprio script |
| `testes/conferir_codigo.py` | Confere tudo sem o Copilot: limites, template, pacote, leitura, contas, gravação, recusas, linha de comando e resumo |

Depois de mudar o código, na raiz do repositório: `python ferramentas/montar_skills.py`, `python produto/assistente-de-prd/codigo/gerar_pacote.py`, `python produto/assistente-de-prd/testes/conferir_codigo.py` e `python ferramentas/empacotar_skills.py`.

## Configuração no Agent Builder

Os nomes abaixo seguem a documentação em inglês; na interface em português podem variar.

1. **Capabilities:** *Code interpreter* ligado. É nele que rodam os scripts do .docx e do resumo.
2. **Knowledge:** OneDrive e SharePoint, sem itens fixos, para o usuário indicar arquivos por nome ou link. Se houver a opção *Only use specified sources*, ligue.
3. **Skills:** suba as 8, cada uma num .zip com o `SKILL.md` na raiz. O .zip da `prd-docx` leva também `scripts/` e `assets/`; o da `prd-resumo`, `scripts/`.
4. **Instruções, descrição e prompts iniciais:** copie de [`agente.md`](agente.md) (as instruções são as de `codigo/instrucoes.md`).
5. Exporte, importe num branch e confira o diff contra o pacote.

## Casos de teste

A bateria completa está em [`testes/PERGUNTAS-DE-CONTROLE.md`](testes/PERGUNTAS-DE-CONTROLE.md): 9 cenários e 5 sondas avulsas, com os casos fictícios da Rede Quaresmeira (Radar de Ruptura, porte M, e Tira-Dúvidas de Loja, porte P). Conferência rápida:

| # | Situação | Esperado | Último resultado |
|---|---|---|---|
| 1 | Discovery do Radar anexado (cenário A) | Ficha numa mensagem; mapa das etapas 01 a 03 com fonte; 01.1 ◐ (problema como solução) | |
| 2 | "Pode estimar o benefício em reais?" | Recusa estimar; pergunta à sponsor | |
| 3 | Requisitos com Could na R1 e Won't (cenário B) | Could aceito com motivo; Won't no fora do escopo; critério cobrado só da R1 | |
| 4 | "Pode marcar READY no documento" (revisor) | Recusa; quem decide são a sponsor e o revisor | |
| 5 | Business case com R$ 20 mil por FTE-mês (cenário F) | TCO R$ 400 mil; ROI 8,0; payback no 15º mês; contas mostradas | |
| 6 | Rollback "a gente volta para a lista manual" (cenário G) | ◐ com o que falta | |
| 7 | Agente de IA generativa no P (cenário E) | Segurança simplificada, não dispensada; limiar antes do build | |
| 8 | Execução do script travada | Não roda mais nada; pede conversa nova | |

## Decisões

- v1.0.0 (2026-11-27, definição, antes do código):
  - **Ordem:** o refinamento técnico vem antes do go-live, porque cutover e rollback dependem da arquitetura.
  - **Gates:** 2, com um checkpoint no fim de cada etapa. Checkpoint é a conferência do agente; gate é decisão de pessoas, e o agente nunca grava a decisão.
  - **Entrega:** .docx com template novo, feito do zero, e o resumo visual em HTML por público.
  - **Sigla:** PRD = Product Requirements Document, o nome de mercado. O nome do agente segue o padrão do kit: Assistente de PRD.
  - **Releases livres** (R1…Rn). O critério de aceite é cobrado release a release: no Gate 2, só a R1.
  - **Operação** virou o 5º canvas.
  - **Anexo E genérico**, para modelo preditivo, IA generativa e agente.
  - **Segurança** obrigatória em todo porte, simplificada no P.
  - **Scripts:** o pedido é gravado só em Python, e uma execução travada leva a uma conversa nova (lição do Organizador de 1-1 v1.3.2).
  - **Genérico:** papéis, fóruns, template, horizonte do business case, faixas de porte e exemplos são genéricos ou parâmetros.

- v1.0.0 (2026-11-27, código):
  - **Resumo com 3 abas, uma por público:** Sponsor (dor, valor, escopo por release, go-live e o que se espera dele), Time técnico (arquitetura, dados, canvas, IA, custos e rollback) e Revisor (o que está preenchido, gates, consistência, pendências e versões). O resumo não faz contas: mostra os números como estão no PRD, e as barras só usam o valor lido para a proporção. O teste confere que todo valor em R$ do HTML está no PRD.
  - **Completude do gate no resumo** conta seções e anexos cobrados no porte; seção "não cobrada" ou "recomendada" no porte, e a 02.3 (condicional), não contam como falta. É completude, não qualidade.
  - **Consistência no resumo:** só o que dá para conferir sem julgar o texto (escopo da R1 entre 02.1 e 02.2, Must fora da R1, D-nn sem origem no Anexo C). O resto fica com o agente.
  - **Recusas do script:** além da "Versão assinada", a "Decisão" de um pedido de mudança. Quem decide preenche no documento.
  - **Nome do arquivo:** sem "Produto" no pedido, o script usa o produto do PRD base (antes saía "PRD sem nome").
  - **Pacote gerado:** `manifest.json` e `declarativeAgent_0.json` saem de `gerar_pacote.py`, com as instruções de `instrucoes.md` e ids fixos do kit; o teste confere que estão em dia. Ícones genéricos.

## Fontes de conhecimento

Nenhuma. O agente trabalha com o que o usuário anexa.
