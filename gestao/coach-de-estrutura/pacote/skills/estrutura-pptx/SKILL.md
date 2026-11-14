---
name: estrutura-pptx
description: 'Script do Coach de Estrutura que lê o plano 30-60-90 do Coach de Gestão, e a análise anterior; soma a carga por pessoa e roda as lentes do mapa; e gera o arquivo confidencial da análise, com o mapa, o diagnóstico, a decisão e os testes gravados, inclusive na revisão do teste. Use com todo anexo, depois do mapa e na entrega.'
---

## Regra

Todo anexo é lido, a carga é somada e o arquivo é gerado **só** pelo script `scripts/estrutura_pptx.py` desta skill. Não some % de cabeça, não escreva código de layout e não use outra skill de apresentações.

**Recusa não é falha.** "NADA FOI GERADO" quer dizer que o script rodou e recusou: resolva com o usuário o que ele lista. Falha é só erro de execução (um traceback ou o script não encontrado): mostre o erro exato num bloco de código e tente o plano B (§Como rodar). Na etapa seguinte, rode o script de novo: **nunca dê o script por indisponível para o resto da conversa**, nem diga que ele falhou sem mostrar o erro. Se a geração falhar de verdade, entregue as tabelas e, num bloco de código, o pedido JSON da ação `gerar`, com a linha "Guarde este bloco: numa conversa nova, anexe o plano e o mapa anterior, cole o bloco e peça para gerar com este pedido."

## Como rodar

1. No interpretador de código, grave o pedido em JSON em `/mnt/data/estrutura_pedido.json`:

~~~python
import json
pedido = {"acao": "ler", "arquivos": ["Plano 30-60-90 2026-11-13.pptx"]}
json.dump(pedido, open("/mnt/data/estrutura_pedido.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/estrutura_pptx.py` desta skill. Ele lê o pedido, trabalha em `/mnt/data`, onde ficam os anexos, e imprime o resultado.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/estrutura-pptx/scripts/estrutura_pptx.py", recursive=True)[0], run_name="__main__")
~~~

Cite os arquivos pelo nome, como aparecem nos anexos. Arquivo "não encontrado" quer dizer que ele não foi anexado nesta conversa: peça para anexar.

## Ler

`{"acao": "ler", "arquivos": [...]}`. Mande todos os anexos numa leitura só.
- **Plano do Coach de Gestão (.pptx):** data, ciclo e semana; prioridades com dono e entregáveis; delegações; KPIs com status; movimentos do retrato com dono; os sinais de estrutura do plano.
- **Análise anterior (.pptx deste agente):** o mapa, a carga e as lentes, a decisão, os testes (em teste, atingido ou não) e o histórico.
- O resultado completo fica em `/mnt/data/estrutura_leitura.json`.

## Carga

`{"acao": "carga", "mapa": [...], "restricoes": [...]}`, ou `{"acao": "carga", "partida": "<análise>.pptx"}`.

Imprime, por pessoa, a soma de %, as frentes, a disponibilidade (100% ou a restrição, com a data) e se passa dela; e as lentes: frentes sem dono, frentes com mais de um dono, dono com autonomia baixa e sem apoio na frente, frentes com uma pessoa só. Use estes números.

## Gerar (só depois do "aprovado")

Análise nova:

~~~json
{"acao": "gerar", "estrutura": {
  "data": "2026-11-13", "usuario": "Lucas", "gatilho": "sinal do plano (Ana em 3 frentes); Buriti 🔴",
  "plano": {"arquivo": "Plano 30-60-90 2026-11-13.pptx", "data": "2026-11-13"},
  "mapa": [{"pessoa": "Ana", "papel": "PO", "frente": "Tarumã", "pct": 50, "autonomia": "alta", "dono": true,
            "fonte": "[Usuário · 13/11]"}],
  "vagas": ["Analista Pleno", "Engenheiro de Dados"],
  "restricoes": [{"pessoa": "Caio", "disponivel_pct": 50, "ate": "2027-01-15", "fonte": "[Usuário · 20/11]"}],
  "pontos_unicos": ["Tarumã e Painel Jatobá dependem só da Ana"],
  "diagnostico": [{"prioridade": "Tarumã", "risco": "Buriti 🔴", "causa": "foco", "secundaria": "capacidade",
                   "evidencia": "Ana em 3 frentes, 110% [Usuário · 13/11]; DL1 [Plano · 13/11]"}],
  "achados": ["Hub Logístico sem dono (o Bruno só apoia)"],
  "decisao": {"texto": "Pausar a Previsão de Ruptura até 18/12 e ...",
              "testes": [{"id": "T1", "movimento": "Pausar a Previsão de Ruptura até 18/12", "nivel": 3,
                          "criterio": "Testes do Buriti concluídos até 11/12", "kpi": "DL1",
                          "inicio": "2026-11-16", "revisao": "2026-12-11"},
                         {"id": "T2", "movimento": "Apoio do Lucas ao Caio no piloto, 2 h por semana", "nivel": 4,
                          "ate": "2026-12-11", "escopo": "condução do piloto", "saida": "piloto em 2 lojas",
                          "criterio": "Piloto iniciado em 2 lojas até 11/12", "kpi": "P2 S4",
                          "inicio": "2026-11-16", "revisao": "2026-12-11"}]},
  "transicao": ["S1 (16–20/11): ...", "S2 (23–27/11): ...", "S3 (...)", "S4 (...): critérios e revisão em 11/12"],
  "historico": [{"data": "2026-11-13", "registro": "Análise de 13/11/2026; teste de 16/11 a 11/12"}]}}
~~~

- `autonomia`: `baixa`, `média` ou `alta`. `causa` e `secundaria`: `capacidade`, `autonomia`, `clareza`, `coordenação` ou `foco`.
- `nivel`: 1 a 7 (`estrutura-movimentos` §1). Nível 4 (apoio) exige `ate`, `escopo` e `saida`.
- `restricoes`: só pessoa, % disponível, data e fonte. **Nunca o motivo.**
- **Não mande interesses:** eles não são gravados no arquivo, nem nos dados ocultos. Se vierem, o script os tira e avisa.
- Nome do arquivo: `Estrutura <data> (confidencial).pptx` (ou `saida`).

Revisão do teste: `{"acao": "gerar", "partida": "<análise>.pptx", "revisao": {"data": "2026-12-11", "resultados": {"T1": {"atingido": true, "evidencia": "...", "fonte": "[Usuário · 11/12]"}}}}`. Todo teste em aberto precisa de resultado.

Mudança no mapa sem nova decisão (ex.: uma restrição de disponibilidade): `{"acao": "gerar", "partida": "<análise>.pptx", "data": "aaaa-mm-dd", "atualizar": {"restricoes": [...]}}`. `atualizar` troca as chaves que vierem (`mapa`, `restricoes`, `diagnostico`, `decisao`, `transicao`…).

## Resultado da geração

- O script **não gera nada** e diz o motivo quando há:
  - rótulo sobre pessoa ("fraco", "alto potencial");
  - termo de saúde ou de vida pessoal;
  - motivo numa restrição;
  - mudança formal na decisão (contratação, reporte, cargo, desligamento);
  - apoio sem prazo, escopo ou saída;
  - teste sem critério ou datas;
  - causa fora das 5;
  - diagnóstico sem evidência;
  - teste sem resultado na revisão.

  Resolva com o usuário e rode de novo. Não troque palavras para passar pela checagem.
- Quando gera, imprime a **CONFERÊNCIA DO ARQUIVO**: slides, "Confidencial" em quantos, se a releitura bate, o mapa e a carga, o diagnóstico, a decisão, os testes e o histórico.
- Descreva a entrega **só** com a conferência. Se ela mostrar ATENÇÃO, corrija o pedido e gere de novo.
- Entregue o link e avise em uma linha que o arquivo é confidencial e não deve circular.
- O arquivo tem 3 slides: Mapa de cobertura, Diagnóstico e Decisão e transição. Os dados ficam numa forma oculta do 1º slide: na revisão do teste, anexe este arquivo.
