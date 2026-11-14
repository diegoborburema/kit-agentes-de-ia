"""Confere o script da skill ata-transcricao contra as fixtures, sem o Copilot, do jeito que o agente o usa:
grava um pedido JSON e roda scripts/atas_transcricao.py.

Uso, na raiz do repositório:
    python produto/redator-de-atas/testes/conferir_codigo.py

O que confere:
  1. Limites do Agent Builder e script em dia com o código (montar_skills.py --conferir).
  2. O script montado não repete nomes entre os módulos de origem.
  3. Leitura das quatro reuniões:
     A (.docx do Teams): 74 falas, 6 pessoas e a sala, nomes em ordem natural, Paula como externa, convidados sem
       fala (Marcos Vieira, Gustavo Lima e Helena Costa), 2 blocos e a última ação (Bruno e Caio) no bloco 2;
     B (.vtt): 22 falas, 5 falantes, sem id de deixa no texto e com as deixas partidas juntadas;
     C (notas coladas): sem falantes, 5 presentes com área, Gustavo só convidado, sem HTML nem [Event];
     D (.docx): 19 falas e 4 falantes.
  4. Busca: a tolerância de 15% e a correção para 12%, com o falante e o vizinho.
  5. Conferência: as quatro atas esperadas sem nada para corrigir e com as perguntas certas; a ata com defeitos
     do Cenário A com os 9 defeitos apontados; status de homologação não declarado; conferência sem leitura.
  6. Recusas: arquivo não anexado, trecho antes da leitura, ação desconhecida.
  7. Plano B: o script roda pelo interpretador (runpy, com o argv de um kernel).
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

RAIZ = pathlib.Path(__file__).resolve().parents[3]
AQUI = pathlib.Path(__file__).resolve().parent
FIX = AQUI / "fixtures"
SCRIPT = RAIZ / "produto/redator-de-atas/pacote/skills/ata-transcricao/scripts/atas_transcricao.py"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="atas-"))
for f in FIX.iterdir():
    shutil.copy(f, TMP / f.name)  # como os anexos em /mnt/data

A = "Refinamento Painel Jatoba 2026-11-10.docx"
B = "Homologacao Taruma Modulo 4 2026-11-11.vtt"
C = "Notas Discovery Previsao de Ruptura 2026-11-05.txt"
D = "Alinhamento Quimera-7 2026-11-09.docx"
CONVITE_A = ["Lucas Andrade", "Ana Souza", "Bruno Prado", "Caio Teles", "Renata Okada", "Paula Reis",
             "Vieira,Marcos,BR-São Paulo", "Lima,Gustavo,BR-São Paulo", "Helena Costa"]


def ok(msg):
    print("ok  " + msg)


def rodar(pedido, pasta=TMP):
    """Grava o pedido e roda o script, como o agente faz. Devolve (código de saída, texto impresso)."""
    (pasta / "ata_pedido.json").write_text(json.dumps(pedido, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(pasta / "ata_pedido.json")],
                       capture_output=True, text=True, cwd=pasta)
    assert r.returncode == 0 and "Traceback" not in r.stderr, r.stdout + r.stderr
    return r.stdout


def leitura():
    return json.loads((TMP / "ata_leitura.json").read_text(encoding="utf-8"))


def pontos(saida, grupo):
    """Linhas de um grupo da conferência ('Corrija', 'Leve' ou 'Para saber')."""
    linhas, dentro = [], False
    for ln in saida.splitlines():
        if not ln.startswith("  - "):
            dentro = ln.startswith(grupo)
            continue
        if dentro:
            linhas.append(ln[4:])
    return linhas


# 1. Limites e script em dia
for cmd in (["ferramentas/conferir_limites.py", "redator-de-atas"], ["ferramentas/montar_skills.py", "--conferir"]):
    r = subprocess.run([sys.executable, str(RAIZ / cmd[0]), cmd[1]], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
ok("limites do Agent Builder respeitados; script em dia com o código")

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

# 3A. Refinamento (.docx do Teams)
s = rodar({"acao": "ler", "arquivos": [A], "convidados": CONVITE_A})
L = leitura()
assert "74 falas · 6 falantes · 2 bloco(s)" in s, s
assert L["titulo"] == "Refinamento Painel Jatobá – Onda 2" and L["data"] == "2026-11-10", (L["titulo"], L["data"])
fal = {f["nome"]: f for f in L["falantes"]}
assert list(fal) == ["Lucas Andrade", "Ana Souza", "Bruno Prado", "Caio Teles", "Renata Okada", "Paula Reis",
                     "Sala SP-12A"], list(fal)
assert fal["Paula Reis"]["marca"] == "externo" and fal["Sala SP-12A"]["marca"] == "sala"
assert fal["Renata Okada"]["falas"] == 19 and fal["Sala SP-12A"]["ids"] == ["T007", "T051", "T053"], fal["Sala SP-12A"]
assert "Lucas Andrade iniciou a transcrição" in s
assert "sem fala nem presença escrita: Marcos Vieira, Gustavo Lima, Helena Costa" in s, s
assert "BR-São Paulo" not in json.dumps([i["falante"] for i in L["itens"]], ensure_ascii=False)
b1 = rodar({"acao": "trecho", "bloco": 1})
b2 = rodar({"acao": "trecho", "bloco": 2})
assert b1.startswith("BLOCO 1/2 · T001–") and "Leia o bloco 2 antes de escrever." in b1, b1[-200:]
assert "BLOCO 2/2" in b2 and "Leitura completa." in b2 and "segunda a gente traz" in b2 and \
       "Bruno e Caio, vocês conseguem estimar" in b2, b2[:300]
assert "segunda a gente traz" not in b1
assert len(b1) < 8600 and len(b2) < 8600, (len(b1), len(b2))
n1 = b1.count("\nT")
assert n1 + b2.count("\nT") == 74, n1
ok(f"A: 74 falas, 6 pessoas e a sala, Paula externa, 3 convidados sem fala, 2 blocos (última ação no bloco 2)")

# 3B. Homologação (.vtt)
s = rodar({"acao": "ler", "arquivos": [B]})
L = leitura()
assert "22 falas · 5 falantes · 1 bloco(s)" in s, s
assert [f["nome"] for f in L["falantes"]] == ["Lucas Andrade", "Ana Souza", "Fernanda Alves", "Otavio Mendes",
                                               "Bruno Prado"], [f["nome"] for f in L["falantes"]]
textos = " ".join(i["texto"] for i in L["itens"])
assert "7c3e1f3a" not in textos and "-->" not in textos and "<v" not in textos
assert "A Ana vai apresentar as três funcionalidades e a gente vai passando" in L["itens"][0]["texto"]
assert L["data"] == "2026-11-11" and L["titulo"] == "Homologacao Taruma Modulo 4 (nome do arquivo)", L["titulo"]
ok("B: 22 falas, 5 falantes com nome em ordem natural, deixas juntadas, sem id de deixa")

# 3C. Discovery (notas)
s = rodar({"acao": "ler", "arquivos": [C]})
L = leitura()
assert "0 falas · 0 falantes" in s and "notas sem falantes" in s, s
assert [(p["nome"], p["area"]) for p in L["presentes"]] == [
    ("Lucas Andrade", None), ("Ana Souza", "Dados"), ("Caio Teles", "Ciência de Dados"),
    ("Renata Okada", "Trade Marketing"), ("Jorge Nunes", "Supply")], L["presentes"]
assert "sem fala nem presença escrita: Gustavo Lima" in s, s
textos = "\n".join(i["texto"] for i in L["itens"])
assert "<" not in textos and "[Event]" not in textos and "class=" not in textos, textos[:300]
ok("C: notas sem falantes, 5 presentes com área, Gustavo só convidado, sem HTML nem [Event]")

# 3D. Alinhamento (.docx)
s = rodar({"acao": "ler", "arquivos": [D]})
assert "19 falas · 4 falantes" in s, s
ok("D: 19 falas e 4 falantes")

# 4. Busca
rodar({"acao": "ler", "arquivos": [A], "convidados": CONVITE_A})
s = rodar({"acao": "buscar", "termos": ["tolerância"], "falante": "Renata"})
assert "» T031 00:06:30 Renata Okada: Na verdade, me corrigindo: a tolerância é 12%" in s, s
s = rodar({"acao": "buscar", "termos": ["15%"]})
assert "» T028" in s and "» T031" in s, s
ok("busca: a correção da tolerância (T031) com falante e vizinhos")

# 5. Conferência
CONF_A = {"acao": "conferir", "tipo": "Refinamento", "ata_arquivo": "Ata esperada Refinamento Painel Jatoba.md",
          "presentes": [{"nome": "Marcos", "turno": "T007"}]}
s = rodar(CONF_A)
assert pontos(s, "Corrija") == [], s
perg = pontos(s, "Leve")
assert len(perg) == 4 and "Gustavo Lima, Helena Costa" in perg[0] and "Marcos" not in perg[0], perg
assert [p.split(" = ")[0].split("] ")[1] for p in perg[1:]] == ["12/11", "13/11", "16/11"], perg
ok("conferência A: ata esperada sem nada para corrigir; convidados e 3 prazos convertidos para o usuário")

s = rodar(dict(CONF_A, presentes=[]))
assert any("Marcos" in p for p in pontos(s, "Corrija")) and any("Sala SP-12A" in p for p in pontos(s, "Leve")), s
ok("conferência A: sem a presença do Marcos pela fala da sala, ele sai da ata e a sala vai para o usuário")

ata = (TMP / "Ata esperada Refinamento Painel Jatoba.md").read_text(encoding="utf-8")
ruim = ata.replace("| Paula Reis | Parceiro+ |\n", "").replace("| Marcos | Vendas |", "| Marcos | Vendas |\n| Gustavo Lima | Dados |")
ruim = ruim.replace("acima de 12%", "acima de 15%").replace("## Riscos", "## Contexto\n\n- Onda 2 do painel <span>.\n\n## Riscos")
ruim = ruim.replace("| Estimar o esforço", "| Ver com o jurídico (T047) | Helena Costa | 20/11 |\n"
                                         "| Orçar o snapshot em R$ 8 mil | Caio Teles | |\n| Estimar o esforço")
(TMP / "ata_ruim.md").write_text(ruim, encoding="utf-8")
s = rodar(dict(CONF_A, ata_arquivo="ata_ruim.md"))
corr = pontos(s, "Corrija")
esperados = ["HTML na ata", "ID interno de fala", '"Contexto" não faz parte', "Gustavo Lima está em Participantes sem prova",
             "Paula Reis falou", 'responsável "Helena Costa" não aparece', "20/11 não aparece",
             '"15%" aparece em T028, mas T031 corrige para "12%"', '"8 mil" não aparece']
for e in esperados:
    assert any(e in c for c in corr), (e, corr)
assert len(corr) == len(esperados), corr
ok(f"conferência A com defeitos: os {len(esperados)} defeitos apontados, nenhum a mais")

sem_prazo = ata.split("## Próximos Passos")[0] + "## Próximos Passos\n\n| Ação | Responsável | Prazo |\n|---|---|---|\n" \
    "| Confirmar se o campo customizado do Portal Araçá vem na API | Bruno Prado | |\n" \
    "| Ver com o jurídico se a tabela pode ter nome de promotor | não informado | |\n"
(TMP / "ata_sem_prazo.md").write_text(sem_prazo, encoding="utf-8")
s = rodar(dict(CONF_A, ata_arquivo="ata_sem_prazo.md"))
assert any("coluna Prazo sem nenhum prazo" in p for p in pontos(s, "Corrija")), s
assert any("sem responsável" in p for p in pontos(s, "Leve")), s
ok("conferência A: coluna Prazo vazia e ação sem responsável apontadas")

rodar({"acao": "ler", "arquivos": [B]})
CONF_B = {"acao": "conferir", "tipo": "Homologação", "ata_arquivo": "Ata esperada Homologacao Taruma Modulo 4.md"}
s = rodar(CONF_B)
assert pontos(s, "Corrija") == [], s
assert pontos(s, "Leve") == ['[Números e datas] 12/11 = "amanhã" em T013, convertido pela data da reunião (11/11): '
                             'mostre a conversão na conferência'], pontos(s, "Leve")
ata_b = (TMP / "Ata esperada Homologacao Taruma Modulo 4.md").read_text(encoding="utf-8")
(TMP / "ata_b_ruim.md").write_text(ata_b.replace("| Sem status declarado |", "| Reprovado |")
                                   .replace("## Conclusão", "## Status\n\n- Em andamento.\n\n## Conclusão"), encoding="utf-8")
s = rodar(dict(CONF_B, ata_arquivo="ata_b_ruim.md"))
corr = pontos(s, "Corrija")
assert any('"reprovado" na ata, mas ninguém declarou' in c for c in corr) and \
       any('"Status" não entra sem pedido' in c for c in corr), corr
s = rodar(dict(CONF_B, ata_arquivo="ata_b_ruim.md", secoes_pedidas=["Status"]))
assert not any('"Status"' in c for c in pontos(s, "Corrija")), s
ok("conferência B: esperada limpa (só o 'amanhã' para o usuário); 'Reprovado' sem declaração e seção extra apontados; "
   "seção pedida aceita")

rodar({"acao": "ler", "arquivos": [C], "convidados": []})
s = rodar({"acao": "conferir", "tipo": "Discovery", "ata_arquivo": "Ata esperada Discovery Previsao de Ruptura.md"})
assert pontos(s, "Corrija") == [], s
assert len(pontos(s, "Leve")) == 1 and "Gustavo Lima" in pontos(s, "Leve")[0], s
ok("conferência C: discovery esperada limpa; Gustavo, só convidado, para o usuário")

rodar({"acao": "ler", "arquivos": [D]})
s = rodar({"acao": "conferir", "tipo": "Alinhamento", "ata_arquivo": "Ata esperada Alinhamento Quimera-7.md"})
assert pontos(s, "Corrija") == [], s
assert len(pontos(s, "Leve")) == 1 and '13/11 = "sexta"' in pontos(s, "Leve")[0], s
ok("conferência D: alinhamento esperada limpa; a sexta convertida para 13/11")

limpa = pathlib.Path(tempfile.mkdtemp(prefix="atas-sem-leitura-"))
(limpa / "ata.md").write_text("Ata da reunião\n\n## Participantes\n\n- Ana\n\n## Resumo Executivo\n\n- x\n",
                              encoding="utf-8")
s = rodar({"acao": "conferir", "tipo": "Refinamento", "ata_arquivo": "ata.md"}, pasta=limpa)
assert "Sem leitura da transcrição nesta conversa" in s and 'começar com "# Ata de Reunião | <tema>"' in s and \
       '"Resumo Executivo" não entra sem pedido' in s, s
ok("conferência sem leitura: só título, seções e formato, e diz isso")

# 6. Recusas
s = rodar({"acao": "ler", "arquivos": ["Refinamento Ipe-Roxo.docx"]})
assert s.startswith("NADA FOI LIDO") and "peça para o usuário anexar" in s, s
s = rodar({"acao": "trecho", "bloco": 1}, pasta=limpa)
assert s.startswith("NADA FOI LIDO"), s
s = rodar({"acao": "resumir"})
assert s.startswith("NADA FOI FEITO"), s
ok("recusas: arquivo não anexado, trecho sem leitura e ação desconhecida")

# 7. Plano B: pelo interpretador, com o argv de um kernel e o pedido em ata_pedido.json na pasta de trabalho
(TMP / "ata_pedido.json").write_text(json.dumps({"acao": "ler", "arquivos": [D]}), encoding="utf-8")
argv, cwd = sys.argv, pathlib.Path.cwd()
try:
    import contextlib
    import io
    import os
    os.chdir(TMP)
    sys.argv = ["/usr/lib/ipykernel_launcher.py", "-f", "/tmp/kernel-1234.json"]
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        try:
            runpy.run_path(str(SCRIPT), run_name="__main__")
        except SystemExit:
            pass
    assert "19 falas · 4 falantes" in saida.getvalue(), saida.getvalue()
finally:
    sys.argv = argv
    os.chdir(cwd)
ok("plano B: o script roda pelo interpretador (runpy) e acha o pedido na pasta de trabalho")

print("\nTudo certo.")
