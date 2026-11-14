---
name: coach-pptx
description: 'Script do Coach de Gestão que calcula as janelas (S1, 30, 60, 90 e recesso), lê os anexos (.pptx do plano, alinhamento e pautas do 1-1 e da Weekly), faz a conta de capacidade (com a reserva para o não planejado e a referência das semanas fechadas), roda a consistência, calcula a nota de execução, lista o que uma remoção afeta, gera o arquivo do plano 30-60-90 com os dados gravados (inclusive na revisão e na virada) e gera a versão para apresentar ao gestor ou ao time. Use na ficha, com todo anexo .pptx e na entrega.'
---

## Regra

Datas, contas e o arquivo saem **só** do script `scripts/coach_pptx.py` desta skill. Não calcule datas, não escreva código de layout e não use outra skill de apresentações.

**Pergunta não é falha.**
- Uma linha que começa com **PERGUNTE** é uma pergunta para o usuário. Faça a pergunta e rode de novo com a resposta.
- **NADA FOI GERADO** quer dizer que o script rodou e recusou. Resolva com o usuário o que ele lista.
- Falha é só erro de execução: um traceback ou o script não encontrado. Mostre o erro exato num bloco de código e tente o plano B (§Como rodar). Na etapa seguinte, rode o script de novo: **nunca dê o script por indisponível para o resto da conversa**, nem diga que ele falhou sem mostrar o erro.
- Se a entrega falhar de verdade, entregue a tabela e, num bloco de código, o pedido JSON completo da ação `gerar` (com o `plano` inteiro, ou com `partida` e `revisao`), com a linha: "Guarde este bloco: numa conversa nova, anexe o plano anterior, se houver, cole o bloco e peça para gerar com este pedido."

## Como rodar

1. No interpretador de código, grave o pedido em JSON em `/mnt/data/gestao_pedido.json`:

~~~python
import json
pedido = {"acao": "janelas", "data": "2026-11-13"}
json.dump(pedido, open("/mnt/data/gestao_pedido.json", "w", encoding="utf-8"), ensure_ascii=False)
~~~

2. Rode o script `scripts/coach_pptx.py` desta skill. Ele lê o pedido, trabalha em `/mnt/data`, onde ficam os anexos, e imprime o resultado.
3. Só se não conseguir rodar o script da skill, rode-o pelo interpretador:

~~~python
import glob, runpy
runpy.run_path(glob.glob("/home/oai/skills/**/coach-pptx/scripts/coach_pptx.py", recursive=True)[0], run_name="__main__")
~~~

Cite os arquivos pelo nome, como aparecem nos anexos. Arquivo "não encontrado" quer dizer que ele não foi anexado nesta conversa: peça para anexar.

## Ações

| Ação | Pedido | Imprime |
|---|---|---|
| `janelas` | `{"data": "2026-11-13"}`; de segunda a quarta, também `"s1": "esta"` ou `"proxima"`; para começar depois do recesso, `"inicio": "2027-01-04"` | S1 a S12, 30, 60, 90, semanas no recesso, janela de busca do Montar e avisos. Sem `s1` numa segunda a quarta: a pergunta a fazer, com as janelas das duas respostas (não é falha) |
| `ler` | `{"arquivos": [...]}` | Plano com dados (itens, KPIs, riscos, descartados, execução do ciclo, vitórias e a lista da revisão por exceção); plano feito à mão (textos por coluna, com a cor); pauta do 1-1 ou da Weekly (linhas e combinados, sem as linhas do tema do 1-1, carreira, sucessão, saúde ou sigilo); outro .pptx (textos por slide). Resultado em `gestao_leitura.json` |
| `capacidade` | `{"partida": "<plano>.pptx", "reunioes": [{"inicio": "2026-11-16T09:00", "fim": "2026-11-16T10:00"}]}`; opcionais: `semana`, `horas_dia` (8), `ausencias` (datas), `esforco_h` ou `atividades` (a semana nova), `nao_planejado_h` (do radar) ou `reserva_pct` (20) | Dias úteis (sem recesso e ausências), horas de jornada, reuniões e horas bloqueadas (sobreposição conta uma vez), horas livres, reserva para o não planejado, horas planejáveis, esforço e se cabe; a referência das últimas 3 semanas fechadas; atividades de mais de 4 h |
| `consistencia` | `{"partida": "<plano>.pptx"}` ou `{"plano": {...}}` | Falhas, atenções (pré-mortem, teste dos 100%, atividade grande, contra-indicador) e sinais de estrutura |
| `afetados` | `{"partida": "<plano>.pptx", "alvo": "P3"}`; `alvo` também pode ser `"90"`, `"60"`, `"30"` ou `"semana"` (para `voltar a`) | O item e tudo ligado a ele |
| `apresentar` | `{"partida": "<plano>.pptx", "publico": "gestor"}` ou `"time"` (ou `{"plano": {...}}`) | A versão para apresentar e a CONFERÊNCIA DA APRESENTAÇÃO (§Apresentar) |
| `gerar` | Montar: `{"plano": {...}}` · Revisão: `{"partida": "<plano>.pptx", "revisao": {...}}` · Virada: `{"partida": "<plano>.pptx", "virada": {...}}` | A conferência do arquivo |

Na `ler` e na `capacidade`, mande todos os anexos e todas as reuniões de uma vez. As reuniões vêm da busca no calendário da semana.

## O plano (Montar)

O `plano` tem o que foi aprovado na conversa, com as marcações (`[suposição]`, `[a confirmar]`): o script as guarda nos dados e as tira das tabelas. Datas em aaaa-mm-dd. IDs nunca são reaproveitados.

~~~json
{"usuario": "Lucas", "data": "2026-11-13", "s1": null, "inicio_ciclo": null,
 "retrato": {"mandato": [{"texto": "...", "fonte": "[Alinhamento · slide 2]"}],
             "direcionadores": [{"id": "D1", "texto": "Capturar o benefício prometido", "fonte": "..."}],
             "movimentos": [{"nome": "Tarumã", "dono": "Ana", "fonte": "..."}],
             "desafios": [{"texto": "...", "fonte": "..."}], "restricoes": [{"texto": "...", "fonte": "..."}],
             "desafio_central": {"texto": "...", "politica": "...", "nao_vamos": ["..."], "fonte": "..."}},
 "resultados": [{"id": "R1", "prioridade": "Quimera-7", "texto": "Recomendador convertendo benefício", "kpis": ["K1"],
                 "dono": "Bruno", "direcionador": "D1", "data": "2027-02-05", "compromisso": "comprometido",
                 "ataca": "...", "fonte": "..."}],
 "marcos": [{"id": "M1", "resultado": "R1", "texto": "Primeira conversão apurada", "data": "2026-12-18"}],
 "prioridades": [{"id": "P1", "nome": "Quimera-7", "resultado": "R1", "dono": "Bruno", "kpis": ["K4"],
                  "feito_quando": "...", "fecha_100": true, "entregaveis": {"S1": "...", "S2": "...", "S3": "...", "S4": "..."}}],
 "kpis": [{"id": "K1", "tipo": "resultado", "nome": "...", "definicao": "...", "fonte_dado": "Analista de Benefícios",
           "baseline": "R$ 0,0 (out/26)", "metas": {"30": "", "60": "R$ 0,25 MM", "90": "R$ 1,0 MM"},
           "frequencia": "Mensal", "dono": "Bruno", "status": "vermelho", "par": "K5", "fonte": "..."}],
 "agenda": {"atividades": [{"id": "A1", "liga": "P1", "texto": "...", "feito_quando": "...", "esforco_h": 3, "levanta": []}],
            "delegacoes": [{"id": "DL1", "quem": "Ana", "frente": "Tarumã", "oque": "...", "checar": "2026-11-20"}],
            "frentes": [{"nome": "Budget 2027", "direcionador": "D1"}],
            "pedidos": [{"id": "PG1", "tipo": "Ajuda", "texto": "..."}],
            "parar": [{"id": "PF1", "texto": "..."}]},
 "riscos": [{"id": "RB1", "texto": "...", "resultado": "R1", "mitigacao": "DL2: ..."}], "fora_do_plano": [], "descartados": [],
 "escolhas": {"prioridades_mantidas": false}}
~~~

- `s1`: `"esta"` ou `"proxima"` quando o plano é montado de segunda a quarta. `inicio_ciclo`: quando o ciclo começa depois do recesso.
- KPI `tipo`: `resultado`, `direcionador` ou `saude`. `status`: `verde`, `amarelo`, `vermelho` ou `sem_dado`. Baseline sem fonte: `""` (sai "a levantar").
- `levanta`: os KPIs cujo baseline a atividade ou a delegação levanta.
- `escolhas.prioridades_mantidas`: `true` quando o usuário manteve mais de 3 prioridades depois do desafio.
- `desafio_central`: o diagnóstico (`texto`), como vamos atacar (`politica`) e o que não vamos fazer (`nao_vamos`).
- Resultado: `compromisso` é `comprometido` ou `aspiracional`; `ataca`, uma linha de como ataca o desafio central.
- Prioridade: `fecha_100: true` depois do teste dos 100% confirmado.
- KPI: `par` é o contra-indicador, um ID do scorecard ou um nome.
- Risco: `mitigacao` é a atividade, a delegação ou o marco que reduz o risco (com o ID, quando houver).
- Atividade: `quando` e `se_entao`, quando combinados (obrigatórios na volta de um 2º escorregão).
- Nome do arquivo: `Plano 30-60-90 <data>.pptx` (ou `saida`).

## Revisão

~~~json
{"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx",
 "revisao": {"data": "2026-11-20",
   "status": {"A1": {"status": "feito", "fonte": "[E-mail · Compras · 18/11]"}, "A5": {"status": "parcial", "nota": "falta lançar"},
              "A6": {"status": "cancelado", "motivo": "..."}, "DL2": {"status": "checar depois", "para": "2026-11-25"},
              "PG1": {"status": "aberto"}, "PF1": {"status": "mantido"}},
   "atividades": [{"id": "A5", "liga": "Budget 2027", "texto": "...", "feito_quando": "...", "esforco_h": 1},
                  {"liga": "P2", "texto": "...", "feito_quando": "...", "esforco_h": 1}],
   "delegacoes": [], "pedidos": [], "parar": [],
   "kpis": {"K3": {"valor": "1 de 2", "data": "2026-11-27", "fonte": "[RH · 27/11]", "status": "amarelo"}},
   "confianca": {"R1": 5, "R2": 6, "R3": 7},
   "vitorias": ["Plano de conversão aceito por Compras"],
   "fora_do_plano": [{"tema": "Hub Logístico", "volume": "2 reuniões", "fonte": "...", "pergunta": "incluir, delegar ou parar?"}],
   "descartar": [{"texto": "Comitê Araçá", "origem": "radar"}],
   "mudancas": [{"op": "concluir", "id": "M5", "data": "2026-11-27", "fonte": "[Usuário · 27/11]"}]}}
~~~

- `status`: **todos** os itens da semana (atividades, delegações, pedidos e parar de fazer). Item sem status: o script não gera e lista o que falta.
- Atividade parcial ou não feita vai em `atividades` com o mesmo ID, ou leva `"destino"` no status.
- **Recesso.** Se as semanas seguintes à que fecha estão no recesso, o script as fecha sem atividades e abre a primeira semana depois dele (no máximo a S4, a da virada). As `atividades` são as dessa semana. Se o usuário vai trabalhar no recesso, mande `"trabalhar_no_recesso": true`.
- `atividades`: a semana nova inteira. Atividade nova vai sem ID: o script dá o próximo.
- Pedidos abertos, parar de fazer mantido e delegações em curso seguem sozinhos; mande em `delegacoes`, `pedidos` e `parar` só o que é novo ou muda.
- **2º escorregão:** atividade que já escorregou na semana anterior e escorrega de novo leva no status `"protocolo": "cortar escopo"` (com `"corte"`: o que sai) ou `"nova data"` (com `"motivo"`), ou vira `cancelado`. Se volta à semana, vai em `atividades` com `quando` e `se_entao`.
- `kpis`: só os que têm dado novo; valor novo exige `data` e `fonte`.
- `confianca`: de 0 a 10 por resultado, dita pelo usuário. Resultado sem nota gera aviso.
- `vitorias`: de 1 a 3 frases curtas; aparecem em Minha semana até a próxima revisão.
- `fora_do_plano`: o radar inteiro; o script tira os descartados e fica com até 5.
- `mudancas`: `concluir` (id, data, fonte), `replanejar` (id, data, motivo), `cortar_escopo` (id, `texto` novo, `corte`, `motivo`; numa prioridade, também a `semana` do entregável, S1 a S4; a data se mantém), `editar` (id, campos), `novo` (tipo: resultado, marco, prioridade, kpi ou risco; item) e `cancelar` (id, motivo, `confirmado`: a lista que a ação `afetados` devolveu e o usuário viu).

## Virada

O mesmo da revisão, em `virada`, mais:

~~~json
{"fechamento": {"P1": {"status": "atingida", "aprendizado": "..."},
                "P2": {"status": "parcial", "porque": "...", "aprendizado": "[suposição] ..."}},
 "resultados_atingidos": {"R3": "2 de 2 [Usuário · 11/12]"},
 "prioridades": null}
~~~

- `fechamento`: todas as prioridades do ciclo, com `atingida`, `parcial` ou `não atingida`, o `porque` (obrigatório quando não foi atingida) e o `aprendizado` (o que repetir ou mudar). O script grava o esperado (o "feito quando").
- `prioridades`: as do novo ciclo, quando mudarem; `null` mantém as que têm resultado no plano.
- O script anda as janelas 4 semanas, tira os resultados atingidos e os marcos concluídos (vão para o fechamento), põe os marcos das novas S1 a S4 como entregáveis e avisa o que falta: marcos para os novos 60 dias, entregáveis vazios, espaço para um resultado novo e o recesso. Também avisa prioridade não atingida em resultado comprometido, imprime a execução do ciclo com a leitura de cada resultado e o **resumo para o 1-1 com o gestor** (5 linhas).

## Apresentar

Depois do arquivo do plano, quando o usuário quiser mostrar o plano ao gestor ou ao time. O arquivo do plano continua sendo o que vai para a revisão e para o Coach de Estrutura; a apresentação não tem dados gravados.

| Público | Slides | Fica de fora |
|---|---|---|
| `gestor` | Plano em uma página (desafio central, resultados com tipo e confiança, marcos, prioridades) · Próximas 4 semanas · Como vamos medir (com a execução e a confiança) · O que preciso de você (pedidos e riscos com mitigação) | Minha semana, parar de fazer, sinal de estrutura |
| `time` | Plano em uma página (sem a confiança) · Próximas 4 semanas · Como vamos medir · Quem faz o quê (delegações por pessoa e as frentes próprias do usuário) | Pedidos ao gestor, parar de fazer, riscos, execução, confiança, sinal de estrutura |

- Sem IDs e sem as marcações entre colchetes. Sem KPIs no plano, o slide Como vamos medir sai e o script avisa.
- Nome: `Plano 30-60-90 <data> (apresentação gestor).pptx` ou `(apresentação time)`.
- O que o usuário chama de guardrails ou "o que não vamos fazer" fica em `desafio_central.nao_vamos` e aparece no slide 1.
- Descreva a entrega só com a CONFERÊNCIA DA APRESENTAÇÃO. Se ela mostrar ATENÇÃO, não entregue o arquivo: diga o que apareceu.

## Resultado da geração

- Se faltar algo (status de um item, motivo, data, fechamento, a lista de um cancelamento) ou o plano tiver termo de carreira, sucessão, saúde ou sigilo, o script **não gera nada** e diz o motivo. Resolva com o usuário e rode de novo.
- Quando gera, imprime a **CONFERÊNCIA DO ARQUIVO**: slides, se a releitura bate, ciclo e semana, janelas, resultados, marcos, prioridades, KPIs sem baseline, Minha semana, se as tabelas saíram sem marcações, descartados, riscos sem mitigação, a execução, as vitórias, mudanças, avisos, consistência, atenções e, na virada, o resumo para o gestor.
- Descreva a entrega **só** com a conferência. Se ela mostrar ATENÇÃO, corrija o pedido e gere de novo.
- O arquivo tem 4 slides (5, se Minha semana não couber num slide): Plano em uma página (com o desafio central, o tipo e a confiança de cada resultado e os riscos com mitigação), As 4 semanas, Scorecard (com o par de cada KPI e a linha de execução e confiança) e Minha semana (com as vitórias, o quando e o se-então). As fontes ficam nas notas, e os dados, numa forma oculta do 1º slide: na próxima revisão, anexe este arquivo.
