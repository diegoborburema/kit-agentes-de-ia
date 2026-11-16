---
name: pauta-1-1-pptx
description: 'Lê a pauta anterior de um arquivo .pptx (inclusive as anotações e os combinados feitos no 1-1) e gera o arquivo .pptx da pauta de 1-1 no layout padrão, para cima (com Tipo e Status) ou para baixo (com Para puxar e Anotações). Use quando o usuário anexar a pauta anterior em PowerPoint e na etapa de entrega.'
---

## Regra

Todo .pptx é lido e gerado **só** pelo script `scripts/pauta_1_1_pptx.py` desta skill. Não escreva código de layout, não use outra skill de apresentações e não desenhe a tabela por conta própria. Se o script falhar, mostre o erro em uma linha e entregue só a tabela.

## Como rodar

1. No interpretador de código **Python**, grave o pedido em JSON em `/mnt/data/pauta_pedido.json` com `json.dump`, como no bloco abaixo. **Nunca grave o pedido pelo terminal** (`bash`, `cat`, `echo`, heredoc `<<`): se o fechamento do heredoc falhar, a execução fica parada esperando para sempre.

~~~python
import json
pedido = {"acao": "ler", "arquivos": ["1-1 Ana 2026-10-29.pptx"]}
json.dump(pedido, open("/mnt/data/pauta_pedido.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/pauta_1_1_pptx.py` desta skill. Ele lê o pedido, trabalha em `/mnt/data`, onde ficam os anexos, e imprime o resultado.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/pauta-1-1-pptx/scripts/pauta_1_1_pptx.py", recursive=True)[0], run_name="__main__")
~~~

Se uma execução não responder em 2 minutos, ela travou: na resposta seguinte, avise o usuário em uma linha e grave o pedido de novo pelo bloco Python.

Cite os arquivos pelo nome, como aparecem nos anexos. Arquivo "não encontrado" quer dizer que ele não foi anexado nesta conversa: peça para anexar.

## 1. Ler a pauta anterior

Pedido: `{"acao": "ler", "arquivos": ["1-1 Ana 2026-10-29.pptx"]}`. O script imprime o título, a semana, a legenda, as linhas da tabela e os combinados, e grava tudo em `/mnt/data/pauta_leitura.json`. Cada linha é um dicionário com `categoria`, `tema`, `texto` (atualização ou bullets para puxar), `tipo`, `status` (`verde`, `amarelo`, `vermelho`, "–" ou vazio) e `anotacoes`. As colunas são reconhecidas pelo cabeçalho, então o script lê os dois layouts. Hiperlinks saem como `texto (endereço)`. Se o arquivo tiver várias semanas, o script usa a mais recente pela data do subtítulo, juntando os slides dela.

- Para descobrir as prioridades, use o grupo "3 PRIORIDADES" da legenda.
- Seção de cada linha: categoria igual a uma prioridade → P1, P2 ou P3, na ordem da legenda; "Pessoas" → PESSOAS; nome de um tema da semana → TEMA; "Temas do …" → LIDERADO; o resto → PROJETOS.
- `anotacoes` é o que o usuário escreveu no 1-1: a última atualização do liderado. Use como fonte `[Anotações dd/mm]`.
- Cada combinado tem `quem`, `oque`, `ate` e `feito`. `feito` é o que o usuário marcou na coluna ✓: preenchido = feito; vazio = em aberto. Pautas sem o bloco devolvem a lista vazia.
- Linhas em branco não são devolvidas. Se não houver tabela, o script avisa "SEM TABELA" e imprime o texto das formas de cima para baixo: monte as linhas a partir dele e peça ao usuário para confirmar.

## 2. Gerar a pauta

Pedido: `{"acao": "gerar", "saida": "1-1 <Pessoa> <aaaa-mm-dd>.pptx", "pauta": {...}}`, com `pauta` preenchida a partir da tabela final aprovada. O script põe as seções na ordem fixa, faz a fonte caber e, se a pauta não couber legível num slide, continua num 2º slide ("1/2", "2/2"), quebrando entre seções.

- `direcao`: `"cima"` (gestor) ou `"baixo"` (liderado).
- `pessoa`: o primeiro nome ou o apelido que o usuário usa, nunca o formato do diretório.
- `secao`: `P1`, `P2`, `P3` (na ordem das prioridades), `PESSOAS`, `PROJETOS`, `TEMA` ou `LIDERADO` (só para baixo).
- Para cima, cada linha leva `atualizacao`, `tipo` (Info, Ajuda, Escalation ou Decisão) e `status` (`verde`, `amarelo`, `vermelho` ou `""`, que sai "–").
- Para baixo, cada linha leva `puxar`: lista de 1 ou 2 bullets. A coluna Anotações sai vazia. Inclua as 2 linhas em branco de Temas do `<nome>` (`tema` vazio e `puxar` vazio).
- `link` (opcional, em qualquer linha): `{"texto": "nome do arquivo", "url": "endereço"}`. Vira um hiperlink na célula de texto.
- `tema_semana`: o nome do tema, ou `None` na semana livre sem tema.
- `combinados`: os combinados em aberto, cada um com `quem`, `oque` e `ate`. O bloco sai depois da tabela, com 3 linhas em branco para os combinados do 1-1; fica no último slide se couber, senão num slide próprio. Sem combinados em aberto, passe a lista vazia: o bloco sai só com as linhas em branco.
- `notas`: vão para as notas do 1º slide. Para baixo, comece com "Contexto" e uma linha por tema (`- <Tema>: <contexto> <fonte>`); nos dois layouts, termine com "Perguntas para levar" e as 3 perguntas, uma por linha.
- Nome do arquivo (`saida`): `1-1 <Pessoa> <aaaa-mm-dd>.pptx`, com a data do 1-1.

Exemplo do pedido de geração (fictício, para baixo):

~~~python
pauta = {  # exemplo fictício, para baixo
    "direcao": "baixo", "usuario": "Lucas", "pessoa": "Beto", "semana": "02–06/11/2026",
    "prioridades": ["Tarumã", "Quimera-7", "Ipê-Roxo"], "tema_semana": "Metas & PDP",
    "linhas": [
        {"secao": "P1", "categoria": "Tarumã", "tema": "Módulo Araçá",
         "puxar": ["Escalou a dependência com a Pitanga?", "Escopo da onda 2 validado"]},
        {"secao": "PESSOAS", "categoria": "Pessoas", "tema": "Plano 2027", "puxar": ["Preencher até 13/11"],
         "link": {"texto": "Planejamento_2027.xlsx", "url": "https://exemplo/planejamento.xlsx"}},
        # ... uma entrada por linha da tabela final
        {"secao": "LIDERADO", "categoria": "Temas do Beto", "tema": "", "puxar": []},
        {"secao": "LIDERADO", "categoria": "Temas do Beto", "tema": "", "puxar": []},
    ],
    "combinados": [{"quem": "Beto", "oque": "Mandar o cronograma revisado (desde 29/10)", "ate": "05/11"}],
    "notas": ["Contexto",
              "- Módulo Araçá: escopo fechado; dependência sem data. Última temperatura dele: 🟡 [Anotações 30/10]",
              "", "Perguntas para levar",
              "1. Como você avalia cada meta hoje: no plano, em atenção ou em risco?",
              "2. O que está travando a meta mais difícil, e o que você precisa de mim?",
              "3. Que ação do PDP você fez desde a última conversa, e o que aprendeu?"],
}
pedido = {"acao": "gerar", "saida": "1-1 Beto 2026-11-05.pptx", "pauta": pauta}
~~~

## 3. Conferir antes de entregar

- O script relê o arquivo gerado e imprime a **CONFERÊNCIA DO ARQUIVO**: slides, linhas (iguais às pedidas e na ordem), combinados em aberto, legenda e as perguntas para levar nas notas. Descreva a entrega só com o que está nela.
- "ATENÇÃO" na conferência: corrija o pedido e gere de novo.
- Se a pauta passar de 2 slides, ela está longa demais: reveja o foco antes de entregar.
- "NADA FOI GERADO": diga em uma linha o que aconteceu. A tabela final continua valendo.
- Entregue o link de download.
