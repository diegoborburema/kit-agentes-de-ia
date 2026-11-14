"""Copia o código-fonte de um agente (pasta codigo/) para os scripts das skills que o usam.

Scripts de skill montados: um arquivo em <tema>/<agente>/pacote/skills/*/scripts/ cuja primeira linha é

    # Gerado por ferramentas/montar_skills.py a partir de: produto/<agente>/codigo/a.py produto/<agente>/codigo/b.py. Não edite aqui.

é refeito com os arquivos listados, na ordem, concatenados. Os caminhos são relativos à raiz do repositório.

Blocos de código dentro do SKILL.md (forma antiga, sujeita ao limite de 20.000 caracteres da skill):

Numa SKILL.md, um bloco de código compartilhado é marcado assim:

    <!-- codigo: produto/<agente>/codigo/arquivo.py -->
    ~~~python
    (conteúdo gerado: não edite aqui)
    ~~~

Uso, na raiz do repositório:
    python ferramentas/montar_skills.py             # atualiza as skills
    python ferramentas/montar_skills.py --conferir  # só confere; sai com erro se alguma estiver desatualizada

Depois de atualizar, rode de novo o importar.py do agente, ou confira o pacote, antes de aplicar no Copilot.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MARCA = re.compile(r"(<!-- codigo: (?P<arq>[^ ]+) -->\n~~~python\n)(?P<corpo>.*?)(~~~)", re.S)
CABECALHO = "# Gerado por ferramentas/montar_skills.py a partir de: "


def montar_script(caminho):
    """Texto do script montado a partir da lista da primeira linha; None se o arquivo não for montado."""
    primeira = caminho.read_text(encoding="utf-8").split("\n", 1)[0]
    if not primeira.startswith(CABECALHO):
        return None
    fontes = primeira[len(CABECALHO):].split(". Não edite")[0].split()
    partes = [primeira]
    for f in fontes:
        rotulo = f
        partes.append(f"\n\n# ==== {rotulo}\n" + (RAIZ / rotulo).read_text(encoding="utf-8").rstrip())
    return "".join(partes) + "\n"


def montar(conferir=False):
    desatualizadas = []
    for script in sorted(RAIZ.glob("*/*/pacote/skills/*/scripts/*.py")):
        novo = montar_script(script)
        if novo is not None and novo != script.read_text(encoding="utf-8"):
            desatualizadas.append(script.relative_to(RAIZ))
            if not conferir:
                script.write_text(novo, encoding="utf-8", newline="\n")
    for skill in sorted(RAIZ.glob("*/*/pacote/skills/*/SKILL.md")):
        texto = skill.read_text(encoding="utf-8")

        def troca(m):
            codigo = (RAIZ / m["arq"]).read_text(encoding="utf-8").rstrip() + "\n"
            return m.group(1) + codigo + m.group(4)
        novo = MARCA.sub(troca, texto)
        if novo != texto:
            desatualizadas.append(skill.relative_to(RAIZ))
            if not conferir:
                skill.write_text(novo, encoding="utf-8", newline="\n")
    return desatualizadas


if __name__ == "__main__":
    conferir = "--conferir" in sys.argv
    lista = montar(conferir)
    for s in lista:
        print(("desatualizada: " if conferir else "atualizada: ") + str(s))
    if not lista:
        print("skills em dia com o código-fonte")
    sys.exit(1 if conferir and lista else 0)
