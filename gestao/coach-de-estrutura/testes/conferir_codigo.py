"""Confere o script da skill estrutura-pptx contra as fixtures, sem o Copilot, do jeito que o agente o usa:
grava um pedido JSON e roda scripts/estrutura_pptx.py.

Uso, na raiz do repositório:
    python gestao/coach-de-estrutura/testes/conferir_codigo.py

O que confere:
  1. Limites do Agent Builder e script em dia com gestao/_codigo/.
  2. O script montado não repete nomes entre os módulos de origem.
  3. Leitura dos planos de 13/11 e 04/12 (ler_plano do Coach de Gestão), com o sinal da Ana em 3 frentes.
  4. Carga do mapa ditado: Ana 110% (acima), Bruno 100%, Caio 100%; Hub Logístico sem dono; Caio com autonomia baixa
     e sem apoio no piloto.
  5. Geração da análise de 13/11: releitura igual à fixture; "Confidencial" nos 3 slides; interesses fora do arquivo,
     inclusive dos dados ocultos.
  6. Recusas: rótulo, mudança formal, motivo de saúde, apoio sem prazo, teste sem critério.
  7. Revisão do teste (Cenário C): T1 atingido, T2 não; teste sem resultado recusado.
  8. Restrição de disponibilidade sem motivo (SAU-01): a carga do Caio passa do disponível.
  9. Plano B: o script roda pelo interpretador (runpy, com o argv de um kernel).
Sai com erro na primeira falha.
"""
import ast
import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
AQUI = pathlib.Path(__file__).resolve().parent
FIX = AQUI / "fixtures"
SCRIPT = RAIZ / "gestao/coach-de-estrutura/pacote/skills/estrutura-pptx/scripts/estrutura_pptx.py"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="estrutura-"))
for f in FIX.iterdir():
    shutil.copy(f, TMP / f.name)  # como os anexos em /mnt/data
ANALISE = "Estrutura 2026-11-13 (confidencial).pptx"


def ok(msg):
    print("ok  " + msg)


def rodar(pedido):
    """Grava o pedido e roda o script, como o agente faz. Devolve (código de saída, texto impresso)."""
    (TMP / "estrutura_pedido.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(TMP / "estrutura_pedido.json")],
                       capture_output=True, text=True, cwd=TMP)
    return r.returncode, r.stdout + r.stderr


def texto_do_arquivo(caminho):
    """Todo o texto do .pptx, inclusive notas e dados ocultos."""
    with zipfile.ZipFile(caminho) as z:
        return " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))


# 1. Limites e fonte única
for cmd in (["ferramentas/conferir_limites.py", "coach-de-estrutura"], ["ferramentas/montar_skills.py", "--conferir"]):
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

# 3. Leitura dos planos
cod, txt = rodar({"acao": "ler", "arquivos": ["Plano 30-60-90 2026-11-13.pptx", "Plano 30-60-90 2026-12-04.pptx",
                                              ANALISE]})
assert cod == 0, txt
for trecho in ("Plano 30-60-90 de 13/11/2026 · ciclo 1, semana 1 de 4", "Plano 30-60-90 de 04/12/2026 · ciclo 1, semana 4 de 4",
               "DL1 delegação · Ana · Tarumã", "K5 Pessoas do time em mais de 2 frentes",
               "Sinal de estrutura do plano: Ana em 3 frentes (Tarumã, Painel Jatobá, Previsão de Ruptura)",
               "Análise de estrutura de 13/11/2026", "T2 · nível 4"):
    assert trecho in txt, (trecho, txt)
ok("leitura: planos de 13/11 e 04/12 com o sinal da Ana; análise anterior")

# 4. Carga do mapa ditado
cod, txt = rodar({"acao": "carga", "mapa": gf.MAPA})
for trecho in ("Ana: 110% em 3 frentes", "ACIMA de 100%", "Bruno: 100% em 3 frentes", "Caio: 100% em 2 frentes",
               "Frentes sem dono: Hub Logístico", "Dono com autonomia baixa e sem apoio na frente: Caio em Piloto do Ipê Triagem",
               "Ana: Tarumã, Painel Jatobá, Previsão de Ruptura"):
    assert trecho in txt, (trecho, txt)
assert "Bruno: 100% em 3 frentes (Quimera-7, Integração Pitanga, Hub Logístico) · ACIMA" not in txt
ok("carga: Ana 110% (acima), Bruno e Caio 100%; Hub sem dono; Caio com autonomia baixa e sem apoio")

# 5. Geração da análise de 13/11
com_interesse = copy.deepcopy(gf.ESTRUTURA_1311)
com_interesse["interesses"] = [{"pessoa": "Ana", "interesse": "Visualização de Dados em 2027"}]
cod, txt = rodar({"acao": "gerar", "estrutura": com_interesse})
assert cod == 0, txt
for trecho in ("Arquivo: Estrutura 2026-11-13 (confidencial).pptx · 3 slides · \"Confidencial\" em 3 de 3 · releitura sem diferença",
               "Mapa: 8 linhas, 3 pessoas · carga: Ana 110% (acima), Bruno 100%, Caio 100%",
               "Tarumã: foco + capacidade; P2 Ipê-Roxo: autonomia", "T1 Pausar a Previsão de Ruptura até 18/12 · revisão em 11/12",
               "Interesses de desenvolvimento não são gravados no arquivo"):
    assert trecho in txt, (trecho, txt)
gerado = TMP / ANALISE
assert "Visualização de Dados" not in texto_do_arquivo(gerado), "o interesse vazou para o arquivo"
assert ns["ler_estrutura"](str(gerado)) == ns["ler_estrutura"](str(FIX / ANALISE))
ok("análise de 13/11: relida igual à fixture; Confidencial nos 3 slides; Visualização de Dados fora do arquivo, inclusive dos dados ocultos")

# 6. Recusas
def recusa(mudar, motivo):
    e = copy.deepcopy(gf.ESTRUTURA_1311)
    mudar(e)
    cod, txt = rodar({"acao": "gerar", "estrutura": e, "saida": "X.pptx"})
    assert cod == 1 and "NADA FOI GERADO" in txt and motivo in txt and not (TMP / "X.pptx").exists(), (motivo, txt)


recusa(lambda e: e["achados"].append("O Bruno é fraco em gestão"), "Rótulo sobre pessoa")
recusa(lambda e: e["decisao"].update(texto="O Caio passa a reportar ao Bruno"), "Mudança formal")
recusa(lambda e: e["decisao"]["testes"].append({"id": "T3", "movimento": "Contratar mais um analista", "nivel": 4, "criterio": "x",
                                                "inicio": "2026-11-23", "revisao": "2026-12-18", "ate": "2026-12-18",
                                                "escopo": "x", "saida": "x"}), "Mudança formal")
recusa(lambda e: e["restricoes"].append({"pessoa": "Caio", "disponivel_pct": 50, "ate": "2027-01-15", "motivo": "tratamento"}),
       "sem o motivo")
recusa(lambda e: e["restricoes"].append({"pessoa": "Caio", "disponivel_pct": 50, "ate": "2027-01-15",
                                         "fonte": "[Usuário · 13/11] tratamento de saúde"}), "saúde")
recusa(lambda e: e["decisao"]["testes"][1].pop("ate"), "apoio sem prazo")
recusa(lambda e: e["decisao"]["testes"][0].pop("criterio"), "falta criterio")
recusa(lambda e: e["diagnostico"][0].update(causa="preguiça"), "causa")
ok("recusas: rótulo, mudança formal (reporte e contratação), motivo na restrição, saúde, apoio sem prazo, teste sem critério, causa fora da lista")

# 7. Revisão do teste (Cenário C)
rev = {"data": "2026-12-11", "resultados": {
    "T1": {"atingido": True, "evidencia": "testes do Buriti em 09/12; entrega em 18/12", "fonte": "[Usuário · 11/12]"},
    "T2": {"atingido": False, "evidencia": "piloto em 1 de 2 lojas; a segunda ficou para janeiro", "fonte": "[Usuário · 11/12]"}}}
falta = copy.deepcopy(rev)
del falta["resultados"]["T2"]
cod, txt = rodar({"acao": "gerar", "partida": ANALISE, "revisao": falta, "saida": "X.pptx"})
assert cod == 1 and "Teste T2 sem resultado" in txt, txt
cod, txt = rodar({"acao": "gerar", "partida": ANALISE, "revisao": rev})
assert cod == 0, txt
for trecho in ("Estrutura 2026-12-11 (confidencial).pptx · 3 slides · \"Confidencial\" em 3 de 3", "T1 atingido", "T2 NÃO atingido",
               "· atingido", "· não atingido", "Histórico: 2 registro(s)", "Mapa: 8 linhas"):
    assert trecho in txt, (trecho, txt)
ok("revisão de 11/12: T1 atingido e T2 não, no histórico; mapa mantido; teste sem resultado recusado")

# 8. Restrição de disponibilidade sem motivo (SAU-01)
cod, txt = rodar({"acao": "gerar", "partida": ANALISE, "data": "2026-11-20", "saida": "Restricao.pptx",
                  "atualizar": {"restricoes": [{"pessoa": "Caio", "disponivel_pct": 50, "ate": "2027-01-15", "fonte": "[Usuário · 20/11]"}]}})
assert cod == 0 and "Caio 100% (acima)" in txt, txt
cod, txt = rodar({"acao": "carga", "partida": "Restricao.pptx"})
assert "Caio: 100% em 2 frentes (Piloto do Ipê Triagem, Sustentação) · disponível 50% até 15/01 · ACIMA de 50%" in txt, txt
ok("restrição sem motivo: Caio disponível 50% até 15/01, carga acima do disponível")

# 9. Plano B: pelo interpretador, com o argv de um kernel
(TMP / "estrutura_pedido.json").write_text(json.dumps({"acao": "carga", "partida": ANALISE}), encoding="utf-8")
r = subprocess.run([sys.executable, "-I", "-c",
                    "import os, sys, runpy; os.chdir(sys.argv[1]); sys.argv = ['ipykernel_launcher', '-f', 'k.json'];"
                    "runpy.run_path(%r, run_name='__main__')" % str(SCRIPT), str(TMP)], capture_output=True, text=True)
assert r.returncode == 0 and "Ana: 110% em 3 frentes" in r.stdout, r.stdout + r.stderr
ok("plano B: o script roda pelo interpretador (runpy) e acha o pedido na pasta de trabalho")

# 10. Validação OOXML, se o validador estiver disponível
validador = pathlib.Path("/mnt/skills/public/pptx/scripts/office/validate.py")
if validador.exists():
    for arq in (FIX / ANALISE, TMP / "Estrutura 2026-12-11 (confidencial).pptx"):
        r = subprocess.run([sys.executable, str(validador), str(arq)], capture_output=True, text=True, cwd=validador.parent)
        assert r.returncode == 0, (arq.name, r.stdout + r.stderr)
    ok("OOXML válido na fixture e no arquivo da revisão")

shutil.rmtree(TMP)

# SCR-02 (uso real do 1-1 em 16/11): o pedido é gravado em Python, nunca por bash/heredoc
_skill_txt = (RAIZ / "gestao/coach-de-estrutura/pacote/skills/estrutura-pptx/SKILL.md").read_text(encoding="utf-8")
assert "json.dump" in _skill_txt and "Nunca grave o pedido pelo terminal" in _skill_txt and "heredoc" in _skill_txt
ok("skill manda gravar o pedido em Python e proíbe bash/heredoc (SCR-02)")
print("\nTudo certo.")
