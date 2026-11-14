"""Sonda do ambiente de scripts das skills do Agent Builder.

Só lê e imprime o que encontra, e grava um .pptx de teste. Não acessa rede nem lê conteúdo de arquivos do usuário
além de contar os slides de um .pptx anexado.
"""
import glob
import importlib
import os
import platform
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)


def secao(t):
    print(f"\n== {t}")


def listar(raiz, nivel=2, limite=40):
    if not os.path.isdir(raiz):
        print(f"{raiz}: não existe")
        return
    vistos = 0
    for base, pastas, arquivos in os.walk(raiz):
        prof = base[len(raiz):].count(os.sep)
        if prof >= nivel:
            pastas[:] = []
        for nome in sorted(pastas)[:10] + sorted(arquivos)[:15]:
            print("  " + os.path.join(base, nome))
            vistos += 1
            if vistos >= limite:
                print("  ...")
                return


secao("Python")
print(sys.version.split()[0], "|", platform.platform())
secao("cwd")
print(os.getcwd())
secao("__file__")
print(os.path.abspath(__file__))
secao("argv")
print(sys.argv)
secao("pastas")
for raiz in (SKILL, os.getcwd(), "/mnt/data", "/mnt/user-data", "/mnt", "/tmp", os.path.expanduser("~")):
    print(f"[{raiz}]")
    listar(raiz)
secao("variáveis de ambiente (só os nomes)")
print(sorted(k for k in os.environ if any(p in k.upper() for p in ("DIR", "PATH", "HOME", "OUT", "DATA", "FILE", "SKILL"))))
secao("bibliotecas")
for mod in ("pptx", "docx", "openpyxl", "lxml", "PIL", "pandas", "matplotlib"):
    try:
        m = importlib.import_module(mod)
        print(f"{mod}: {getattr(m, '__version__', 'ok')}")
    except Exception as e:
        print(f"{mod}: FALTA ({type(e).__name__})")
secao("outro arquivo da skill")
try:
    sys.path.insert(0, AQUI)
    import auxiliar
    print(auxiliar.MENSAGEM)
except Exception as e:
    print("import de outro arquivo da skill: FALHOU", type(e).__name__, e)
try:
    print(open(os.path.join(SKILL, "assets", "exemplo.txt"), encoding="utf-8").read().strip())
except Exception as e:
    print("leitura de arquivo de recurso da skill: FALHOU", type(e).__name__, e)
secao("anexos do usuário (.pptx, .docx, .xlsx)")
achados = []
for raiz in (os.getcwd(), "/mnt", "/tmp", os.path.expanduser("~")):
    for ext in ("pptx", "docx", "xlsx"):
        achados += glob.glob(os.path.join(raiz, "**", f"*.{ext}"), recursive=True)
achados = sorted(set(a for a in achados if SKILL not in a))[:20]
for a in achados:
    print(f"  {a} ({os.path.getsize(a)} bytes)")
print(f"total: {len(achados)}")
pptxs = [a for a in achados if a.endswith(".pptx")]
if pptxs:
    try:
        from pptx import Presentation
        print(f"abrindo {pptxs[0]}: {len(Presentation(pptxs[0]).slides)} slide(s)")
    except Exception as e:
        print("abrir o .pptx anexado: FALHOU", type(e).__name__, e)
secao("gravar um .pptx de teste")
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    prs = Presentation()
    s = prs.slides.add_slide(prs.slide_layouts[6])
    tf = s.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(1)).text_frame
    tf.text = "Sonda das skills: arquivo gravado pelo script"
    tf.paragraphs[0].runs[0].font.size = Pt(28)
    for pasta in ("/mnt/data", os.getcwd(), "/tmp/outputs", "/tmp"):
        try:
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, "sonda.pptx")
            prs.save(caminho)
            print("gravado em:", caminho)
            break
        except Exception as e:
            print(f"não gravou em {pasta}: {type(e).__name__}")
except Exception as e:
    print("gravar .pptx: FALHOU", type(e).__name__, e)
print("\nFIM DA SONDA")
