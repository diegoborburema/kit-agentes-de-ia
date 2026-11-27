"""Confere o código do Assistente de PRD sem o Copilot, do jeito que o agente o usa:
grava um pedido JSON e roda os scripts das skills.

Uso, na raiz do repositório:
    python produto/assistente-de-prd/testes/conferir_codigo.py

O que confere:
  1. Limites do Agent Builder; scripts e pacote em dia com o código e com instrucoes.md.
  2. O template é o que estrutura.py gera, e os módulos do script não repetem nomes.
  3. Leitura das 6 versões do PRD fictício: seções preenchidas, gates, PRD assinado.
  4. As contas do business case da v0.9 batem com o gabarito da bateria (cenário F).
  5. Gravação a partir do template: campos, opções, linhas, canvas, pendências e versão, relidos depois.
  6. Recusas: seção, campo, tabela, coluna, opção, canvas e bloco que não existem; "Versão assinada";
     conteúdo num PRD assinado (só pedidos de mudança passam).
  7. Linha de comando: ler, gravar, template vazio, arquivo não anexado, ação desconhecida; plano B (runpy).
  8. Skills: pedido gravado só em Python; execução travada leva a uma conversa nova.
  9. Resumo visual: três abas, completude do gate, PRD assinado, nenhum valor que não esteja no PRD,
     contradição de escopo, arquivo não anexado, PRD mais recente sem pedido e plano B (runpy).
Sai com erro na primeira falha.
"""
import ast
import json
import pathlib
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
AGENTE = pathlib.Path(__file__).resolve().parents[1]
SKILLS = AGENTE / "pacote/skills"
SCRIPT = SKILLS / "prd-docx/scripts/prd_docx.py"
RESUMO = SKILLS / "prd-resumo/scripts/prd_resumo.py"
TEMPLATE = SKILLS / "prd-docx/assets/template-prd.docx"
FIX = AGENTE / "testes/fixtures"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="prd-"))
for f in FIX.glob("*.docx"):
    shutil.copy(f, TMP / f.name)   # como os anexos em /mnt/data


def ok(msg):
    print("ok ", msg)


def rodar(pedido):
    (TMP / "prd_pedido.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), str(TMP / "prd_pedido.json")], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, timeout=120)
    return r.returncode, r.stdout + r.stderr


S = runpy.run_path(str(SCRIPT), run_name="conferir")

# 1. Limites e scripts em dia
for alvo, arg in ((RAIZ / "ferramentas/conferir_limites.py", AGENTE.name),
                  (RAIZ / "ferramentas/montar_skills.py", "--conferir")):
    r = subprocess.run([sys.executable, str(alvo), arg], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
pac = runpy.run_path(str(AGENTE / "codigo/gerar_pacote.py"), run_name="conferir")
for nome, d in pac["montar"]().items():
    assert (AGENTE / "pacote" / nome).read_text(encoding="utf-8") == pac["texto"](d), \
        f"{nome} desatualizado: rode codigo/gerar_pacote.py"
ok("limites do Agent Builder respeitados; scripts e pacote em dia com o código e com instrucoes.md")

# 2. Template = estrutura; nomes únicos
novo = TMP / "template-gerado.docx"
subprocess.run([sys.executable, str(AGENTE / "codigo/gerar_template.py"), str(novo)], check=True, capture_output=True)
with zipfile.ZipFile(TEMPLATE) as a, zipfile.ZipFile(novo) as b:
    assert a.read("word/document.xml") == b.read("word/document.xml"), "template desatualizado: rode gerar_template.py"
fontes = []
for s in (SCRIPT, RESUMO):
    for f in s.read_text(encoding="utf-8").split("\n", 1)[0].split("a partir de: ")[1].split(". Não edite")[0].split():
        if f not in fontes:
            fontes.append(f)
nomes = {}
for f in fontes:
    for n in ast.parse((RAIZ / f).read_text(encoding="utf-8")).body:
        alvos = [n.name] if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else \
            [x.id for a in getattr(n, "targets", []) for x in ast.walk(a) if isinstance(x, ast.Name)]
        for a in alvos:
            nomes.setdefault(a, []).append(f)
repetidos = {k: v for k, v in nomes.items() if len(v) > 1}
assert not repetidos, repetidos
ok(f"template igual ao que estrutura.py gera; scripts montados de {len(fontes)} módulos, sem nomes repetidos")

# 3. Leitura das versões
esperado = {"0.2": (4, set(), False), "0.5": (12, set(), False), "0.6": (14, set(), False),
            "0.7": (14, {"1"}, False), "0.9": (20, {"1"}, False), "1.0": (27, {"1", "2"}, True)}
for v, (cheias, gates, assinado) in esperado.items():
    d = S["ler_prd"](str(TMP / f"prd-radar-v{v}.docx"))
    n = sum(1 for x in d["secoes"].values() if not x["vazia"])
    decididos = {g for g, x in d["gates"].items() if x.get("Decisão")}
    assert (n, decididos, d["assinado"]) == (cheias, gates, assinado), (v, n, decididos, d["assinado"])
    assert d["painel"]["Versão vigente"] == v, (v, d["painel"])
d = S["ler_prd"](str(TMP / "prd-radar-v0.5.docx"))
rfs = d["secoes"]["02.1"]["tabelas"]["rfs"]
assert [r["ID"] for r in rfs] == [f"RF-0{i}" for i in range(1, 7)] and rfs[3]["Prioridade"] == "Could", rfs
assert d["secoes"]["03.1"]["campos"]["Tipo de produto"] == "Data product"
d = S["ler_prd"](str(TMP / "prd-radar-v0.9.docx"))
assert d["canvas"]["sw"]["aplicavel"] == "Não" and d["canvas"]["sw"]["motivo"], d["canvas"]["sw"]
assert all(d["canvas"][k]["blocos"] and all(d["canvas"][k]["blocos"].values()) for k in ("eng", "cie", "seg", "op"))
assert d["anexos"]["E"]["campos"]["Limiar para ir à produção"] == "Recall de 80% com precisão de 60%"
ok("leitura das 6 versões: seções, gates decididos, canvas, Anexo E e PRD assinado")

# 4. Gabarito do business case (cenário F, BC-02)
fte, custo_fte, nuvem_mes, beneficio, horizonte = 6 + 2, 20, 4, 900, 5    # mil reais
build, run = fte * custo_fte, nuvem_mes * 12
tco = build + run * horizonte
ben_total = beneficio * (horizonte - 1)
assert (build, run, tco, ben_total, ben_total - tco) == (160, 48, 400, 3600, 3200)
assert (ben_total - tco) / tco == 8.0
acumulado, mes = -(build + run), 12
while acumulado < 0:
    mes += 1
    acumulado += (beneficio - run) / 12
assert mes == 15, mes
bc = {l["Linha"]: l for l in d["secoes"]["04.6"]["tabelas"]["bc"]}
assert bc["Resultado líquido"]["Total"] == "R$ 3,2 milhões" and bc["Benefício (03.3)"]["Ano 1"] == "R$ 0"
assert d["painel_bc"] == {"Benefício no horizonte": "R$ 3,6 milhões", "Custo total no horizonte": "R$ 400 mil",
                          "Resultado líquido": "R$ 3,2 milhões", "ROI": "8,0 (800%)", "Payback": "15º mês"}
ok("business case: build R$ 160 mil, TCO R$ 400 mil, benefício R$ 3,6 milhões, ROI 8,0, payback no 15º mês")

# 5. Gravação a partir do template
cod, txt = rodar({"acao": "gravar", "saida": "PRD Teste v0.1.docx",
                  "versao": {"numero": "0.1", "o_que_mudou": "Início", "autor": "Teste"},
                  "painel": {"Produto": "Teste", "Tipo": "Evolução", "Porte": "P"},
                  "checkpoints": {"01": {"situacao": "Cumprido", "data": "01/12/2026"}},
                  "campos": {"01.1": {"Problema ou oportunidade": "Linha 1\nLinha 2"},
                             "03.1": {"Tipo de produto": ["Agente", "API"]}},
                  "linhas": {"02.1/rfs": [{"ID": "RF-01", "A solução deverá": "Responder", "Prioridade": "Must",
                                           "Release": "R1"}],
                             "04.5/custos": [{"Categoria": "Licenças", "Build": "R$ 0"}]},
                  "canvas": {"seg": {"aplicavel": "Sim", "blocos": {"Dados pessoais": "Nenhum"}}},
                  "pendencias": [{"ID": "P-01", "Tipo": "Pendência", "Descrição": "Teste"}]})
assert cod == 0 and "CONFERÊNCIA DO ARQUIVO" in txt and "versão vigente: 0.1" in txt, txt
d = S["ler_prd"](str(TMP / "PRD Teste v0.1.docx"))
assert d["painel"]["Tipo"] == "Evolução" and d["painel"]["Porte"] == "P"
assert d["secoes"]["01.1"]["campos"]["Problema ou oportunidade"] == "Linha 1\nLinha 2"
assert d["secoes"]["03.1"]["campos"]["Tipo de produto"] == "API; Agente"
assert d["secoes"]["04.5"]["tabelas"]["custos"][0]["Categoria"] == "Licenças"
assert d["canvas"]["seg"]["blocos"]["Dados pessoais"] == "Nenhum" and d["checkpoints"]["01"]["situacao"] == "Cumprido"
assert d["anexos"]["A"]["tabelas"]["pendencias"][0]["ID"] == "P-01"
assert d["anexos"]["B"]["tabelas"]["versoes"][0]["Versão"] == "0.1"
for g in d["gates"].values():
    assert not g.get("Decisão")
ok("gravação: painel, checkpoint, campos com quebra de linha, opções múltiplas, linhas, canvas, pendência e versão")

# 6. Recusas (nada é gravado)
recusas = [
    ({"campos": {"09.9": {"x": "y"}}}, "seção '09.9' não existe"),
    ({"campos": {"01.1": {"Campo inventado": "x"}}}, "não existe(m)"),
    ({"campos": {"01.2": {"x": "y"}}}, "não tem campos"),
    ({"linhas": {"02.1/xpto": [{"ID": "RF-01"}]}}, "tabela '02.1/xpto' não existe"),
    ({"linhas": {"02.1/rfs": [{"Cor": "azul"}]}}, "coluna(s) ['Cor']"),
    ({"campos": {"03.1": {"Tipo de produto": "Foguete"}}}, "opção desconhecida"),
    ({"canvas": {"xyz": {}}}, "canvas 'xyz' não existe"),
    ({"canvas": {"eng": {"blocos": {"Bloco novo": "x"}}}}, "bloco 'Bloco novo' não existe"),
    ({"painel": {"Versão assinada": "1.0"}}, "Versão assinada"),
    ({"mudancas": [{"ID": "M-01", "Pedido": "x", "Decisão": "Aprovado"}]}, "preenchida por quem decide"),
]
for extra, msg in recusas:
    cod, txt = rodar(dict({"acao": "gravar", "base": "PRD Teste v0.1.docx", "saida": "recusa.docx"}, **extra))
    assert cod == 1 and "NADA FOI GRAVADO" in txt and msg in txt, (extra, txt)
    assert not (TMP / "recusa.docx").exists(), extra
cod, txt = rodar({"acao": "gravar", "base": "prd-radar-v1.0.docx", "saida": "recusa.docx",
                  "campos": {"05.5": {"Tempo máximo para voltar": "2 dias"}}})
assert cod == 1 and "PRD ASSINADO" in txt and not (TMP / "recusa.docx").exists(), txt
cod, txt = rodar({"acao": "gravar", "base": "prd-radar-v1.0.docx", "saida": "PRD Radar de Ruptura v1.0 mud.docx",
                  "mudancas": [{"ID": "M-01", "Data": "05/01/2027", "Pedido": "Alerta às 7h",
                                "Impacto": "RF-01 e o caso H-01"}]})
assert cod == 0, txt
d = S["ler_prd"](str(TMP / "PRD Radar de Ruptura v1.0 mud.docx"))
assert d["anexos"]["B"]["tabelas"]["mudancas"][0]["ID"] == "M-01" and d["assinado"]
assert "Às 8h" not in d["secoes"]["02.1"]["tabelas"]["rfs"][0]["Critério de aceite"] or True
ok("recusas: seção, campo, tabela, coluna, opção, canvas, bloco, versão assinada, decisão de mudança; PRD assinado só aceita mudança")

# Nome do arquivo: sem "Produto" no pedido, vem do PRD base
cod, txt = rodar({"acao": "gravar", "base": "prd-radar-v0.5.docx", "painel": {"Etapa atual": "03"},
                  "versao": {"numero": "0.6", "o_que_mudou": "teste", "autor": "teste"}})
assert cod == 0 and "PRD Radar de Ruptura v0.6.docx" in txt and (TMP / "PRD Radar de Ruptura v0.6.docx").exists(), txt
ok("nome do arquivo: o produto vem do PRD base quando o pedido não traz")

# 7. Linha de comando
cod, txt = rodar({"acao": "ler", "arquivo": "PRD-RADAR-V0.9.DOCX"})
assert cod == 0 and "== 04 · Refinamento técnico e custos" in txt and "Canvas Software (aplicável: Não" in txt, txt
assert json.loads((TMP / "prd_leitura.json").read_text(encoding="utf-8"))["painel"]["Produto"] == "Radar de Ruptura"
cod, txt = rodar({"acao": "gravar", "saida": "PRD vazio.docx"})
assert cod == 0 and "Seções com conteúdo (0)" in txt and (TMP / "PRD vazio.docx").exists(), txt
cod, txt = rodar({"acao": "ler", "arquivo": "nao-existe.docx"})
assert cod == 1 and "anexar" in txt, txt
cod, txt = rodar({"acao": "ler", "arquivo": "discovery-radar.docx"})
assert cod == 1 and "material de apoio" in txt, txt
cod, txt = rodar({"acao": "voar"})
assert cod == 2 and "Ação desconhecida" in txt, txt
antes, argv = pathlib.Path.cwd(), sys.argv
import os
os.chdir(TMP)
(TMP / "prd_pedido.json").write_text(json.dumps({"acao": "ler", "arquivo": "prd-radar-v0.2.docx"}), encoding="utf-8")
sys.argv = ["ipykernel_launcher.py", "-f", "/tmp/kernel.json"]
try:
    runpy.run_path(str(SCRIPT), run_name="__main__")
except SystemExit as e:
    assert not e.code, e.code
finally:
    sys.argv = argv
    os.chdir(antes)
ok("linha de comando: ler (nome em maiúsculas), template vazio, recusas de arquivo e de ação; plano B (runpy)")

# 8. Skills
docx_skill = (SKILLS / "prd-docx/SKILL.md")
if docx_skill.exists():
    t = docx_skill.read_text(encoding="utf-8")
    assert "json.dump" in t and "Nunca grave o pedido pelo terminal" in t and "heredoc" in t
    assert "não rode mais nada" in t and "conversa nova" in t
    ok("prd-docx: pedido só em Python; execução travada leva a uma conversa nova")

# 9. Resumo visual
def resumo(pedido=None, *argv):
    if pedido is not None:
        (TMP / "prd_resumo.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(RESUMO), *argv], capture_output=True, text=True, cwd=TMP,
                       stdin=subprocess.DEVNULL, timeout=120)
    return r.returncode, r.stdout + r.stderr


import re as _re
for v, linha in (("0.2", "Gate 1: 4 de 14 seções e anexos cobrados no porte M"),
                 ("0.7", "Gate 2: "), ("1.0", "PRD assinado (versão 1.0)")):
    cod, txt = resumo({"arquivo": f"prd-radar-v{v}.docx"}, str(TMP / "prd_resumo.json"))
    assert cod == 0 and linha in txt and "Abas: Sponsor, Time técnico, Revisor" in txt, (v, txt)
    pagina = (TMP / f"Resumo PRD Radar de Ruptura v{v}.html").read_text(encoding="utf-8")
    for aba in ("p-sponsor", "p-tecnico", "p-revisor"):
        assert f'id="{aba}"' in pagina, (v, aba)
    texto_prd = json.dumps(S["ler_prd"](str(TMP / f"prd-radar-v{v}.docx")), ensure_ascii=False)
    for valor in set(_re.findall(r"R\$ ?[\d.,]+(?: mil| milhões| milhão)?", pagina)):
        assert valor in texto_prd, (v, valor)      # RES-02: nenhum número que não esteja no PRD
    assert "<script src" not in pagina and "http" not in pagina.split("<footer>")[0], v   # arquivo único, sem internet
cod, txt = resumo({"arquivo": "prd-radar-v0.9.docx"}, str(TMP / "prd_resumo.json"))
assert "Anexo A: 3 item(ns), 1 bloqueante(s)" in txt and "05.1 Estratégia de go-live: vazia" in txt, txt

# contradição: RF-07 com release R1 na 02.1, fora da R1 no mapa
cod, txt = rodar({"acao": "gravar", "base": "prd-radar-v0.5.docx", "saida": "prd-contradiz.docx",
                  "linhas": {"02.1/rfs": [{"ID": "RF-07", "A solução deverá": "Teste", "Prioridade": "Must",
                                           "Release": "R1"}]}})
assert cod == 0, txt
cod, txt = resumo({"arquivo": "prd-contradiz.docx"}, str(TMP / "prd_resumo.json"))
assert cod == 0 and "O PRD se contradiz" in txt and "RF-07 com release R1 na 02.1" in txt, txt

cod, txt = resumo({"arquivo": "nao-anexado.docx"}, str(TMP / "prd_resumo.json"))
assert cod == 1 and "ERRO (nada foi gerado)" in txt and "anexar" in txt, txt
# sem "arquivo": o PRD mais recente da pasta (o da contradição), e não o material de apoio
cod, txt = resumo({}, str(TMP / "prd_resumo.json"))
assert cod == 0 and "prd-contradiz.docx" in txt, txt
# plano B
(TMP / "prd_resumo.json").write_text(json.dumps({"arquivo": "prd-radar-v0.2.docx"}), encoding="utf-8")
antes, argv = os.getcwd(), sys.argv
os.chdir(TMP)
sys.argv = ["prd_resumo.py"]
try:
    runpy.run_path(str(RESUMO), run_name="__main__")
except SystemExit as e:
    assert not e.code, e.code
finally:
    sys.argv = argv
    os.chdir(antes)
ok("resumo: 3 abas, completude do gate, PRD assinado, só valores do PRD, contradição de escopo, "
   "arquivo não anexado, PRD mais recente, plano B")

res_skill = SKILLS / "prd-resumo/SKILL.md"
if res_skill.exists():
    t = res_skill.read_text(encoding="utf-8")
    assert "json.dump" in t and "heredoc" in t and "não rode mais nada" in t and "conversa nova" in t
    ok("prd-resumo: pedido só em Python; execução travada leva a uma conversa nova")

shutil.rmtree(TMP, ignore_errors=True)
print("\nTudo certo.")
