"""Gera os .zip das skills, prontos para subir no Agent Builder do Microsoft 365 Copilot.

Cada skill vira <tema>/<agente>/skills-zip/<skill>.zip, com o SKILL.md na raiz do .zip (é o formato que o
Agent Builder aceita). A sonda vira ferramentas/sonda-skills.zip. Os .zip são determinísticos: rodar de novo
sem mudar a skill não muda o arquivo.

Uso, na raiz do repositório:
    python ferramentas/empacotar_skills.py             # gera ou atualiza os .zip
    python ferramentas/empacotar_skills.py --conferir  # só confere; sai com erro se algum .zip estiver desatualizado
"""
import io
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = (2026, 1, 1, 0, 0, 0)


def zip_da_pasta(pasta):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for arq in sorted(p for p in pasta.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
            info = zipfile.ZipInfo(arq.relative_to(pasta).as_posix(), DATA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, arq.read_bytes())
    return buf.getvalue()


def alvos():
    for skill in sorted(RAIZ.glob("*/*/pacote/skills/*/SKILL.md")):
        pasta = skill.parent
        agente = pasta.parent.parent.parent
        yield pasta, agente / "skills-zip" / f"{pasta.name}.zip"
    sonda = RAIZ / "ferramentas" / "sonda-skills"
    yield sonda, RAIZ / "ferramentas" / "sonda-skills.zip"


def main(conferir=False):
    desatualizados = []
    for pasta, destino in alvos():
        novo = zip_da_pasta(pasta)
        if not destino.exists() or destino.read_bytes() != novo:
            desatualizados.append(destino.relative_to(RAIZ).as_posix())
            if not conferir:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(novo)
    for d in desatualizados:
        print(("desatualizado: " if conferir else "gerado: ") + d)
    if not desatualizados:
        print("zips das skills em dia")
    return 1 if conferir and desatualizados else 0


if __name__ == "__main__":
    sys.exit(main("--conferir" in sys.argv))
