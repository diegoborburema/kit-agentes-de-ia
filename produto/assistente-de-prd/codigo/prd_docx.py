# ---------------------------------------------------------------- PRD: leitura e gravação do .docx
# Montado depois de estrutura.py (usa SECOES, CANVAS, ANEXOS, GATES, rotulo, opcoes, secao sem importar).
# Este módulo só lê e grava dados. Quem julga a qualidade de cada seção é o agente.
import copy
import re
import unicodedata
from datetime import date

from docx import Document
from docx.oxml.ns import qn
from docx.shared import RGBColor

GUIA_COR = "808080"
MARCADO, VAZIO_OP = "☒", "☐"


class PedidoInvalido(Exception):
    """Erro no pedido de gravação: nada é gravado."""


def _n(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9.%/ ]", " ", t)).strip()


def _eh_guia(run):
    try:
        cor = run.font.color.rgb if run.font.color is not None and run.font.color.type is not None else None
    except Exception:
        cor = None
    return bool(run.italic) and cor is not None and str(cor).upper() == GUIA_COR


def _texto_celula(cel, pular=0):
    """Texto de uma célula sem a orientação em cinza; `pular` ignora os primeiros parágrafos (título do bloco)."""
    linhas = []
    for p in cel.paragraphs[pular:]:
        t = "".join(r.text for r in p.runs if not _eh_guia(r)).strip()
        if t:
            linhas.append(t)
    return "\n".join(linhas)


def _opcao_valor(texto):
    """'☒ Sim   ☐ Não' -> 'Sim'; só caixas vazias -> ''; texto livre -> o próprio texto."""
    if VAZIO_OP not in texto and MARCADO not in texto:
        return texto
    marcadas = re.findall(r"☒\s*([^☐☒]+)", texto)
    return "; ".join(m.strip() for m in marcadas)


def _nivel(par):
    try:
        nome = (par.style.name or "").lower()
    except Exception:
        nome = ""
    m = re.search(r"(heading|t[ií]tulo)\s*(\d)", nome)
    if m:
        return int(m.group(2))
    ppr = par._p.pPr
    ol = ppr.find(qn("w:outlineLvl")) if ppr is not None else None
    return int(ol.get(qn("w:val"))) + 1 if ol is not None else None


_CANVAS_POR_NOME = {_n(v[0]): k for k, v in CANVAS.items()}


def _mapa(doc):
    """{chave: [tabelas na ordem]}. Chaves: painel, checkpoints, gates, painel_bc, pessoas, '01.1'…,
    'canvas:eng'…, 'gate1', 'gate2', 'A'…'E'. A chave vem do título (Heading) que precede a tabela."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    mapa, atual = {}, None
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            par = Paragraph(el, doc)
            nivel = _nivel(par)
            if not nivel:
                continue
            t = par.text.strip()
            n = _n(t)
            if nivel == 1:
                m = re.match(r"^anexo ([a-e])\b", n)
                g = re.match(r"^gate ([12])\b", n)
                atual = (m.group(1).upper() if m else f"gate{g.group(1)}" if g else
                         "painel" if n.startswith("painel") else None)
            elif nivel == 2:
                m = re.match(r"^(\d\d\.\d)\b", t)
                sub = {"checkpoints": "checkpoints", "gates": "gates", "business case": "painel_bc",
                       "pessoas": "pessoas"}
                atual = m.group(1) if m else sub.get(n, atual)
            elif nivel == 3 and n.startswith("canvas"):
                nome = _n(t.split("·", 1)[-1])
                atual = f"canvas:{_CANVAS_POR_NOME.get(nome, nome)}"
        elif el.tag == qn("w:tbl") and atual:
            mapa.setdefault(atual, []).append(Table(el, doc))
    return mapa


def _blocos_de(sid):
    """Blocos de tabela (campos e tabela) de uma seção ou anexo, na ordem do documento."""
    return [b for b in secao(sid)["blocos"] if b[0] in ("campos", "tabela")]


# ---------------------------------------------------------------- leitura

def _ler_campos(t):
    out = {}
    for row in t.rows:
        rot = _texto_celula(row.cells[0])
        if rot:
            out[rot] = _opcao_valor(_texto_celula(row.cells[-1]))
    return out


def _ler_tabela(t, fixas):
    cab = [_texto_celula(c) for c in t.rows[0].cells]
    linhas = []
    for row in t.rows[1:]:
        vals = [_opcao_valor(_texto_celula(c)) for c in row.cells]
        d = dict(zip(cab, vals))
        chave_fixa = vals and _n(vals[0]) in {_n(f) for f in fixas}
        conteudo = any(v for v in (vals[1:] if chave_fixa else vals))
        if conteudo:
            linhas.append(d)
    return linhas


def _ler_grade(t, chave):
    blocos = {}
    for row in t.rows:
        for cel in row.cells:
            if not cel.paragraphs or not cel.paragraphs[0].text.strip():
                continue
            titulo = cel.paragraphs[0].text.strip()
            blocos[titulo] = _texto_celula(cel, pular=1)
    return blocos


def ler_prd(caminho):
    """Lê o PRD e devolve um dicionário com o painel, as seções, os canvas, os gates e os anexos."""
    doc = Document(caminho)
    mapa = _mapa(doc)
    if not any(k in mapa for k in ("01.1", "painel")):
        raise ValueError("o arquivo não segue o template do PRD (não achei o painel nem a seção 01.1)")
    d = {"painel": {}, "checkpoints": {}, "gates": {}, "painel_bc": {}, "pessoas": {}, "secoes": {}, "canvas": {},
         "gate": {}, "anexos": {}}
    if mapa.get("painel"):
        d["painel"] = _ler_campos(mapa["painel"][0])
    if mapa.get("checkpoints"):
        d["checkpoints"] = {l["Etapa"][:2]: {"situacao": l.get("Situação", ""), "data": l.get("Data", "")}
                            for l in _ler_tabela(mapa["checkpoints"][0], [])}
    if mapa.get("gates"):
        d["gates"] = {l["Gate"][5:6]: {k: v for k, v in l.items() if k != "Gate"}
                      for l in _ler_tabela(mapa["gates"][0], [])}
    if mapa.get("painel_bc"):
        d["painel_bc"] = {k: v for k, v in _ler_campos(mapa["painel_bc"][0]).items() if v}
    if mapa.get("pessoas"):
        d["pessoas"] = {l["Papel"]: {k: v for k, v in l.items() if k != "Papel" and v}
                        for l in _ler_tabela(mapa["pessoas"][0], [])}
    for s in SECOES + ANEXOS:
        tabelas, blocos = mapa.get(s["id"], []), _blocos_de(s["id"])
        sec = {"campos": {}, "tabelas": {}}
        for b, t in zip(blocos, tabelas):
            if b[0] == "campos":
                sec["campos"].update(_ler_campos(t))
            else:
                sec["tabelas"][b[1]] = _ler_tabela(t, b[3])
        sec["vazia"] = not any(sec["campos"].values()) and not any(sec["tabelas"].values())
        (d["anexos"] if len(s["id"]) == 1 else d["secoes"])[s["id"]] = sec
    for chave in CANVAS:
        ts = mapa.get(f"canvas:{chave}", [])
        if len(ts) >= 2:
            ap = _ler_campos(ts[0])
            blocos = _ler_grade(ts[1], chave)
            d["canvas"][chave] = {"aplicavel": ap.get("Aplicável?", ""),
                                  "motivo": ap.get("Motivo, se não se aplica", ""), "blocos": blocos,
                                  "vazio": not any(blocos.values()) and not ap.get("Aplicável?")}
    if "04.2" in d["secoes"]:   # a 04.2 só tem os canvas: está vazia se todos estiverem
        d["secoes"]["04.2"]["vazia"] = all(c["vazio"] for c in d["canvas"].values())
    for n in ("1", "2"):
        ts = mapa.get(f"gate{n}", [])
        if ts:
            d["gate"][n] = {"checklist": _ler_tabela(ts[0], GATES[n][1]),
                            "decisao": _ler_campos(ts[1]) if len(ts) > 1 else {}}
    d["assinado"] = bool(d["painel"].get("Versão assinada"))
    return d


# ---------------------------------------------------------------- gravação

def _limpar(cel, manter=0):
    """Apaga o conteúdo da célula, mantendo os `manter` primeiros parágrafos."""
    for p in cel.paragraphs[max(manter, 1):]:
        p._p.getparent().remove(p._p)
    if manter == 0:
        p = cel.paragraphs[0]
        for r in list(p.runs):
            r._r.getparent().remove(r._r)


def _escrever(cel, texto, manter=0):
    _limpar(cel, manter)
    linhas = str(texto).split("\n") if texto is not None else [""]
    if manter == 0:
        cel.paragraphs[0].add_run(linhas[0])
        linhas = linhas[1:]
    for l in linhas:
        cel.add_paragraph(l)


def _escrever_opcao(cel, ops, valor):
    escolhidas = {_n(v) for v in (valor if isinstance(valor, list) else re.split(r";|,", str(valor)))
                  if str(v).strip()}
    desconhecidas = escolhidas - {_n(o) for o in ops}
    if desconhecidas:
        raise PedidoInvalido(f"opção desconhecida {sorted(desconhecidas)}; válidas: {', '.join(ops)}")
    _escrever(cel, "   ".join(f"{MARCADO if _n(o) in escolhidas else VAZIO_OP} {o}" for o in ops))


def _campos_por_rotulo(t):
    return {_n(_texto_celula(row.cells[0])): row for row in t.rows}


def _gravar_campos(t, lista, valores, onde):
    linhas = _campos_por_rotulo(t)
    por_rotulo = {_n(rotulo(c)): c for c in lista}
    for rot, val in valores.items():
        c = por_rotulo.get(_n(rot))
        row = linhas.get(_n(rot))
        if c is None or row is None:
            raise PedidoInvalido(f"{onde}: campo {rot!r} não existe; campos: {', '.join(rotulo(x) for x in lista)}")
        if opcoes(c):
            _escrever_opcao(row.cells[-1], opcoes(c), val)
        else:
            _escrever(row.cells[-1], val)


def _nova_linha(t, antes=None):
    modelo = t.rows[-1]._tr if antes is None else t.rows[1]._tr
    nova = copy.deepcopy(modelo)
    if antes is None:
        t._tbl.append(nova)
    else:
        antes._tr.addprevious(nova)
    from docx.table import _Row
    row = _Row(nova, t)
    for cel in row.cells:
        _escrever(cel, "")
    return row


def _gravar_linhas(t, colunas, fixas, linhas, onde):
    cab = [_n(_texto_celula(c)) for c in t.rows[0].cells]
    for l in linhas:
        extra = [k for k in l if _n(k) not in cab]
        if extra:
            raise PedidoInvalido(f"{onde}: coluna(s) {extra} não existe(m); colunas: {', '.join(colunas)}")
        chave = _n(l.get(colunas[0], ""))
        alvo = None
        for row in t.rows[1:]:
            if chave and _n(_texto_celula(row.cells[0])) == chave:
                alvo = row
                break
        if alvo is None:
            vazias = [row for row in t.rows[1:] if not any(_texto_celula(c) for c in row.cells)]
            total = next((row for row in t.rows[1:] if _n(_texto_celula(row.cells[0])) == "total"), None)
            alvo = vazias[0] if vazias else _nova_linha(t, antes=total) if total else _nova_linha(t)
        for k, v in l.items():
            _escrever(alvo.cells[cab.index(_n(k))], v)


def _gravar_grade(t, chave, blocos, onde):
    por_titulo = {}
    for row in t.rows:
        for cel in row.cells:
            if cel.paragraphs and cel.paragraphs[0].text.strip():
                por_titulo[_n(cel.paragraphs[0].text)] = cel
    for titulo, texto in blocos.items():
        cel = por_titulo.get(_n(titulo))
        if cel is None:
            validos = ", ".join(b for b, _ in CANVAS[chave][2])
            raise PedidoInvalido(f"{onde}: bloco {titulo!r} não existe; blocos: {validos}")
        _escrever(cel, texto, manter=2)


PROIBIDOS_PAINEL = {_n("Versão assinada")}


def gravar_prd(pedido, base, saida, hoje=None):
    """Grava o pedido em `base` (PRD em andamento ou template) e salva em `saida`. Devolve a lista do que foi
    gravado. Valida tudo antes: um erro no pedido levanta PedidoInvalido e nada é salvo."""
    doc = Document(base)
    mapa = _mapa(doc)
    lido = ler_prd(base)
    hoje = hoje or date.today().strftime("%d/%m/%Y")
    feito = []
    conteudo = any(pedido.get(k) for k in ("campos", "linhas", "canvas", "painel", "checkpoints", "pessoas",
                                           "pendencias", "painel_bc"))
    if lido["assinado"] and conteudo:
        raise PedidoInvalido("PRD ASSINADO: o conteúdo acordado não é reescrito. Registre a mudança em "
                             "\"mudancas\" (Anexo B) e grave só ela")

    painel = pedido.get("painel") or {}
    if any(_n(k) in PROIBIDOS_PAINEL for k in painel):
        raise PedidoInvalido("painel: \"Versão assinada\" é preenchida por quem assina, nunca pelo agente")
    if painel:
        _gravar_campos(mapa["painel"][0], PAINEL_CAMPOS, painel, "painel")
        feito.append(f"painel: {', '.join(painel)}")
    if pedido.get("painel_bc"):
        _gravar_campos(mapa["painel_bc"][0], PAINEL_BC, pedido["painel_bc"], "painel_bc")
        feito.append("painel: business case")
    for etapa, v in (pedido.get("checkpoints") or {}).items():
        num = str(etapa)[:2].zfill(2)
        nome = next((f"{n} · {t}" for n, t, _ in ETAPAS if n == num), None)
        if not nome:
            raise PedidoInvalido(f"checkpoints: etapa {etapa!r} não existe (01 a 05)")
        _gravar_linhas(mapa["checkpoints"][0], ["Etapa", "Situação", "Data"], [],
                       [{"Etapa": nome, "Situação": v.get("situacao", ""), "Data": v.get("data", hoje)}],
                       "checkpoints")
        feito.append(f"checkpoint {num}")
    for papel, v in (pedido.get("pessoas") or {}).items():
        _gravar_linhas(mapa["pessoas"][0], ["Papel", "Nome", "Área"], PESSOAS, [dict(v, Papel=papel)], "pessoas")
        feito.append(f"pessoas: {papel}")

    for sid, valores in (pedido.get("campos") or {}).items():
        try:
            blocos = _blocos_de(sid)
        except KeyError:
            raise PedidoInvalido(f"campos: seção {sid!r} não existe")
        indices = [i for i, b in enumerate(blocos) if b[0] == "campos"]
        if not indices:
            raise PedidoInvalido(f"campos: a seção {sid} não tem campos, só tabela (use \"linhas\")")
        restantes = dict(valores)
        for i in indices:
            lista = blocos[i][1]
            parte = {k: v for k, v in restantes.items() if _n(k) in {_n(rotulo(c)) for c in lista}}
            if parte:
                _gravar_campos(mapa[sid][i], lista, parte, sid)
                for k in parte:
                    restantes.pop(k)
        if restantes:
            todos = [rotulo(c) for i in indices for c in blocos[i][1]]
            raise PedidoInvalido(f"{sid}: campo(s) {list(restantes)} não existe(m); campos: {', '.join(todos)}")
        feito.append(f"{sid}: {len(valores)} campo(s)")

    for alvo, linhas in (pedido.get("linhas") or {}).items():
        sid, _, nome = alvo.partition("/")
        try:
            blocos = _blocos_de(sid)
        except KeyError:
            raise PedidoInvalido(f"linhas: seção {sid!r} não existe")
        idx = next((i for i, b in enumerate(blocos) if b[0] == "tabela" and b[1] == nome), None)
        if idx is None:
            nomes = [b[1] for b in blocos if b[0] == "tabela"]
            raise PedidoInvalido(f"linhas: tabela {alvo!r} não existe; tabelas de {sid}: {', '.join(nomes) or '—'}")
        b = blocos[idx]
        _gravar_linhas(mapa[sid][idx], b[2], b[3], linhas, alvo)
        feito.append(f"{alvo}: {len(linhas)} linha(s)")

    for chave, v in (pedido.get("canvas") or {}).items():
        if chave not in CANVAS:
            raise PedidoInvalido(f"canvas {chave!r} não existe; canvas: {', '.join(CANVAS)}")
        ts = mapa[f"canvas:{chave}"]
        cab = {}
        if "aplicavel" in v:
            cab["Aplicável?"] = v["aplicavel"]
        if v.get("motivo"):
            cab["Motivo, se não se aplica"] = v["motivo"]
        if cab:
            _gravar_campos(ts[0], [("Aplicável?", ["Sim", "Não"]), "Motivo, se não se aplica"], cab, chave)
        if v.get("blocos"):
            _gravar_grade(ts[1], chave, v["blocos"], f"canvas {chave}")
        feito.append(f"canvas {chave}: {len(v.get('blocos') or {})} bloco(s)")

    if pedido.get("pendencias"):
        b = _blocos_de("A")[0]
        _gravar_linhas(mapa["A"][0], b[2], b[3], pedido["pendencias"], "pendencias")
        feito.append(f"Anexo A: {len(pedido['pendencias'])} pendência(s)")
    if pedido.get("mudancas"):
        if any(str(v).strip() for m in pedido["mudancas"] for k, v in m.items() if _n(k) == _n("Decisão")):
            raise PedidoInvalido("mudancas: a \"Decisão\" de um pedido de mudança é preenchida por quem decide, "
                                 "nunca pelo agente")
        b = _blocos_de("B")[1]
        _gravar_linhas(mapa["B"][1], b[2], b[3], pedido["mudancas"], "mudancas")
        feito.append(f"Anexo B: {len(pedido['mudancas'])} pedido(s) de mudança")

    versao = pedido.get("versao") or {}
    if versao.get("numero"):
        b = _blocos_de("B")[0]
        _gravar_linhas(mapa["B"][0], b[2], b[3], [{"Versão": versao["numero"], "Data": hoje,
                                                    "O que mudou": versao.get("o_que_mudou", ""),
                                                    "Autor": versao.get("autor", "")}], "versão")
        if not lido["assinado"]:
            _gravar_campos(mapa["painel"][0], PAINEL_CAMPOS, {"Versão vigente": versao["numero"]}, "painel")
        feito.append(f"versão {versao['numero']}")

    produto = painel.get("Produto") or lido["painel"].get("Produto")
    if produto:
        doc.core_properties.title = f"PRD · {produto}"
    doc.save(saida)
    return feito
