"""Confere o script da skill coach-pptx contra as fixtures, sem o Copilot, do jeito que o agente o usa:
grava um pedido JSON e roda scripts/coach_pptx.py.

Uso, na raiz do repositório:
    python gestao/coach-de-gestao/testes/conferir_codigo.py

O que confere:
  1. Limites do Agent Builder e script em dia com gestao/_codigo/.
  2. O script montado não repete nomes entre os módulos de origem.
  3. Janelas dos Cenários A, B, D e F: S1 pelo dia da semana, pergunta de segunda a quarta, recesso.
  4. Montar: o plano de 13/11 gerado e relido igual; tabelas sem marcações; recusa de carreira no plano e de S1
     sem resposta; desafio central, tipo do resultado, riscos com mitigação e par do KPI na conferência.
  5. Leitura: alinhamento por slide; 1-1 sem a linha de Carreira; weekly do time; plano feito à mão por coluna;
     a lista da revisão por exceção.
  6. Consistência (desafio, tipo, pré-mortem, teste dos 100%, atividade grande), afetados (P3) e capacidade
     (reserva para o não planejado, referência das semanas fechadas).
  7. Revisão de 20/11 (Cenário C): status, nada some em silêncio, a nova semana, descartado fora do radar,
     remoção só com a lista do que afeta, nota de execução, confiança e vitórias.
  7b. 2º escorregão (Cenário G): protocolo (cortar escopo, nova data com motivo ou cancelar), quando e se-então;
     cortar escopo de um entregável; queda de confiança.
  8. Fixture de 04/12 (3 revisões) e virada de 11/12 (Cenário D): janelas, fechamento com os 4 pontos da revisão
     pós-ação, resultado atingido, marcos concluídos e marcos que viram entregáveis, recesso, execução do ciclo
     e o resumo para o 1-1 com o gestor.
  8b. Recesso: a revisão de 18/12 pula as semanas de recesso e abre a S4 (a virada é em 08/01).
  8c. Minha semana cheia vai para um slide de continuação, sem corte.
  8d. Apresentação para o gestor e para o time: sem dados gravados, sem IDs, e o time sem pedidos, parar de fazer,
      riscos e confiança.
  9. Plano B: o script roda pelo interpretador (runpy, com o argv de um kernel).
Sai com erro na primeira falha.
"""
import ast
import copy
import re
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
AQUI = pathlib.Path(__file__).resolve().parent
FIX = AQUI / "fixtures"
SCRIPT = RAIZ / "gestao/coach-de-gestao/pacote/skills/coach-pptx/scripts/coach_pptx.py"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="gestao-"))
for f in FIX.iterdir():
    shutil.copy(f, TMP / f.name)  # como os anexos em /mnt/data


def ok(msg):
    print("ok  " + msg)


def rodar(pedido):
    """Grava o pedido e roda o script, como o agente faz. Devolve (código de saída, texto impresso)."""
    (TMP / "gestao_pedido.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(TMP / "gestao_pedido.json")],
                       capture_output=True, text=True, cwd=TMP)
    return r.returncode, r.stdout + r.stderr


def resultado():
    return json.loads((TMP / "gestao_resultado.json").read_text(encoding="utf-8"))


# 1. Limites e fonte única
for cmd in (["ferramentas/conferir_limites.py", "coach-de-gestao"], ["ferramentas/montar_skills.py", "--conferir"]):
    r = subprocess.run([sys.executable, str(RAIZ / cmd[0]), cmd[1]], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
ok("limites do Agent Builder respeitados; script em dia com gestao/_codigo/")

# 2. Nomes únicos entre os módulos do script montado
fontes = SCRIPT.read_text(encoding="utf-8").split("\n", 1)[0].split("a partir de: ")[1].split(". Não edite")[0].split()
nomes = {}
for f in fontes:
    for n in ast.parse((RAIZ / f).read_text(encoding="utf-8")).body:
        alvos = [n.name] if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else \
                [x.id for a in getattr(n, "targets", []) for x in ast.walk(a) if isinstance(x, ast.Name)]
        for a in alvos:
            nomes.setdefault(a, []).append(f)
repetidos = {k: v for k, v in nomes.items() if len(v) > 1 and not k.startswith("_codigo")}
assert not repetidos, repetidos
ok(f"script montado de {len(fontes)} módulos, sem nomes repetidos")

spec = importlib.util.spec_from_file_location("gf", AQUI / "gerar_fixtures.py")
gf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf)
ns = {}
exec(SCRIPT.read_text(encoding="utf-8").replace('if __name__ == "__main__":', "if False:"), ns)

# 3. Janelas
casos = [
    ({"data": "2026-11-13"}, "S1 16–20/11 · 30 dias 16/11–11/12 · 60 dias 14/12–08/01 · 90 dias até 05/02/2027",
     "Janela de busca do Montar: 16/10–13/11"),
    ({"data": "2026-11-27"}, "S1 30/11–04/12 · 30 dias 30/11–25/12 · 60 dias 28/12–22/01 · 90 dias até 19/02/2027",
     "S4 (21–25/12) no recesso"),
    ({"data": "2026-11-18", "s1": "proxima"}, "S1 23–27/11 · 30 dias 23/11–18/12 · 60 dias 21/12–15/01 · 90 dias até 12/02/2027", ""),
    ({"data": "2026-12-18"}, "S1 21–25/12", "S1 e S2 no recesso: pergunte se o ciclo começa depois do recesso (04/01)"),
    ({"data": "2026-12-18", "inicio": "2027-01-04"}, "S1 04–08/01 · 30 dias 04–29/01 · 60 dias 01–26/02 · 90 dias até 26/03/2027", ""),
]
for pedido, janelas, extra in casos:
    cod, txt = rodar(dict(pedido, acao="janelas"))
    assert cod == 0 and janelas in txt and extra in txt, (pedido, txt)
cod, txt = rodar({"acao": "janelas", "data": "2026-11-18"})
assert "PERGUNTE" in txt and "16–20/11" in txt and "23–27/11" in txt, txt
cod, txt = rodar({"acao": "janelas", "data": "2026-11-10"})
for trecho in ("PERGUNTE ao usuário, em uma linha (é uma pergunta, não uma falha do script)",
               'Se for esta semana ("s1": "esta"): S1 09–13/11 · 30 dias 09/11–04/12 · 60 dias 07/12–01/01 · 90 dias até 29/01/2027',
               'Se for a próxima ("s1": "proxima"): S1 16–20/11 · 30 dias 16/11–11/12 · 60 dias 14/12–08/01 · 90 dias até 05/02/2027'):
    assert cod == 0 and trecho in txt, (trecho, txt)
ok("janelas: A (13/11), B (27/11, S4 no recesso), F1 (quarta: pergunta; próxima), F2 (S1 e S2 no recesso; 04/01); "
   "terça: a pergunta vem com as datas das duas respostas")

# 4. Montar
cod, txt = rodar({"acao": "gerar", "saida": "Montar.pptx", "plano": gf.PLANO_1311})
assert cod == 0, txt
for trecho in ("Montar.pptx · 4 slides · dados gravados · releitura sem diferença",
               "Ciclo 1, semana 1 de 4 · S1 16–20/11 · 30 dias 16/11–11/12 · 60 dias 14/12–08/01 · 90 dias até 05/02/2027",
               "Prioridades: P1 Quimera-7, P2 Ipê-Roxo, P3 Vagas em aberto", "sem baseline: K2, K4, K6",
               "6 atividades, 3 delegações, 1 pedidos ao gestor, 1 parar de fazer", "Tabelas sem marcações",
               "sinal de estrutura: Ana em 3 frentes", "Riscos: 2 · sem mitigação: nenhum",
               "Execução: nenhuma semana fechada neste ciclo", "- K3 Vagas preenchidas sem contra-indicador (par)"):
    assert trecho in txt, (trecho, txt)
assert "Sem desafio central" not in txt and "sem tipo" not in txt and "RESUMO PARA O 1-1" not in txt, txt
slides = [" ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame) + " ".join(
    c.text for sh in s.shapes if sh.has_table for r in sh.table.rows for c in r.cells)
    for s in ns["Presentation"](str(TMP / "Montar.pptx")).slides]
for n, trecho in ((0, "Desafio central: O Recomendador não converte benefício"), (0, "Não vamos: Abrir produto novo sem problema"),
                  (0, "Comprometido"), (0, "Aspiracional"), (0, "RB1 TI não fazer a carga do Recomendador em 25/11 → DL2"),
                  (2, "Par: K5 Pessoas do time em mais de 2 frentes"), (2, "Par: % de chamados reabertos depois da Triagem"),
                  (2, "Execução: nenhuma semana fechada")):
    assert trecho in slides[n], (n, trecho, slides[n][:400])
dados, _ = ns["ler_plano"](str(TMP / "Montar.pptx"))
fix, _ = ns["ler_plano"](str(FIX / "Plano 30-60-90 2026-11-13.pptx"))
assert dados == fix, "o plano montado difere da fixture de 13/11"
marcado = copy.deepcopy(gf.PLANO_1311)
marcado["marcos"][1]["texto"] += " [suposição]"
marcado["kpis"][1]["metas"]["90"] = "40% [a confirmar]"
cod, txt = rodar({"acao": "gerar", "saida": "Marcado.pptx", "plano": marcado})
assert cod == 0 and "Tabelas sem marcações" in txt, txt
assert ns["ler_plano"](str(TMP / "Marcado.pptx"))[0]["marcos"][1]["texto"].endswith("[suposição]")
carreira = copy.deepcopy(gf.PLANO_1311)
carreira["riscos"] = [{"id": "RB1", "texto": "Ana quer ir para Visualização de Dados em 2027"}]
cod, txt = rodar({"acao": "gerar", "saida": "Carreira.pptx", "plano": carreira})
assert cod == 1 and "NADA FOI GERADO" in txt and "carreira" in txt and not (TMP / "Carreira.pptx").exists(), txt
quarta = dict(gf.PLANO_1311, data="2026-11-18")
cod, txt = rodar({"acao": "gerar", "saida": "Quarta.pptx", "plano": quarta})
assert cod == 1 and "S1 é esta semana" in txt and "não é falha do script" in txt and "S1 23–27/11 · 30 dias 23/11–18/12" in txt, txt
ok("montar: plano de 13/11 relido igual à fixture; tabelas limpas com os dados marcados; recusa carreira e S1 sem resposta")

# 5. Leitura
cod, txt = rodar({"acao": "ler", "arquivos": ["Alinhamento Nucleo 2027 ficticio.pptx", "1-1 Ana 2026-11-09 anotada.pptx",
                                              "Weekly time 2026-11-18 anotada.pptx", "Plano 30-60-90 sem dados.pptx",
                                              "Plano 30-60-90 2026-11-13.pptx"]})
assert cod == 0, txt
bruto = txt + (TMP / "gestao_leitura.json").read_text(encoding="utf-8")
assert "Visualização de Dados" not in bruto and "Não comentar" not in bruto, "a linha de Carreira vazou na leitura"
for trecho in ("Slide 4: Movimentos / Quimera-7 (Bruno)", "1 linha(s) omitida(s) pelo script",
               "🔴 Buriti não fecha em 04/12: nova data 18/12", "Hub Logístico (pedido do negócio)",
               "Plano SEM os dados gravados", "  [60 dias]", "● vermelho · Analista Pleno contratado",
               "(sem cor) · Proposta ao Engenheiro de Dados", "Plano com os dados gravados · data 13/11/2026 · ciclo 1, semana 1 de 4",
               "Desafio central: O Recomendador não converte benefício", "RB2 | risco: A finalista do Analista Pleno recusar a proposta",
               "REVISÃO POR EXCEÇÃO", "KPI K1 Benefício capturado do Recomendador (R$ MM/mês) 🔴",
               "DL1 Ana · Buriti, replanejamento para 18/12: checar em 20/11"):
    assert trecho in txt, (trecho, txt)
assert "KPI K7" not in txt.split("REVISÃO POR EXCEÇÃO")[1], "KPI verde na lista de exceções"
cod, txt = rodar({"acao": "ler", "arquivos": ["Plano 30-60-90 2026-11-20.pptx"]})
for trecho in ("A4 Escrever a descrição da vaga de Engenheiro de Dados já escorregou uma semana",
               "Execução: S1 40% · ciclo 2 de 5 (40%)", "Vitórias da última semana: Plano de conversão aceito por Compras",
               "R1 Recomendador convertendo benefício com confiança 5/10"):
    assert trecho in txt, (trecho, txt)
assert "A7 " not in txt.split("REVISÃO POR EXCEÇÃO")[1], txt
ok("leitura: alinhamento por slide; 1-1 sem a linha de Carreira; weekly do time; plano feito à mão por coluna e cor; "
   "revisão por exceção (KPIs fora do verde, checagens da semana, atividade que já escorregou, confiança baixa)")

# 6. Consistência, afetados e capacidade
cod, txt = rodar({"acao": "consistencia", "partida": "Plano 30-60-90 2026-11-13.pptx"})
assert "K4 % de lojas do piloto com recomendação aplicada sem baseline: ponha o levantamento" in txt, txt
assert "Ana em 3 frentes (Tarumã, Painel Jatobá, Previsão de Ruptura)" in txt and "6 de 9 itens da semana com você" in txt, txt
orfa = copy.deepcopy(fix)
orfa["agenda"]["atividades"].append({"id": "A7", "liga": "", "texto": "Revisar o deck do MOR de dezembro",
                                     "feito_quando": "Deck revisado", "esforco_h": 2})
cod, txt = rodar({"acao": "consistencia", "plano": orfa})
assert "A7 sem prioridade nem frente própria acima" in txt, txt
cru = copy.deepcopy(fix)
del cru["retrato"]["desafio_central"]
del cru["resultados"][1]["compromisso"]
cru["riscos"][1].pop("mitigacao")
cru["prioridades"][0].pop("fecha_100")
cru["agenda"]["atividades"][0]["esforco_h"] = 6
cod, txt = rodar({"acao": "consistencia", "plano": cru})
for trecho in ("Sem desafio central: pergunte qual é, e o que não vamos fazer", "R2 sem tipo: comprometido ou aspiracional",
               "RB2 sem mitigação", "P1 Quimera-7: faça o teste dos 100%", "A1 com 6 h: quebre em passos"):
    assert trecho in txt, (trecho, txt)
sem_riscos = dict(copy.deepcopy(fix), riscos=[])
cod, txt = rodar({"acao": "consistencia", "plano": sem_riscos})
assert "Sem riscos: faça o pré-mortem" in txt, txt
cod, txt = rodar({"acao": "afetados", "partida": "Plano 30-60-90 2026-11-13.pptx", "alvo": "P3"})
afet = [x.split()[0] for x in txt.split(": ", 1)[1].split("; ")]
assert afet == ["R3", "M5", "M6", "P3", "K3", "K7", "A3", "A4"], afet
cod, txt = rodar({"acao": "capacidade", "partida": "Plano 30-60-90 2026-11-13.pptx", "reunioes": [
    {"inicio": "2026-11-16T09:00", "fim": "2026-11-16T10:30"}, {"inicio": "2026-11-16T10:00", "fim": "2026-11-16T11:00"},
    {"data": "2026-11-18", "horas": 3}]})
assert ("5 dias úteis · 40 h de jornada · 3 reuniões, 5 h bloqueadas · 35 h livres · reserva para o não planejado 7 h "
        "(20% das horas livres) · 28 h planejáveis · esforço planejado 10 h · cabe") in txt, txt
assert "Referência: sem semanas fechadas ainda" in txt, txt
cod, txt = rodar({"acao": "capacidade", "semana": ["2026-11-16", "2026-11-20"], "reunioes": [{"data": "2026-11-17", "horas": 20}],
                  "nao_planejado_h": 12, "esforco_h": 10})
assert "20 h livres · reserva para o não planejado 12 h (volume do radar) · 8 h planejáveis" in txt and "NÃO CABE: faltam 2 h" in txt, txt
cod, txt = rodar({"acao": "capacidade", "partida": "Plano 30-60-90 2026-12-04.pptx", "esforco_h": 10,
                  "atividades": [{"texto": "Fechar o budget 2027 da área", "esforco_h": 6}]})
for trecho in ("Referência (visão de fora): S1 16–20/11: 5 h concluídas de 9 h · S2 23–27/11: 6 h concluídas de 6 h · "
               "S3 30/11–04/12: 7 h concluídas de 8 h · média 6.0 h concluídas por semana",
               "o esforço planejado (10 h) passa de 1,25 × o que foi concluído em média (6.0 h)",
               "atividade (Fechar o budget 2027 da área) com 6 h: quebre em passos de até 4 h"):
    assert trecho in txt, (trecho, txt)
cod, txt = rodar({"acao": "capacidade", "semana": ["2026-12-21", "2026-12-25"], "esforco_h": 4})
assert "0 dias úteis" in txt and "NÃO CABE" in txt, txt
ok("consistência (K4, atividade órfã, delegação, sinal da Ana, desafio, tipo, pré-mortem, 100%, atividade grande), "
   "afetados de P3 e capacidade (sobreposição, recesso, reserva de 20% ou do radar, referência das semanas fechadas)")

# 7. Revisão de 20/11
rev = copy.deepcopy(gf.REV_2011)
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": rev})
assert cod == 0, txt
for trecho in ("Plano 30-60-90 2026-11-20.pptx · 4 slides · dados gravados · releitura sem diferença",
               "Ciclo 1, semana 2 de 4 · S1 16–20/11 · 30 dias 16/11–11/12", "5 atividades, 3 delegações, 1 pedidos ao gestor, 1 parar de fazer",
               "S1 (16–20/11) fechada: A1 feito, A2 não feito, A3 feito, A4 não feito, A5 parcial, A6 cancelado",
               "Execução da S1: 2 de 5 atividades (40%) · 5 h concluídas de 9 h planejadas · 1 cancelada(s) fora da conta",
               "Execução da S1 em 40%, abaixo de 85%", "Confiança: R1 5 · R2 6 · R3 7",
               "Vitórias: Plano de conversão aceito por Compras; Analista Pleno decidido", "Execução: S1 40% · ciclo 2 de 5 (40%)"):
    assert trecho in txt, (trecho, txt)
s4 = " ".join(sh.text_frame.text for sh in ns["Presentation"](str(TMP / "Plano 30-60-90 2026-11-20.pptx")).slides[3].shapes
              if sh.has_text_frame)
assert "VITÓRIAS DA SEMANA PASSADA" in s4 and "Analista Pleno decidido" in s4, s4
p = resultado()["plano"]
assert [a["id"] for a in p["agenda"]["atividades"]] == ["A2", "A4", "A5", "A7", "A8"], p["agenda"]["atividades"]
assert {d["id"]: d["checar"] for d in p["agenda"]["delegacoes"]} == {"DL1": "2026-11-27", "DL2": "2026-11-25", "DL3": "2026-12-04"}
assert [x["id"] for x in p["agenda"]["pedidos"]] == ["PG1"] and p["fora_do_plano"][0]["tema"] == "Hub Logístico"
falta = copy.deepcopy(gf.REV_2011)
del falta["status"]["A6"]
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": falta, "saida": "X.pptx"})
assert cod == 1 and "A6 sem destino" in txt and "nada some em silêncio" in txt, txt
sem_s2 = copy.deepcopy(gf.REV_2011)
sem_s2["atividades"] = [a for a in sem_s2["atividades"] if a["id"] != "A4"]
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": sem_s2, "saida": "X.pptx"})
assert cod == 1 and "A4 não feito: ponha na nova semana" in txt, txt
radar = copy.deepcopy(gf.REV_2011)
radar["descartar"] = [{"texto": "Comitê Araçá", "origem": "radar"}]
radar["fora_do_plano"].append({"tema": "Comitê Araçá", "volume": "3 reuniões", "fonte": "[Reunião · 19/11]",
                               "pergunta": "incluir, delegar ou parar?"})
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": radar, "saida": "Radar.pptx"})
p = resultado()["plano"]
assert cod == 0 and [t["tema"] for t in p["fora_do_plano"]] == ["Hub Logístico"] and p["descartados"][0]["texto"] == "Comitê Araçá", txt
remover = copy.deepcopy(gf.REV_2011)
remover["mudancas"] = [{"op": "cancelar", "id": "P3", "motivo": "o usuário não quer mais ver"}]
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": remover, "saida": "X.pptx"})
assert cod == 1 and "Cancelar P3 afeta R3, M5, M6, P3, K3, K7, A4, A8" in txt and not (TMP / "X.pptx").exists(), txt
conf_ruim = copy.deepcopy(gf.REV_2011)
conf_ruim["confianca"]["R2"] = 11
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "revisao": conf_ruim, "saida": "X.pptx"})
assert cod == 1 and "Confiança de R2: 11 (de 0 a 10)" in txt, txt
ok("revisão de 20/11: S1 fechada, A2, A4 e A5 na S2, PG1 em aberto, DL2 em 25/11, execução 40% com aviso, confiança "
   "e vitórias; sem destino, sem S2, descartado no radar, remoção sem a lista e confiança fora de 0–10: recusados ou filtrados")

# 7b. 2º escorregão (Cenário G): A4 não feito em 20/11 e de novo em 27/11
p20, _ = ns["ler_plano"](str(FIX / "Plano 30-60-90 2026-11-20.pptx"))
assert p20 == resultado()["plano"] or p20["semana"] == 2
rev27 = copy.deepcopy(gf.REV_2711)
rev27["status"]["A4"] = gf.ST("não feito", nota="o RH não mandou o modelo")
a4 = gf.A("A4", "P3", "Escrever a descrição da vaga de Engenheiro de Dados", "Descrição enviada ao RH", 2)
rev27["atividades"].insert(0, dict(a4))
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-20.pptx", "revisao": rev27, "saida": "X.pptx"})
assert cod == 1 and "A4 escorregou pela 2ª semana: ofereça, nesta ordem, cortar escopo, nova data com motivo ou cancelar" in txt, txt
rev27["status"]["A4"]["protocolo"] = "nova data"
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-20.pptx", "revisao": rev27, "saida": "X.pptx"})
assert cod == 1 and "A4: nova data sem motivo" in txt, txt
rev27["status"]["A4"].update(protocolo="cortar escopo", corte="a parte de requisitos técnicos fica com o Bruno")
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-20.pptx", "revisao": rev27, "saida": "X.pptx"})
assert cod == 1 and "A4 volta à semana pela 3ª vez: combine quando (dia e hora) e um se-então" in txt, txt
rev27["atividades"][0].update(texto="Escrever a descrição da vaga (sem os requisitos técnicos)", quando="ter 01/12, 9h",
                              se_entao="se o RH não mandar o modelo até segunda, então uso a vaga do Analista Pleno como base")
rev27["mudancas"].append({"op": "cortar_escopo", "id": "P2", "semana": "S3", "texto": "Roteiro de treinamento da 1ª loja",
                          "corte": "o roteiro da 2ª loja vai para S4", "motivo": "a 2ª loja ainda não foi escolhida"})
rev27["confianca"] = {"R1": 5, "R2": 3, "R3": 7}
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-20.pptx", "revisao": rev27, "saida": "G.pptx"})
assert cod == 0, txt
for trecho in ("P2 com escopo cortado (entregável S3): sai o roteiro da 2ª loja vai para S4; a data se mantém",
               "Confiança de R2 caiu de 6 para 3: pergunte o porquê e o risco", "Execução da S2: 4 de 5 atividades (80%)"):
    assert trecho in txt, (trecho, txt)
p = resultado()["plano"]
assert p["historico"][-1]["itens"]["A4"]["protocolo"] == "cortar escopo"
assert next(x for x in p["prioridades"] if x["id"] == "P2")["entregaveis"]["S3"] == "Roteiro de treinamento da 1ª loja"
assert next(x for x in p["prioridades"] if x["id"] == "P2")["cortes"][0]["antes"] == "Roteiro de treinamento"
s4 = " ".join(c.text for sh in ns["Presentation"](str(TMP / "G.pptx")).slides[3].shapes if sh.has_table
              for r in sh.table.rows for c in r.cells)
assert "Quando: ter 01/12, 9h" in s4 and "Se-então: se o RH não mandar o modelo" in s4, s4
cancela = copy.deepcopy(gf.REV_2711)
cancela["status"]["A4"] = gf.ST("cancelado", motivo="a vaga muda de perfil em jan/27")
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-20.pptx", "revisao": cancela, "saida": "X.pptx"})
assert cod == 0 and "1 cancelada(s) fora da conta" in txt, txt
antes, _ = ns["ler_plano"](str(FIX / "Plano 30-60-90 2026-12-04.pptx"))
p27 = gf.plano_revisado([gf.REV_2011, gf.REV_2711])
_, _, erros, avisos = ns["pl_revisar"](p27, gf.REV_0412)
assert not erros and "Confiança de R2 caiu de 6 para 4: pergunte o porquê e o risco" in avisos, avisos
ok("2º escorregão: sem protocolo, nova data sem motivo e 3ª vez sem quando e se-então recusados; cortar escopo de A4 e "
   "do entregável S3 de P2; cancelar sai da conta; queda de confiança de R2 avisada")

# 8. Fixture de 04/12 e virada de 11/12
p4, _ = ns["ler_plano"](str(FIX / "Plano 30-60-90 2026-12-04.pptx"))
assert p4["semana"] == 4 and len(p4["historico"]) == 3 and p4["descartados"][0]["texto"] == "Comitê Araçá"
assert next(m for m in p4["marcos"] if m["id"] == "M5")["status"] == "concluido"
assert next(k for k in p4["kpis"] if k["id"] == "K3")["ultimo"]["valor"] == "1 de 2"
assert len(p4["agenda"]["atividades"]) == 5
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-11-13.pptx", "virada": {"data": "2026-11-20"}, "saida": "X.pptx"})
assert cod == 1 and "a virada é na 4ª revisão".lower() in txt.lower(), txt
status_s4 = {i: {"status": "feito"} for i in ("A13", "A14", "A15", "A16", "A17")}
status_s4.update({"DL1": {"status": "checar depois", "para": "2026-12-18"}, "DL3": {"status": "checar depois", "para": "2026-12-18"},
                  "PG1": {"status": "aberto"}, "PF1": {"status": "mantido"}})
virada = {"data": "2026-12-11", "status": status_s4,
          "fechamento": {"P1": {"status": "atingida", "aprendizado": "A carga com TI destravou a leitura"},
                         "P2": {"status": "parcial", "porque": "As lojas foram escolhidas depois do roteiro",
                                "aprendizado": "[suposição] Escolher as lojas antes do roteiro"},
                         "P3": {"status": "atingida", "aprendizado": "Decidir rápido entre finalistas"}},
          "resultados_atingidos": {"R3": "2 de 2 [Usuário · 11/12]"}, "confianca": {"R1": 6, "R2": 5, "R3": 9},
          "vitorias": ["Time completo"],
          "kpis": {"K1": {"valor": "R$ 0,3 MM/mês (nov)", "data": "2026-12-10", "fonte": "[Painel do Recomendador · 10/12]",
                          "status": "amarelo"}},
          "mudancas": [{"op": "concluir", "id": "M1", "data": "2026-12-10", "fonte": "[Usuário · 11/12]"},
                       {"op": "concluir", "id": "M6", "data": "2026-12-10", "fonte": "[Usuário · 11/12]"}],
          "atividades": [gf.A(None, "P1", "Rodar o plano de conversão na 1ª loja", "Loja rodando", 2),
                         gf.A(None, "P2", "Fechar a 2ª loja do piloto", "Loja confirmada", 1)]}
sem_fecha = copy.deepcopy(virada)
del sem_fecha["fechamento"]["P2"]
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-12-04.pptx", "virada": sem_fecha, "saida": "X.pptx"})
assert cod == 1 and "Fechamento de P2" in txt, txt
sem_porque = copy.deepcopy(virada)
del sem_porque["fechamento"]["P2"]["porque"]
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-12-04.pptx", "virada": sem_porque, "saida": "X.pptx"})
assert cod == 1 and "Fechamento de P2 (parcial): falta o porquê da diferença" in txt, txt
p1_parcial = copy.deepcopy(virada)
p1_parcial["fechamento"]["P1"] = {"status": "parcial", "porque": "A carga atrasou uma semana", "aprendizado": "Puxar TI antes"}
_, _, erros, avisos = ns["pl_virar"](antes, p1_parcial)
assert not erros and any("P1 Quimera-7 parcial num resultado comprometido (R1)" in a for a in avisos), avisos
cod, txt = rodar({"acao": "gerar", "partida": "Plano 30-60-90 2026-12-04.pptx", "virada": virada})
assert cod == 0, txt
for trecho in ("Plano 30-60-90 2026-12-11.pptx · 4 slides · dados gravados · releitura sem diferença",
               "Ciclo 2, semana 1 de 4 · S1 14–18/12 · 30 dias 14/12–08/01 · 60 dias 11/01–05/02 · 90 dias até 05/03/2027",
               "R3 atingido, sai com registro", "M1 concluído em 10/12", "M3 (18/12) vira entregável de P2 Ipê-Roxo em S1",
               "M2 (08/01) vira entregável de P1 Quimera-7 em S4", "M4 (08/01) vira entregável de P2 Ipê-Roxo em S4",
               "R1 precisa de marco para 11/01–05/02", "R2 precisa de marco para 11/01–05/02",
               "S2 (21–25/12) no recesso", "S3 (28/12–01/01) no recesso", "Prioridades: P1 Quimera-7, P2 Ipê-Roxo",
               "KPI K1: R$ 0,3 MM/mês (nov) (10/12)", "Descartados gravados: 1",
               "P2 Ipê-Roxo parcial num resultado aspiracional (R2): dentro do esperado",
               "Execução do ciclo 1: S1 40% · S2 100% · S3 80% · S4 100% · ciclo 16 de 20 (80%)",
               "R1 · KPI K1 🟡 · confiança 6 · execução baixa: revise o tamanho do plano",
               "RESUMO PARA O 1-1 COM O GESTOR",
               "Ciclo 1 fechado: P1 Quimera-7 atingida; P2 Ipê-Roxo parcial; P3 Vagas em aberto atingida",
               "Saem: R3 Time completo (2 de 2 [Usuário · 11/12])",
               "Ciclo 2 (14/12–08/01): P1 Quimera-7, P2 Ipê-Roxo · desafio central: O Recomendador não converte benefício",
               "Pedidos em aberto: PG1 · Ajuda · Patrocínio do plano de conversão",
               "Execução do ciclo: 80% · confiança: R1 6, R2 5"):
    assert trecho in txt, (trecho, txt)
assert len(txt.split("RESUMO PARA O 1-1 COM O GESTOR")[1].strip().splitlines()[1:]) == 5
p = resultado()["plano"]
assert {m["id"] for m in p["marcos"]} == {"M2", "M3", "M4"} and {r["id"] for r in p["resultados"]} == {"R1", "R2"}
assert p["fechamentos"][0]["prioridades"][1] == {"status": "parcial", "porque": "As lojas foram escolhidas depois do roteiro",
                                                 "aprendizado": "[suposição] Escolher as lojas antes do roteiro",
                                                 "esperado": "Piloto iniciado em 2 lojas", "id": "P2", "nome": "Ipê-Roxo"}
assert p["fechamentos"][0]["execucao"]["pct"] == 80 and len(p["resumo_gestor"]) == 5
assert {x["id"] for x in p["fechamentos"][0]["saidos"]} >= {"R3", "M5", "M6", "K3", "M1"}
assert [a["id"] for a in p["agenda"]["atividades"]] == ["A18", "A19"], p["agenda"]["atividades"]
ok("virada de 11/12: janelas do ciclo 2; R3, M1, M5 e M6 no fechamento; M2, M3 e M4 viram entregáveis; marcos pedidos "
   "para R1 e R2; recesso em S2 e S3; IDs novos sem reaproveitar; revisão pós-ação com porquê; comprometido x "
   "aspiracional; execução do ciclo com KPI e confiança; resumo de 5 linhas para o gestor")

# 8b. Recesso: a revisão de 18/12 fecha a S1 do ciclo 2 e pula a S2 e a S3, que estão no recesso
p11 = resultado()["plano"]
st18 = {"A18": {"status": "feito"}, "A19": {"status": "parcial"}, "DL1": {"status": "checar depois", "para": "2027-01-08"},
        "DL3": {"status": "checar depois", "para": "2027-01-08"}, "PG1": {"status": "aberto"}, "PF1": {"status": "mantido"}}
rev18 = {"data": "2026-12-18", "status": st18, "confianca": {"R1": 6, "R2": 5},
         "atividades": [gf.A("A19", "P2", "Fechar a 2ª loja do piloto", "Loja confirmada", 1),
                        gf.A(None, "P1", "Ler a conversão de dezembro com o Bruno", "Leitura registrada", 1)]}
cod, txt = rodar({"acao": "gerar", "plano": p11, "revisao": rev18, "saida": "R18.pptx"})
assert cod == 0, txt
for trecho in ("S2 (21–25/12) no recesso: fechada sem atividades", "S3 (28/12–01/01) no recesso: fechada sem atividades",
               "A semana nova é a S4 (04–08/01): a próxima revisão é em 08/01, a virada do ciclo", "Ciclo 2, semana 4 de 4"):
    assert trecho in txt, (trecho, txt)
p18 = resultado()["plano"]
assert [h["semana"] for h in p18["historico"] if h["ciclo"] == 2] == [1, 2, 3] and p18["historico"][-1]["recesso"]
assert ns["pl_escorregou"](p18, "A19"), "o recesso apagou o escorregão da A19"
cod, txt = rodar({"acao": "gerar", "plano": p11, "revisao": dict(rev18, trabalhar_no_recesso=True), "saida": "R18b.pptx"})
assert cod == 0 and "Ciclo 2, semana 2 de 4" in txt and "fechada sem atividades" not in txt, txt
ok("recesso: a revisão de 18/12 pula S2 e S3 e abre a S4 (virada em 08/01); o escorregão da A19 sobrevive ao recesso; "
   "com trabalhar_no_recesso, abre a S2")

# 8c. Semana cheia: delegações, pedidos e parar de fazer vão para um slide de continuação
cheio = copy.deepcopy(gf.PLANO_1311)
cheio["agenda"]["delegacoes"] += [{"id": f"DL{k}", "quem": "Bruno", "frente": f"Frente {k}", "liga": "P1", "checar": "2026-11-20",
                                   "oque": "Completar o discovery e registrar lacunas, próxima etapa, dependências e bloqueios no PRD"}
                                  for k in range(4, 9)]
cheio["agenda"]["pedidos"] += [{"id": f"PG{k}", "tipo": "Ajuda", "texto": "Escalonamento executivo para pendências do fornecedor "
                                "que ameacem o go-live"} for k in range(2, 5)]
for a in cheio["agenda"]["atividades"]:
    a["quando"] = "até 18/11"
cod, txt = rodar({"acao": "gerar", "plano": cheio, "saida": "Cheio.pptx"})
assert cod == 0 and "Cheio.pptx · 5 slides" in txt and "passou da altura" not in txt and "releitura sem diferença" in txt, txt
ultimo = " ".join(sh.text_frame.text for sh in ns["Presentation"](str(TMP / "Cheio.pptx")).slides[4].shapes if sh.has_text_frame)
assert "(continuação)" in ultimo and "DL8" in ultimo and "PG4" in ultimo and "PF1" in ultimo, ultimo
ok("semana cheia: 8 delegações, 4 pedidos e o parar de fazer num slide de continuação, sem corte")

# 8d. Apresentação para o gestor e para o time
def textos(arq):
    prs = ns["Presentation"](str(TMP / arq))
    return [" ".join([sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
                     + [c.text for sh in s.shapes if sh.has_table for r in sh.table.rows for c in r.cells]) for s in prs.slides]
cod, txt = rodar({"acao": "apresentar", "partida": "Plano 30-60-90 2026-12-04.pptx", "publico": "gestor"})
for trecho in ("Plano 30-60-90 2026-12-04 (apresentação gestor).pptx · 4 slides: Plano em uma página · Próximas 4 semanas · "
               "Como vamos medir · O que preciso de você", "Sem dados gravados", "Sem IDs nem marcações entre colchetes"):
    assert cod == 0 and trecho in txt, (trecho, txt)
g = textos("Plano 30-60-90 2026-12-04 (apresentação gestor).pptx")
assert "Desafio central: O Recomendador não converte benefício" in g[0] and "Comprometido · confiança 6/10" in g[0], g[0]
assert "PEDIDOS" in g[3] and "Patrocínio do plano de conversão" in g[3] and "→ Bruno confirma a janela com TI" in g[3], g[3]
assert "Confiança:" in g[2] and "Execução: S1 40%" in g[2], g[2]
assert not any(re.search(r"\b(?:DL|PG|PF|RB|[RMPKA])\d+\b", x) for x in g), g
cod, txt = rodar({"acao": "apresentar", "partida": "Plano 30-60-90 2026-12-04.pptx", "publico": "time"})
assert cod == 0 and "Quem faz o quê" in txt and "Nada do que é só do gestor" in txt, txt
tm = " ".join(textos("Plano 30-60-90 2026-12-04 (apresentação time).pptx"))
for fora in ("PEDIDOS", "PARAR DE FAZER", "RISCOS", "Patrocínio", "Tarumã no detalhe", "confiança", "Execução"):
    assert fora not in tm, fora
assert "Ana" in tm and "Buriti" in tm and "Comprometido" in tm, tm
assert ns["ler_plano"](str(TMP / "Plano 30-60-90 2026-12-04 (apresentação time).pptx"))[0] is None
cod, txt = rodar({"acao": "apresentar", "partida": "Plano 30-60-90 2026-12-04.pptx", "publico": "diretoria"})
assert cod == 1 and "Nada foi gerado" in txt, txt
cod, txt = rodar({"acao": "apresentar", "plano": carreira, "publico": "gestor"})
assert cod == 1 and "NADA FOI GERADO" in txt and "carreira" in txt, txt
ok("apresentação: gestor com desafio, tipo e confiança, pedidos, riscos e execução; time com quem faz o quê e sem o que "
   "é só do gestor; sem dados gravados e sem IDs; público errado e carreira recusados")

# 9. Plano B: pelo interpretador, com o argv de um kernel
(TMP / "gestao_pedido.json").write_text(json.dumps({"acao": "janelas", "data": "2026-11-13"}), encoding="utf-8")
r = subprocess.run([sys.executable, "-I", "-c",
                    "import os, sys, runpy; os.chdir(sys.argv[1]); sys.argv = ['ipykernel_launcher', '-f', 'k.json'];"
                    "runpy.run_path(%r, run_name='__main__')" % str(SCRIPT), str(TMP)], capture_output=True, text=True)
assert r.returncode == 0 and "90 dias até 05/02/2027" in r.stdout, r.stdout + r.stderr
ok("plano B: o script roda pelo interpretador (runpy) e acha o pedido na pasta de trabalho")

# 10. Validação OOXML, se o validador estiver disponível
validador = pathlib.Path("/mnt/skills/public/pptx/scripts/office/validate.py")
if validador.exists():
    for arq in list(FIX.glob("Plano*.pptx")) + [TMP / "Plano 30-60-90 2026-12-11.pptx", TMP / "Cheio.pptx",
                                                TMP / "Plano 30-60-90 2026-12-04 (apresentação gestor).pptx",
                                                TMP / "Plano 30-60-90 2026-12-04 (apresentação time).pptx"]:
        r = subprocess.run([sys.executable, str(validador), str(arq)], capture_output=True, text=True, cwd=validador.parent)
        assert r.returncode == 0, (arq.name, r.stdout + r.stderr)
    ok("OOXML válido nas fixtures e nos arquivos gerados")

shutil.rmtree(TMP)
print("\nTudo certo.")
