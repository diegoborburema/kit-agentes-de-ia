"""Confere o script da skill pauta-1-1-pptx contra as fixtures, sem o Copilot, do jeito que o agente o usa:
grava um pedido JSON e roda scripts/pauta_1_1_pptx.py.

Uso, na raiz do repositório:
    python gestao/organizador-1-1/testes/conferir_codigo.py

O que confere:
  1. Limites do Agent Builder e script em dia com o código (montar_skills.py --conferir).
  2. O script montado não repete nomes entre os módulos de origem.
  3. Leitura das duas pautas anteriores: para cima (9 linhas, sem combinados) e para baixo (8 linhas, 3 combinados,
     1 marcado como feito), com as prioridades da legenda.
  4. Geração para baixo (exemplo da skill) e para cima com combinados: linhas iguais às pedidas, na ordem,
     perguntas nas notas e quebra em 2 slides quando não cabe.
  5. Recusas: pedido sem campos, seção inválida, arquivo não anexado, ação desconhecida.
  6. Plano B: o script roda pelo interpretador (runpy).
Sai com erro na primeira falha.
"""
import ast
import json
import pathlib
import re
import runpy
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
AQUI = pathlib.Path(__file__).resolve().parent
SCRIPT = AQUI.parent / "pacote/skills/pauta-1-1-pptx/scripts/pauta_1_1_pptx.py"
SKILL = AQUI.parent / "pacote/skills/pauta-1-1-pptx/SKILL.md"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="pauta11-"))
for f in (AQUI.parent / "fixtures").glob("*.pptx"):
    shutil.copy(f, TMP / f.name)  # como os anexos em /mnt/data


def ok(msg):
    print("ok ", msg)


def rodar(pedido):
    (TMP / "pauta_pedido.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), str(TMP / "pauta_pedido.json")], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


# 1. Limites e script em dia
nome_tema = AQUI.parent.name
for cmd in (["conferir_limites.py", nome_tema], ["montar_skills.py", "--conferir"]):
    alvo = next(p for p in (RAIZ / "gestao/_codigo" / cmd[0], RAIZ / "ferramentas" / cmd[0]) if p.exists())
    r = subprocess.run([sys.executable, str(alvo), cmd[1]], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
ok("limites do Agent Builder respeitados; script em dia com o código")

# 1b. Caso de teste 11 (uso real de 16/11): o pedido é gravado em Python, nunca por bash/heredoc
texto_skill = SKILL.read_text(encoding="utf-8")
assert "json.dump" in texto_skill and "Nunca grave o pedido pelo terminal" in texto_skill and "heredoc" in texto_skill
ok("skill manda gravar o pedido em Python e proíbe bash/heredoc (caso 11)")

# 2. Nomes únicos entre os módulos do script montado
fontes = SCRIPT.read_text(encoding="utf-8").split("\n", 1)[0].split("a partir de: ")[1].split(". Não edite")[0].split()
nomes = {}
for f in fontes:
    caminho = RAIZ / f
    for n in ast.parse(caminho.read_text(encoding="utf-8")).body:
        alvos = [n.name] if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else \
            [x.id for a in getattr(n, "targets", []) for x in ast.walk(a) if isinstance(x, ast.Name)]
        for a in alvos:
            nomes.setdefault(a, []).append(f)
repetidos = {k: v for k, v in nomes.items() if len(v) > 1}
assert not repetidos, repetidos
ok(f"script montado de {len(fontes)} módulos, sem nomes repetidos")

# 3. Leitura
cod, txt = rodar({"acao": "ler", "arquivos": ["pauta-anterior.pptx", "PAUTA-ANTERIOR-LIDERADO.pptx"]})
assert cod == 0, txt
lido = json.loads((TMP / "pauta_leitura.json").read_text(encoding="utf-8"))
cima, baixo = lido[0]["pauta"], lido[1]["pauta"]
assert len(cima["linhas"]) == 9 and not cima["combinados"], cima
assert cima["legenda"]["3 PRIORIDADES"] == ["Quimera-7", "Tarumã", "Ipê-Roxo"], cima["legenda"]
assert len(baixo["linhas"]) == 8 and [c["feito"] for c in baixo["combinados"]] == ["✓", "", ""], baixo["combinados"]
assert "Combinados (Quem | O quê | Até | Feito):" in txt and "em aberto" in txt, txt
ok("leitura: para cima 9 linhas sem combinados; para baixo 8 linhas e 3 combinados (1 feito); legenda; maiúsculas no nome")

# 4. Geração
ns = {}
exemplo = re.search(r"Exemplo do pedido de geração.*?~~~python\n(.*?)~~~", SKILL.read_text(encoding="utf-8"), re.S)[1]
exec(exemplo, ns)
cod, txt = rodar(ns["pedido"])
assert cod == 0 and "(iguais às pedidas, na ordem)" in txt and "Perguntas para levar nas notas: sim" in txt, txt
assert (TMP / ns["pedido"]["saida"]).exists(), txt
ok("geração para baixo (exemplo da skill): linhas iguais às pedidas, perguntas nas notas")

secao = {"Quimera-7": "P1", "Tarumã": "P2", "Ipê-Roxo": "P3", "Pessoas": "PESSOAS", "Carga & bem-estar": "TEMA"}
pauta_cima = {"direcao": "cima", "usuario": "Lucas", "pessoa": "Gustavo", "semana": "02–06/11/2026",
              "prioridades": ["Quimera-7", "Tarumã", "Ipê-Roxo"], "tema_semana": "Carga & bem-estar",
              "linhas": [{"secao": secao.get(l["categoria"], "PROJETOS"), "categoria": l["categoria"], "tema": l["tema"],
                          "atualizacao": l["texto"], "tipo": l["tipo"],
                          "status": l["status"] if l["status"] in ("verde", "amarelo", "vermelho") else ""}
                         for l in cima["linhas"]],
              "combinados": [{"quem": "Lucas", "oque": "Enviar o modelo de PRD atualizado", "ate": "03/11"}],
              "notas": ["Perguntas para levar", "1. a", "2. b", "3. c"]}
cod, txt = rodar({"acao": "gerar", "saida": "1-1 Gustavo 2026-11-05.pptx", "pauta": pauta_cima})
assert cod == 0 and "· 2 slide(s)" in txt and "(iguais às pedidas, na ordem)" in txt and "Combinados: 1 em aberto" in txt, txt
ok("geração para cima com combinado: 2 slides, linhas na ordem, combinado em aberto")

# 5. Recusas
cod, txt = rodar({"acao": "gerar", "pauta": {"direcao": "lado"}})
assert cod == 1 and "NADA FOI GERADO" in txt and "falta o campo 'pessoa'" in txt and "direcao deve ser" in txt, txt
cod, txt = rodar({"acao": "gerar", "pauta": dict(pauta_cima, linhas=[{"secao": "X", "tema": "t"}])})
assert cod == 1 and "secao 'X' inválida" in txt, txt
cod, txt = rodar({"acao": "ler", "arquivos": ["nao-existe.pptx"]})
assert "não está em" in txt and "anexar" in txt, txt
cod, txt = rodar({"acao": "voar"})
assert cod == 2 and "Ação desconhecida" in txt, txt
ok("recusas: campos faltando, seção inválida, arquivo não anexado, ação desconhecida")

# 6. Plano B: pelo interpretador, com o pedido na pasta de trabalho
import os
antes = os.getcwd()
os.chdir(TMP)
(TMP / "pauta_pedido.json").write_text(json.dumps({"acao": "ler", "arquivos": ["pauta-anterior.pptx"]}), encoding="utf-8")
argv = sys.argv
sys.argv = ["ipykernel_launcher.py", "-f", "/tmp/kernel.json"]
try:
    runpy.run_path(str(SCRIPT), run_name="__main__")
except SystemExit as e:
    assert not e.code, e.code
finally:
    sys.argv = argv
    os.chdir(antes)
ok("plano B: o script roda pelo interpretador (runpy) e acha o pedido na pasta de trabalho")

shutil.rmtree(TMP, ignore_errors=True)
print("\nTudo certo.")
