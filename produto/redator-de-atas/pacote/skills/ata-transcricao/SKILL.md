---
name: ata-transcricao
description: 'Script que lê a reunião anexada (transcrição do Teams em .docx ou .vtt, texto ou notas em .txt e .md, material de apoio em .docx e .pptx), numera as falas, lista quem falou com o nome em ordem natural, separa convidados de presentes, divide a leitura em blocos, busca os trechos que sustentam um item e confere a ata contra a fonte (participantes, responsáveis, números, datas, seções e formato). Use sempre que houver arquivo anexado, antes de escrever, no comando evidência e antes de mostrar qualquer versão da ata.'
---

## Regra

Toda transcrição, nota ou material anexado é lido **só** pelo script `scripts/atas_transcricao.py` desta skill. Não leia o anexo por outro caminho, não escreva código próprio para ler arquivos e não refaça as contas do script: falantes, falas, blocos e conferência são os que ele imprime.

**Pergunta e recusa não são falha.** "NADA FOI LIDO", "NADA FOI CONFERIDO" e "NADA FOI FEITO" querem dizer que o script rodou e recusou: resolva o que ele lista. Falha é só erro de execução (um traceback ou o script não encontrado): mostre o erro exato num bloco de código e tente o plano B (§Como rodar). Na etapa seguinte, rode o script de novo: **nunca dê o script por indisponível para o resto da conversa**, nem diga que ele falhou sem mostrar o erro. Se o script falhar também pelo plano B, diga isso em uma linha e pergunte se o usuário quer seguir com a sua leitura do anexo. Nesse caso, a linha de status diz "Cobertura: leitura sem o script, pode estar incompleta", e a conferência de participantes, responsáveis e números fica com você.

## Como rodar

1. No interpretador de código, grave o pedido em JSON em `/mnt/data/ata_pedido.json`:

~~~python
import json
pedido = {"acao": "ler", "arquivos": ["Refinamento Jatobá.docx"]}
json.dump(pedido, open("/mnt/data/ata_pedido.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/atas_transcricao.py` desta skill. Ele lê o pedido, trabalha em `/mnt/data`, onde ficam os anexos, e imprime o resultado.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/ata-transcricao/scripts/atas_transcricao.py", recursive=True)[0], run_name="__main__")
~~~

Cite os arquivos pelo nome, como aparecem nos anexos. Arquivo "não encontrado" quer dizer que ele não foi anexado nesta conversa: peça para anexar. Arquivo só citado, ou achado na busca do Teams, não chega ao script.

## Ler

~~~json
{"acao": "ler", "arquivos": ["Refinamento Jatobá.docx", "Deck Onda 2.pptx"],
 "convidados": ["Gustavo Lima", "Helena Costa"], "data_reuniao": "2026-11-10"}
~~~

Mande todos os anexos da reunião numa leitura só. `convidados` é opcional: a lista do convite (do calendário ou do que o usuário colar), para o script dizer quem foi convidado e não falou. `data_reuniao` só quando o arquivo não traz a data; ela converte "sexta" e "amanhã" em data na conferência.

O script imprime:
- **Cabeçalho:** título, data e duração do arquivo, número de falas, de falantes e de blocos.
- **Por arquivo:** o tipo. Transcrição tem falas com falante; notas são texto sem falante; apoio é deck ou documento. Também diz quantas marcas automáticas ou trechos em HTML foram removidos.
- **Falantes:** nome em ordem natural, como aparece no arquivo, falas, palavras, primeira e última fala, e a marca:
  - `externo`: convidado de fora (ex.: "(Convidado)"); é participante, sem o sufixo;
  - `sala`: dispositivo de sala, não é pessoa. Leia as falas: quem se identifica nelas ("aqui é o Marcos, de Vendas") é participante pela fonte;
  - `não identificado`: "Speaker 1", "Participante 2". Não vira participante.
- **Presentes escritos nas notas** ("Presentes:", "Participantes:"): provam presença, com a área quando escrita.
- **Eventos** ("X iniciou a transcrição"): provam presença.
- **Convidados sem fala nem presença escrita:** convite não é presença. Não entram na ata.
- **Próximo passo:** quantos blocos ler. O resultado completo fica em `/mnt/data/ata_leitura.json`.

## Trecho

~~~json
{"acao": "trecho", "bloco": 1}
~~~

Imprime um bloco, uma linha por item: `T012 00:09:12 Ana Souza: texto`. Os IDs são `T` para falas, `N` para linhas de notas e `A` para o material de apoio.

- **Leia todos os blocos, do 1 ao último, antes de escrever a ata.** A ação mais importante muitas vezes está no fim da reunião.
- Cada bloco termina com "Fim do bloco k/n". Se a saída não terminar assim, ela foi cortada: rode `ler` de novo com `"tamanho": 5000` e leia os blocos novos.
- Os IDs servem para você conferir e para o comando evidência. **Nunca entram na ata.**

## Buscar

~~~json
{"acao": "buscar", "termos": ["jurídico", "promotor"], "falante": "Renata", "todos": false}
~~~

Acha as falas que contêm os termos, sem diferença de acento e de maiúsculas, com a fala anterior e a seguinte para dar contexto (`»` marca o acerto). `falante` e `todos` (todos os termos na mesma fala) são opcionais. Use:
- no comando **evidência <item>**: mostre as falas que sustentam o item, com ID, hora e falante;
- antes de registrar um **responsável** ou um **prazo**: confirme quem assumiu e o que foi dito;
- quando um número ou uma regra aparece mais de uma vez: veja se houve correção.

Sem nenhuma fala com os termos, o item não entra na ata como fato.

## Conferir

Grave a ata em Markdown num arquivo e confira:

~~~python
ata = r"""# Ata de Reunião | ...
"""
open("/mnt/data/ata_rascunho.md", "w", encoding="utf-8").write(ata)
pedido = {"acao": "conferir", "tipo": "Refinamento", "ata_arquivo": "ata_rascunho.md",
          "presentes": [{"nome": "Marcos", "turno": "T007"}], "confirmados": [], "extras": "", "secoes_pedidas": []}
~~~

- `tipo`: Homologação, Discovery, Refinamento, Alinhamento ou Outro.
- `presentes`: quem está presente pela fonte sem ter falado com o próprio nome, com o ID da fala que o mostra (ex.: alguém que se identifica na fala da sala). O script confere se o nome está na fala.
- `confirmados`: quem o usuário disse que estava presente.
- `extras`: números, datas e nomes que o usuário disse na conversa, para não serem apontados como sem fonte.
- `secoes_pedidas`: seções que o usuário pediu e que o tipo não traz (ex.: "Resumo Executivo").

O script imprime os pontos em três grupos:
- **Corrija pela fonte antes de mostrar.** Exemplos: participante sem prova de presença; quem falou e ficou de fora; responsável que não aparece na fonte; número ou data que não está na fonte; valor corrigido na reunião; seção fora do tipo; coluna Prazo vazia; título; HTML, `[Event]` ou ID de fala na ata. Corrija e rode `conferir` de novo, até não sobrar nada neste grupo. Se a correção depender do usuário, leve o ponto à conferência.
- **Leve à conferência do usuário.** Exemplos: convidados sem fala, dispositivo de sala, ação sem responsável, responsável que não participou, prazo convertido de dia da semana. Vão para a Conferência, no máximo 6 pontos, juntando os do mesmo tipo numa linha.
- **Para saber.** Ex.: ata longa. Use para enxugar; não mostre ao usuário.

Sem leitura nesta conversa (ata feita pela busca do Teams ou por texto colado), o script confere só título, seções e formato, e diz isso. Nesse caso, a conferência de participantes, responsáveis e números fica com você, pelas regras da `ata-fidelidade`.

O que o script **não** confere, e fica com você: se uma decisão foi mesmo uma decisão, se o responsável assumiu a ação ou só comentou, se um tema é lateral, e a área de cada pessoa.
