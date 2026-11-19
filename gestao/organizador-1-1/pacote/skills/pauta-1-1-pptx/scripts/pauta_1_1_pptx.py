# Gerado por ferramentas/montar_skills.py a partir de: gestao/_codigo/pptx/ler_pauta.py gestao/_codigo/pptx/gerar_pauta.py gestao/_codigo/pptx/cli_1_1.py. Não edite aqui.

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

# ==== gestao/_codigo/pptx/cli_1_1.py
# ---------------------------------------------------------------- linha de comando do Organizador de 1-1
# O agente grava o pedido em /mnt/data/pauta_pedido.json e roda este script. O script lê as pautas anexadas
# ou gera o .pptx da pauta nova, e imprime o resultado. O agente não escreve código de layout.
import json
import os
import sys

from pptx import Presentation


def _p11_base(argv):
    """(pasta de trabalho, caminho do pedido). O pedido pode vir como argumento ou em pauta_pedido.json."""
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "pauta_pedido.json")):
            return pasta, os.path.join(pasta, "pauta_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _p11_arquivo(base, nome):
    """Caminho de um anexo pelo nome; aceita diferença de maiúsculas."""
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _p11_txt(d):
    linhas = [f"Título: {d['titulo']} · {d['semana']}"]
    linhas += [f"Legenda {g}: {', '.join(itens)}" for g, itens in d["legenda"].items()]
    if not d["linhas"]:
        linhas.append("SEM TABELA. Textos do slide, de cima para baixo (monte as linhas e confirme com o usuário):")
        linhas += ["  " + t.replace("\n", " / ") for t in d["textos"]]
        return linhas
    linhas.append("Linhas (Categoria | Tema | Texto | Tipo | Status | Anotações):")
    for x in d["linhas"]:
        linhas.append("  " + " | ".join([x["categoria"], x["tema"], x["texto"].replace("\n", " / "), x["tipo"],
                                         x["status"] or "", x["anotacoes"].replace("\n", " / ")]))
    linhas.append("Combinados (Quem | O quê | Até | Feito):")
    linhas += ["  " + " | ".join([c["quem"], c["oque"], c["ate"], c["feito"] or "em aberto"]) for c in d["combinados"]]
    return linhas


def p11_ler(base, pedido):
    saida, texto = [], []
    for nome in pedido.get("arquivos", []):
        item = {"arquivo": nome}
        texto.append(f"\n=== {nome}")
        try:
            d = ler_pauta(_p11_arquivo(base, nome), completo=True)
        except FileNotFoundError as e:
            item["erro"] = str(e)
            texto.append(f"ERRO: {e}")
        except Exception as e:
            item["erro"] = f"{type(e).__name__}: {e}"
            texto.append(f"ERRO ao ler: {type(e).__name__}: {e}. Peça a pauta como imagem ou texto")
        else:
            item["pauta"] = d
            texto += _p11_txt(d)
        saida.append(item)
    json.dump(saida, open(os.path.join(base, "pauta_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(texto).strip())
    return 0


def _p11_validar(dados):
    erros = []
    for chave in ("direcao", "pessoa", "semana", "linhas"):
        if chave not in dados:
            erros.append(f"falta o campo {chave!r}")
    if dados.get("direcao") not in ("cima", "baixo"):
        erros.append('direcao deve ser "cima" ou "baixo"')
    for i, l in enumerate(dados.get("linhas", []), start=1):
        if l.get("secao") not in ORDEM:
            erros.append(f"linha {i}: secao {l.get('secao')!r} inválida (válidas: {', '.join(ORDEM)})")
    return erros


def _p11_normalizar(dados):
    """`puxar` deve ser uma lista; um texto só vira 1 bullet, e não um bullet por letra."""
    for l in dados.get("linhas", []):
        if isinstance(l.get("puxar"), str):
            l["puxar"] = [l["puxar"]] if l["puxar"].strip() else []


def p11_gerar(base, pedido):
    dados = pedido.get("pauta") or {}
    _p11_normalizar(dados)
    erros = _p11_validar(dados)
    if erros:
        print("NADA FOI GERADO. Corrija o pedido e rode de novo:\n" + "\n".join("- " + e for e in erros))
        return 1
    caminho = os.path.join(base, pedido.get("saida") or f"1-1 {dados['pessoa']}.pptx")
    try:
        n = gerar_pauta(json.loads(json.dumps(dados)), caminho)
    except Exception as e:
        print(f"NADA FOI GERADO. Erro na geração: {type(e).__name__}: {e}. Entregue só a tabela final")
        return 1

    # Conferência: o arquivo relido, para a entrega descrever só o que ele tem
    d = ler_pauta(caminho, completo=True)
    pedidas = [l["tema"] for l in sorted(dados["linhas"], key=lambda l: ORDEM.index(l["secao"]))
               if l.get("tema") or l.get("atualizacao") or l.get("puxar")]
    lidas = [l["tema"] for l in d["linhas"]]
    notas = ""
    prs = Presentation(caminho)
    if prs.slides[0].has_notes_slide:
        notas = prs.slides[0].notes_slide.notes_text_frame.text
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(caminho)} · {n} slide(s)" + (" · ATENÇÃO: mais de 2 slides, a pauta está longa demais" if n > 2 else ""),
            f"Linhas: {len(lidas)}" + (" (iguais às pedidas, na ordem)" if lidas == pedidas else f" ATENÇÃO: diferentes das pedidas {pedidas}"),
            f"Combinados: {len(d['combinados'])} em aberto + 3 linhas em branco"]
    conf += [f"Legenda {g}: {', '.join(itens)}" for g, itens in d["legenda"].items()]
    conf.append("Perguntas para levar nas notas: " + ("sim" if "Perguntas para levar" in notas else "NÃO"))
    json.dump({"arquivo": caminho, "slides": n, "conferencia": conf},
              open(os.path.join(base, "pauta_resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def p11_main(argv):
    base, pedido_caminho = _p11_base(argv)
    if not pedido_caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/pauta_pedido.json e rode o script de novo")
        return 2
    pedido = json.load(open(pedido_caminho, encoding="utf-8"))
    acao = pedido.get("acao")
    if acao == "ler":
        return p11_ler(base, pedido)
    if acao == "gerar":
        return p11_gerar(base, pedido)
    print(f'Ação desconhecida {acao!r}: use "ler" ou "gerar"')
    return 2


if __name__ == "__main__":
    _codigo_p11 = p11_main(sys.argv)
    if _codigo_p11:
        sys.exit(_codigo_p11)
