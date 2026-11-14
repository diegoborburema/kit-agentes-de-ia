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
