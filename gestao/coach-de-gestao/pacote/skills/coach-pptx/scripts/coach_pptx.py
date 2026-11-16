# Gerado por ferramentas/montar_skills.py a partir de: gestao/_codigo/pptx/ler_pauta.py gestao/_codigo/pptx/gerar_pauta.py gestao/_codigo/plano/plano.py gestao/_codigo/plano/plano_pptx.py gestao/_codigo/plano/cli_gestao.py. Não edite aqui.

# ==== gestao/_codigo/pptx/ler_pauta.py
import re
from pptx import Presentation
from pptx.util import Emu

REF = {"verde": (0x89, 0xA6, 0x47), "amarelo": (0xFF, 0xD5, 0x4F), "vermelho": (0xFA, 0x76, 0x76)}


def _status(rgb):
    return min(REF, key=lambda k: sum((a - b) ** 2 for a, b in zip(REF[k], rgb)))


def _cor_ponto(cel):
    for p in cel.text_frame.paragraphs:
        for r in p.runs:
            try:
                c = r.font.color.rgb
            except Exception:
                c = None
            if c is not None and r.text.strip() in ("●", "•", "⬤"):
                return _status(tuple(c))
    return None


def _texto(cel):
    """Texto da célula; hiperlinks saem como 'texto (url)'."""
    linhas = []
    for p in cel.text_frame.paragraphs:
        partes = []
        for r in p.runs:
            url = r.hyperlink.address if r.hyperlink is not None else None
            partes.append(f"{r.text} ({url})" if url else r.text)
        linhas.append("".join(partes).strip())
    return "\n".join(l for l in linhas if l)


def _data_fim(slide):
    for sh in slide.shapes:
        if sh.has_text_frame:
            m = re.search(r"(\d{1,2})(?:/\d{1,2})?\s*[–-]\s*(\d{1,2})/(\d{1,2})/(\d{4})", sh.text_frame.text)
            if m:
                return (int(m[4]), int(m[3]), int(m[2]))
    return (0, 0, 0)


def _tabelas(s):
    """(principal, combinados, desdobrar) do slide, reconhecidas pelo cabeçalho; None quando não houver."""
    principal = combinados = desdobrar = None
    for sh in s.shapes:
        if sh.has_table:
            cab = [c.text.strip().upper() for c in sh.table.rows[0].cells]
            if cab[0].startswith("QUEM"):
                combinados = sh
            elif any(h.startswith("O QUE LEVAR") for h in cab):
                desdobrar = sh
            else:
                principal = principal or sh
    return principal, combinados, desdobrar


def _ler_combinados(gf):
    cab = [c.text.strip().upper() for c in gf.table.rows[0].cells]
    i = {h: n for n, h in enumerate(cab)}
    itens = []
    for r in list(gf.table.rows)[1:]:
        cels = list(r.cells)
        c = {"quem": _texto(cels[i.get("QUEM", 0)]), "oque": _texto(cels[i.get("O QUÊ", 1)]),
             "ate": _texto(cels[i.get("ATÉ", 2)]), "feito": _texto(cels[i.get("✓", 3)])}
        if c["oque"]:  # linhas em branco não contam
            itens.append(c)
    return itens


def _ler_desdobrar(gf):
    itens = []
    for r in list(gf.table.rows)[1:]:
        c = {"tema": _texto(r.cells[0]), "oque": _texto(r.cells[1])}
        if c["tema"] or c["oque"]:  # linhas em branco não contam
            itens.append(c)
    return itens


def _legenda(s):
    """Grupos da legenda lateral: {"3 PRIORIDADES": [nomes], "TEMA DA SEMANA": [tema], ...}."""
    formas = sorted((sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()
                     and sh.left < Emu(914400 * 2.65) and sh.top > Emu(914400 * 1.35)), key=lambda sh: sh.top)
    grupos, atual = {}, None
    for sh in formas:
        t = sh.text_frame.text.strip()
        m = re.match(r"^\d+\s+(.+)$", t)
        if m:
            atual = grupos.setdefault(m[1].strip(), [])
        elif atual is not None and t.replace(" ", "") not in ("LEGENDA", "STATUS"):
            if t in ("No plano", "Atenção", "Risco / bloqueio"):
                atual = None
            else:
                atual.append(t)
    return grupos


def _linhas(s):
    gf = _tabelas(s)[0]
    if gf is None:
        return []
    cab = [c.text.strip().upper() for c in gf.table.rows[0].cells]

    def col(*nomes):
        return next((i for i, h in enumerate(cab) if any(h.startswith(n) for n in nomes)), None)
    i_cat, i_tema, i_txt = col("CATEGORIA"), col("TEMA"), col("ATUALIZA", "PARA PUXAR")
    i_tipo, i_st, i_not = col("TIPO"), col("●"), col("ANOTA")
    ovais = [sh for sh in s.shapes if sh.shape_type == 1 and sh.left > gf.left + gf.width * 0.8]
    linhas, topo = [], gf.top + gf.table.rows[0].height
    for r in list(gf.table.rows)[1:]:
        cels = list(r.cells)
        pega = lambda i: _texto(cels[i]) if i is not None else ""
        st = ""
        if i_st is not None:
            st = _cor_ponto(cels[i_st])
            if st is None:  # status desenhado como forma alinhada à linha
                for o in ovais:
                    if topo <= o.top + o.height / 2 <= topo + r.height and o.fill.type == 1:
                        st = _status(tuple(o.fill.fore_color.rgb))
            st = st or cels[i_st].text.strip()
        topo += r.height
        linha = {"categoria": pega(i_cat), "tema": pega(i_tema), "texto": pega(i_txt),
                 "tipo": pega(i_tipo), "status": st, "anotacoes": pega(i_not)}
        if linha["tema"] or linha["texto"] or linha["anotacoes"]:  # linhas em branco não contam
            linhas.append(linha)
    return linhas


def ler_pauta(caminho, completo=False):
    """Devolve (textos fora das tabelas, linhas, combinados). Cada linha é um dicionário com categoria, tema,
    texto (atualização ou pontos para puxar), tipo, status e anotacoes; o que o layout não tiver sai vazio.
    Cada combinado tem quem, oque, ate e feito (o que o usuário marcou na coluna ✓; vazio = em aberto).
    Com completo=True, devolve um dicionário com titulo, semana, legenda, textos, linhas, combinados e
    desdobrar (bloco Para desdobrar no time: tema e oque)."""
    prs = Presentation(caminho)
    com_tabela = [s for s in prs.slides if any(sh.has_table for sh in s.shapes)]
    if not com_tabela:  # sem tabela: texto por posição (de cima para baixo, da esquerda para a direita)
        s = prs.slides[-1]
        formas = sorted((sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()),
                        key=lambda sh: (round(sh.top / Emu(91440)), sh.left))
        textos = [sh.text_frame.text.strip() for sh in formas]
        if completo:
            return {"titulo": "", "semana": "", "legenda": {}, "textos": textos, "linhas": [], "combinados": [],
                    "desdobrar": []}
        return textos, [], []
    fim = max(_data_fim(s) for s in com_tabela)
    semana = [s for s in com_tabela if _data_fim(s) == fim]  # a pauta mais recente, em 1 ou mais slides
    linhas, combinados, desdobrar = [], [], []
    for s in semana:
        linhas += _linhas(s)
        _, tab_c, tab_d = _tabelas(s)
        combinados += _ler_combinados(tab_c) if tab_c is not None else []
        desdobrar += _ler_desdobrar(tab_d) if tab_d is not None else []
    s = semana[0]
    textos = [sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    if not completo:
        return textos, linhas, combinados
    topo = sorted((sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()), key=lambda sh: sh.top)
    return {"titulo": topo[0].text_frame.text.strip() if topo else "",
            "semana": next((t for t in textos if t.startswith("Semana")), ""), "legenda": _legenda(s),
            "textos": textos, "linhas": linhas, "combinados": combinados, "desdobrar": desdobrar}

# ==== gestao/_codigo/pptx/gerar_pauta.py
import re
import textwrap
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from lxml import etree

COR = {"fundo": "1A1D21", "painel": "24272C", "linha_a": "202328", "linha_b": "24272C",
       "titulo": "F4F3F6", "texto": "D8D7DD", "suave": "B8B7BE", "separador": "3A3D43", "link": "6EC1E4",
       "P1": "7D5DA2", "P2": "9F88BA", "P3": "523D6B",
       "PESSOAS": "00ABA3", "PROJETOS": "087BA7", "TEMA": "C27C3E", "LIDERADO": "4F8A5B", "LIDERANCA": "A0476B"}
ORDEM = ["LIDERANCA", "P1", "P2", "P3", "PESSOAS", "PROJETOS", "TEMA", "LIDERADO"]
STATUS = {"verde": ("89A647", "No plano"), "amarelo": ("FFD54F", "Atenção"),
          "vermelho": ("FA7676", "Risco / bloqueio")}
TIPO = {"Info": "8A8D93", "Ajuda": "9F88BA", "Acompanhar": "9F88BA",
        "Escalation": "FFD54F", "Desbloquear": "FFD54F", "Decisão": "6EC1E4"}
FONTE = "Segoe UI"


def _rgb(h):
    return RGBColor.from_string(h)


def _run(par, texto, pt, cor, negrito=False, url=None):
    r = par.add_run()
    r.text = texto
    r.font.name, r.font.size, r.font.bold = FONTE, Pt(pt), negrito
    r.font.color.rgb = _rgb(cor)
    if url:
        r.hyperlink.address = url
        r.font.underline = True
    return r


def _caixa(slide, x, y, w, h, texto, pt, cor, negrito=False, alinhar=PP_ALIGN.LEFT):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = alinhar
    _run(p, texto, pt, cor, negrito)


def _forma(slide, tipo, x, y, w, h, cor):
    s = slide.shapes.add_shape(tipo, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = _rgb(cor)
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def _celula(cel, textos, pt, cor, fundo, negrito=False, alinhar=PP_ALIGN.LEFT, link=None):
    """textos: str ou lista de str (uma linha por item). link: {"texto", "url"} vira a última linha."""
    cel.fill.solid()
    cel.fill.fore_color.rgb = _rgb(fundo)
    tcPr = cel._tc.get_or_add_tcPr()
    for i, lado in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        for velho in tcPr.findall(qn(lado)):
            tcPr.remove(velho)
        ln = etree.SubElement(tcPr, qn(lado), w="19050")
        etree.SubElement(etree.SubElement(ln, qn("a:solidFill")), qn("a:srgbClr"), val=COR["fundo"])
        tcPr.remove(ln)
        tcPr.insert(i, ln)
    cel.vertical_anchor = MSO_ANCHOR.MIDDLE
    cel.margin_left = cel.margin_right = Inches(0.1)
    cel.margin_top = cel.margin_bottom = Inches(0.04)
    tf = cel.text_frame
    tf.word_wrap = True
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    p = tf.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    linhas = [textos] if isinstance(textos, str) else list(textos)
    for i, t in enumerate(linhas):
        q = p if i == 0 else tf.add_paragraph()
        q.alignment = alinhar
        _run(q, t, pt, cor, negrito)
    if link:
        q = p if not any(linhas) else tf.add_paragraph()
        q.alignment = alinhar
        _run(q, "↗ " + link["texto"], pt, COR["link"], False, link["url"])
    fim = etree.SubElement(tf.paragraphs[-1]._p, qn("a:endParaRPr"), lang="pt-BR", sz=str(int(pt * 100)))
    etree.SubElement(etree.SubElement(fim, qn("a:solidFill")), qn("a:srgbClr"), val=cor)
    etree.SubElement(fim, qn("a:latin"), typeface=FONTE)  # quem digitar na célula herda fonte, tamanho e cor


def _cor_hiperlink(prs):
    """Hiperlinks legíveis no fundo escuro: troca a cor de hiperlink do tema."""
    tema = prs.slide_master.part.part_related_by(RT.THEME)
    xml = tema.blob.decode("utf-8")
    for tag in ("hlink", "folHlink"):
        xml = re.sub(rf"<a:{tag}>.*?</a:{tag}>", f'<a:{tag}><a:srgbClr val="{COR["link"]}"/></a:{tag}>', xml, flags=re.S)
    tema._blob = xml.encode("utf-8")


def _nova_tabela(s, y, cab, larguras, alt, h_cab=0.45):
    """Tabela no estilo da pauta: sem estilo do PowerPoint, bordas na cor do fundo, cabeçalho suave."""
    gf = s.shapes.add_table(len(alt) + 1, len(cab), Inches(2.83), Inches(y), Inches(sum(larguras)),
                            Inches(h_cab + sum(alt)))
    tbl = gf.table
    gf._element.graphic.graphicData.tbl.tblPr.find(qn("a:tableStyleId")).text = \
        "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    tbl.first_row = tbl.horz_banding = False
    for i, w in enumerate(larguras):
        tbl.columns[i].width = Inches(w)
    tbl.rows[0].height = Inches(h_cab)
    for i, h in enumerate(cab):
        _celula(tbl.cell(0, i), h, 10.5, COR["suave"], COR["fundo"], True,
                PP_ALIGN.CENTER if h in ("●", "✓") else PP_ALIGN.LEFT)
    for n, a in enumerate(alt, start=1):
        tbl.rows[n].height = Inches(a)
    return tbl


def _bloco_combinados(s, y, itens, n_branco, alt, e):
    """Bloco de combinados: abertos da pauta anterior + linhas em branco para os novos."""
    _caixa(s, 2.9, y, 6, 0.3, "C O M B I N A D O S", 11, COR["suave"], True)
    tbl = _nova_tabela(s, y + 0.32, ["QUEM", "O QUÊ", "ATÉ", "✓"], [1.6, 6.25, 1.35, 1.25], alt, 0.36)
    for n, c in enumerate(list(itens) + [{}] * n_branco, start=1):
        fundo = COR["linha_a"] if n % 2 else COR["linha_b"]
        _celula(tbl.cell(n, 0), c.get("quem", ""), 11 * e, "FFFFFF", fundo, True)
        _celula(tbl.cell(n, 1), c.get("oque", ""), 11.5 * e, COR["texto"], fundo)
        _celula(tbl.cell(n, 2), c.get("ate", ""), 11.5 * e, COR["texto"], fundo)
        _celula(tbl.cell(n, 3), "", 11.5 * e, COR["texto"], fundo, False, PP_ALIGN.CENTER)  # o usuário marca


def _bloco_desdobrar(s, y, itens, n_branco, alt, e):
    """Bloco da weekly de pares: o que levar para a weekly do time, preenchido durante a reunião."""
    _caixa(s, 2.9, y, 8, 0.3, "P A R A   D E S D O B R A R   N O   T I M E", 11, COR["suave"], True)
    tbl = _nova_tabela(s, y + 0.32, ["TEMA", "O QUE LEVAR AO TIME"], [2.75, 7.7], alt, 0.36)
    for n, c in enumerate(list(itens) + [{}] * n_branco, start=1):
        fundo = COR["linha_a"] if n % 2 else COR["linha_b"]
        _celula(tbl.cell(n, 0), c.get("tema", ""), 11.5 * e, "FFFFFF", fundo, True)
        _celula(tbl.cell(n, 1), c.get("oque", ""), 11.5 * e, COR["texto"], fundo)


def _slide(prs, dados, linhas, alt, e, pagina, total):
    baixo = dados.get("direcao") == "baixo"
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = _rgb(COR["fundo"])
    _caixa(s, 0.48, 0.3, 9, 0.6, dados.get("titulo") or f"1–1 | {dados['usuario']} & {dados['pessoa']}", 28,
           COR["titulo"], True)
    _caixa(s, 0.48, 0.9, 9, 0.35, f"Semana {dados['semana']}" + (f" · {pagina}/{total}" if total > 1 else ""),
           14, COR["suave"])

    # Legenda lateral
    _forma(s, MSO_SHAPE.RECTANGLE, 0.2, 1.35, 2.45, 5.85, COR["painel"])
    y = 1.6
    _caixa(s, 0.45, y, 2, 0.3, "L E G E N D A", 11, COR["suave"], True)
    y += 0.42
    grupos = [("3 PRIORIDADES", [(n, COR[f"P{i + 1}"]) for i, n in enumerate(dados["prioridades"][:3])]),
              ("PESSOAS", [("Pessoas", COR["PESSOAS"])]),
              ("CRONOGRAMA PROJETOS", [("Projetos", COR["PROJETOS"])]),
              ("TEMA DA SEMANA", [(dados.get("tema_semana") or "Livre", COR["TEMA"])])]
    if any(l["secao"] == "LIDERANCA" for l in dados["linhas"]):
        grupos.insert(0, ("DA WEEKLY DE PARES", [("Da weekly de pares", COR["LIDERANCA"])]))
    if baixo:
        rotulo = dados.get("rotulo_liderado") or f"Temas do {dados['pessoa']}"
        grupos.append((rotulo.upper(), [(rotulo, COR["LIDERADO"])]))
    for num, (titulo, itens) in enumerate(grupos, start=1):  # numeração segue as seções da legenda
        _caixa(s, 0.45, y, 2.15, 0.3, f"{num}  {titulo}", 10.5, COR["titulo"], True)
        y += 0.32
        for nome, cor in itens:
            _forma(s, MSO_SHAPE.RECTANGLE, 0.5, y + 0.02, 0.07, 0.28, cor)
            _caixa(s, 0.7, y + 0.03, 1.9, 0.3, nome, 12, COR["titulo"])
            y += 0.4
    if not baixo:
        _forma(s, MSO_SHAPE.RECTANGLE, 0.4, y + 0.05, 2.05, 0.012, COR["separador"])
        y += 0.2
        _caixa(s, 0.45, y, 2, 0.3, "S T A T U S", 11, COR["suave"], True)
        y += 0.38
        for cor, rotulo in STATUS.values():
            _forma(s, MSO_SHAPE.OVAL, 0.5, y + 0.05, 0.16, 0.16, cor)
            _caixa(s, 0.78, y + 0.02, 1.8, 0.3, rotulo, 11, COR["suave"])
            y += 0.32

    # Tabela
    if not linhas:  # slide só com os combinados
        return s
    if baixo:
        cab, larguras = ["CATEGORIA", "TEMA", "PARA PUXAR", "ANOTAÇÕES"], [1.5, 1.85, 3.6, 3.5]
    else:
        cab, larguras = ["CATEGORIA", "TEMA", "ATUALIZAÇÃO / PRÓXIMA AÇÃO", "TIPO", "●"], [1.85, 2.25, 4.6, 1.15, 0.6]
    tbl = _nova_tabela(s, 1.4, cab, larguras, alt)
    for n, l in enumerate(linhas, start=1):
        fundo = COR["linha_a"] if n % 2 else COR["linha_b"]
        _celula(tbl.cell(n, 0), l["categoria"], 10.5 * e, "FFFFFF", COR[l["secao"]], True)
        _celula(tbl.cell(n, 1), l["tema"], 12 * e, "FFFFFF", fundo, True)
        if baixo:
            _celula(tbl.cell(n, 2), [f"• {b}" for b in l.get("puxar", [])] or "", 11.5 * e, COR["texto"],
                    fundo, link=l.get("link"))
            _celula(tbl.cell(n, 3), "", 11.5 * e, COR["texto"], fundo)  # o usuário anota durante o 1-1
        else:
            _celula(tbl.cell(n, 2), l.get("atualizacao", ""), 11.5 * e, COR["texto"], fundo, link=l.get("link"))
            _celula(tbl.cell(n, 3), l.get("tipo", ""), 11 * e, TIPO.get(l.get("tipo"), COR["suave"]), fundo, True)
            st = STATUS.get(l.get("status") or "")
            _celula(tbl.cell(n, 4), "●" if st else ("" if l.get("status", "") is None else "–"), 16 * e if st else 11 * e,
                    st[0] if st else COR["suave"], fundo, False, PP_ALIGN.CENTER)
    return s


def nova_apresentacao():
    """Apresentação vazia em 16:9, com a cor de hiperlink legível no fundo escuro."""
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    _cor_hiperlink(prs)
    return prs


def gerar_pauta(dados, caminho=None, prs=None):
    """dados = {"direcao": "cima" | "baixo", "usuario", "pessoa" (primeiro nome ou apelido),
    "semana" ("02–06/11/2026"), "prioridades" [até 3 nomes], "tema_semana" (nome ou None),
    "titulo" (opcional; padrão "1–1 | <usuario> & <pessoa>"),
    "rotulo_liderado" (opcional; padrão "Temas do <pessoa>"),
    "linhas": [{"secao": LIDERANCA|P1|P2|P3|PESSOAS|PROJETOS|TEMA|LIDERADO, "categoria", "tema",
                para cima: "atualizacao", "tipo", "status": verde|amarelo|vermelho|"";
                para baixo: "puxar": [1 ou 2 bullets]; opcional: "link": {"texto", "url"}}],
    "desdobrar": [{"tema", "oque"}] (opcional; o bloco Para desdobrar no time ganha 3 linhas em branco),
    "combinados": [{"quem", "oque", "ate"}] (os abertos da pauta anterior; o bloco ganha 3 linhas em branco),
    "notas": [linhas de texto] (opcional)}
    Com `prs`, acrescenta os slides a essa apresentação e não salva; sem `prs`, salva em `caminho`.
    Devolve o número de slides da pauta. A pauta passa para um 2º slide quando não cabe com fonte legível;
    para baixo, sobra espaço para as anotações."""
    baixo = dados.get("direcao") == "baixo"
    linhas = sorted(dados["linhas"], key=lambda l: ORDEM.index(l["secao"]))  # seções na ordem fixa
    larg_txt, larg_tema, larg_cat = (3.4, 1.65, 1.3) if baixo else (4.4, 2.05, 1.65)
    capacidade = 4.6 if baixo else 5.3  # altura da tabela abaixo do cabeçalho, em polegadas
    e_min = 0.84 if baixo else 0.72  # para baixo, fonte maior e folga para as anotações

    def n_linhas(txt, pt, larg, fator, e):
        return max(1, len(textwrap.wrap(txt or "-", max(8, int(larg / (pt * e * fator / 72))))))

    def altura(l, e):
        itens = [f"• {b}" for b in l.get("puxar", [])] if baixo else [l.get("atualizacao", "")]
        itens += [f"↗ {l['link']['texto']}"] if l.get("link") else []
        return max(0.44 * e, 0.12 + 1.25 * e / 72 * max(
            11.5 * sum(n_linhas(t, 11.5, larg_txt, 0.52, e) for t in (itens or ["-"])),
            12 * n_linhas(l["tema"], 12, larg_tema, 0.58, e), 10.5 * n_linhas(l["categoria"], 10.5, larg_cat, 0.6, e)))

    e = 1.0
    while sum(altura(l, e) for l in linhas) > capacidade and e > e_min:
        e -= 0.04
    # Quebra de slide entre seções; uma seção só se divide se não couber sozinha num slide
    secoes = [[l for l in linhas if l["secao"] == sec] for sec in ORDEM]
    paginas, atual, usado = [], [], 0.0
    for sec in (s for s in secoes if s):
        h_sec = sum(altura(l, e) for l in sec)
        if atual and usado + h_sec > capacidade:
            paginas.append(atual)
            atual, usado = [], 0.0
        for l in sec:
            h = altura(l, e)
            if atual and usado + h > capacidade:
                paginas.append(atual)
                atual, usado = [], 0.0
            atual.append(l)
            usado += h
    paginas.append(atual)

    # Blocos depois da tabela (Para desdobrar no time, se houver, e Combinados): no último slide se couberem;
    # senão, num slide próprio
    def alturas_bloco(itens, larg):
        return [max(0.36 * e, 0.12 + 1.25 * e / 72 * 11.5 * n_linhas(c.get("oque"), 11.5, larg, 0.52, e))
                for c in itens] + [0.36 * e] * 3
    blocos = []
    if dados.get("desdobrar") is not None:
        blocos.append((_bloco_desdobrar, dados["desdobrar"], alturas_bloco(dados["desdobrar"], 7.5)))
    blocos.append((_bloco_combinados, dados.get("combinados", []), alturas_bloco(dados.get("combinados", []), 6.05)))
    h_blocos = sum(0.32 + 0.36 + sum(alt) for _, _, alt in blocos) + 0.25 * len(blocos)
    y_bloco = 1.4 + 0.45 + sum(altura(l, e) for l in paginas[-1]) + 0.25
    if y_bloco + h_blocos - 0.25 > 7.2:
        paginas.append([])
        y_bloco = 1.4

    salvar = prs is None
    prs = prs or nova_apresentacao()
    _cor_hiperlink(prs)
    for i, pag in enumerate(paginas, start=1):
        s = _slide(prs, dados, pag, [altura(l, e) for l in pag], e, i, len(paginas))
        if i == 1 and dados.get("notas"):  # contexto e perguntas para levar, nas notas do 1º slide
            s.notes_slide.notes_text_frame.text = "\n".join(dados["notas"])
    for desenhar, itens, alt in blocos:
        desenhar(s, y_bloco, itens, 3, alt, e)
        y_bloco += 0.32 + 0.36 + sum(alt) + 0.25
    if salvar:
        prs.save(caminho)
    return len(paginas)

# ==== gestao/_codigo/plano/plano.py
# ---------------------------------------------------------------- plano 30-60-90: datas, contas e regras (Coach de Gestão)
# Janelas, capacidade, consistência, revisão da semana e virada do ciclo. Tudo que é data ou conta sai daqui, não
# do modelo. O plano é um dicionário (ver a skill coach-pptx); datas em aaaa-mm-dd.
import copy
import datetime as _pl_dt
import re
import unicodedata

PL_ITEM = ["feito", "parcial", "não feito", "replanejado", "cancelado", "a confirmar"]
PL_DELEG = ["em dia", "atrasada", "concluída", "checar depois", "cancelada"]
PL_PEDIDO = ["aberto", "atendido", "cancelado"]
PL_PARAR = ["mantido", "retomado"]
PL_FECHA = ["atingida", "parcial", "não atingida"]
PL_KPI_STATUS = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴", "sem_dado": "⚪"}
PL_PROTOCOLO = ["cortar escopo", "nova data"]  # 2º escorregão (cancelar = status cancelado, com motivo)
PL_COMPROMISSO = ["comprometido", "aspiracional"]
PL_EXECUCAO_ALVO = 85  # % (Moran, 12 Week Year: heurística, não estudo controlado)
PL_RESERVA_PCT = 20  # % das horas livres para o não planejado, quando o radar não dá o volume
PL_ATIVIDADE_MAX_H = 4  # atividade maior: quebre em passos antes de estimar
PL_MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _pl_d(iso):
    return _pl_dt.date.fromisoformat(str(iso)[:10])


def pl_dm(iso):
    d = _pl_d(iso)
    return f"{d.day:02d}/{d.month:02d}"


def pl_dma(iso):
    d = _pl_d(iso)
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def pl_periodo(ini, fim):
    """('2026-11-16', '2026-11-20') → '16–20/11'; meses diferentes → '30/11–04/12'."""
    a, b = _pl_d(ini), _pl_d(fim)
    return f"{a.day:02d}–{pl_dm(fim)}" if a.month == b.month else f"{pl_dm(ini)}–{pl_dm(fim)}"


def pl_norm(texto):
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t.lower()).strip()


def pl_recesso_padrao(anos):
    """Recesso de fim de ano: as semanas (seg–sex) que contêm 25/12 e 01/01."""
    saida = []
    for a in anos:
        for d in (_pl_dt.date(a, 12, 25), _pl_dt.date(a + 1, 1, 1)):
            seg = d - _pl_dt.timedelta(days=d.weekday())
            par = (seg.isoformat(), (seg + _pl_dt.timedelta(days=4)).isoformat())
            if par not in saida:
                saida.append(par)
    return saida


def pl_janelas(data, s1=None, inicio=None, recesso=None, rolagem=False):
    """Janelas do ciclo a partir da data do plano.
    S1: de quinta a domingo, a semana seguinte; de segunda a quarta, `s1` = "esta" ou "proxima" (sem ele, devolve
    a pergunta). `inicio` (aaaa-mm-dd) força o começo do ciclo (ex.: depois do recesso).
    Devolve semanas S1–S12 (seg–sex), 30 (S1–S4), 60 (S5–S8), 90 (até S12), as semanas no recesso, a janela de busca
    do Montar (4 semanas antes da data do plano até ela) e os avisos. Com `rolagem` (virada), o recesso no começo do
    ciclo só desconta a capacidade: o ciclo não muda de data."""
    d = _pl_d(data)
    seg_esta = d - _pl_dt.timedelta(days=d.weekday())
    seg_prox = seg_esta + _pl_dt.timedelta(days=7)
    if inicio:
        i = _pl_d(inicio)
        seg = i - _pl_dt.timedelta(days=i.weekday())
    elif d.weekday() >= 3:
        seg = seg_prox
    elif s1 in ("esta", "proxima", "próxima"):
        seg = seg_esta if s1 == "esta" else seg_prox
    else:
        return {"pergunta": f"S1 é esta semana ({pl_periodo(seg_esta.isoformat(), (seg_esta + _pl_dt.timedelta(days=4)).isoformat())}) "
                            f"ou a próxima ({pl_periodo(seg_prox.isoformat(), (seg_prox + _pl_dt.timedelta(days=4)).isoformat())})?"}
    semanas = [((seg + _pl_dt.timedelta(weeks=k)).isoformat(), (seg + _pl_dt.timedelta(weeks=k, days=4)).isoformat())
               for k in range(12)]
    rec = [tuple(r) for r in (recesso if recesso is not None else pl_recesso_padrao(sorted({d.year - 1, d.year, d.year + 1})))]
    no_recesso = [k + 1 for k, (a, b) in enumerate(semanas) if any(not (b < r[0] or a > r[1]) for r in rec)]
    avisos = []
    if not rolagem and (1 in no_recesso or 2 in no_recesso):
        k = max(x for x in no_recesso if x <= 2)
        while k + 1 in no_recesso:  # o recesso pode continuar depois da S2
            k += 1
        volta = semanas[k][0] if k < len(semanas) else semanas[-1][0]
        quais = " e ".join(f"S{x}" for x in no_recesso if x <= 2)
        avisos.append(f"{quais} no recesso: pergunte se o ciclo começa depois do recesso ({pl_dm(volta)}) "
                      "ou segue com capacidade reduzida")
    for k in no_recesso:
        if k > 2 or rolagem:
            avisos.append(f"S{k} ({pl_periodo(*semanas[k - 1])}) no recesso: desconte a capacidade e não planeje entregável "
                          "cheio nela sem perguntar")
    return {"data": d.isoformat(), "inicio": semanas[0][0], "semanas": semanas, "s1": list(semanas[0]),
            "d30": [semanas[0][0], semanas[3][1]], "d60": [semanas[4][0], semanas[7][1]], "d90": [semanas[0][0], semanas[11][1]],
            "recesso": no_recesso, "busca": [(d - _pl_dt.timedelta(days=28)).isoformat(), d.isoformat()], "avisos": avisos}


def pl_janelas_opcoes(data, recesso=None):
    """De segunda a quarta: a pergunta da S1 com as janelas completas das duas respostas. Pergunta não é falha."""
    j = pl_janelas(data, recesso=recesso)
    if "pergunta" not in j:
        return None
    esta, prox = pl_janelas(data, "esta", recesso=recesso), pl_janelas(data, "proxima", recesso=recesso)
    return [f"PERGUNTE ao usuário, em uma linha (é uma pergunta, não uma falha do script): {j['pergunta']}",
            f"Se for esta semana (\"s1\": \"esta\"): {pl_janelas_txt(esta)}",
            f"Se for a próxima (\"s1\": \"proxima\"): {pl_janelas_txt(prox)}",
            "Com a resposta, rode janelas de novo com o \"s1\" escolhido e mande o mesmo \"s1\" no plano do gerar."]


def pl_janelas_txt(j):
    return (f"S1 {pl_periodo(*j['s1'])} · 30 dias {pl_periodo(*j['d30'])} · 60 dias {pl_periodo(*j['d60'])} · "
            f"90 dias até {pl_dma(j['d90'][1])}")


def pl_capacidade(semana, reunioes=(), horas_dia=8.0, ausencias=(), esforco_h=0.0, recesso=None, reserva_pct=None,
                  nao_planejado_h=None):
    """Horas livres da semana (seg–sex): dias úteis × horas_dia, menos recesso e ausências, menos as reuniões
    (sobreposições contam uma vez). `reunioes`: [{"inicio", "fim"}] em aaaa-mm-ddThh:mm, ou [{"data", "horas"}].
    Das horas livres sai a reserva para o não planejado: o volume medido pelo radar (`nao_planejado_h`) ou
    `reserva_pct` (padrão PL_RESERVA_PCT). O esforço é comparado com as horas planejáveis que sobram."""
    ini, fim = _pl_d(semana[0]), _pl_d(semana[1])
    rec = [tuple(r) for r in (recesso if recesso is not None else pl_recesso_padrao([ini.year - 1, ini.year]))]
    fora = set(ausencias)
    dias = []
    for k in range((fim - ini).days + 1):
        x = ini + _pl_dt.timedelta(days=k)
        if x.weekday() < 5 and x.isoformat() not in fora and not any(r[0] <= x.isoformat() <= r[1] for r in rec):
            dias.append(x.isoformat())
    por_dia, n, sem_hora = {}, 0, 0.0
    for r in reunioes:
        if r.get("inicio") and r.get("fim"):
            a, b = _pl_dt.datetime.fromisoformat(r["inicio"]), _pl_dt.datetime.fromisoformat(r["fim"])
            if a.date().isoformat() in dias:
                por_dia.setdefault(a.date().isoformat(), []).append((a, b))
                n += 1
        elif r.get("data") in dias:
            sem_hora += float(r.get("horas") or 0)
            n += 1
    ocupado = sem_hora
    for lista in por_dia.values():
        lista.sort()
        atual = None
        for a, b in lista:
            if atual and a <= atual[1]:
                atual = (atual[0], max(atual[1], b))
            else:
                if atual:
                    ocupado += (atual[1] - atual[0]).total_seconds() / 3600
                atual = (a, b)
        if atual:
            ocupado += (atual[1] - atual[0]).total_seconds() / 3600
    disponivel = len(dias) * float(horas_dia)
    livres = round(disponivel - ocupado, 1)
    if nao_planejado_h is not None:
        reserva, origem = round(min(max(livres, 0), float(nao_planejado_h)), 1), "volume do radar"
    else:
        pct = PL_RESERVA_PCT if reserva_pct is None else float(reserva_pct)
        reserva, origem = round(max(livres, 0) * pct / 100, 1), f"{pct:g}% das horas livres"
    planejaveis = round(livres - reserva, 1)
    return {"dias_uteis": len(dias), "disponivel_h": disponivel, "reunioes": n, "bloqueado_h": round(ocupado, 1),
            "livres_h": livres, "reserva_h": reserva, "reserva_origem": origem, "planejaveis_h": planejaveis,
            "esforco_h": float(esforco_h), "cabe": float(esforco_h) <= planejaveis,
            "folga_h": round(planejaveis - float(esforco_h), 1)}


def pl_execucao(atividades, status):
    """Nota de execução de uma semana: atividades feitas / planejadas (as canceladas, com motivo, ficam fora da conta),
    e o esforço planejado e concluído, em horas."""
    plan = [a for a in atividades if status.get(a["id"], {}).get("status") != "cancelado"]
    feitas = [a for a in plan if status.get(a["id"], {}).get("status") == "feito"]
    h = lambda xs: round(sum(float(x.get("esforco_h") or 0) for x in xs), 1)
    return {"planejadas": len(plan), "feitas": len(feitas), "pct": round(100 * len(feitas) / len(plan)) if plan else None,
            "esforco_planejado": h(plan), "esforco_concluido": h(feitas),
            "canceladas": len(atividades) - len(plan)}


def pl_execucao_ciclo(plano, ciclo=None):
    """As notas de execução das semanas fechadas de um ciclo e a nota do ciclo (soma das feitas / soma das planejadas)."""
    ciclo = ciclo or plano.get("ciclo", 1)
    semanas = [(h["semana"], h["execucao"]) for h in plano.get("historico", []) if h.get("ciclo") == ciclo and h.get("execucao")]
    pl = sum(e["planejadas"] for _, e in semanas)
    fe = sum(e["feitas"] for _, e in semanas)
    return {"semanas": semanas, "planejadas": pl, "feitas": fe, "pct": round(100 * fe / pl) if pl else None}


def pl_execucao_txt(ex):
    if not ex["semanas"]:
        return "Execução: nenhuma semana fechada neste ciclo"
    return ("Execução: " + " · ".join(f"S{s} {e['pct']}%" if e["pct"] is not None else f"S{s} –" for s, e in ex["semanas"])
            + f" · ciclo {ex['feitas']} de {ex['planejadas']} ({ex['pct']}%)")


def pl_referencia(plano, n=3):
    """Visão de fora para a capacidade: o esforço concluído e o planejado nas últimas `n` semanas fechadas."""
    return [(h["semana"], h["periodo"], h["execucao"]["esforco_concluido"], h["execucao"]["esforco_planejado"])
            for h in plano.get("historico", []) if h.get("execucao")][-n:]


# ---------------------------------------------------------------- itens do plano
def pl_itens(plano):
    """Todos os itens com ID: {id: (tipo, item)}."""
    saida = {}
    for tipo, lista in (("direcionador", plano.get("retrato", {}).get("direcionadores", [])),
                        ("resultado", plano.get("resultados", [])), ("marco", plano.get("marcos", [])),
                        ("prioridade", plano.get("prioridades", [])), ("kpi", plano.get("kpis", [])),
                        ("atividade", plano.get("agenda", {}).get("atividades", [])),
                        ("delegacao", plano.get("agenda", {}).get("delegacoes", [])),
                        ("pedido", plano.get("agenda", {}).get("pedidos", [])),
                        ("parar", plano.get("agenda", {}).get("parar", [])), ("risco", plano.get("riscos", []))):
        for it in lista:
            if it.get("id"):
                saida[it["id"]] = (tipo, it)
    return saida


def pl_proximo_id(plano, prefixo):
    """Próximo ID livre (nunca reaproveitado: conta também o histórico)."""
    usados = set(pl_itens(plano))
    for h in plano.get("historico", []):
        usados |= set(h.get("itens", {}))
    for f in plano.get("fechamentos", []):
        usados |= {x.get("id") for x in f.get("saidos", [])}
    n = max([int(m[1]) for u in usados for m in [re.fullmatch(prefixo + r"(\d+)", u or "")] if m] + [0])
    return f"{prefixo}{n + 1}"


def pl_afetados(plano, alvo):
    """O que uma remoção ou reabertura afeta: o item e tudo que está ligado a ele, acima e abaixo.
    `alvo`: um ID ou uma janela ("90", "60", "30", "semana")."""
    itens = pl_itens(plano)
    if alvo in ("90", "60", "30", "semana"):
        tipos = {"90": ["resultado"], "60": ["marco"], "30": ["prioridade"], "semana": ["atividade", "delegacao", "pedido", "parar"]}[alvo]
        base = [i for i, (t, _) in itens.items() if t in tipos]
    else:
        base = [alvo] if alvo in itens else []
    afet, fila = set(base), list(base)
    while fila:
        x = fila.pop()
        t, it = itens[x]
        ligados = []
        if t == "prioridade":
            ligados += [it.get("resultado")] + list(it.get("kpis", []))
            ligados += [i for i, (t2, y) in itens.items() if t2 in ("atividade", "delegacao") and y.get("liga") == x]
        if t == "resultado":
            ligados += list(it.get("kpis", []))
            ligados += [i for i, (t2, y) in itens.items() if t2 == "marco" and y.get("resultado") == x]
            ligados += [i for i, (t2, y) in itens.items() if t2 == "prioridade" and y.get("resultado") == x]
        for l in ligados:
            if l and l in itens and l not in afet:
                afet.add(l)
                fila.append(l)
    ordem = list(itens)
    return sorted(afet, key=ordem.index)


def pl_consistencia(plano):
    """O que não fecha no plano: (falhas, atenções, sinais de estrutura)."""
    falhas, atencao, sinais = [], [], []
    itens = pl_itens(plano)
    ag = plano.get("agenda", {})
    prios = plano.get("prioridades", [])
    ids_p = {p["id"] for p in prios}
    frentes = {pl_norm(f.get("nome")) for f in ag.get("frentes", [])}
    if len(prios) > 3 and not plano.get("escolhas", {}).get("prioridades_mantidas"):
        falhas.append(f"{len(prios)} prioridades (o limite é 3): desafie uma vez; se o usuário mantiver, registre a escolha")
    for a in ag.get("atividades", []):
        if a.get("liga") not in ids_p and pl_norm(a.get("liga")) not in frentes and not pl_norm(a.get("liga")).startswith("frente"):
            falhas.append(f"{a['id']} sem prioridade nem frente própria acima ({a.get('texto', '')})")
        if not a.get("feito_quando"):
            falhas.append(f"{a['id']} sem \"feito quando\"")
    ligadas = {x.get("liga") for x in ag.get("atividades", []) + ag.get("delegacoes", [])}
    semana = plano.get("semana", 1)
    for p in prios:
        if p["id"] not in ligadas:
            falhas.append(f"{p['id']} {p.get('nome')} sem atividade nem delegação na semana")
        if not p.get("feito_quando"):
            falhas.append(f"{p['id']} {p.get('nome')} sem \"feito quando\"")
        ent = p.get("entregaveis", {})
        vazias = [f"S{k}" for k in range(semana, 5) if not ent.get(f"S{k}")]
        if vazias:
            falhas.append(f"{p['id']} {p.get('nome')} sem entregável em {', '.join(vazias)}")
        if not any(itens.get(k, ("", {}))[1].get("tipo") == "direcionador" for k in p.get("kpis", [])):
            falhas.append(f"{p['id']} {p.get('nome')} sem KPI direcionador")
        if not p.get("dono"):
            sinais.append(f"{p['id']} {p.get('nome')} sem dono")
    desafio = plano.get("retrato", {}).get("desafio_central") or {}
    if not desafio.get("texto"):
        falhas.append("Sem desafio central: pergunte qual é, e o que não vamos fazer")
    elif plano.get("resultados") and not any(r.get("ataca") for r in plano.get("resultados", [])):
        atencao.append("Nenhum resultado diz como ataca o desafio central")
    riscos = plano.get("riscos", [])
    if plano.get("resultados") and not riscos:
        atencao.append("Sem riscos: faça o pré-mortem dos resultados de 90 dias")
    for rb in riscos:
        if not rb.get("mitigacao"):
            atencao.append(f"{rb.get('id')} sem mitigação (atividade, delegação ou marco)")
    for p in prios:
        if not p.get("fecha_100"):
            atencao.append(f"{p['id']} {p.get('nome')}: faça o teste dos 100% (os 4 entregáveis fecham o \"feito quando\"?)")
    for a in ag.get("atividades", []):
        if float(a.get("esforco_h") or 0) > PL_ATIVIDADE_MAX_H:
            atencao.append(f"{a['id']} com {float(a['esforco_h']):g} h: quebre em passos antes de estimar")
    for r in plano.get("resultados", []):
        if r.get("compromisso") not in PL_COMPROMISSO:
            falhas.append(f"{r['id']} sem tipo: comprometido ou aspiracional")
        ks = [k for k in r.get("kpis", []) if k in itens]
        if not ks:
            falhas.append(f"{r['id']} sem KPI de resultado")
        if len(ks) > 2:
            atencao.append(f"{r['id']} com {len(ks)} KPIs (o limite é 2)")
        if not any(m.get("resultado") == r["id"] for m in plano.get("marcos", [])):
            atencao.append(f"{r['id']} sem marco de 60 dias")
    levanta = {k for x in ag.get("atividades", []) + ag.get("delegacoes", []) for k in x.get("levanta", [])}
    kpis = plano.get("kpis", [])
    for k in kpis:
        if not k.get("baseline"):
            (atencao if k["id"] in levanta else falhas).append(
                f"{k['id']} {k.get('nome')} sem baseline" + (" (levantamento na semana)" if k["id"] in levanta
                                                            else ": ponha o levantamento na semana"))
        if not k.get("fonte_dado"):
            falhas.append(f"{k['id']} {k.get('nome')} sem fonte do dado")
        if k.get("tipo") == "resultado" and not k.get("par"):
            atencao.append(f"{k['id']} {k.get('nome')} sem contra-indicador (par)")
    if len(kpis) > 8:
        falhas.append(f"{len(kpis)} KPIs no scorecard (o limite é 8)")
    for dl in ag.get("delegacoes", []):
        if not dl.get("checar"):
            falhas.append(f"{dl['id']} sem data de checagem")
    n_at = len(ag.get("atividades", []))
    if not 5 <= n_at <= 7:
        atencao.append(f"{n_at} atividades na semana (o alvo é de 5 a 7)")
    if not ag.get("parar"):
        falhas.append("Parar de fazer vazio")
    n_dl = len(ag.get("delegacoes", []))
    if n_at + n_dl and n_at / (n_at + n_dl) > 0.5:
        atencao.append(f"{n_at} de {n_at + n_dl} itens da semana com você (mais da metade): teste a delegação")
    # Sinais de estrutura: alguém em 3 ou mais frentes; delegação atrasada 2 semanas seguidas
    por_pessoa = {}
    for m in plano.get("retrato", {}).get("movimentos", []):
        if m.get("dono") and pl_norm(m["dono"]) != pl_norm(plano.get("usuario")):
            por_pessoa.setdefault(m["dono"], []).append(m["nome"])
    for quem, fr in por_pessoa.items():
        if len(fr) >= 3:
            sinais.append(f"{quem} em {len(fr)} frentes ({', '.join(fr)})")
    hist = [h for h in _pl_hist_trabalho(plano) if h.get("ciclo") == plano.get("ciclo")][-2:]
    if len(hist) == 2:
        for i in hist[-1].get("itens", {}):
            if all(h.get("itens", {}).get(i, {}).get("status") == "atrasada" for h in hist):
                sinais.append(f"{i} atrasada duas semanas seguidas")
    return falhas, atencao, sinais


# ---------------------------------------------------------------- revisão da semana
def _pl_validar_status(itens_semana, status, erros):
    validos = {"atividade": PL_ITEM, "delegacao": PL_DELEG, "pedido": PL_PEDIDO, "parar": PL_PARAR}
    for i, (tipo, it) in itens_semana.items():
        s = status.get(i)
        if not s:
            erros.append(f"{i} sem destino ({it.get('texto') or it.get('oque', '')}): nada some em silêncio")
            continue
        if s.get("status") not in validos[tipo]:
            erros.append(f"{i}: status {s.get('status')!r} (válidos: {', '.join(validos[tipo])})")
        if s.get("status") in ("cancelado", "cancelada") and not s.get("motivo"):
            erros.append(f"{i}: cancelado sem motivo")
        if s.get("status") in ("replanejado", "checar depois") and not s.get("para"):
            erros.append(f"{i}: {s['status']} sem a nova data (para)")


def pl_excecoes(plano):
    """Revisão por exceção: o que merece conversa na revisão desta semana. O resto só se confirma em bloco."""
    saida = []
    semana = plano.get("semana", 1)
    sems = plano.get("janelas", {}).get("semanas", [])
    fim = sems[min(semana, len(sems)) - 1][1] if sems else plano.get("data")
    for k in plano.get("kpis", []):
        if (k.get("status") or "sem_dado") != "verde":
            saida.append(f"KPI {k['id']} {k.get('nome')} {PL_KPI_STATUS.get(k.get('status') or 'sem_dado')}")
    for r in plano.get("resultados", []):
        if r.get("confianca") is not None and r["confianca"] <= 5:
            saida.append(f"{r['id']} {r.get('texto')} com confiança {r['confianca']}/10")
    for m in plano.get("marcos", []):
        if m.get("status") != "concluido" and m.get("data") and m["data"] <= fim:
            saida.append(f"{m['id']} {m.get('texto')} vence em {pl_dm(m['data'])}")
    ag = plano.get("agenda", {})
    for a in ag.get("atividades", []):
        if pl_escorregou(plano, a["id"]):
            saida.append(f"{a['id']} {a.get('texto')} já escorregou uma semana: se escorregar de novo, cortar escopo, nova data "
                         "com motivo ou cancelar")
    for d in ag.get("delegacoes", []):
        if d.get("checar") and d["checar"] <= fim:
            saida.append(f"{d['id']} {d.get('quem')} · {d.get('oque')}: checar em {pl_dm(d['checar'])}")
    return saida


def _pl_hist_trabalho(plano):
    """O histórico sem as semanas de recesso puladas."""
    return [h for h in plano.get("historico", []) if not h.get("recesso")]


def pl_escorregou(plano, aid):
    """True se a atividade escorregou na última semana trabalhada (parcial, não feito ou replanejado)."""
    hist = _pl_hist_trabalho(plano)
    return bool(hist) and hist[-1].get("itens", {}).get(aid, {}).get("status") in ("parcial", "não feito", "replanejado")


def _pl_semana_nova(p, semana, rev):
    """A semana que abre depois de fechar `semana`: pula as semanas de recesso que vêm em seguida (até a S4, onde é a
    virada), a não ser que o usuário vá trabalhar no recesso (`trabalhar_no_recesso`)."""
    nova = semana + 1
    rec = p.get("janelas", {}).get("recesso", [])
    if rev.get("_virada") or rev.get("trabalhar_no_recesso"):
        return nova
    while nova in rec and nova < 4:
        nova += 1
    return nova


def pl_revisar(plano, rev):
    """Fecha a semana do plano e abre a seguinte. `rev` = {"data", "status": {id: {"status", "nota", "motivo",
    "para", "fonte", "protocolo", "corte"}}, "atividades": [...], "delegacoes": [...], "pedidos": [...],
    "parar": [...], "kpis": {id: {...}}, "confianca": {Rid: 0–10}, "vitorias": [...], "fora_do_plano": [...],
    "descartar": [...], "mudancas": [...]}. Devolve (plano novo, log, erros, avisos)."""
    p = copy.deepcopy(plano)
    erros, log, avisos = [], [], []
    ag = p.setdefault("agenda", {})
    semana_itens = {i: (t, it) for i, (t, it) in pl_itens(p).items() if t in ("atividade", "delegacao", "pedido", "parar")}
    st = rev.get("status", {})
    _pl_validar_status(semana_itens, st, erros)
    novas = {a.get("id"): a for a in rev.get("atividades", []) if a.get("id")}
    for i, (t, it) in semana_itens.items():
        s = st.get(i, {})
        if t == "atividade" and s.get("status") in ("parcial", "não feito") and i not in novas and not s.get("destino"):
            erros.append(f"{i} {s['status']}: ponha na nova semana (mesmo ID) ou diga o destino")
        # 2º escorregão seguido: cortar escopo ou nova data com motivo (ou cancelar), e um se-então com quando
        if t == "atividade" and s.get("status") in ("parcial", "não feito", "replanejado") and pl_escorregou(p, i):
            prot = s.get("protocolo")
            if prot not in PL_PROTOCOLO:
                erros.append(f"{i} escorregou pela 2ª semana: ofereça, nesta ordem, cortar escopo, nova data com motivo ou "
                             f"cancelar; mande \"protocolo\" ({' ou '.join(PL_PROTOCOLO)}) ou o status cancelado")
            elif prot == "cortar escopo" and not s.get("corte"):
                erros.append(f"{i}: cortar escopo sem dizer o que sai (corte)")
            elif prot == "nova data" and not s.get("motivo"):
                erros.append(f"{i}: nova data sem motivo")
            if prot in PL_PROTOCOLO and i in novas and not (novas[i].get("quando") and novas[i].get("se_entao")):
                erros.append(f"{i} volta à semana pela 3ª vez: combine quando (dia e hora) e um se-então (se X, então Y)")
    conf = rev.get("confianca", {})
    for rid, v in conf.items():
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            erros.append(f"Confiança de {rid}: {v!r} (de 0 a 10)")
    semana = p.get("semana", 1)
    if semana >= 4 and not rev.get("_virada"):
        erros.append("Esta é a 4ª revisão do ciclo: use a ação virar")
    if erros:
        return plano, log, erros, avisos
    sem = p["janelas"]["semanas"][semana - 1]
    ex = pl_execucao(ag.get("atividades", []), st)
    anterior = next((h.get("confianca") for h in reversed(p.get("historico", [])) if h.get("confianca")), {}) or {}
    p.setdefault("historico", []).append({"ciclo": p.get("ciclo", 1), "semana": semana, "periodo": list(sem),
                                          "fechada_em": rev["data"], "execucao": ex, "confianca": dict(conf),
                                          "vitorias": list(rev.get("vitorias", [])),
                                          "itens": {i: dict(st[i], texto=it.get("texto") or it.get("oque", ""),
                                                            **({"esforco_h": it["esforco_h"]} if it.get("esforco_h") else {}))
                                                    for i, (_, it) in semana_itens.items()}})
    log.append(f"S{semana} ({pl_periodo(*sem)}) fechada: " + ", ".join(f"{i} {st[i]['status']}" for i in semana_itens))
    if ex["pct"] is not None:
        log.append(f"Execução da S{semana}: {ex['feitas']} de {ex['planejadas']} atividades ({ex['pct']}%) · "
                   f"{ex['esforco_concluido']:g} h concluídas de {ex['esforco_planejado']:g} h planejadas"
                   + (f" · {ex['canceladas']} cancelada(s) fora da conta" if ex["canceladas"] else ""))
        if ex["pct"] < PL_EXECUCAO_ALVO:
            avisos.append(f"Execução da S{semana} em {ex['pct']}%, abaixo de {PL_EXECUCAO_ALVO}%: pergunte se o plano estava "
                          "grande demais ou se algo travou, e não aumente a carga da semana nova")
    for r in p.get("resultados", []):
        v = conf.get(r["id"])
        if v is None:
            avisos.append(f"Confiança de {r['id']} não registrada: pergunte de 0 a 10")
            continue
        r["confianca"] = v
        if anterior.get(r["id"]) is not None and anterior[r["id"]] - v >= 2:
            avisos.append(f"Confiança de {r['id']} caiu de {anterior[r['id']]} para {v}: pergunte o porquê e o risco")
        elif v <= 3:
            avisos.append(f"Confiança de {r['id']} em {v} (vermelho): pergunte o que mudaria a nota")
    if conf:
        log.append("Confiança: " + " · ".join(f"{k} {v}" for k, v in conf.items()))
    p["vitorias"] = list(rev.get("vitorias", []))
    # Nova semana: atividades do pedido; seguem os pedidos abertos, o parar mantido e as delegações em curso
    atividades = []
    for a in rev.get("atividades", []):
        a = dict(a)
        a["id"] = a.get("id") or pl_proximo_id(p, "A")
        atividades.append(a)
        ag["atividades"] = atividades  # para o próximo ID contar as novas
    ag["atividades"] = atividades
    deleg = [dict(d, checar=st[d["id"]].get("para") or d.get("checar")) for d in ag.get("delegacoes", [])
             if st[d["id"]]["status"] not in ("concluída", "cancelada")]
    for d in rev.get("delegacoes", []):
        d = dict(d)
        velha = next((x for x in deleg if x["id"] == d.get("id")), None)
        if velha:
            velha.update(d)
        else:
            d["id"] = d.get("id") or pl_proximo_id(dict(p, agenda=dict(ag, delegacoes=deleg)), "DL")
            deleg.append(d)
    ag["delegacoes"] = deleg
    nova = _pl_semana_nova(p, semana, rev)
    prox_seg = p["janelas"]["semanas"][nova - 1][0] if nova <= len(p["janelas"]["semanas"]) else rev["data"]
    for d in deleg:
        if d.get("checar") and d["checar"] < prox_seg:
            log.append(f"{d['id']} segue com checagem em {pl_dm(d['checar'])}, que já passou: pergunte a próxima data")
    ag["pedidos"] = [x for x in ag.get("pedidos", []) if st[x["id"]]["status"] == "aberto"]
    for x in rev.get("pedidos", []):
        x = dict(x)
        x["id"] = x.get("id") or pl_proximo_id(p, "PG")
        if not any(y["id"] == x["id"] for y in ag["pedidos"]):
            ag["pedidos"].append(x)
    ag["parar"] = [x for x in ag.get("parar", []) if st[x["id"]]["status"] == "mantido"]
    for x in rev.get("parar", []):
        x = dict(x)
        x["id"] = x.get("id") or pl_proximo_id(p, "PF")
        if not any(y["id"] == x["id"] for y in ag["parar"]):
            ag["parar"].append(x)
    _pl_comum(p, rev, log, erros)
    for k in range(semana + 1, nova):
        per = p["janelas"]["semanas"][k - 1]
        p["historico"].append({"ciclo": p.get("ciclo", 1), "semana": k, "periodo": list(per), "fechada_em": rev["data"],
                               "recesso": True, "itens": {}})
        log.append(f"S{k} ({pl_periodo(*per)}) no recesso: fechada sem atividades")
    if nova > semana + 1:
        log.append(f"A semana nova é a S{nova} ({pl_periodo(*p['janelas']['semanas'][nova - 1])}): a próxima revisão é "
                   f"em {pl_dm(p['janelas']['semanas'][nova - 1][1])}" + (", a virada do ciclo" if nova == 4 else ""))
    p["semana"] = nova
    p["data"] = rev["data"]
    return p, log, erros, avisos


def _pl_comum(p, rev, log, erros):
    """Pulso dos KPIs, radar, descartados e mudanças: o que a revisão e a virada têm em comum."""
    itens = pl_itens(p)
    for k, v in rev.get("kpis", {}).items():
        if k not in itens or itens[k][0] != "kpi":
            erros.append(f"KPI {k} não existe no plano")
            continue
        if v.get("valor") is not None and not (v.get("fonte") and v.get("data")):
            erros.append(f"KPI {k}: valor novo sem fonte e data")
            continue
        itens[k][1].setdefault("pulsos", []).append({c: v.get(c) for c in ("valor", "data", "fonte", "status") if v.get(c) is not None})
        if v.get("status"):
            itens[k][1]["status"] = v["status"]
        if v.get("valor") is not None:
            itens[k][1]["ultimo"] = {c: v.get(c) for c in ("valor", "data", "fonte")}
        log.append(f"KPI {k}: " + (f"{v['valor']} ({pl_dm(v['data'])})" if v.get("valor") is not None else "sem dado novo")
                   + (f", status {v['status']}" if v.get("status") else ""))
    for d in rev.get("descartar", []):
        d = {"texto": d.get("texto") if isinstance(d, dict) else str(d), "data": rev["data"],
             "origem": (d.get("origem") if isinstance(d, dict) else None) or "busca"}
        if not any(pl_norm(x["texto"]) == pl_norm(d["texto"]) for x in p.setdefault("descartados", [])):
            p["descartados"].append(d)
            log.append(f"Descartado: {d['texto']}")
    if "fora_do_plano" in rev:
        desc = {pl_norm(x["texto"]) for x in p.get("descartados", [])}
        radar, fora = [], []
        for t in rev["fora_do_plano"]:
            (fora if pl_norm(t.get("tema")) in desc or any(x and x in pl_norm(t.get("tema")) for x in desc) else radar).append(t)
        p["fora_do_plano"] = radar[:5]
        if fora:
            log.append("Fora do radar por já terem sido descartados: " + ", ".join(t["tema"] for t in fora))
        if len(radar) > 5:
            log.append(f"Radar com {len(radar)} temas: ficaram os 5 primeiros")
    for m in rev.get("mudancas", []):
        _pl_mudar(p, m, log, erros, rev["data"])


def _pl_mudar(p, m, log, erros, data):
    itens = pl_itens(p)
    op, alvo = m.get("op"), m.get("id")
    if op == "novo":
        lista = {"resultado": p.setdefault("resultados", []), "marco": p.setdefault("marcos", []),
                 "prioridade": p.setdefault("prioridades", []), "kpi": p.setdefault("kpis", []),
                 "risco": p.setdefault("riscos", [])}.get(m.get("tipo"))
        if lista is None:
            erros.append(f"Mudança novo: tipo {m.get('tipo')!r} (resultado, marco, prioridade, kpi ou risco)")
            return
        item = dict(m.get("item", {}))
        item["id"] = item.get("id") or pl_proximo_id(p, {"resultado": "R", "marco": "M", "prioridade": "P", "kpi": "K",
                                                          "risco": "RB"}[m["tipo"]])
        lista.append(item)
        log.append(f"Novo {m['tipo']} {item['id']}: {item.get('texto') or item.get('nome', '')}")
        return
    if alvo not in itens:
        erros.append(f"Mudança {op}: {alvo!r} não existe no plano (IDs: {', '.join(itens)})")
        return
    tipo, it = itens[alvo]
    if op == "editar":
        it.update(m.get("campos", {}))
        log.append(f"{alvo} editado: {', '.join(m.get('campos', {}))}")
    elif op == "replanejar":
        if not m.get("data") or not m.get("motivo"):
            erros.append(f"Replanejar {alvo}: precisa da nova data e do motivo")
            return
        it.setdefault("replanejamentos", []).append({"de": it.get("data"), "para": m["data"], "motivo": m["motivo"], "em": data})
        log.append(f"{alvo} replanejado de {pl_dm(it['data']) if it.get('data') else '–'} para {pl_dm(m['data'])}: {m['motivo']}")
        it["data"] = m["data"]
    elif op == "cortar_escopo":
        if not m.get("texto") or not m.get("corte"):
            erros.append(f"Cortar escopo de {alvo}: precisa do texto novo e do que sai (corte)")
            return
        campo = "texto"
        if tipo == "prioridade":
            if m.get("semana") not in ("S1", "S2", "S3", "S4"):
                erros.append(f"Cortar escopo de {alvo}: diga a semana do entregável (S1 a S4)")
                return
            antes = it.setdefault("entregaveis", {}).get(m["semana"], "")
            it["entregaveis"][m["semana"]] = m["texto"]
            campo = f"entregável {m['semana']}"
        else:
            antes = it.get("texto", "")
            it["texto"] = m["texto"]
        it.setdefault("cortes", []).append({"antes": antes, "depois": m["texto"], "corte": m["corte"],
                                            "motivo": m.get("motivo", ""), "em": data})
        log.append(f"{alvo} com escopo cortado ({campo}): sai {m['corte']}; a data se mantém")
    elif op == "concluir":
        it["status"] = "concluido"
        it["concluido_em"] = m.get("data") or data
        it["fonte_conclusao"] = m.get("fonte", "")
        log.append(f"{alvo} concluído em {pl_dm(it['concluido_em'])}")
    elif op == "cancelar":
        if not m.get("motivo"):
            erros.append(f"Cancelar {alvo}: precisa do motivo")
            return
        afet = pl_afetados(p, alvo)
        if m.get("confirmado") != afet:
            erros.append(f"Cancelar {alvo} afeta {', '.join(afet)}: mostre a lista ao usuário e mande \"confirmado\" com ela")
            return
        for i in afet:
            t, x = itens[i]
            for lista in (p.get("resultados", []), p.get("marcos", []), p.get("prioridades", []), p.get("kpis", []),
                          p.get("agenda", {}).get("atividades", []), p.get("agenda", {}).get("delegacoes", [])):
                if x in lista:
                    lista.remove(x)
        p.setdefault("cancelados", []).append({"ids": afet, "motivo": m["motivo"], "data": data})
        log.append(f"Cancelados {', '.join(afet)}: {m['motivo']}")
    else:
        erros.append(f"Mudança {op!r} desconhecida (novo, editar, replanejar, cortar_escopo, concluir ou cancelar)")


# ---------------------------------------------------------------- virada do ciclo
def pl_virar(plano, vir):
    """4ª revisão: fecha a semana e o ciclo e anda as janelas 4 semanas. `vir` = o mesmo da revisão, mais
    "fechamento": {Pid: {"status", "aprendizado"}}, "resultados_atingidos": {Rid: "registro"} e, opcional,
    "prioridades" (as do novo ciclo). Os itens mantêm as datas; os marcos que caem nas novas S1–S4 viram
    entregáveis da prioridade do mesmo resultado. Devolve (plano novo, log, erros, avisos)."""
    erros, avisos = [], []
    if plano.get("semana", 1) != 4:
        erros.append(f"A virada é na 4ª revisão do ciclo; o plano está na semana {plano.get('semana')} de 4: use revisar")
    fecha = copy.deepcopy(vir.get("fechamento", {}))
    for pr in plano.get("prioridades", []):
        f = fecha.get(pr["id"])
        if not f or f.get("status") not in PL_FECHA:
            erros.append(f"Fechamento de {pr['id']} {pr.get('nome')}: status ({', '.join(PL_FECHA)}), o que aconteceu, "
                         "por quê e o que repetir ou mudar")
            continue
        if not f.get("aprendizado"):
            erros.append(f"Fechamento de {pr['id']}: falta o que repetir ou mudar (aprendizado)")
        if f["status"] != "atingida" and not f.get("porque"):
            erros.append(f"Fechamento de {pr['id']} ({f['status']}): falta o porquê da diferença (porque)")
    if erros:
        return plano, [], erros, avisos
    p, log, erros, avisos = pl_revisar(plano, dict(vir, _virada=True))
    if erros:
        return plano, log, erros, avisos
    ex_ciclo = pl_execucao_ciclo(p, p.get("ciclo", 1))
    res = {r["id"]: r for r in p.get("resultados", [])}
    for pr in plano.get("prioridades", []):
        f, r = fecha[pr["id"]], res.get(pr.get("resultado"), {})
        f["esperado"] = pr.get("feito_quando", "")
        tipo = r.get("compromisso")
        if f["status"] != "atingida" and tipo == "comprometido":
            avisos.append(f"{pr['id']} {pr.get('nome')} {f['status']} num resultado comprometido ({r.get('id')}): explique a "
                          "diferença e combine o plano de recuperação")
        elif f["status"] == "parcial" and tipo == "aspiracional":
            log.append(f"{pr['id']} {pr.get('nome')} parcial num resultado aspiracional ({r.get('id')}): dentro do esperado "
                       "(cerca de 70% já é bom)")
    if ex_ciclo["pct"] is not None:
        log.append(f"Execução do ciclo {p.get('ciclo', 1)}: " + pl_execucao_txt(ex_ciclo).split("Execução: ", 1)[1])
        for r in p.get("resultados", []):
            ks = [x for x in p.get("kpis", []) if x["id"] in r.get("kpis", [])]
            k = next((x for x in ks if x.get("tipo") == "resultado"), ks[0] if ks else {})
            leitura = ("execução alta: se o resultado não andou, questione a alavanca" if ex_ciclo["pct"] >= PL_EXECUCAO_ALVO
                       else "execução baixa: revise o tamanho do plano e a capacidade antes de trocar a alavanca")
            avisos.append(f"{r['id']} · KPI {k.get('id', '–')} {PL_KPI_STATUS.get(k.get('status') or 'sem_dado')} · "
                          f"confiança {r.get('confianca', '–')} · {leitura}")
    j = pl_janelas(vir["data"], inicio=(_pl_d(p["janelas"]["inicio"]) + _pl_dt.timedelta(days=28)).isoformat(),
                   recesso=p.get("recesso_periodos"), rolagem=True)
    fech = {"ciclo": p.get("ciclo", 1), "fechado_em": vir["data"],
            "prioridades": [dict(fecha[x["id"]], id=x["id"], nome=x.get("nome")) for x in plano.get("prioridades", [])],
            "saidos": []}
    # Resultados atingidos saem, com os marcos e KPIs só deles
    for rid, registro in vir.get("resultados_atingidos", {}).items():
        r = next((x for x in p.get("resultados", []) if x["id"] == rid), None)
        if r is None:
            erros.append(f"Resultado {rid} não existe")
            continue
        p["resultados"].remove(r)
        fech["saidos"].append(dict(r, registro=registro))
        for m in [m for m in p.get("marcos", []) if m.get("resultado") == rid]:
            p["marcos"].remove(m)
            fech["saidos"].append(m)
        for k in [k for k in p.get("kpis", []) if k["id"] in r.get("kpis", [])]:
            p["kpis"].remove(k)
            fech["saidos"].append(k)
        log.append(f"{rid} atingido, sai com registro: {registro}")
    # Marcos concluídos saem para o fechamento
    for m in [m for m in p.get("marcos", []) if m.get("status") == "concluido"]:
        p["marcos"].remove(m)
        fech["saidos"].append(m)
        log.append(f"{m['id']} concluído em {pl_dm(m['concluido_em'])}, registrado no fechamento")
    # Prioridades do novo ciclo
    ids_r = {r["id"] for r in p.get("resultados", [])}
    if vir.get("prioridades") is not None:
        p["prioridades"] = [dict(x) for x in vir["prioridades"]]
    else:
        p["prioridades"] = [dict(x, entregaveis={}) for x in p.get("prioridades", []) if x.get("resultado") in ids_r]
    for pr in p["prioridades"]:
        pr.setdefault("entregaveis", {})
    for m in sorted(p.get("marcos", []), key=lambda m: m.get("data") or ""):
        if not m.get("data") or not (j["d30"][0] <= m["data"] <= j["d30"][1]):
            continue
        k = min(4, (_pl_d(m["data"]) - _pl_d(j["inicio"])).days // 7 + 1)
        pr = next((x for x in p["prioridades"] if x.get("resultado") == m.get("resultado")), None)
        if pr is None:
            avisos.append(f"{m['id']} ({pl_dm(m['data'])}) cai nos novos 30 dias, mas nenhuma prioridade tem o {m.get('resultado')}")
            continue
        texto = f"{m['id']}: {m.get('texto')} ({pl_dm(m['data'])})"
        atual = pr["entregaveis"].get(f"S{k}")
        if m["id"] not in (atual or ""):
            pr["entregaveis"][f"S{k}"] = f"{atual} · {texto}" if atual else texto
        m["no_30"] = True
        log.append(f"{m['id']} ({pl_dm(m['data'])}) vira entregável de {pr['id']} {pr.get('nome')} em S{k}")
    for r in p.get("resultados", []):
        if not any(m.get("resultado") == r["id"] and j["d60"][0] <= (m.get("data") or "") <= j["d60"][1] for m in p.get("marcos", [])):
            avisos.append(f"{r['id']} precisa de marco para {pl_periodo(*j['d60'])} (proponha como [suposição])")
    for pr in p["prioridades"]:
        vazias = [f"S{k}" for k in range(1, 5) if not pr["entregaveis"].get(f"S{k}")]
        if vazias:
            avisos.append(f"{pr['id']} {pr.get('nome')} sem entregável em {', '.join(vazias)} (proponha como [suposição])")
    if len(p.get("resultados", [])) < 3:
        avisos.append(f"{len(p.get('resultados', []))} resultados: há espaço para um novo (até 3), a partir do retrato, como [suposição]")
    avisos += j["avisos"]
    fech["execucao"] = ex_ciclo
    p.setdefault("fechamentos", []).append(fech)
    p["janelas"] = j
    p["ciclo"] = p.get("ciclo", 1) + 1
    p["semana"] = 1
    log.append(f"Ciclo {p['ciclo']}: {pl_janelas_txt(j)}")
    if not vir.get("trabalhar_no_recesso"):
        while p["semana"] in j["recesso"] and p["semana"] < 4:
            per = j["semanas"][p["semana"] - 1]
            p["historico"].append({"ciclo": p["ciclo"], "semana": p["semana"], "periodo": list(per), "fechada_em": vir["data"],
                                   "recesso": True, "itens": {}})
            log.append(f"S{p['semana']} ({pl_periodo(*per)}) no recesso: fechada sem atividades")
            p["semana"] += 1
    # Resumo para o 1-1 com o gestor (até 5 linhas)
    desafio = (p.get("retrato", {}).get("desafio_central") or {}).get("texto")
    saidos = [x for x in fech["saidos"] if x.get("registro")]
    p["resumo_gestor"] = [
        f"Ciclo {fech['ciclo']} fechado: " + "; ".join(f"{x['id']} {x.get('nome')} {x['status']}" for x in fech["prioridades"]),
        "Saem: " + ("; ".join(f"{x['id']} {x.get('texto')} ({x['registro']})" for x in saidos) or "nenhum resultado"),
        f"Ciclo {p['ciclo']} ({pl_periodo(*j['d30'])}): " + ", ".join(f"{x['id']} {x.get('nome')}" for x in p["prioridades"])
        + (f" · desafio central: {desafio}" if desafio else ""),
        "Pedidos em aberto: " + ("; ".join(f"{x['id']} · {x.get('tipo', '')} · {x.get('texto', '')}"
                                           for x in p.get("agenda", {}).get("pedidos", [])) or "nenhum"),
        f"Execução do ciclo: {ex_ciclo['pct']}% · confiança: "
        + (", ".join(f"{r['id']} {r.get('confianca', '–')}" for r in p.get("resultados", [])) or "–")]
    return p, log, erros, avisos

# ==== gestao/_codigo/plano/plano_pptx.py
# ---------------------------------------------------------------- arquivo do plano 30-60-90 (.pptx)
# Quatro slides (plano em uma página, as 4 semanas, scorecard, minha semana), com os dados gravados numa forma
# oculta do 1º slide: o arquivo é o estado do plano. Usa os ajudantes de layout de pptx/gerar_pauta.py.
import json
import re

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

PL_COR = {"D": "4F8A5B", "R": "7D5DA2", "M": "9F88BA", "P": "087BA7", "K": "C27C3E", "A": "00ABA3"}
PL_TIPO_KPI = {"resultado": "Resultado", "direcionador": "Direcionador", "saude": "Saúde"}
PL_TIPO_RES = {"comprometido": "Comprometido", "aspiracional": "Aspiracional"}
PL_MARCAS = re.compile(r"\s*\[(?:suposição|a confirmar|a levantar|a elaborar)\]", re.I)


def pl_limpo(texto):
    """Texto da tabela final: sem as marcações entre colchetes."""
    return PL_MARCAS.sub("", str(texto or "")).strip()


def _pl_tabela(s, x, y, cab, larguras, linhas, pt=10.5, alt=0.42, cores=None):
    """Tabela no estilo das pautas. linhas: listas de células (texto ou lista de linhas). cores: cor da 1ª coluna."""
    gf = s.shapes.add_table(len(linhas) + 1, len(cab), Inches(x), Inches(y), Inches(sum(larguras)),
                            Inches(0.36 + alt * len(linhas)))
    tbl = gf.table
    gf._element.graphic.graphicData.tbl.tblPr.find(qn("a:tableStyleId")).text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    tbl.first_row = tbl.horz_banding = False
    for i, w in enumerate(larguras):
        tbl.columns[i].width = Inches(w)
    tbl.rows[0].height = Inches(0.36)
    for i, h in enumerate(cab):
        _celula(tbl.cell(0, i), h, 9.5, COR["suave"], COR["fundo"], True)
    for n, linha in enumerate(linhas, start=1):
        tbl.rows[n].height = Inches(alt)
        fundo = COR["linha_a"] if n % 2 else COR["linha_b"]
        for i, v in enumerate(linha):
            v = [pl_limpo(x) for x in v] if isinstance(v, list) else pl_limpo(v)
            if i == 0 and cores:
                _celula(tbl.cell(n, i), v, pt, "FFFFFF", cores[n - 1], True)
            else:
                _celula(tbl.cell(n, i), v, pt, COR["texto"], fundo)
    return tbl


def _pl_slide(prs, titulo, sub):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = _rgb(COR["fundo"])
    _caixa(s, 0.45, 0.25, 12.4, 0.55, titulo, 24, COR["titulo"], True)
    _caixa(s, 0.45, 0.82, 12.4, 0.35, sub, 12, COR["suave"])
    return s


def _pl_notas(s, linhas):
    s.notes_slide.notes_text_frame.text = "\n".join(linhas) if linhas else "Sem fontes registradas."


def _pl_altura(itens, largura, pt):
    """Altura estimada de um bloco (título + linhas com quebra), em polegadas."""
    por_linha = max(20, int(largura * 13.5 * 10.5 / pt))
    linhas = sum(max(1, -(-len(x) // por_linha)) for x in itens) or 1
    return 0.3 + linhas * 0.205 * pt / 10.5 + 0.15


def _pl_blocos(s, blocos, x, y, w, pt=10.5):
    """Desenha os blocos (título, itens) em coluna a partir de y. Devolve o y do fim."""
    for titulo, itens in blocos:
        _caixa(s, x, y, w, 0.3, titulo, 10, COR["suave"], True)
        y += 0.3
        txt = list(itens) or ["–"]
        h = _pl_altura(txt, w, pt) - 0.45
        tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for i, linha in enumerate(txt):
            par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            _run(par, linha, pt, COR["texto"])
        y += h + 0.15
    return y


def _pl_fonte(it):
    return f" {it['fonte']}" if it.get("fonte") else ""


def gerar_plano(plano, caminho):
    """Gera o arquivo do plano. Devolve a lista de avisos de layout."""
    j = plano["janelas"]
    usuario = plano.get("usuario") or ""
    prs = nova_apresentacao()
    cab = f"Ciclo {plano.get('ciclo', 1)} · semana {plano.get('semana', 1)} de 4 · {pl_janelas_txt(j)}"
    itens = pl_itens(plano)

    # 1. Plano em uma página
    s = _pl_slide(prs, f"Plano 30-60-90{' · ' + usuario if usuario else ''}", cab)
    direc = {d["id"]: d for d in plano.get("retrato", {}).get("direcionadores", [])}
    desafio = plano.get("retrato", {}).get("desafio_central") or {}
    y_tab = 1.35
    if desafio.get("texto"):
        partes = [f"Desafio central: {pl_limpo(desafio['texto'])}"]
        if desafio.get("politica"):
            partes.append(f"Como vamos atacar: {pl_limpo(desafio['politica'])}")
        if desafio.get("nao_vamos"):
            partes.append("Não vamos: " + "; ".join(pl_limpo(x) for x in desafio["nao_vamos"]))
        _caixa(s, 0.45, 1.2, 12.4, 0.45, " · ".join(partes), 10.5, COR["texto"])
        y_tab = 1.75
    linhas, cores, notas = [], [], ["Fontes"]
    if desafio.get("texto"):
        notas.append(f"- Desafio central: {desafio['texto']}{_pl_fonte(desafio)}")
    for r in plano.get("resultados", []):
        d = direc.get(r.get("direcionador"), {})
        ks = [itens[k][1] for k in r.get("kpis", []) if k in itens]
        marcos = [m for m in plano.get("marcos", []) if m.get("resultado") == r["id"]]
        prios = [p for p in plano.get("prioridades", []) if p.get("resultado") == r["id"]]
        linhas.append([
            f"{d.get('id', '')} {d.get('texto', '')}".strip() or "–",
            [f"{r['id']} · {r.get('texto', '')}"] + [f"KPI {k['id']}: {k.get('nome', '')} · meta 90: {k.get('metas', {}).get('90') or '–'}" for k in ks]
            + [f"Dono: {r.get('dono') or '–'} · até {pl_dm(r.get('data') or j['d90'][1])}"]
            + ([" · ".join(x for x in (PL_TIPO_RES.get(r.get("compromisso"), ""),
                                       f"confiança {r['confianca']}/10" if r.get("confianca") is not None else "") if x)]
               if r.get("compromisso") or r.get("confianca") is not None else []),
            [("✓ " if m.get("status") == "concluido" else "") + f"{m['id']} {pl_dm(m['data']) if m.get('data') else 's/ data'} · {m.get('texto', '')}"
             for m in marcos] or "–",
            [f"{p['id']} {p.get('nome', '')}" + (f" · Feito quando: {p['feito_quando']}" if p.get("feito_quando") else "") for p in prios] or "–"])
        cores.append(PL_COR["D"])
        notas += [f"- {x['id']}: {x.get('texto') or x.get('nome', '')}{_pl_fonte(x)}" for x in [d, r] + marcos + prios if x]
        if r.get("ataca"):
            notas.append(f"  {r['id']} ataca o desafio central: {r['ataca']}")
    for p in plano.get("prioridades", []):
        if not p.get("resultado") or p.get("resultado") not in itens:
            linhas.append(["–", "–", "–", f"{p['id']} {p.get('nome', '')}" + (f" · Feito quando: {p['feito_quando']}" if p.get("feito_quando") else "")])
            cores.append(PL_COR["D"])
    riscos = plano.get("riscos", [])
    livre = 7.3 - y_tab - 0.36 - (0.55 if riscos else 0)
    alt = max(0.5, min(1.3, livre / max(1, len(linhas))))
    _pl_tabela(s, 0.45, y_tab, ["DIRECIONADOR", "90 DIAS · RESULTADO", "60 DIAS · MARCOS", "30 DIAS · PRIORIDADE"],
               [2.3, 3.4, 3.4, 3.33], linhas, 10, alt, cores)
    if riscos:
        y = min(6.75, y_tab + 0.36 + alt * len(linhas) + 0.12)
        _caixa(s, 0.45, y, 12.4, 0.5, "Riscos (pré-mortem): " + " · ".join(
            f"{x.get('id', '')} {pl_limpo(x.get('texto'))}" + (f" → {pl_limpo(x['mitigacao'])}" if x.get("mitigacao") else " → sem mitigação")
            for x in riscos), 10, COR["suave"])
    for d in plano.get("descartados", []):
        notas.append(f"Descartado em {pl_dm(d['data'])} ({d.get('origem', '')}): {d['texto']}")
    _pl_notas(s, notas)
    dados = s.shapes.add_textbox(Inches(0), Inches(7.45), Inches(0.5), Inches(0.05))
    dados.name = "plano-dados"
    dados.text_frame.text = json.dumps(plano, ensure_ascii=False)
    dados.text_frame.paragraphs[0].runs[0].font.size = Pt(1)
    dados._element.nvSpPr.cNvPr.set("hidden", "1")

    # 2. As 4 semanas
    semana = plano.get("semana", 1)
    s = _pl_slide(prs, "As 4 semanas", cab)
    cab_s = ["PRIORIDADE"]
    for k in range(1, 5):
        a, b = j["semanas"][k - 1]
        cab_s.append(f"S{k} · {pl_periodo(a, b)}" + (" · recesso" if k in j.get("recesso", []) else "")
                     + (" ◀ próxima" if k == semana else ""))
    linhas = [[f"{p['id']} {p.get('nome', '')}"] + [p.get("entregaveis", {}).get(f"S{k}") or "–" for k in range(1, 5)]
              for p in plano.get("prioridades", [])]
    _pl_tabela(s, 0.45, 1.35, cab_s, [2.0, 2.6, 2.6, 2.6, 2.63], linhas, 10.5,
               max(0.6, min(1.5, 5.4 / max(1, len(linhas)))), [PL_COR["P"]] * len(linhas))
    _pl_notas(s, ["Fontes"] + [f"- {p['id']}: {p.get('nome')}{_pl_fonte(p)}" for p in plano.get("prioridades", [])])

    # 3. Scorecard
    s = _pl_slide(prs, "Scorecard", cab)
    linhas = []
    for k in plano.get("kpis", []):
        ult = k.get("ultimo") or {}
        st = PL_KPI_STATUS.get(k.get("status") or "sem_dado", "⚪")
        metas = k.get("metas", {})
        par = k.get("par")
        par_txt = (f"Par: {par} {itens[par][1].get('nome', '')}" if par in itens else f"Par: {par}") if par else None
        linhas.append([k["id"], [k.get("nome", "")] + ([k["definicao"]] if k.get("definicao") else []) + ([par_txt] if par_txt else []),
                       PL_TIPO_KPI.get(k.get("tipo"), k.get("tipo", "")), pl_limpo(k.get("fonte_dado")) or "–",
                       k.get("baseline") or "a levantar", metas.get("30") or "–", metas.get("60") or "–", metas.get("90") or "–",
                       k.get("frequencia") or "–", k.get("dono") or "–",
                       f"{st} {ult['valor']} ({pl_dm(ult['data'])})" if ult.get("valor") is not None else st])
    alt = max(0.42, min(0.8, 5.0 / max(1, len(linhas))))
    _pl_tabela(s, 0.45, 1.35, ["ID", "KPI", "TIPO", "FONTE", "BASELINE", "META 30", "META 60", "META 90", "FREQ.", "DONO", "STATUS"],
               [0.45, 2.75, 1.05, 1.45, 1.1, 0.9, 0.9, 0.9, 0.85, 0.8, 1.28], linhas, 9.5, alt, [PL_COR["K"]] * len(linhas))
    conf = [f"{r['id']} {r['confianca']}" for r in plano.get("resultados", []) if r.get("confianca") is not None]
    _caixa(s, 0.45, min(6.85, 1.35 + 0.36 + alt * len(linhas) + 0.15), 12.4, 0.4,
           pl_execucao_txt(pl_execucao_ciclo(plano)) + (" · Confiança (0–10): " + " · ".join(conf) if conf else ""),
           10, COR["suave"])
    _pl_notas(s, ["Fontes"] + [f"- {k['id']}: {k.get('nome')}{_pl_fonte(k)}" for k in plano.get("kpis", [])])

    # 4. Minha semana
    ag = plano.get("agenda", {})
    a, b = j["semanas"][min(semana, 12) - 1]
    s = _pl_slide(prs, f"Minha semana · S{semana} · {pl_periodo(a, b)}",
                  f"Esforço planejado: {sum(float(x.get('esforco_h') or 0) for x in ag.get('atividades', [])):g} h · "
                  + " · ".join(f"Frente própria: {f['nome']}" for f in ag.get("frentes", [])))
    linhas, extra = [], 0
    for x in ag.get("atividades", []):
        cel = [x.get("texto", "")] + ([f"Quando: {x['quando']}"] if x.get("quando") else []) \
            + ([f"Se-então: {x['se_entao']}"] if x.get("se_entao") else [])
        extra = max(extra, len(cel) - 1)
        linhas.append([x["id"], x.get("liga", ""), cel if len(cel) > 1 else cel[0], x.get("feito_quando", ""),
                       f"{float(x['esforco_h']):g} h" if x.get("esforco_h") else "–"])
    tbl_alt = 0.38 + 0.2 * extra
    _pl_tabela(s, 0.45, 1.3, ["ID", "LIGA A", "ATIVIDADE", "FEITO QUANDO", "ESFORÇO"], [0.55, 1.9, 4.9, 4.2, 0.88],
               linhas, 10, tbl_alt, [PL_COR["A"]] * len(linhas))
    y = 1.3 + 0.36 + tbl_alt * len(linhas) + 0.25
    blocos = ([("VITÓRIAS DA SEMANA PASSADA", [pl_limpo(v) for v in plano["vitorias"]])] if plano.get("vitorias") else []) + [
              ("DELEGAÇÕES A CHECAR", [f"{d['id']} · {d.get('quem', '')} · {pl_limpo(d.get('oque', ''))} · checar em "
                                       + (pl_dm(d['checar']) if d.get('checar') else '–') for d in ag.get("delegacoes", [])]),
              ("PEDIDOS AO GESTOR", [f"{x['id']} · {x.get('tipo', '')} · {pl_limpo(x.get('texto', ''))}" for x in ag.get("pedidos", [])]),
              ("PARAR DE FAZER", [f"{x['id']} · {pl_limpo(x.get('texto', ''))}" for x in ag.get("parar", [])])]
    avisos = []
    alto = lambda bs, w: sum(_pl_altura(i or ["–"], w, 10.5) for _, i in bs)
    esq = [b for b in blocos if b[0] in ("VITÓRIAS DA SEMANA PASSADA", "DELEGAÇÕES A CHECAR")]
    dir_ = [b for b in blocos if b not in esq]
    if y + alto(blocos, 12.4) <= 7.35:
        _pl_blocos(s, blocos, 0.45, y, 12.4)
    elif y + max(alto(esq, 6.05), alto(dir_, 6.05)) <= 7.35:
        _pl_blocos(s, esq, 0.45, y, 6.05)
        _pl_blocos(s, dir_, 6.8, y, 6.05)
    else:
        # Semana cheia: delegações, pedidos e parar de fazer vão para um slide de continuação
        _caixa(s, 0.45, y, 12.4, 0.3, "Delegações, pedidos ao gestor e parar de fazer: no próximo slide", 10.5, COR["suave"])
        s2 = _pl_slide(prs, f"Minha semana · S{semana} · {pl_periodo(a, b)} (continuação)", "Delegações, pedidos ao gestor e parar de fazer")
        f1 = _pl_blocos(s2, esq, 0.45, 1.3, 6.05)
        f2 = _pl_blocos(s2, dir_, 6.8, 1.3, 6.05)
        if max(f1, f2) > 7.4:
            avisos.append("Minha semana (continuação) passou da altura do slide: confira o último slide")
        _pl_notas(s2, ["Continuação de Minha semana"])
    _pl_notas(s, ["Fontes"] + [f"- {x['id']}: {x.get('texto') or x.get('oque', '')}{_pl_fonte(x)}"
                               for x in ag.get("atividades", []) + ag.get("delegacoes", []) + ag.get("pedidos", [])])
    prs.save(caminho)
    return avisos


PL_ID = re.compile(r"\b(?:DL|PG|PF|RB|[RMPKAD])\d+\b\s*(?::\s*)?")
PL_PUBLICOS = {"gestor": "gestor", "time": "time"}


def pl_sem_id(texto):
    """Texto para apresentar: sem as marcações entre colchetes e sem os IDs do plano (M3:, DL2:…)."""
    return re.sub(r"\s{2,}", " ", PL_ID.sub("", pl_limpo(texto))).strip(" ·:")


def gerar_apresentacao(plano, publico, caminho):
    """Versão para apresentar, sem dados gravados e sem IDs. `publico`: "gestor" (com os pedidos, os riscos, a execução e a
    confiança) ou "time" (com quem faz o quê; sem pedidos, parar de fazer, riscos, execução e confiança). Devolve
    (títulos dos slides, avisos)."""
    j = plano["janelas"]
    usuario = plano.get("usuario") or ""
    prs = nova_apresentacao()
    itens = pl_itens(plano)
    sub = (f"Próximos 30 dias: {pl_periodo(*j['d30'])} · 60 dias: {pl_periodo(*j['d60'])} · 90 dias: até {pl_dma(j['d90'][1])}")
    titulos, avisos = [], []

    # 1. Plano em uma página
    s = _pl_slide(prs, f"Plano 30-60-90{' · ' + usuario if usuario else ''}", sub)
    titulos.append("Plano em uma página")
    desafio = plano.get("retrato", {}).get("desafio_central") or {}
    y_tab = 1.35
    partes = ([f"Desafio central: {pl_sem_id(desafio['texto'])}"] if desafio.get("texto") else []) \
        + ([f"Como vamos atacar: {pl_sem_id(desafio['politica'])}"] if desafio.get("politica") else []) \
        + (["Não vamos: " + "; ".join(pl_sem_id(x) for x in desafio["nao_vamos"])] if desafio.get("nao_vamos") else [])
    if partes:
        _caixa(s, 0.45, 1.2, 12.4, 0.5, " · ".join(partes), 11, COR["texto"])
        y_tab = 1.8
    direc = {d["id"]: d for d in plano.get("retrato", {}).get("direcionadores", [])}
    linhas = []
    for r in plano.get("resultados", []):
        ks = [itens[k][1] for k in r.get("kpis", []) if k in itens]
        marcos = [m for m in plano.get("marcos", []) if m.get("resultado") == r["id"]]
        prios = [x for x in plano.get("prioridades", []) if x.get("resultado") == r["id"]]
        tipo = PL_TIPO_RES.get(r.get("compromisso"), "")
        conf = f"confiança {r['confianca']}/10" if publico == "gestor" and r.get("confianca") is not None else ""
        d = direc.get(r.get("direcionador"), {})
        linhas.append([
            [pl_sem_id(r.get("texto", ""))] + ([f"Para: {pl_sem_id(d['texto'])}"] if d.get("texto") else [])
            + [f"{pl_sem_id(k.get('nome', ''))}: meta {pl_limpo(k['metas']['90'])}" for k in ks if k.get("metas", {}).get("90")]
            + [f"Dono: {r.get('dono') or '–'} · até {pl_dm(r.get('data') or j['d90'][1])}"]
            + ([" · ".join(x for x in (tipo, conf) if x)] if (tipo or conf) else []),
            [("✓ " if m.get("status") == "concluido" else "") + (f"{pl_dm(m['data'])} · " if m.get("data") else "")
             + pl_sem_id(m.get("texto", "")) for m in marcos] or "–",
            sum(([pl_sem_id(x.get("nome", ""))] + ([f"Feito quando: {pl_sem_id(x['feito_quando'])}"] if x.get("feito_quando") else [])
                 for x in prios), []) or "–"])
    for x in plano.get("prioridades", []):
        if not x.get("resultado") or x.get("resultado") not in itens:
            linhas.append(["–", "–", [pl_sem_id(x.get("nome", ""))] + ([f"Feito quando: {pl_sem_id(x['feito_quando'])}"] if x.get("feito_quando") else [])])
    alt = max(0.6, min(1.5, (7.2 - y_tab - 0.36) / max(1, len(linhas))))
    _pl_tabela(s, 0.45, y_tab, ["90 DIAS · RESULTADO", "60 DIAS · MARCOS", "30 DIAS · PRIORIDADE"], [4.4, 4.0, 4.03],
               linhas, 10.5, alt, [PL_COR["R"]] * len(linhas))

    # 2. Próximas 4 semanas
    semana = plano.get("semana", 1)
    s = _pl_slide(prs, "Próximas 4 semanas", sub)
    titulos.append("Próximas 4 semanas")
    cab = ["PRIORIDADE"] + [f"{pl_periodo(*j['semanas'][k - 1])}" + (" · recesso" if k in j.get("recesso", []) else "")
                            + (" · agora" if k == semana else "") for k in range(1, 5)]
    linhas = [[pl_sem_id(x.get("nome", ""))] + [pl_sem_id(x.get("entregaveis", {}).get(f"S{k}") or "") or "–" for k in range(1, 5)]
              for x in plano.get("prioridades", [])]
    _pl_tabela(s, 0.45, 1.35, cab, [2.0, 2.6, 2.6, 2.6, 2.63], linhas, 11,
               max(0.7, min(1.6, 5.4 / max(1, len(linhas)))), [PL_COR["P"]] * len(linhas))

    # 3. Como vamos medir (só com KPIs)
    if plano.get("kpis"):
        s = _pl_slide(prs, "Como vamos medir", sub)
        titulos.append("Como vamos medir")
        linhas = []
        for k in plano["kpis"]:
            par = k.get("par")
            par_txt = (f"Par: {itens[par][1].get('nome', '')}" if par in itens else f"Par: {par}") if par else None
            ult = k.get("ultimo") or {}
            st = PL_KPI_STATUS.get(k.get("status") or "sem_dado", "⚪")
            metas = k.get("metas", {})
            linhas.append([[pl_sem_id(k.get("nome", ""))] + ([pl_sem_id(par_txt)] if par_txt else []),
                           PL_TIPO_KPI.get(k.get("tipo"), k.get("tipo", "")), pl_limpo(k.get("baseline")) or "a levantar",
                           metas.get("30") or "–", metas.get("60") or "–", metas.get("90") or "–", k.get("dono") or "–",
                           f"{st} {ult['valor']} ({pl_dm(ult['data'])})" if ult.get("valor") is not None else st])
        alt = max(0.45, min(0.85, 5.0 / max(1, len(linhas))))
        _pl_tabela(s, 0.45, 1.35, ["INDICADOR", "TIPO", "BASELINE", "META 30", "META 60", "META 90", "DONO", "STATUS"],
                   [3.6, 1.2, 1.4, 1.1, 1.1, 1.1, 1.0, 1.93], linhas, 10, alt, [PL_COR["K"]] * len(linhas))
        if publico == "gestor":
            conf = [f"{pl_sem_id(r.get('texto', ''))} {r['confianca']}/10" for r in plano.get("resultados", []) if r.get("confianca") is not None]
            _caixa(s, 0.45, min(6.85, 1.35 + 0.36 + alt * len(linhas) + 0.15), 12.4, 0.4,
                   pl_execucao_txt(pl_execucao_ciclo(plano)) + (" · Confiança: " + " · ".join(conf) if conf else ""), 10, COR["suave"])
    else:
        avisos.append("Sem KPIs no plano: o slide Como vamos medir ficou de fora")

    ag = plano.get("agenda", {})
    if publico == "gestor":
        # 4. O que preciso de você e riscos
        s = _pl_slide(prs, "O que preciso de você", sub)
        titulos.append("O que preciso de você")
        blocos = [("PEDIDOS", [f"{x.get('tipo', '')} · {pl_sem_id(x.get('texto', ''))}" for x in ag.get("pedidos", [])]),
                  ("RISCOS E COMO VAMOS REDUZIR", [f"{pl_sem_id(x.get('texto', ''))} → " + (pl_sem_id(x['mitigacao']) if x.get("mitigacao") else "mitigação a definir")
                                                    for x in plano.get("riscos", [])])]
        if _pl_blocos(s, blocos, 0.45, 1.35, 12.4, 12) > 7.4:
            avisos.append("O que preciso de você passou da altura do slide: confira o último slide")
    else:
        # 4. Quem faz o quê
        s = _pl_slide(prs, "Quem faz o quê", sub)
        titulos.append("Quem faz o quê")
        linhas = [[d.get("quem", ""), pl_sem_id(d.get("frente") or ""), pl_sem_id(d.get("oque", "")),
                   pl_dm(d["checar"]) if d.get("checar") else "–"]
                  for d in sorted(ag.get("delegacoes", []), key=lambda d: d.get("quem", ""))]
        linhas += [[usuario or "Eu", pl_sem_id(f.get("nome", "")), "Frente própria", "–"] for f in ag.get("frentes", [])]
        alt = max(0.42, min(0.8, 5.6 / max(1, len(linhas))))
        _pl_tabela(s, 0.45, 1.35, ["QUEM", "FRENTE", "O QUÊ", "ACOMPANHAMENTO"], [1.9, 2.6, 6.0, 1.93], linhas, 10.5, alt,
                   [PL_COR["A"]] * len(linhas))
        if 1.35 + 0.36 + alt * len(linhas) > 7.4:
            avisos.append("Quem faz o quê passou da altura do slide: confira o último slide")
    for sl in prs.slides:
        _pl_notas(sl, [f"Versão para apresentar ({'gestor' if publico == 'gestor' else 'time'}), gerada do plano de "
                       f"{pl_dm(plano['data'])}. Sem dados gravados: para revisar o plano, use o arquivo do plano."])
    prs.save(caminho)
    return titulos, avisos


def ler_plano(caminho):
    """(dados, None) quando o arquivo tem os dados gravados; (None, colunas) quando é um plano feito à mão: os textos
    de cada coluna do slide, de cima para baixo, com a cor do ponto de status quando houver."""
    prs = Presentation(caminho)
    for s in prs.slides:
        for sh in s.shapes:
            if sh.name == "plano-dados" and sh.has_text_frame:
                return json.loads(sh.text_frame.text), None
    colunas = []
    for n, s in enumerate(prs.slides, start=1):
        largura = prs.slide_width
        formas = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        titulos = [sh for sh in formas if sh.width > largura * 0.6]  # caixas largas: título do slide, não coluna
        formas = sorted((sh for sh in formas if sh not in titulos), key=lambda sh: (sh.left, sh.top))
        grupos = []
        for sh in formas:
            g = next((g for g in grupos if abs(g["meio"] - sh.left) < Inches(1.0)), None)
            if g is None:
                g = {"meio": sh.left, "formas": []}
                grupos.append(g)
            g["formas"].append(sh)
        for g in sorted(grupos, key=lambda g: g["meio"]):
            linhas = []
            for sh in sorted(g["formas"], key=lambda sh: sh.top):
                for par in sh.text_frame.paragraphs:
                    texto = "".join(r.text for r in par.runs).strip()
                    if not texto:
                        continue
                    cor = None
                    for r in par.runs:
                        try:
                            rgb = r.font.color.rgb
                        except Exception:
                            rgb = None
                        if rgb is not None and r.text.strip() in ("●", "•", "⬤"):
                            cor = _status(tuple(rgb))
                    linhas.append({"texto": texto.lstrip("●•⬤ ").strip(), "cor": cor})
            if linhas:
                colunas.append({"slide": n, "titulo": linhas[0]["texto"], "linhas": linhas[1:]})
    return None, colunas

# ==== gestao/_codigo/plano/cli_gestao.py
# ---------------------------------------------------------------- linha de comando do Coach de Gestão
# O agente grava o pedido em /mnt/data/gestao_pedido.json e roda este script. Ações: janelas, ler, capacidade,
# consistencia, afetados, gerar (Montar, revisão ou virada) e apresentar (versão para o gestor ou o time). O agente não calcula datas nem escreve código de layout.
import json
import os
import re
import sys

from pptx import Presentation

PL_TEMAS_1_1 = {"metas & pdp", "carreira", "feedback mutuo", "carga & bem-estar", "pdp", "planos de sucessao"}
PL_PRIVADO = [r"\bcarreira\b", r"\bpromovid[oa]\b", r"promocao (de cargo|para)", r"\bsucess[aã]o\b", r"\bquer ir para\b", r"nao comentar", r"\bsigil",
              r"\bconfidencial", r"licenca[ -]?medica", r"\batestado", r"\bsaude\b", r"\bdoen", r"\bavaliacao de desempenho"]


def _gc_base(argv):
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "gestao_pedido.json")):
            return pasta, os.path.join(pasta, "gestao_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _gc_arquivo(base, nome):
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _gc_privado(texto):
    t = pl_norm(texto)
    return any(re.search(p, t) for p in PL_PRIVADO)


def _gc_partida(base, pedido):
    """O plano do pedido: `plano` (dicionário) ou `partida` (o .pptx anexado, com dados)."""
    if pedido.get("plano"):
        return pedido["plano"]
    dados, _ = ler_plano(_gc_arquivo(base, pedido["partida"]))
    if dados is None:
        raise ValueError("O plano de partida não tem os dados gravados: monte os dados com o usuário e mande em plano")
    return dados


def gc_janelas(base, pedido):
    j = pl_janelas(pedido["data"], pedido.get("s1"), pedido.get("inicio"), pedido.get("recesso"))
    if "pergunta" in j:
        print("\n".join(pl_janelas_opcoes(pedido["data"], pedido.get("recesso"))))
        return 0
    linhas = [f"Data do plano: {pl_dma(j['data'])} · {pl_janelas_txt(j)}",
              "Semanas: " + " · ".join(f"S{k} {pl_periodo(a, b)}" + (" (recesso)" if k in j["recesso"] else "")
                                       for k, (a, b) in enumerate(j["semanas"], start=1)),
              f"30 dias: {pl_periodo(*j['d30'])} · 60 dias: {pl_periodo(*j['d60'])} · 90 dias: {pl_periodo(*j['d90'])}",
              f"Janela de busca do Montar: {pl_periodo(*j['busca'])} (até hoje)"]
    linhas += [f"AVISO: {a}" for a in j["avisos"]]
    json.dump(j, open(os.path.join(base, "gestao_janelas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(linhas))
    return 0


def _gc_txt_plano(d):
    j = d["janelas"]
    linhas = [f"Plano com os dados gravados · data {pl_dma(d['data'])} · ciclo {d.get('ciclo', 1)}, semana {d.get('semana', 1)} de 4",
              pl_janelas_txt(j)]
    desafio = d.get("retrato", {}).get("desafio_central") or {}
    if desafio.get("texto"):
        linhas.append(f"  Desafio central: {desafio['texto']}" + (f" | como vamos atacar: {desafio['politica']}" if desafio.get("politica") else "")
                      + (f" | não vamos: {'; '.join(desafio['nao_vamos'])}" if desafio.get("nao_vamos") else ""))
    for r in d.get("resultados", []):
        linhas.append(f"  {r['id']} | {r.get('prioridade', '')} | {r.get('texto', '')} | KPI {', '.join(r.get('kpis', []))} | dono {r.get('dono', '–')}"
                      f" | {r.get('compromisso') or 'tipo a definir'} | confiança {r.get('confianca', '–')}")
    for m in d.get("marcos", []):
        linhas.append(f"  {m['id']} | {m.get('resultado')} | {m.get('texto', '')} | {pl_dm(m['data']) if m.get('data') else 's/ data'}"
                      + (f" | concluído em {pl_dm(m['concluido_em'])}" if m.get("status") == "concluido" else ""))
    for p in d.get("prioridades", []):
        ent = p.get("entregaveis", {})
        linhas.append(f"  {p['id']} {p.get('nome')} | " + " | ".join(f"S{k}: {ent.get(f'S{k}') or '–'}" for k in range(1, 5)))
    for k in d.get("kpis", []):
        u = k.get("ultimo") or {}
        linhas.append(f"  {k['id']} | {k.get('tipo')} | {k.get('nome')} | baseline {k.get('baseline') or '[a levantar]'} | "
                      f"metas {k.get('metas', {})} | último {u.get('valor', '–')} {('(' + pl_dm(u['data']) + ')') if u.get('data') else ''}"
                      + (f" | par {k['par']}" if k.get("par") else ""))
    for rb in d.get("riscos", []):
        linhas.append(f"  {rb.get('id')} | risco: {rb.get('texto')} | mitigação: {rb.get('mitigacao') or '–'}")
    ag = d.get("agenda", {})
    for a in ag.get("atividades", []):
        linhas.append(f"  {a['id']} | {a.get('liga')} | {a.get('texto')} | feito quando: {a.get('feito_quando')} | {a.get('esforco_h', '–')} h"
                      + (f" | quando: {a['quando']}" if a.get("quando") else "") + (f" | se-então: {a['se_entao']}" if a.get("se_entao") else ""))
    for x in ag.get("delegacoes", []):
        linhas.append(f"  {x['id']} | {x.get('quem')} · {x.get('oque')} · checar em {pl_dm(x['checar']) if x.get('checar') else '–'}")
    for x in ag.get("pedidos", []) + ag.get("parar", []):
        linhas.append(f"  {x['id']} | {x.get('tipo', '')} {x.get('texto', '')}".replace("|  ", "| "))
    if d.get("descartados"):
        linhas.append("Descartados (não trazer de volta): " + "; ".join(x["texto"] for x in d["descartados"]))
    linhas.append(f"Histórico: {len(d.get('historico', []))} semana(s) fechada(s); fechamentos de ciclo: {len(d.get('fechamentos', []))}")
    linhas.append(pl_execucao_txt(pl_execucao_ciclo(d)))
    if d.get("vitorias"):
        linhas.append("Vitórias da última semana: " + "; ".join(d["vitorias"]))
    exc = pl_excecoes(d)
    linhas.append("REVISÃO POR EXCEÇÃO (converse sobre isto; o resto, confirme em bloco):")
    linhas += [f"  - {x}" for x in exc] or ["  - nada fora do trilho no plano: pergunte só o que não saiu como planejado"]
    return linhas


def gc_ler(base, pedido):
    saida, texto = [], []
    for nome in pedido.get("arquivos", []):
        item = {"arquivo": nome}
        texto.append(f"\n=== {nome}")
        try:
            caminho = _gc_arquivo(base, nome)
        except FileNotFoundError as e:
            item["erro"] = str(e)
            texto.append(f"ERRO: {e}")
            saida.append(item)
            continue
        if not caminho.lower().endswith(".pptx"):
            item["erro"] = "formato não lido pelo script"
            texto.append("Formato não lido pelo script: leia o conteúdo na conversa ou peça em texto")
            saida.append(item)
            continue
        prs = Presentation(caminho)
        tem_pauta = any(sh.has_table and sh.table.rows[0].cells[0].text.strip().upper().startswith("CATEGORIA")
                        for s in prs.slides for sh in s.shapes)
        dados, colunas = ler_plano(caminho)
        if dados is not None:
            item["plano"] = dados
            texto += _gc_txt_plano(dados)
        elif tem_pauta:
            d = ler_pauta(caminho, completo=True)
            omitidas = 0
            linhas = []
            for l in d["linhas"]:
                if pl_norm(l["categoria"]) in PL_TEMAS_1_1 or _gc_privado(" ".join([l["tema"], l["texto"], l["anotacoes"]])):
                    omitidas += 1
                    continue
                linhas.append(l)
            item["pauta"] = dict(d, linhas=linhas, omitidas=omitidas)
            texto.append(f"Pauta: {d['titulo']} · {d['semana']}")
            texto.append("Linhas (Categoria | Tema | Texto | Status | Anotações):")
            texto += ["  " + " | ".join([l["categoria"], l["tema"], l["texto"].replace("\n", " / "), l["status"] or "",
                                          l["anotacoes"].replace("\n", " / ")]) for l in linhas]
            if d["combinados"]:
                texto.append("Combinados: " + "; ".join(f"{c['quem']} · {c['oque']} · {c['ate']} · {c['feito'] or 'em aberto'}"
                                                        for c in d["combinados"]))
            if omitidas:
                texto.append(f"{omitidas} linha(s) omitida(s) pelo script: tema do 1-1, carreira, sucessão, saúde ou sigilo "
                             "não entram no plano")
        elif any("30" in c["titulo"] or "60" in c["titulo"] or "90" in c["titulo"] for c in colunas):
            item["plano_sem_dados"] = colunas
            texto.append("Plano SEM os dados gravados (feito à mão). Textos por coluna, de cima para baixo, com a cor do ponto:")
            for c in colunas:
                texto.append(f"  [{c['titulo']}]")
                texto += [f"    {'● ' + x['cor'] if x['cor'] else '(sem cor)'} · {x['texto']}" for x in c["linhas"]]
            texto.append("Monte os dados com o usuário (status só pela cor; data ou dono ausentes ficam [a confirmar]) antes de revisar")
        else:
            slides = []
            for n, s in enumerate(prs.slides, start=1):
                txts = [sh.text_frame.text.strip() for sh in sorted((x for x in s.shapes if x.has_text_frame), key=lambda x: (x.top, x.left))
                        if sh.text_frame.text.strip()]
                slides.append({"slide": n, "textos": txts})
                texto.append(f"  Slide {n}: " + " / ".join(t.replace("\n", " / ") for t in txts))
            item["slides"] = slides
            texto.append("Fonte de cada item: [Arquivo · <nome curto> · slide N]")
        saida.append(item)
    json.dump(saida, open(os.path.join(base, "gestao_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(texto).strip())
    return 0


def gc_capacidade(base, pedido):
    plano = _gc_partida(base, pedido) if (pedido.get("plano") or pedido.get("partida")) else None
    if pedido.get("semana"):
        sem = pedido["semana"]
    elif plano:
        sem = plano["janelas"]["semanas"][plano.get("semana", 1) - 1]
    else:
        print("Falta a semana ([aaaa-mm-dd, aaaa-mm-dd]) ou o plano")
        return 2
    esforco = pedido.get("esforco_h")
    if esforco is None and pedido.get("atividades"):
        esforco = sum(float(a.get("esforco_h") or 0) for a in pedido["atividades"])
    if esforco is None and plano:
        esforco = sum(float(a.get("esforco_h") or 0) for a in plano.get("agenda", {}).get("atividades", []))
    c = pl_capacidade(sem, pedido.get("reunioes", []), pedido.get("horas_dia", 8), pedido.get("ausencias", []),
                      esforco or 0, pedido.get("recesso"), pedido.get("reserva_pct"), pedido.get("nao_planejado_h"))
    linhas = [f"CAPACIDADE {pl_periodo(*sem)}: {c['dias_uteis']} dias úteis · {c['disponivel_h']:g} h de jornada · "
              f"{c['reunioes']} reuniões, {c['bloqueado_h']:g} h bloqueadas · {c['livres_h']:g} h livres · reserva para o não "
              f"planejado {c['reserva_h']:g} h ({c['reserva_origem']}) · {c['planejaveis_h']:g} h planejáveis · esforço planejado "
              f"{c['esforco_h']:g} h · " + ("cabe" if c["cabe"] else f"NÃO CABE: faltam {-c['folga_h']:g} h; avise e proponha o corte")]
    ref = pl_referencia(plano) if plano else []
    if ref:
        linhas.append("Referência (visão de fora): " + " · ".join(f"S{s} {pl_periodo(*per)}: {feito:g} h concluídas de {plan:g} h"
                                                                   for s, per, feito, plan in ref)
                      + f" · média {sum(x[2] for x in ref) / len(ref):.1f} h concluídas por semana")
        media = sum(x[2] for x in ref) / len(ref)
        if c["esforco_h"] > 1.25 * media:
            linhas.append(f"ATENÇÃO: o esforço planejado ({c['esforco_h']:g} h) passa de 1,25 × o que foi concluído em média "
                          f"({media:.1f} h): pergunte o que mudou para esta semana render mais")
    else:
        linhas.append("Referência: sem semanas fechadas ainda; use a reserva padrão e compare na revisão")
    grandes = [a for a in (pedido.get("atividades") or (plano or {}).get("agenda", {}).get("atividades", []))
               if float(a.get("esforco_h") or 0) > PL_ATIVIDADE_MAX_H]
    for a in grandes:
        linhas.append(f"ATENÇÃO: {a.get('id') or 'atividade'} ({a.get('texto', '')}) com {float(a['esforco_h']):g} h: quebre em passos "
                      f"de até {PL_ATIVIDADE_MAX_H} h antes de estimar")
    print("\n".join(linhas))
    return 0


def gc_consistencia(base, pedido):
    plano = _gc_partida(base, pedido)
    falhas, atencao, sinais = pl_consistencia(plano)
    linhas = ["CONSISTÊNCIA"] + ([f"- {x}" for x in falhas] or ["- tudo ligado: nenhuma falha"])
    if atencao:
        linhas += ["Atenção:"] + [f"- {x}" for x in atencao]
    if sinais:
        linhas += ["Sinal de estrutura (levar ao Coach de Estrutura; não recomende movimento entre pessoas):"] + [f"- {x}" for x in sinais]
    print("\n".join(linhas))
    return 0


def gc_afetados(base, pedido):
    plano = _gc_partida(base, pedido)
    afet = pl_afetados(plano, pedido["alvo"])
    itens = pl_itens(plano)
    if not afet:
        print(f"{pedido['alvo']!r} não existe no plano (IDs: {', '.join(itens)})")
        return 1
    print(f"AFETADOS por {pedido['alvo']}: " + "; ".join(f"{i} {itens[i][1].get('texto') or itens[i][1].get('nome') or itens[i][1].get('oque', '')}"
                                                       for i in afet))
    return 0


def _gc_validar(plano, erros):
    ids = {}
    for i, (t, it) in pl_itens(plano).items():
        ids[i] = t
    vistos = []
    for lista in (plano.get("resultados", []), plano.get("marcos", []), plano.get("prioridades", []), plano.get("kpis", []),
                  plano.get("agenda", {}).get("atividades", []), plano.get("agenda", {}).get("delegacoes", [])):
        for it in lista:
            if not it.get("id"):
                erros.append(f"Item sem ID: {it}")
            elif it["id"] in vistos:
                erros.append(f"ID repetido: {it['id']}")
            vistos.append(it.get("id"))
    for p in plano.get("prioridades", []):
        if p.get("resultado") and p["resultado"] not in ids:
            erros.append(f"{p['id']}: resultado {p['resultado']} não existe")
    for x in plano.get("resultados", []) + plano.get("prioridades", []):
        for k in x.get("kpis", []):
            if ids.get(k) != "kpi":
                erros.append(f"{x['id']}: KPI {k} não existe")
    for m in plano.get("marcos", []):
        if ids.get(m.get("resultado")) != "resultado":
            erros.append(f"{m['id']}: resultado {m.get('resultado')} não existe")
    for k in plano.get("kpis", []):
        if k.get("tipo") not in PL_TIPO_KPI:
            erros.append(f"{k['id']}: tipo {k.get('tipo')!r} (resultado, direcionador ou saude)")
        if k.get("status") and k["status"] not in PL_KPI_STATUS:
            erros.append(f"{k['id']}: status {k['status']!r} (verde, amarelo, vermelho ou sem_dado)")
    textos = []

    def junta(x, chave=None):
        if isinstance(x, dict):
            for k, v in x.items():
                if k not in ("tipo", "id", "descartados", "historico", "fechamentos", "janelas"):
                    junta(v, k)
        elif isinstance(x, list):
            for v in x:
                junta(v, chave)
        elif isinstance(x, str):
            textos.append(x)
    junta(plano)
    if _gc_privado(" · ".join(textos)):
        erros.append("O plano tem termo de carreira, sucessão, saúde ou sigilo: tire e use uma linha neutra com [conversar ao vivo]")


def gc_gerar(base, pedido):
    erros, log, avisos = [], [], []
    try:
        if pedido.get("revisao") or pedido.get("virada"):
            partida = _gc_partida(base, pedido)
            if pedido.get("revisao"):
                plano, log, erros, avisos = pl_revisar(partida, pedido["revisao"])
            else:
                plano, log, erros, avisos = pl_virar(partida, pedido["virada"])
        else:
            plano = dict(pedido["plano"])
            j = pl_janelas(plano["data"], plano.get("s1"), plano.get("inicio_ciclo"), plano.get("recesso_periodos"))
            if "pergunta" in j:
                erros.append("Falta o \"s1\" no plano (não é falha do script). " + " | ".join(
                    pl_janelas_opcoes(plano["data"], plano.get("recesso_periodos"))[:3]))
            else:
                plano["janelas"] = j
                plano.setdefault("ciclo", 1)
                plano.setdefault("semana", 1)
                avisos += j["avisos"]
    except (FileNotFoundError, ValueError, KeyError) as e:
        erros.append(str(e))
    if not erros:
        _gc_validar(plano, erros)
    if erros:
        print("NADA FOI GERADO. Resolva com o usuário e rode de novo:\n" + "\n".join("- " + e for e in erros))
        return 1
    caminho = os.path.join(base, pedido.get("saida") or f"Plano 30-60-90 {plano['data']}.pptx")
    avisos += gerar_plano(plano, caminho)
    relido, _ = ler_plano(caminho)
    prs = Presentation(caminho)
    sujos = [c.text for s in prs.slides for sh in s.shapes if sh.has_table for r in sh.table.rows for c in r.cells
             if PL_MARCAS.search(c.text)]
    falhas, atencao, sinais = pl_consistencia(plano)
    ag = plano.get("agenda", {})
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(caminho)} · {len(prs.slides)} slides · dados gravados · "
            + ("releitura sem diferença" if relido == json.loads(json.dumps(plano, ensure_ascii=False)) else "ATENÇÃO: a releitura difere"),
            f"Ciclo {plano['ciclo']}, semana {plano['semana']} de 4 · {pl_janelas_txt(plano['janelas'])}",
            f"Resultados: {', '.join(r['id'] for r in plano.get('resultados', [])) or 'nenhum'} · Marcos: "
            f"{', '.join(m['id'] for m in plano.get('marcos', [])) or 'nenhum'} · Prioridades: "
            + (", ".join(f"{p['id']} {p.get('nome')}" for p in plano.get("prioridades", [])) or "nenhuma"),
            f"KPIs: {len(plano.get('kpis', []))} · sem baseline: " + (", ".join(k["id"] for k in plano.get("kpis", []) if not k.get("baseline")) or "nenhum"),
            f"Minha semana: {len(ag.get('atividades', []))} atividades, {len(ag.get('delegacoes', []))} delegações, "
            f"{len(ag.get('pedidos', []))} pedidos ao gestor, {len(ag.get('parar', []))} parar de fazer",
            "Tabelas sem marcações entre colchetes" if not sujos else f"ATENÇÃO: marcações nas tabelas: {sujos[:3]}",
            f"Descartados gravados: {len(plano.get('descartados', []))} · semanas no histórico: {len(plano.get('historico', []))}",
            f"Riscos: {len(plano.get('riscos', []))} · sem mitigação: "
            + (", ".join(x.get("id", "?") for x in plano.get("riscos", []) if not x.get("mitigacao")) or "nenhum"),
            pl_execucao_txt(pl_execucao_ciclo(plano, plano.get("ciclo", 1) - (1 if pedido.get("virada") else 0)))]
    if plano.get("vitorias") and (pedido.get("revisao") or pedido.get("virada")):
        conf.append("Vitórias: " + "; ".join(plano["vitorias"]))
    if log:
        conf += ["Mudanças:"] + [f"- {x}" for x in log]
    if avisos:
        conf += ["Avisos:"] + [f"- {x}" for x in avisos]
    if falhas or sinais:
        conf += ["Consistência:"] + [f"- {x}" for x in falhas] + [f"- sinal de estrutura: {x}" for x in sinais]
    if atencao:
        conf += ["Atenção:"] + [f"- {x}" for x in atencao]
    if pedido.get("virada") and plano.get("resumo_gestor"):
        conf += ["RESUMO PARA O 1-1 COM O GESTOR (até 5 linhas, para colar):"] + [f"  {x}" for x in plano["resumo_gestor"]]
    json.dump({"arquivo": caminho, "conferencia": conf, "plano": plano}, open(os.path.join(base, "gestao_resultado.json"), "w",
                                                                            encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def gc_apresentar(base, pedido):
    plano = _gc_partida(base, pedido)
    publico = pl_norm(pedido.get("publico"))
    if publico not in PL_PUBLICOS:
        print(f"Público {pedido.get('publico')!r}: use \"gestor\" ou \"time\". Nada foi gerado")
        return 1
    erros = []
    _gc_validar(plano, erros)
    if erros:
        print("NADA FOI GERADO. Resolva com o usuário e rode de novo:\n" + "\n".join("- " + e for e in erros))
        return 1
    caminho = os.path.join(base, pedido.get("saida") or f"Plano 30-60-90 {plano['data']} (apresentação {publico}).pptx")
    titulos, avisos = gerar_apresentacao(plano, publico, caminho)
    prs = Presentation(caminho)
    textos = [sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame] + \
             [c.text for s in prs.slides for sh in s.shapes if sh.has_table for r in sh.table.rows for c in r.cells]
    tudo = " ".join(textos)
    ids = sorted({m.group(0).strip(" :") for x in textos for m in PL_ID.finditer(x)})
    sem_dados = ler_plano(caminho)[0] is None
    fora = ["pedidos ao gestor", "parar de fazer", "riscos", "execução", "confiança", "sinal de estrutura"] if publico == "time" \
        else ["parar de fazer", "Minha semana", "sinal de estrutura"]
    conf = ["CONFERÊNCIA DA APRESENTAÇÃO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(caminho)} · {len(prs.slides)} slides: " + " · ".join(titulos),
            f"Público: {publico} · fica de fora: " + ", ".join(fora),
            "Sem dados gravados (para revisar o plano, use o arquivo do plano)" if sem_dados else "ATENÇÃO: o arquivo tem dados gravados",
            "Sem IDs nem marcações entre colchetes" if not ids and not PL_MARCAS.search(tudo)
            else f"ATENÇÃO: sobrou ID ou marcação: {ids[:5]}"]
    if publico == "time":
        vaz = [n for n, ok in (("pedidos ao gestor", "PEDIDOS" in tudo), ("parar de fazer", "PARAR DE FAZER" in tudo),
                               ("riscos", "RISCOS E COMO" in tudo), ("confiança", re.search(r"[Cc]onfiança:? \d", tudo))) if ok]
        conf.append("Nada do que é só do gestor" if not vaz else f"ATENÇÃO: apareceu no arquivo do time: {', '.join(vaz)}")
    conf += [f"AVISO: {a}" for a in avisos]
    print("\n".join(conf))
    return 0


def gc_main(argv):
    base, pedido_caminho = _gc_base(argv)
    if not pedido_caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/gestao_pedido.json e rode o script de novo")
        return 2
    pedido = json.load(open(pedido_caminho, encoding="utf-8"))
    acoes = {"janelas": gc_janelas, "ler": gc_ler, "capacidade": gc_capacidade, "consistencia": gc_consistencia,
             "afetados": gc_afetados, "gerar": gc_gerar, "apresentar": gc_apresentar}
    if pedido.get("acao") not in acoes:
        print(f"Ação desconhecida {pedido.get('acao')!r}: use {', '.join(acoes)}")
        return 2
    try:
        return acoes[pedido["acao"]](base, pedido)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERRO: {e}")
        return 1


if __name__ == "__main__":
    _codigo = gc_main(sys.argv)
    if _codigo:
        sys.exit(_codigo)
