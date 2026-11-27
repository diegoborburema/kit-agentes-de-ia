---
name: prd-docx
description: 'Script que lê um PRD em .docx (o que está preenchido em cada seção, canvas, checkpoint, gate e anexo) e grava o PRD atualizado (painel, pessoas, checkpoints, campos, linhas de tabela, canvas, pendências, versão e pedidos de mudança), a partir do PRD anexado ou do template que vem com a skill. Use quando o usuário anexar um PRD e em toda entrega do documento.'
---

## Regra

Todo .docx do PRD é lido e gravado **só** pelo script `scripts/prd_docx.py` desta skill. Não escreva código de .docx nem use outra skill de documentos. Se o script falhar, mostre o erro em uma linha e entregue o conteúdo aprovado por seção, pronto para colar.

Material de apoio (discovery, arquitetura, atas) é lido normalmente, sem o script.

## Como rodar

1. No interpretador de código **Python**, grave o pedido em JSON em `/mnt/data/prd_pedido.json` com `json.dump`, como no bloco abaixo. **Nunca grave o pedido pelo terminal** (`bash`, `cat`, `echo`, heredoc `<<`): se o fechamento do heredoc falhar, a execução fica parada esperando.

~~~python
import json
pedido = {"acao": "ler", "arquivo": "PRD Radar de Ruptura v0.5.docx"}
json.dump(pedido, open("/mnt/data/prd_pedido.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/prd_docx.py` desta skill. Ele lê o pedido, trabalha em `/mnt/data`, onde ficam os anexos, e imprime o resultado.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/prd-docx/scripts/prd_docx.py", recursive=True)[0], run_name="__main__")
~~~

- **Se uma execução não responder em 2 minutos, não rode mais nada nesta conversa**: o ambiente travou, e outra execução também vai travar. Diga em uma linha que é preciso abrir uma conversa nova, anexar o PRD de novo e repetir o pedido; entregue, nesta mesma resposta, o conteúdo aprovado por seção, pronto para colar.
- Cite os arquivos pelo nome, como aparecem nos anexos. Arquivo "não encontrado" quer dizer que ele não foi anexado nesta conversa: peça para anexar.

## Ler

`{"acao": "ler", "arquivo": "<nome do .docx>"}`

- O script imprime, etapa por etapa, só o que tem conteúdo: painel, checkpoints, decisões de gate, pessoas, cada seção (campos e linhas de tabela) ou "VAZIA", cada canvas (aplicável, motivo e blocos) e os anexos. A leitura completa fica em `/mnt/data/prd_leitura.json`.
- Vazio é o que tem só a orientação em cinza ou caixas ☐ sem marcar. A orientação em cinza nunca é conteúdo.
- A leitura mostra o que existe, não se está bom. A qualidade é dada pelo "bom quando" (`prd-negocio`, `prd-tecnico`, `prd-canvas`, `prd-ia`).
- "PRD ASSINADO": siga a regra de mudança de `prd-etapas`.
- Erro de leitura num .docx que não é deste template: leia o arquivo como material de apoio e proponha passar o conteúdo para o template.

## Gravar

Grave **só o que o usuário confirmou na conversa**, sem fontes, status nem `[suposição]`. Um pedido por entrega.

~~~python
pedido = {
  "acao": "gravar",
  "base": "PRD Radar de Ruptura v0.5.docx",
  "painel": {"Etapa atual": "03"},
  "checkpoints": {"02": {"situacao": "Cumprido"}},
  "pessoas": {"Revisor do gate": {"Nome": "Rita Moura", "Área": "Escritório de produto"}},
  "campos": {"03.1": {"O que a solução faz": "Uma lista diária…", "Tipo de produto": ["Dashboard", "Automação"]},
             "E": {"Tipo de IA": "Modelo preditivo", "Limiar para ir à produção": "Recall de 80%…"}},
  "linhas": {"02.1/rfs": [{"ID": "RF-03", "Critério de aceite": "Pronto quando…"}],
             "04.5/custos": [{"Categoria": "Nuvem – processamento", "Build": "R$ 0", "Run no ano 1": "R$ 36 mil"}]},
  "canvas": {"eng": {"aplicavel": "Sim", "blocos": {"Fontes e acesso": "D-01 no ERP…"}},
             "sw": {"aplicavel": "Não", "motivo": "Sai no portal de relatórios que já existe"}},
  "pendencias": [{"ID": "P-03", "Tipo": "Pendência", "Descrição": "Custo por FTE-mês sem fonte",
                  "Origem": "04.5", "Gate": "2", "Bloqueante": "Sim", "Dono": "Caio Rezende", "Prazo": "28/11"}],
  "versao": {"numero": "0.6", "o_que_mudou": "03.1, RF-03, 04.5 e canvas", "autor": "Caio Rezende"}
}
~~~

- **base:** o PRD em andamento que o usuário anexou. Numa **demanda nova sem .docx**, não mande `base`: o script parte do template que vem com a skill. Para **continuar um PRD que já existe**, o arquivo é obrigatório: peça o upload e não comece outro.
- **painel:** rótulos do painel (`prd-negocio`). O script atualiza "Versão vigente" pela `versao`.
- **checkpoints:** `{"<etapa 01 a 05>": {"situacao": "Cumprido" ou "Cumprido com pendências", "data": "dd/mm/aaaa"}}`. Sem data, vale a de hoje.
- **pessoas:** chave = papel (Sponsor, PM, Engenharia de dados, Ciência de dados, Software, Segurança, Operação, Revisor do gate, Dono da mudança); valores "Nome" e "Área".
- **campos:** `{"<seção>": {"<rótulo>": "<texto>"}}`. Seções 01.1 a 05.7 e o Anexo E (`"E"`). O rótulo é o nome inteiro, como no template; acentos e maiúsculas não importam. Caixas ☐: o texto da opção, ou uma lista para marcar mais de uma.
- **linhas:** `{"<seção>/<tabela>": [{"<coluna>": "<texto>"}]}`, com os nomes de tabela e colunas de `prd-negocio` e `prd-tecnico`; anexos como `"C/origem"`, `"D/capacity"`, `"D/consolidacao"`. A **1ª coluna é a chave**: se uma linha com esse valor já existe, ela é atualizada (só as colunas enviadas); se não, entra na primeira linha vazia ou numa nova, antes da linha TOTAL. Mande só as colunas que mudaram. **O TOTAL não é recalculado**: faça a conta, mostre na conversa e mande a linha TOTAL também.
- **canvas:** `{"eng" | "cie" | "sw" | "seg" | "op": {"aplicavel": "Sim" ou "Não", "motivo": "…", "blocos": {"<título do bloco>": "<texto>"}}}`, com os títulos de `prd-canvas`.
- **pendencias** (Anexo A): colunas ID, Tipo, Descrição, Origem, Gate, Bloqueante, Dono, Prazo. Mande o ID (P-nn, R-nn, C-nn): o script não numera.
- **mudancas** (Anexo B, depois do PRD assinado): colunas ID (M-nn), Data, Pedido, Impacto. Sem "Decisão".
- **versao:** `numero` (a seguinte à vigente: 0.5 → 0.6), `o_que_mudou` (seções e IDs) e `autor`. Entra no histórico de versões com a data de hoje.
- `"\n"` quebra a linha dentro da célula. **Modo completo** (`prd-perfis`): o conteúdo de outro papel entra com ` [validar: <papel>]` no fim do texto.
- O arquivo sai como `PRD <produto> v<versão>.docx` em `/mnt/data`.

## Recusas

O script valida o pedido inteiro antes de gravar. Qualquer erro imprime "NADA FOI GRAVADO" e o motivo:
- seção, rótulo, tabela, coluna, opção, canvas ou bloco que não existe: a mensagem lista os que existem. Corrija com o equivalente e rode de novo;
- "Versão assinada" no painel, ou a "Decisão" de um pedido de mudança: diga em uma linha que quem preenche é quem assina ou decide, no documento;
- conteúdo num **PRD assinado**: só `mudancas` são aceitas (e `versao`, se o usuário pedir).

Decisões e checklists dos gates não são graváveis por nenhum pedido: quem decide marca no documento.

## Conferir antes de entregar

Depois de gravar, o script relê o arquivo e imprime a **CONFERÊNCIA DO ARQUIVO**: o que foi gravado, as seções com conteúdo e as vazias, os canvas com conteúdo, a versão vigente e as decisões de gate (que devem continuar como estavam). Descreva a entrega **só com o que a conferência mostra**. Entregue o link de download e diga a versão.
