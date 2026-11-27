"""Gera o template do PRD a partir de estrutura.py.

Uso, na raiz do repositório:
    python produto/assistente-de-prd/codigo/gerar_template.py [saida.docx]

Sem argumento, grava em pacote/skills/prd-docx/assets/template-prd.docx. O template não tem data nem nada que
mude entre execuções, para o arquivo só mudar quando a estrutura mudar.
"""
import pathlib
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estrutura as E  # noqa: E402

AQUI = pathlib.Path(__file__).resolve().parent
PADRAO = AQUI.parent / "pacote/skills/prd-docx/assets/template-prd.docx"

TINTA = RGBColor(0x1F, 0x3A, 0x4D)
DESTAQUE = RGBColor(0x2A, 0x7F, 0x8E)
CINZA = RGBColor(0x80, 0x80, 0x80)
FUNDO_CAB = "E3ECEF"
FUNDO_ROT = "F2F6F7"
FONTE = "Arial"


def _sombra(cel, cor):
    tcpr = cel._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), cor)
    tcpr.append(shd)


def _guia(par, texto):
    r = par.add_run(texto)
    r.italic = True
    r.font.color.rgb = CINZA
    r.font.size = Pt(8.5)
    return r


def _texto(cel, texto, negrito=False):
    p = cel.paragraphs[0]
    r = p.add_run(texto)
    r.bold = negrito
    return r


def _tabela(doc, linhas, colunas, larguras=None):
    t = doc.add_table(rows=linhas, cols=colunas)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if larguras:
        t.autofit = False
        # Word lê a largura das células; o LibreOffice, a grade da tabela: as duas são gravadas
        for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), larguras):
            gc.set(qn("w:w"), str(int(w * 567)))
        for i, w in enumerate(larguras):
            for cel in t.columns[i].cells:
                cel.width = Cm(w)
    return t


def campos(doc, lista):
    t = _tabela(doc, len(lista), 2, [5.6, 11.4])
    for i, c in enumerate(lista):
        _texto(t.cell(i, 0), E.rotulo(c), True)
        _sombra(t.cell(i, 0), FUNDO_ROT)
        ops = E.opcoes(c)
        if ops:
            _texto(t.cell(i, 1), "   ".join(f"☐ {o}" for o in ops))
    doc.add_paragraph()
    return t


def _larguras(colunas, fixas, total=17.0):
    """Primeira coluna mais larga nas tabelas de chave fixa e mais estreita nas de ID; o resto divide o que sobra."""
    n = len(colunas)
    primeira = 1.6 if colunas[0] in ("ID", "Caso") else (4.6 if fixas else total / n)
    resto = (total - primeira) / (n - 1) if n > 1 else 0
    return [primeira] + [resto] * (n - 1)


def tabela(doc, colunas, fixas, vazias, larguras=None):
    t = _tabela(doc, 1 + len(fixas) + vazias, len(colunas), larguras or _larguras(colunas, fixas))
    t.autofit = False
    for j, c in enumerate(colunas):
        _texto(t.cell(0, j), c, True)
        _sombra(t.cell(0, j), FUNDO_CAB)
    for i, chave in enumerate(fixas, start=1):
        _texto(t.cell(i, 0), chave, chave == "TOTAL")
    # tabela com cabeçalho repetido em cada página
    trpr = t.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    h.set(qn("w:val"), "true")
    trpr.append(h)
    doc.add_paragraph()
    return t


def grade(doc, chave):
    nome, quando, blocos = E.CANVAS[chave]
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading(f"Canvas · {nome}", level=3)
    _guia(doc.add_paragraph(), f"Quando se aplica: {quando}. Cada bloco: preenchido, ou \"N/A\" com o motivo.")
    campos(doc, [("Aplicável?", ["Sim", "Não"]), "Motivo, se não se aplica"])
    linhas = (len(blocos) + 1) // 2
    t = _tabela(doc, linhas, 2, [8.5, 8.5])
    for k, (titulo, pergunta) in enumerate(blocos):
        cel = t.cell(k // 2, k % 2)
        p = cel.paragraphs[0]
        r = p.add_run(titulo)
        r.bold = True
        r.font.color.rgb = DESTAQUE
        _guia(cel.add_paragraph(), pergunta)
        cel.add_paragraph()
    for row in t.rows:
        row.height = Cm(4.2)
    if len(blocos) % 2:
        _guia(t.cell(linhas - 1, 1).paragraphs[0], "")
    doc.add_paragraph()


def blocos(doc, lista):
    for b in lista:
        if b[0] == "campos":
            campos(doc, b[1])
        elif b[0] == "tabela":
            tabela(doc, b[2], b[3], b[4])
        elif b[0] == "grade":
            grade(doc, b[1])


def gate(doc, n):
    titulo, criterios = E.GATES[n]
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading(titulo, level=1)
    _guia(doc.add_paragraph(), "O agente prepara o checklist e o parecer; quem decide são o sponsor e o revisor do "
                               "gate. A decisão, os nomes e a data são preenchidos por quem decide.")
    t = tabela(doc, ["Critério", "Atendido?", "Observação"], criterios, 0, [8.5, 3.2, 5.3])
    for i in range(1, len(criterios) + 1):
        _texto(t.cell(i, 1), "☐ Sim   ☐ Não")
    campos(doc, [("Decisão", E.DECISOES_GATE), "Condições", "Quem decidiu", "Data"])


def rodape(sec):
    p = sec.footer.paragraphs[0]
    _guia(p, "Product Requirements Document · página ")
    run = p.add_run()
    for tipo, texto in (("begin", None), (None, "PAGE"), ("end", None)):
        if tipo:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), tipo)
            run._r.append(f)
        else:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = texto
            run._r.append(instr)
    run.font.size = Pt(8.5)
    run.font.color.rgb = CINZA


def estilos(doc):
    st = doc.styles
    st["Normal"].font.name = FONTE
    st["Normal"].font.size = Pt(10)
    st["Normal"].element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
    for nome, tam, cor in (("Title", 26, TINTA), ("Heading 1", 18, TINTA), ("Heading 2", 13, DESTAQUE),
                           ("Heading 3", 12, TINTA)):
        s = st[nome]
        s.font.name = FONTE
        s.font.size = Pt(tam)
        s.font.color.rgb = cor
        s.font.bold = True
        rpr = s.element.get_or_add_rPr()
        fontes = rpr.find(qn("w:rFonts"))
        if fontes is None:
            fontes = OxmlElement("w:rFonts")
            rpr.append(fontes)
        for atr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            fontes.set(qn(atr), FONTE)


def gerar(saida=PADRAO):
    doc = Document()
    estilos(doc)
    zoom = doc.settings.element.find(qn("w:zoom"))
    if zoom is not None:   # o template padrão do python-docx traz o zoom sem o percentual, que o schema exige
        zoom.set(qn("w:percent"), "100")
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, lado, Cm(2))
    rodape(sec)
    doc.core_properties.title = "Product Requirements Document"
    doc.core_properties.author = "Assistente de PRD"

    # Capa e painel
    doc.add_paragraph("Product Requirements Document", style="Title")
    _guia(doc.add_paragraph(), "PRD em 5 etapas, com um checkpoint no fim de cada uma e 2 gates. Texto em cinza "
                               "itálico é orientação: pode ficar ou ser apagado.")
    doc.add_heading("Painel", level=1)
    campos(doc, E.PAINEL_CAMPOS)
    doc.add_heading("Checkpoints", level=2)
    tabela(doc, ["Etapa", "Situação", "Data"], [f"{n} · {t}" for n, t, _ in E.ETAPAS], 0)
    doc.add_heading("Gates", level=2)
    tabela(doc, ["Gate", "Decisão", "Quem decidiu", "Data"], ["Gate 1 · Vale construir?", "Gate 2 · PRD assinado"], 0)
    doc.add_heading("Business case", level=2)
    campos(doc, E.PAINEL_BC)
    doc.add_heading("Pessoas", level=2)
    tabela(doc, ["Papel", "Nome", "Área"], E.PESSOAS, 0)

    # Etapas
    for num, titulo, pergunta in E.ETAPAS:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading(f"{num} · {titulo}", level=1)
        _guia(doc.add_paragraph(), pergunta)
        for s in (x for x in E.SECOES if x["etapa"] == num):
            doc.add_heading(f"{s['id']} · {s['titulo']}", level=2)
            _guia(doc.add_paragraph(), f"Preenche: {s['dono']}. {s['guia']}")
            blocos(doc, s["blocos"])
        if num == "03":
            gate(doc, "1")
        if num == "05":
            gate(doc, "2")

    # Anexos
    for a in E.ANEXOS:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading(f"Anexo {a['id']} · {a['titulo']}", level=1)
        _guia(doc.add_paragraph(), a["guia"])
        blocos(doc, a["blocos"])

    saida = pathlib.Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(saida)
    return saida


if __name__ == "__main__":
    print(gerar(sys.argv[1] if len(sys.argv) > 1 else PADRAO))
