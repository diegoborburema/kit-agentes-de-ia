---
name: prd-resumo
description: 'Script que gera o resumo visual do PRD num arquivo HTML que abre no navegador, com uma aba por público: Sponsor (dor, valor, escopo por release, go-live e o que se espera dele), Time técnico (arquitetura, dados, canvas, IA, custos e rollback) e Revisor (o que está preenchido, gates, consistência, pendências e versões). Use quando pedirem o resumo, uma visão para um público ou material para apresentar o PRD.'
---

## Regra

O resumo é gerado **só** pelo script `scripts/prd_resumo.py` desta skill, a partir do PRD em .docx. Não escreva HTML, não edite o arquivo gerado e não troque o arquivo por um resumo em texto na conversa. O resumo mostra o que está escrito no PRD, sem reescrever e sem fazer contas, e cada bloco cita a seção de origem. Para mudar o que aparece, mude o PRD (`prd-docx`) e gere de novo.

## Quando usar

- O usuário pede "resumo", uma versão do PRD para um público (sponsor, time técnico, revisor), algo visual ou um material para apresentar ou levar ao gate.
- Depois de gravar uma versão nova com `prd-docx`, ofereça uma vez, em uma linha: "Quer o resumo visual desta versão?".
- Precisa do PRD em .docx na conversa: o anexado ou o que acabou de ser gravado. Sem .docx, peça o upload.

## Como rodar

1. No interpretador de código **Python**, grave o pedido com `json.dump`, como abaixo. **Nunca grave pelo terminal** (`bash`, `cat`, `echo`, heredoc `<<`): se o fechamento do heredoc falhar, a execução fica parada esperando.

~~~python
import json
json.dump({"arquivo": "PRD Radar de Ruptura v0.9.docx"}, open("/mnt/data/prd_resumo.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/prd_resumo.py` desta skill. Ele gera `Resumo PRD <produto> v<versão>.html` em `/mnt/data` e imprime um relatório.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/prd-resumo/scripts/prd_resumo.py", recursive=True)[0], run_name="__main__")
~~~

- Sem `arquivo` no pedido, o script usa o PRD mais recente da conversa.
- **Se uma execução não responder em 2 minutos, não rode mais nada nesta conversa**: o ambiente travou. Diga em uma linha que é preciso abrir uma conversa nova, anexar o PRD e pedir o resumo de novo.

## O que dizer ao usuário

No máximo 6 linhas, a partir do relatório do script, sem repetir o conteúdo das abas:

1. O link do arquivo .html, com o nome que o script imprimiu. Abre no navegador, sem internet, e dá para imprimir.
2. As abas: Sponsor, Time técnico e Revisor.
3. Se o relatório trouxer "O PRD se contradiz", repita essas linhas e ofereça corrigir o PRD.
4. A linha do gate ("X de Y seções e anexos cobrados com conteúdo") e até 3 faltas, com o dono. É completude, não qualidade: a qualidade é dada pelo "bom quando" no checkpoint e no gate.
5. "PRD assinado": o que mudar agora entra como pedido de mudança (Anexo B).

## O que cada aba mostra

Para responder dúvidas sobre o arquivo, sem abrir o HTML:

- **No topo** (todas as abas): produto, tipo, porte, versão e horizonte; a trilha das 5 etapas e dos 2 gates, com a situação de cada checkpoint e a decisão de cada gate.
- **Sponsor:** o problema e o tamanho da dor (01.1, 01.3); a solução (03.1); quanto vale: os totais do business case do painel, benefício e custos por ano em barras, como os KPIs são medidos, premissas e sensibilidade (03.3, 04.5, 04.6); o que entra em cada release, com prioridade e critério de aceite de cada RF, e o fora do escopo (02.1, 02.2, 02.6); como entra em produção: forma, convivência, critério para desligar a solução atual, fases e gatilhos de rollback (05.1 ou 03.4, 05.3, 05.5); o que o PRD pede do sponsor: as pendências com o nome dele e as seções vazias que ele preenche (Anexo A).
- **Time técnico:** arquitetura e componentes (04.1); decisões (04.3); do dado ao uso: cada D-nn com origem, acesso, classificação, dados pessoais e dono (02.5 e Anexo C); os 5 canvas, com quantos blocos estão preenchidos, o esforço ou o motivo de não se aplicar (04.2); não funcionais (02.4); requisitos de IA, quando houver (04.4 e Anexo E), com aviso se faltar o limiar; custos (04.5); cutover, contingência e rollback (05.5).
- **Revisor:** o que está preenchido em cada etapa e nos anexos de cada gate, com o dono do que está vazio (seções não cobradas no porte aparecem tracejadas); os gates, com a decisão e o checklist; a consistência que dá para conferir sem julgar o texto (escopo da R1 entre 02.1 e 02.2, Must fora da R1, D-nn sem origem no Anexo C); riscos e pendências, bloqueantes primeiro; versões e pedidos de mudança.

`[validar: …]` aparece como etiqueta laranja. Seção vazia aparece como "Ainda não preenchido no PRD".

## Compartilhar

O arquivo traz o conteúdo do PRD: compartilhe só com quem pode ver o PRD, junto do documento ou na mesma pasta. Se o programa de mensagens ou o repositório de arquivos só baixar o arquivo em vez de abrir, abra o arquivo baixado no navegador.

## Erros

"ERRO (nada foi gerado)": mostre o erro em uma linha. Arquivo "não está" quer dizer que não foi anexado nesta conversa: peça para anexar. Um .docx que não é deste template não gera resumo: diga isso e proponha passar o conteúdo para o template.
