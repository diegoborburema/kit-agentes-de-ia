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
