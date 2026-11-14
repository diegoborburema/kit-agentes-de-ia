"""Confere os limites do Agent Builder em todos os agentes do repositório.

Uso, na raiz do repositório:
    python ferramentas/conferir_limites.py            # todos os agentes
    python ferramentas/conferir_limites.py redator-de-atas

Limites conferidos (documentação e laboratórios da Microsoft sobre skills em agentes declarativos):
  - instruções do agente: até 8.000 caracteres;
  - SKILL.md: instruções abaixo de 20.000 caracteres;
  - descrição da skill (frontmatter): até 1.024 caracteres;
  - nome da skill igual ao nome da pasta;
  - até 8 skills por agente.
Sai com erro se algum limite for ultrapassado.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIM_INSTRUCOES, LIM_SKILL, LIM_DESCRICAO, LIM_SKILLS = 8000, 20000, 1024, 8


def conferir(agentes=None):
    erros, linhas = [], []
    for da in sorted(RAIZ.glob("*/*/pacote/declarativeAgent_0.json")):
        pasta = da.parent.parent  # <tema>/<agente>
        if agentes and pasta.name not in agentes:
            continue
        d = json.loads(da.read_text(encoding="utf-8"))
        n = len(d.get("instructions", ""))
        linhas.append(f"{pasta.name}: instruções {n} / {LIM_INSTRUCOES}")
        if n > LIM_INSTRUCOES:
            erros.append(f"{pasta.name}: instruções com {n} caracteres (limite {LIM_INSTRUCOES})")
        skills = d.get("agent_skills", [])
        if len(skills) > LIM_SKILLS:
            erros.append(f"{pasta.name}: {len(skills)} skills (limite {LIM_SKILLS})")
        for s in skills:
            md = pasta / "pacote" / s["folder"] / "SKILL.md"
            if not md.exists():
                erros.append(f"{pasta.name}/{s['folder']}: listada no agente, mas sem SKILL.md")
                continue
            texto = md.read_text(encoding="utf-8")
            nome = re.search(r"^name:\s*(.+)$", texto, re.M)
            desc = re.search(r"^description:\s*'?(.*?)'?\s*$", texto, re.M)
            n = len(texto)
            linhas.append(f"  {s['folder']}: {n} / {LIM_SKILL}" + ("  ← ACIMA" if n > LIM_SKILL else ""))
            if n > LIM_SKILL:
                erros.append(f"{pasta.name}/{s['folder']}: SKILL.md com {n} caracteres (limite {LIM_SKILL})")
            if not nome or nome[1].strip() != pathlib.PurePosixPath(s["folder"]).name:
                erros.append(f"{pasta.name}/{s['folder']}: name diferente do nome da pasta")
            if desc and len(desc[1]) > LIM_DESCRICAO:
                erros.append(f"{pasta.name}/{s['folder']}: descrição com {len(desc[1])} caracteres (limite {LIM_DESCRICAO})")
    return linhas, erros


if __name__ == "__main__":
    linhas, erros = conferir(sys.argv[1:] or None)
    print("\n".join(linhas))
    if erros:
        print("\nLimites ultrapassados:")
        print("\n".join("- " + e for e in erros))
        sys.exit(1)
    print("\nDentro dos limites.")
