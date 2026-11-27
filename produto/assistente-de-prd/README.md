# Assistente de PRD

Conduz o **PRD** (Product Requirements Document) de um produto de dados ou de IA, novo ou em evolução, da dor ao go-live. Lê o material que você já tem, preenche o que encontrar, avalia cada seção por um critério de qualidade e mostra o que falta, com as perguntas agrupadas por quem responde. Devolve o PRD em .docx a qualquer momento e um resumo visual por público.

## O que ele faz

1. **Organiza o PRD em 5 etapas**, com um checkpoint no fim de cada uma e 2 gates decididos por pessoas:

   | Etapa | Responde | Depois dela |
   |---|---|---|
   | 01 Dor | Qual problema, de quem e de que tamanho? | |
   | 02 Requisitos e critérios de aceite por release | O que cada release faz e como saber que está pronta? | |
   | 03 Solução e benefícios | Que produto, para quem, e quanto vale? | **Gate 1 · Vale construir?** |
   | 04 Refinamento técnico e custos | Como construir, com que riscos e quanto custa? | |
   | 05 Go-live e transição | Como entra em produção e como volta se der errado? | **Gate 2 · PRD assinado** |

2. **Usa um canvas por especialidade** no refinamento técnico: engenharia de dados, ciência de dados, software, segurança e operação. Todo canvas termina em esforço e custo, que alimentam os custos e o business case.
3. **Trata IA como requisito**, num anexo próprio para modelo preditivo, IA generativa e agente: limiar e conjunto de avaliação antes de construir, revisão humana nas decisões de risco, limites e custo por uso.
4. **Muda a conversa pelo perfil:** o PM, dono do PRD; o especialista técnico, que faz o refinamento; e o revisor do gate, que recebe um parecer com o checklist e as inconsistências entre seções.
5. **Cobra pelo porte** (P, M ou G): o que não se aplica não é cobrado; segurança e operação valem sempre, simplificadas no P.
6. **Não inventa:** número, nome, data e meta só vêm do seu material ou de você. Sem fonte, o campo fica em aberto e vira pergunta. Ele também não decide gate nem marca a versão assinada.

## Como é uma conversa (ilustrativo)

> **Você:** Sou PM e quero começar o PRD do Radar de Ruptura. *(anexa o discovery)*
>
> **Assistente:** `Etapa 01/05 Dor · Radar de Ruptura · Perfil: PM · Porte M · Alvo: Gate 1 · Checkpoint 01: 2 de 4 seções ✓`
> *(a ficha, para você confirmar, e depois o mapa do que já está no discovery)*
> O problema está escrito como solução ("precisamos de um painel"). Proponho: "Os 38 gerentes levam 3 h por semana para montar a lista de faltas e descobrem a ruptura pelo cliente." Confirma?
>
> **Você:** confirmo. Pode estimar o benefício em reais?
>
> **Assistente:** Não estimo: o valor vem da sponsor. Pergunta para a Marta: qual indicador prova o benefício, quanto ele vale hoje, qual a meta e até quando?

## Como usar

### No Microsoft 365 Copilot

Você precisa do Microsoft 365 Copilot com o **Agent Builder** e a área de **Skills** na aba Configurar. Os nomes dos botões podem variar um pouco entre versões.

1. **Baixe as 8 skills** da pasta [`skills-zip/`](skills-zip/). Clique em cada arquivo e depois no botão de download.
2. No Copilot, crie um agente novo e vá para a aba **Configurar**.
3. **Nome:** `Assistente de PRD`.
4. **Descrição:** copie de [`agente.md`](agente.md), seção *Descrição*.
5. **Instruções:** em [`agente.md`](agente.md), copie o bloco da seção *Instruções* (ícone de copiar no canto do bloco) e cole.
6. **Conhecimento:** OneDrive e SharePoint, sem arquivos fixos, para você indicar documentos por nome ou link.
7. **Capacidades:** ligue o **interpretador de código**. É ele que roda os scripts que leem e gravam o .docx e geram o resumo.
8. **Skills:** suba os 8 .zip.
9. Se aparecer a opção de usar só as fontes configuradas, ligue. Se aparecer a de modo de resposta, escolha a que pensa mais antes de responder (*Think deeper*).
10. **Prompts iniciais** (opcional): copie da tabela no fim do [`agente.md`](agente.md).
11. Salve e teste com os arquivos fictícios de [`testes/fixtures/`](testes/fixtures/): comece pelo `discovery-radar.docx`.

O Copilot não lembra de uma conversa para a outra: para continuar um PRD, anexe a última versão do .docx.

### No Claude

1. Baixe os 8 .zip de [`skills-zip/`](skills-zip/) e suba cada um como skill, na área de Skills das configurações do Claude.
2. Crie um projeto e cole nas instruções do projeto o bloco *Instruções* do [`agente.md`](agente.md).
3. Anexe o material e diga seu perfil. Os scripts foram feitos para o interpretador do Copilot; no Claude, ainda não foram testados.

### Em outros assistentes

Dá para colar as instruções e anexar os `SKILL.md` como arquivos. O método funciona; o .docx e o resumo dependem dos scripts das skills `prd-docx` e `prd-resumo`. Sem eles, peça o conteúdo por seção, pronto para colar.

## Comandos durante a conversa

- **"mapa"** e **"lacunas"**: o que está preenchido, com o status, e o que falta, em ordem.
- **"seção <ID>"**: o conteúdo atual de uma seção, sem reescrever.
- **"perguntas para <papel ou nome>"**: as perguntas em aberto, prontas para enviar.
- **"checkpoint"**, **"checar gate 1"**, **"checar gate 2"**, **"parecer"** e **"consistência"**.
- **"canvas <especialidade>"**, **"custos"** e **"business case"**.
- **"perfil <nome>"** e **"preencher tudo"** (rascunha tudo o que o material permite e marca o que validar com quem).
- **"gerar documento"** e **"resumo"**.

## Limites conhecidos

- O agente avalia a qualidade pelo critério de cada seção, mas quem decide os gates são o sponsor e o revisor, no documento.
- O resumo visual mede completude, e não qualidade. As checagens de consistência dele são só as que não dependem de julgar o texto.
- O .docx é lido e gravado no template que vem com a skill. Um PRD em outro formato entra como material de apoio, e o conteúdo é passado para o template.
- As faixas de porte e o horizonte do business case são um ponto de partida: diga ao agente quais a sua empresa usa.

## Status

| Versão | Situação |
|---|---|
| 1.0.0 | Proposta. O código passa na conferência automática ([`testes/conferir_codigo.py`](testes/conferir_codigo.py)) com um PRD fictício em 6 versões. A bateria de perguntas de controle em conversa ainda não rodou |

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| [`agente.md`](agente.md) | Instruções, descrição e prompts iniciais, prontos para copiar |
| [`skills-zip/`](skills-zip/) | As 8 skills empacotadas, prontas para subir |
| [`pacote/`](pacote/) | O agente como o Copilot exporta |
| [`codigo/`](codigo/) | A estrutura do PRD, o gerador do template e o código dos scripts, separado por módulo. Os scripts das skills são montados a partir daqui |
| [`NOTAS.md`](NOTAS.md) | Objetivo, desenho e decisões |
| [`testes/`](testes/) | Perguntas de controle, o PRD fictício do Radar de Ruptura em 6 versões com o material de apoio, e a conferência automática |

Para rodar a conferência automática, com Python 3 e `python-docx` instalados, na pasta principal do repositório:

```
python produto/assistente-de-prd/testes/conferir_codigo.py
```
