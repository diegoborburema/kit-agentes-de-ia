# ---------------------------------------------------------------- arquivo da estrutura (.pptx confidencial)
# Três slides (mapa de cobertura, diagnóstico, decisão e transição), "Confidencial" em todos, com os dados gravados numa
# forma oculta do 1º slide. Interesses de desenvolvimento não entram no arquivo.
import json

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ES_MARCA = "CONFIDENCIAL · não circule este arquivo"


def _es_slide(prs, titulo, sub):
    s = _pl_slide(prs, titulo, sub)
    _caixa(s, 8.4, 0.3, 4.5, 0.3, ES_MARCA, 10, "FA7676", True, PP_ALIGN.RIGHT)
    _caixa(s, 0.45, 7.1, 12.4, 0.25, "Confidencial · análise de estrutura · uso do gestor", 9, COR["suave"])
    return s


def gerar_estrutura(e, caminho):
    """Gera o arquivo da análise. Devolve a lista de avisos de layout."""
    prs = nova_apresentacao()
    sub = f"Análise de {pl_dma(e['data'])}" + (f" · gatilho: {e['gatilho']}" if e.get("gatilho") else "")
    carga = es_carga(e.get("mapa", []), e.get("restricoes", []))
    lentes = es_lentes(e.get("mapa", []))

    # 1. Mapa de cobertura: pessoa × frente
    s = _es_slide(prs, "Mapa de cobertura", sub)
    frentes = list(dict.fromkeys(l["frente"] for l in e.get("mapa", [])))
    pessoas = list(carga)
    larg_f = min(1.45, 8.6 / max(1, len(frentes)))
    linhas = []
    for p in pessoas:
        celulas = [f"{p}" + (f" · {carga[p]['papel']}" if carga[p]["papel"] else "")]
        for f in frentes:
            l = next((x for x in e["mapa"] if x["pessoa"] == p and x["frente"] == f), None)
            celulas.append([f"{float(l.get('pct') or 0):g}%", ("dono · " if l.get("dono") else "apoio · ") + (l.get("autonomia") or "–")]
                           if l else "")
        c = carga[p]
        celulas.append([f"{c['soma']:g}% em {len(c['frentes'])} frentes"]
                       + ([f"⚠ acima de {c['disponivel']:g}%"] if c["acima"] else [])
                       + ([f"disponível {c['disponivel']:g}% até {pl_dm(c['ate'])}"] if c["disponivel"] < 100 and c.get("ate") else []))
        linhas.append(celulas)
    _pl_tabela(s, 0.45, 1.35, ["PESSOA"] + [f.upper() for f in frentes] + ["CARGA"],
               [1.6] + [larg_f] * len(frentes) + [1.9], linhas, 9.5, 0.75, ["523D6B"] * len(linhas))
    y = 1.35 + 0.36 + 0.75 * len(linhas) + 0.3
    rodape = []
    if lentes["sem_dono"]:
        rodape.append("Frentes sem dono: " + ", ".join(lentes["sem_dono"]))
    if lentes["varios_donos"]:
        rodape.append("Frentes com mais de um dono: " + ", ".join(lentes["varios_donos"]))
    if e.get("pontos_unicos"):
        rodape.append("Dependem de uma pessoa só: " + "; ".join(e["pontos_unicos"]))
    if e.get("vagas"):
        rodape.append("Vagas em aberto: " + ", ".join(e["vagas"]))
    for t in rodape:
        _caixa(s, 0.45, y, 12.4, 0.3, pl_limpo(t), 11, COR["texto"])
        y += 0.34
    _pl_notas(s, ["Fontes"] + [f"- {l['pessoa']} · {l['frente']}: {l.get('fonte', '')}" for l in e.get("mapa", [])])
    dados = s.shapes.add_textbox(Inches(0), Inches(7.45), Inches(0.5), Inches(0.05))
    dados.name = "estrutura-dados"
    dados.text_frame.text = json.dumps(e, ensure_ascii=False)
    dados.text_frame.paragraphs[0].runs[0].font.size = Pt(1)
    dados._element.nvSpPr.cNvPr.set("hidden", "1")

    # 2. Diagnóstico
    s = _es_slide(prs, "Diagnóstico", sub)
    linhas = [[d["prioridade"] + (f" · {d['risco']}" if d.get("risco") else ""), d["causa"], d.get("secundaria") or "–",
               d.get("evidencia", "")] for d in e.get("diagnostico", [])]
    _pl_tabela(s, 0.45, 1.35, ["PRIORIDADE EM RISCO", "CAUSA PRINCIPAL", "CAUSA SECUNDÁRIA", "EVIDÊNCIA"], [3.0, 1.8, 1.8, 5.83],
               linhas, 10.5, 0.8, ["087BA7"] * len(linhas))
    y = 1.35 + 0.36 + 0.8 * len(linhas) + 0.3
    if e.get("achados"):
        _caixa(s, 0.45, y, 12.4, 0.3, "OUTROS ACHADOS", 10, COR["suave"], True)
        y += 0.32
        for a in e["achados"]:
            _caixa(s, 0.45, y, 12.4, 0.3, "• " + pl_limpo(a), 11, COR["texto"])
            y += 0.32
    _pl_notas(s, ["Fontes"] + [f"- {d['prioridade']}: {d.get('evidencia', '')}" for d in e.get("diagnostico", [])])

    # 3. Decisão e transição
    dec = e.get("decisao") or {}
    s = _es_slide(prs, "Decisão e transição", sub)
    _caixa(s, 0.45, 1.3, 12.4, 0.4, pl_limpo(dec.get("texto") or "Manter: nenhuma mudança"), 13, COR["titulo"], True)
    linhas = []
    for t in dec.get("testes", []):
        r = t.get("resultado")
        linhas.append([t["id"], [pl_limpo(t["movimento"])] + ([f"até {pl_dm(t['ate'])} · {t.get('escopo', '')}"] if t.get("ate") else []),
                       f"{t['nivel']} · {ES_NIVEIS.get(int(t['nivel']), '')}", pl_limpo(t["criterio"]),
                       f"{pl_dm(t['inicio'])}–{pl_dm(t['revisao'])}",
                       ("✓ atingido" if r["atingido"] else "✗ não atingido") + f" ({pl_dm(r['data'])})" if r else "em teste"])
    _pl_tabela(s, 0.45, 1.85, ["ID", "MOVIMENTO", "NÍVEL", "CRITÉRIO DE SUCESSO", "TESTE", "RESULTADO"], [0.5, 3.6, 2.0, 3.6, 1.3, 1.43],
               linhas, 10, 0.85, ["C27C3E"] * len(linhas))
    y = 1.85 + 0.36 + 0.85 * len(linhas) + 0.3
    if e.get("transicao"):
        _caixa(s, 0.45, y, 12.4, 0.3, "TRANSIÇÃO (4 SEMANAS)", 10, COR["suave"], True)
        y += 0.32
        for t in e["transicao"]:
            _caixa(s, 0.45, y, 12.4, 0.3, "• " + pl_limpo(t), 10.5, COR["texto"])
            y += 0.3
    _pl_notas(s, ["Histórico"] + [f"- {pl_dm(h['data'])}: {h['registro']}" for h in e.get("historico", [])])
    prs.save(caminho)
    return [] if y <= 7.05 else ["A transição passou da altura do slide 3: encurte os itens"]


def ler_estrutura(caminho):
    """Os dados gravados da análise, ou None se o arquivo não for uma análise do Coach de Estrutura."""
    for s in Presentation(caminho).slides:
        for sh in s.shapes:
            if sh.name == "estrutura-dados" and sh.has_text_frame:
                return json.loads(sh.text_frame.text)
    return None
