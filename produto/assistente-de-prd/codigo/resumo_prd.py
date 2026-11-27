# ---------------------------------------------------------------- PRD: resumo visual por público (HTML)
# Montado depois de estrutura.py e prd_docx.py (usa ler_prd, _n, SECOES, ETAPAS, CANVAS, GATES sem importar).
# Gera um HTML de um arquivo, com uma aba por público: Sponsor, Time técnico e Revisor. Mostra o que está escrito
# no PRD, sem reescrever e sem fazer contas: cada bloco cita a seção de origem. Números aparecem como estão no PRD;
# as barras só usam o valor lido para a proporção.
import html
import os
import re

# Seções que não contam como falta quando vazias, por porte ("–" não cobrar e "○" recomendada, em prd-etapas §2)
RS_NAO_COBRA = {"P": {"01.4": "não cobrada no P", "03.2": "não cobrada no P", "04.3": "não cobrada no P"},
                "M": {"03.2": "recomendada no M", "04.3": "recomendada no M"},
                "G": {}}
RS_CONDICIONAL = {"02.3": "só se o produto calcula ou mostra indicador"}
RS_GATE_ETAPAS = {"1": ("01", "02", "03", "A1"), "2": ("04", "05", "A2")}
RS_DONO_ANEXO = {"A": "PM", "C": "Engenharia de dados, com o negócio", "D": "Especialistas",
                 "E": "Ciência de dados, com o sponsor"}

RS_CSS = r"""/* VOICE: documento de trabalho, direto, como a página de gráficos de um bom jornal.
   IDEA: a folha que cada público leva para a reunião do PRD: o sponsor, o time técnico e o revisor do gate.
   PICTURE: no topo, a trilha das 5 etapas e dos 2 gates; em cada aba, o quadro principal primeiro.
   COLOUR and TYPE: azul-ardósia do template como campo dominante, petróleo de apoio, laranja-queimado só para o que
   falta; fonte do sistema.
   LAYOUT: faixa do topo de ponta a ponta; blocos em grade de duas colunas que viram uma no celular. */
:root{color-scheme:light dark;
 --bg:light-dark(#ffffff,#10171d);--ink:light-dark(#17262f,#e6edf1);--mut:light-dark(#5a6973,#98a8b2);
 --tinta:#1F3A4D;--pet:light-dark(#22717F,#4fb9c9);--acc:light-dark(#B4501E,#ff9a62);
 --line:light-dark(#dbe3e8,#26343d);--soft:light-dark(#f2f6f8,#17232b);--petsoft:light-dark(#e2f1f3,#123038);
 --accsoft:light-dark(#fbece3,#3a2418)}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Segoe UI",system-ui,-apple-system,Arial,sans-serif}
h1,h2,h3,h4{margin:0;line-height:1.2;text-wrap:balance}p{margin:0 0 .5em}
small{font-size:13px;color:var(--mut)}
.topo{background:var(--tinta);color:#fff}
.topo .in{max-width:1200px;margin:0 auto;padding:clamp(22px,4vw,40px) max(4vw,16px) 16px}
.marca{font-size:13px;opacity:.75;margin:0 0 6px}
h1{font-size:clamp(30px,5vw,44px);font-weight:700}
.meta{font-size:14px;opacity:.85;margin-top:8px}
.trilha{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 0;padding:0}
.trilha li{flex:1 1 120px;padding:9px 11px;border-top:4px solid rgba(255,255,255,.25);background:rgba(255,255,255,.06)}
.trilha li b{display:block;font-size:14px}.trilha li span{font-size:13px;opacity:.85}
.trilha .feito{border-color:#5fd0de}.trilha .atual{border-color:#ffb38a;background:rgba(255,179,138,.12)}
.trilha .gate{flex-basis:150px}
.abas{max-width:1200px;margin:0 auto;padding:0 max(4vw,16px);display:flex;gap:4px;flex-wrap:wrap}
.abas button{font:inherit;color:#fff;background:none;border:0;cursor:pointer;padding:12px 18px;min-height:44px;
 border-radius:8px 8px 0 0;font-weight:600;opacity:.8}
.abas button[aria-selected=true]{background:var(--bg);color:var(--ink);opacity:1}
.abas button:focus-visible{outline:3px solid #5fd0de;outline-offset:-3px}
main{max-width:1200px;margin:0 auto;padding:22px max(4vw,16px) 8px}
.js section[role=tabpanel][hidden]{display:none}
section[role=tabpanel]>h2{font-size:15px;color:var(--mut);font-weight:600;margin:0 0 14px}
.grade{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-bottom:18px}.grade>.bloco{margin:0}
.bloco{border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:18px}
.bloco.abre{border-color:transparent;background:var(--soft)}
.bloco>header{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin-bottom:12px}
.bloco>header h3{font-size:20px;flex:1 1 auto}
.secs{display:inline-flex;flex-wrap:wrap;gap:4px}
.sec{font-size:12px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:1px 8px;white-space:nowrap}
.frase{font-size:20px;line-height:1.4;font-weight:600}
.kv{display:grid;grid-template-columns:minmax(0,12em) minmax(0,1fr);gap:6px 14px;margin:0}
.kv dt{color:var(--mut);font-size:14px}.kv dd{margin:0;white-space:pre-line}
.vazio{color:var(--mut);font-style:italic}
.validar{display:inline-block;font-size:12px;font-weight:600;color:var(--acc);background:var(--accsoft);
 border-radius:999px;padding:0 8px;margin-left:4px;font-style:normal}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}
.kpis div{background:var(--bg);border-radius:8px;padding:12px}.kpis strong{display:block;font-size:22px;line-height:1.2}
.legenda{font-size:13px;color:var(--mut);margin:6px 0}.legenda i{display:inline-block;width:12px;height:12px;border-radius:2px;
 margin:0 4px 0 10px;vertical-align:-1px}
i.b{background:var(--pet)}i.c{background:var(--tinta);opacity:.55}
.ano{display:grid;grid-template-columns:3.8em minmax(0,1fr) 10em;gap:10px;align-items:center;padding:5px 0}
.ano i{display:block;height:13px;border-radius:0 3px 3px 0;margin:2px 0}
.num{text-align:right;font-variant-numeric:tabular-nums;font-size:13px;line-height:1.3}
.releases{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.releases>div{background:var(--soft);border-radius:8px;padding:12px 14px}
.releases h4{font-size:16px;margin-bottom:4px}.releases ul{list-style:none;margin:10px 0 0;padding:0}
.releases li{padding:8px 0;border-top:1px solid var(--line);font-size:15px}
.aceite{display:block;font-size:13px;color:var(--mut);margin-top:3px}.aceite.falta{color:var(--acc);font-weight:600}
.pri{display:inline-block;font-size:12px;font-weight:600;border-radius:4px;padding:0 6px;margin-right:6px;background:var(--line)}
.pri.must{background:var(--pet);color:#fff}.pri.should{background:var(--petsoft);color:var(--pet)}
.lista{list-style:none;margin:0;padding:0}.lista li{padding:8px 0;border-top:1px solid var(--line)}
.lista li:first-child{border-top:0}.lista b,.lista small{display:block}
.pede{border-color:var(--acc);border-width:2px}
.canvas{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.canvas>div{border-radius:8px;padding:12px 14px;background:var(--soft);border-left:4px solid var(--pet)}
.canvas .na{border-color:var(--line);opacity:.8}.canvas .parcial{border-color:var(--acc)}
.canvas b,.canvas small{display:block}.canvas .conta{font-size:13px;font-weight:600;color:var(--pet);margin:4px 0}
.canvas .parcial .conta{color:var(--acc)}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-size:13px;color:var(--mut);font-weight:600;border-bottom:2px solid var(--line);padding:6px 8px}
td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top;white-space:pre-line}
td.curto{white-space:nowrap}
.scroll{overflow-x:auto}
.etapas{display:grid;gap:14px}
.etapa{display:grid;grid-template-columns:minmax(0,12em) minmax(0,1fr);gap:8px 16px;padding-top:12px;border-top:1px solid var(--line)}
.etapa:first-child{border-top:0;padding-top:0}.etapa .conta{display:block;font-size:13px;font-weight:600;color:var(--pet)}
.etapa .conta.falta{color:var(--acc)}
.tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px}
.tiles li{padding:8px 10px;border-radius:8px;border:2px solid var(--line);font-size:14px}
.tiles li b{color:var(--mut);margin-right:6px;font-size:13px}.tiles li small{display:block;line-height:1.35;margin-top:2px}
.tiles .ok{border-color:var(--petsoft)}.tiles .ok small{color:var(--pet)}
.tiles .falta{border-color:var(--acc);background:var(--accsoft)}.tiles .falta small{color:var(--acc)}
.tiles .nc{border-style:dashed;opacity:.75}
.gates{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.gates>div{border-radius:8px;padding:12px 14px;background:var(--soft)}.gates strong{display:block;font-size:20px}
.gates .aberto strong{color:var(--acc)}.gates ol{margin:8px 0 0;padding-left:1.2em;font-size:14px;color:var(--mut)}
.aviso{border-left:4px solid var(--acc);background:var(--accsoft);padding:10px 14px;border-radius:0 8px 8px 0;margin-bottom:10px}
.ok-txt{color:var(--pet);font-weight:600}
.log{list-style:none;margin:0;padding:0}.log li{display:grid;grid-template-columns:4em 6.5em minmax(0,1fr);gap:8px;
 padding:6px 0;border-top:1px solid var(--line);font-size:14px}.log li:first-child{border-top:0}
footer{max-width:1200px;margin:0 auto;padding:10px max(4vw,16px) 30px;font-size:13px;color:var(--mut)}
@media (max-width:760px){.grade,.gates{grid-template-columns:1fr}.kv,.etapa{grid-template-columns:1fr}
 .bloco{padding:14px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.kpis strong{font-size:19px}table{font-size:13px}td,th{padding:6px 5px}
 .ano{grid-template-columns:3.2em minmax(0,1fr) 6.2em}}
@media print{.abas{display:none}section[role=tabpanel][hidden]{display:block!important}.topo{background:#fff;color:#000}}
"""

RS_JS = r"""document.documentElement.classList.add('js');
const abas=[...document.querySelectorAll('.abas button')];
function abrir(b){abas.forEach(x=>{const s=x===b;x.setAttribute('aria-selected',s);x.tabIndex=s?0:-1;
 document.getElementById(x.getAttribute('aria-controls')).hidden=!s});}
abas.forEach((b,i)=>{b.addEventListener('click',()=>abrir(b));
 b.addEventListener('keydown',e=>{const d={ArrowRight:1,ArrowLeft:-1}[e.key];if(d){const n=abas[(i+d+abas.length)%abas.length];
 abrir(n);n.focus();}});});
abrir(abas[0]);"""


def rs_e(t):
    """Escapa o texto e mostra "[validar: …]" como etiqueta."""
    t = html.escape(str(t or "").strip())
    return re.sub(r"\[validar:\s*([^\]]+)\]", r'<span class="validar">validar: \1</span>', t)


def rs_reais(t):
    """Valor em reais de um texto do PRD ("R$ 900 mil", "−R$ 208 mil", "R$ 3,6 milhões"), só para a proporção das
    barras. None se não houver valor."""
    m = re.search(r"([−-])?\s*R\$\s*([\d.]+(?:,\d+)?)\s*(mil|milh[õo]es|milh[ãa]o|mi|bi)?", str(t or ""))
    if not m:
        return None
    v = float(m.group(2).replace(".", "").replace(",", "."))
    suf = (m.group(3) or "").lower()
    v *= 1e3 if suf == "mil" else 1e6 if suf.startswith("mi") else 1e9 if suf == "bi" else 1
    return -v if m.group(1) else v


def rs_secs(*ids):
    return '<span class="secs">' + "".join(f'<span class="sec">{html.escape(i)}</span>' for i in ids if i) + "</span>"


def rs_bloco(titulo, corpo, secs=(), classe=""):
    return (f'<article class="bloco {classe}"><header><h3>{rs_e(titulo)}</h3>{rs_secs(*secs)}</header>'
            f"{corpo}</article>")


def rs_vazio(sid):
    return f'<p class="vazio">Ainda não preenchido no PRD ({html.escape(sid)}).</p>'


def rs_kv(pares):
    itens = [(k, v) for k, v in pares if v]
    if not itens:
        return ""
    return "<dl class=kv>" + "".join(f"<dt>{rs_e(k)}</dt><dd>{rs_e(v)}</dd>" for k, v in itens) + "</dl>"


def rs_tabela(linhas, colunas=None):
    if not linhas:
        return ""
    colunas = colunas or list(linhas[0])
    colunas = [c for c in colunas if any(l.get(c) for l in linhas)]
    cab = "".join(f"<th>{rs_e(c)}</th>" for c in colunas)
    def td(l, i, col):
        v = l.get(col, "")
        return f'<td class="curto">{rs_e(v)}</td>' if i == 0 and len(str(v)) <= 8 else f"<td>{rs_e(v)}</td>"

    corpo = "".join("<tr>" + "".join(td(l, i, col) for i, col in enumerate(colunas)) + "</tr>" for l in linhas)
    return f'<div class="scroll"><table><thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table></div>'


def rs_contexto(d):
    """Tudo o que as abas usam, lido uma vez."""
    S = d["secoes"]

    def campo(sid, rot):
        alvo = S.get(sid) or d["anexos"].get(sid) or {}
        for r, v in alvo.get("campos", {}).items():
            if _n(r) == _n(rot):
                return v
        return ""

    def linhas(sid, nome):
        alvo = S.get(sid) or d["anexos"].get(sid) or {}
        return [l for l in alvo.get("tabelas", {}).get(nome, []) if any(l.values())]

    porte = (d["painel"].get("Porte") or "").strip()[:1].upper()
    sponsor = (d["pessoas"].get("Sponsor") or {}).get("Nome", "")
    return {"d": d, "S": S, "campo": campo, "linhas": linhas, "porte": porte if porte in RS_NAO_COBRA else "",
            "sponsor": sponsor, "produto": d["painel"].get("Produto") or "PRD"}


def rs_gate_alvo(d):
    if d["assinado"]:
        return None
    if not (d["gates"].get("1") or {}).get("Decisão"):
        return "1"
    if not (d["gates"].get("2") or {}).get("Decisão"):
        return "2"
    return None


def rs_ia(c):
    tipo = c["campo"]("03.1", "Tipo de produto")
    return (_n(c["campo"]("04.4", "Há IA na solução?")) == "sim" or any(t in tipo for t in ("Modelo", "Agente"))
            or not c["d"]["anexos"].get("E", {}).get("vazia", True))


def rs_completude(c):
    """Por etapa: (sid, título, dono, situação) com situação ok, falta, nc (não cobrada ou condicional)."""
    nao = RS_NAO_COBRA.get(c["porte"], {})
    out = {}
    for num, _, _ in ETAPAS:
        itens = []
        for s in (x for x in SECOES if x["etapa"] == num):
            vazia = c["S"].get(s["id"], {}).get("vazia", True)
            if not vazia:
                sit, nota = "ok", "com conteúdo"
            elif s["id"] in nao:
                sit, nota = "nc", nao[s["id"]]
            elif s["id"] in RS_CONDICIONAL:
                sit, nota = "nc", RS_CONDICIONAL[s["id"]]
            else:
                sit, nota = "falta", f"vazia · {s['dono']}"
            itens.append((s["id"], s["titulo"], s["dono"], sit, nota))
        out[num] = itens
    for chave, ids in (("A1", ["A"]), ("A2", ["C", "D"] + (["E"] if rs_ia(c) else []))):
        itens = []
        for a in (x for x in ANEXOS if x["id"] in ids):
            vazia = c["d"]["anexos"].get(a["id"], {}).get("vazia", True)
            dono = RS_DONO_ANEXO[a["id"]]
            itens.append((f"Anexo {a['id']}", a["titulo"], dono, "falta" if vazia else "ok",
                          f"vazio · {dono}" if vazia else "com conteúdo"))
        out[chave] = itens
    return out


def rs_divergencias(c):
    """Checagens que dá para fazer sem julgar o texto: o escopo da R1 e os dados no Anexo C."""
    out = []
    rfs = c["linhas"]("02.1", "rfs")
    r1_rfs = {l["ID"].strip() for l in rfs if l.get("ID") and _n(l.get("Release")) == "r1"}
    r1 = next((l for l in c["linhas"]("02.2", "releases") if _n(l.get("Release")) == "r1"), None)
    if r1 and r1_rfs:
        mapa = set(re.findall(r"RF-\d+", r1.get("RFs incluídos", "")))
        so_rf, so_mapa = sorted(r1_rfs - mapa), sorted(mapa - r1_rfs)
        if so_rf:
            out.append(f"{', '.join(so_rf)} com release R1 na 02.1, mas fora da R1 no mapa de releases (02.2)")
        if so_mapa:
            out.append(f"{', '.join(so_mapa)} na R1 do mapa de releases (02.2), mas sem release R1 na 02.1")
    for l in rfs:
        if _n(l.get("Prioridade")) == "must" and l.get("Release") and _n(l["Release"]) != "r1":
            out.append(f"{l.get('ID')} é Must, mas está na {l['Release']} (02.1)")
    dados = {l["ID"].strip() for l in c["linhas"]("02.5", "dados") if l.get("ID")}
    origem = {l["ID"].strip() for l in c["linhas"]("C", "origem") if l.get("ID")}
    if origem and dados - origem:
        out.append(f"{', '.join(sorted(dados - origem))} na 02.5, mas sem origem no Anexo C")
    return out


# ---------------------------------------------------------------- topo

def rs_topo(c, gate):
    d = c["d"]
    p = d["painel"]
    meta = " · ".join(x for x in (p.get("Tipo"), f"Porte {p['Porte']}" if p.get("Porte") else "",
                                  f"Versão {p['Versão vigente']}" if p.get("Versão vigente") else "",
                                  f"Assinada: {p['Versão assinada']}" if p.get("Versão assinada") else "",
                                  f"Horizonte {p['Horizonte do business case']}" if p.get(
                                      "Horizonte do business case") else "") if x)
    atual = (p.get("Etapa atual") or "").strip()[:2]
    trilha = []
    for num, titulo, _ in ETAPAS:
        ck = d["checkpoints"].get(num) or {}
        cl = "feito" if ck.get("situacao") else "atual" if num == atual else ""
        estado = (f"{ck['situacao']}{' · ' + ck['data'] if ck.get('data') else ''}" if ck.get("situacao")
                  else "em andamento" if num == atual else "")
        trilha.append(f'<li class="{cl}"><b>{num} · {rs_e(titulo)}</b><span>{rs_e(estado)}</span></li>')
        if num in ("03", "05"):
            g = "1" if num == "03" else "2"
            dec = d["gates"].get(g) or {}
            nome = GATES[g][0]
            cl = "feito" if dec.get("Decisão") else "atual" if gate == g else ""
            estado = f"{dec['Decisão']}{' · ' + dec['Data'] if dec.get('Data') else ''}" if dec.get("Decisão") \
                else "próximo" if gate == g else ""
            trilha.append(f'<li class="gate {cl}"><b>{rs_e(nome)}</b><span>{rs_e(estado)}</span></li>')
    return (f'<header class="topo"><div class="in"><p class="marca">PRD · Product Requirements Document</p>'
            f"<h1>{rs_e(c['produto'])}</h1><p class=meta>{rs_e(meta)}</p>"
            f'<ol class="trilha">{"".join(trilha)}</ol></div>'
            '<nav class="abas" role="tablist" aria-label="Públicos">'
            '<button role="tab" id="t-sponsor" aria-controls="p-sponsor">Sponsor</button>'
            '<button role="tab" id="t-tecnico" aria-controls="p-tecnico">Time técnico</button>'
            '<button role="tab" id="t-revisor" aria-controls="p-revisor">Revisor</button></nav></header>')


# ---------------------------------------------------------------- aba Sponsor

def rs_valor(c):
    d = c["d"]
    bc = d["painel_bc"]
    tiles = "".join(f"<div><small>{rs_e(k)}</small><strong>{rs_e(v)}</strong></div>" for k, v in bc.items() if v)
    corpo = f'<div class="kpis">{tiles}</div>' if tiles else ""
    linhas_bc = c["linhas"]("04.6", "bc")
    anos = [k for k in (linhas_bc[0] if linhas_bc else {}) if k.startswith("Ano")]
    ben = next((l for l in linhas_bc if _n(l.get("Linha")).startswith("beneficio")), None)
    custos = [l for l in linhas_bc if _n(l.get("Linha")).startswith(("build", "run"))]
    if ben and anos:
        vals = []
        for a in anos:
            b = rs_reais(ben.get(a)) or 0
            cu = sum((rs_reais(l.get(a)) or 0) for l in custos)
            vals.append((a, b, cu, ben.get(a, ""), " + ".join(l.get(a, "") for l in custos if l.get(a))))
        topo_ = max([max(b, cu) for _, b, cu, _, _ in vals] + [1])
        barras = "".join(
            f'<div class="ano"><span>{rs_e(a)}</span><span><i class=b style="width:{b / topo_ * 100:.1f}%"></i>'
            f'<i class=c style="width:{cu / topo_ * 100:.1f}%"></i></span>'
            f'<span class=num>{rs_e(tb) or "—"}<br><small>{rs_e(tc) or "—"}</small></span></div>'
            for a, b, cu, tb, tc in vals)
        corpo += (f'<p class=legenda><i class=b></i>Benefício<i class=c></i>Build + run</p>{barras}')
    elif c["linhas"]("03.3", "valores"):
        corpo += rs_tabela(c["linhas"]("03.3", "valores"))
    kpis = c["linhas"]("03.3", "kpis")
    if kpis:
        corpo += "<h4 style='margin:16px 0 6px'>Como o benefício é medido</h4>" + rs_tabela(
            kpis, ["KPI", "Baseline", "Meta e prazo", "Método e responsável", "Release"])
    corpo += rs_kv([("Premissas", c["campo"]("03.3", "Premissas do benefício")),
                    ("Sensibilidade", c["campo"]("04.6", "Sensibilidade (benefício 30% menor)"))])
    return rs_bloco("Quanto vale", corpo or rs_vazio("03.3 e 04.6"), ("03.3", "04.5", "04.6"))


def rs_releases(c):
    rfs = c["linhas"]("02.1", "rfs")
    rels = c["linhas"]("02.2", "releases")
    nomes = [r.get("Release", "") for r in rels] or sorted({r.get("Release", "") for r in rfs if r.get("Release")})
    if not nomes and not rfs:
        return rs_bloco("O que entra em cada release", rs_vazio("02.1 e 02.2"), ("02.1", "02.2"))
    colunas = []
    for nome in nomes:
        r = next((x for x in rels if x.get("Release") == nome), {})
        itens = []
        for rf in (x for x in rfs if _n(x.get("Release")) == _n(nome)):
            pri = rf.get("Prioridade", "")
            crit = rf.get("Critério de aceite", "")
            aceite = (f'<span class="aceite">{rs_e(crit)}</span>' if crit else
                      '<span class="aceite falta">sem critério de aceite</span>' if _n(nome) == "r1" else "")
            itens.append(f'<li><span class="pri {_n(pri)}">{rs_e(pri) or "—"}</span><b>{rs_e(rf.get("ID"))}</b> '
                         f'{rs_e(rf.get("A solução deverá"))}{aceite}</li>')
        meta = " · ".join(x for x in (r.get("Data-alvo"), r.get("Critério de saída") and "saída: " + r["Critério de saída"]) if x)
        colunas.append(f'<div><h4>{rs_e(nome)}</h4><p>{rs_e(r.get("Objetivo"))}</p><small>{rs_e(meta)}</small>'
                       f'<ul>{"".join(itens)}</ul></div>')
    sem = [x for x in rfs if not x.get("Release")]
    corpo = f'<div class="releases">{"".join(colunas)}</div>'
    if sem:
        corpo += f'<p class="aviso">Sem release: {rs_e(", ".join(x.get("ID", "") for x in sem))} (02.1)</p>'
    fora = c["linhas"]("02.6", "fora")
    if fora:
        corpo += "<h4 style='margin:16px 0 6px'>Fora do escopo</h4><ul class=lista>" + "".join(
            f"<li><b>{rs_e(f.get('Item'))}</b><small>{rs_e(f.get('Motivo'))}"
            f"{' · reavaliar: ' + rs_e(f['Reavaliar quando']) if f.get('Reavaliar quando') else ''}</small></li>"
            for f in fora) + "</ul>"
    return rs_bloco("O que entra em cada release", corpo, ("02.1", "02.2", "02.6"))


def rs_golive(c):
    sid = "05.1" if not c["S"].get("05.1", {}).get("vazia", True) else "03.4"
    campos = ["Forma de lançamento", "O que a solução substitui", "Convivência com a solução atual",
              "Critério para desligar a solução atual", "Time do negócio na transição", "Dono da mudança"]
    corpo = rs_kv([(k, c["campo"](sid, k)) for k in campos])
    fases = [f for f in c["linhas"]("05.3", "fases") if _n(f.get("O que acontece")) != "n/a"]
    if fases:
        corpo += "<h4 style='margin:16px 0 6px'>Fases</h4><ul class=lista>" + "".join(
            f"<li><b>{rs_e(f.get('Fase'))} · {rs_e(f.get('Início e fim'))}</b>"
            f"<small>{rs_e(f.get('O que acontece'))}{' · saída: ' + rs_e(f['Critério de saída']) if f.get('Critério de saída') else ''}</small></li>"
            for f in fases) + "</ul>"
    corpo += rs_kv([("Gatilhos de rollback", c["campo"]("05.5", "Gatilhos de rollback")),
                    ("Solução atual disponível até", c["campo"]("05.5", "Solução atual disponível até"))])
    return rs_bloco("Como entra em produção", corpo or rs_vazio("03.4 e 05.1"), (sid, "05.3", "05.5"))


def rs_pede(c, comp):
    """O que o PRD pede do sponsor: pendências dele, seções vazias que ele preenche e o gate."""
    nome = c["sponsor"]
    itens = []
    for p in c["linhas"]("A", "pendencias"):
        if nome and _n(nome) in _n(p.get("Dono")):
            itens.append((p.get("Descrição", ""), f"{p.get('ID', '')} · {p.get('Tipo', '')}"
                          f"{' · prazo ' + p['Prazo'] if p.get('Prazo') else ''}"
                          f"{' · bloqueia' if _n(p.get('Bloqueante')) == 'sim' else ''}", p.get("Origem", "")))
    for itens_etapa in comp.values():
        for sid, tit, dono, sit, _ in itens_etapa:
            if sit == "falta" and "sponsor" in _n(dono):
                itens.append((f"Preencher {tit}", dono, sid))
    if not itens:
        return ""
    lis = "".join(f"<li><b>{rs_e(a)}</b><small>{rs_e(b)}{' · ' + rs_e(s) if s else ''}</small></li>"
                  for a, b, s in itens[:8])
    titulo = f"O que o PRD pede de {nome}" if nome else "O que o PRD pede do sponsor"
    return rs_bloco(titulo, f"<ul class=lista>{lis}</ul>", ("Anexo A",), "pede")


def rs_aba_sponsor(c, comp):
    prob = c["campo"]("01.1", "Problema ou oportunidade")
    corpo = (f'<p class="frase">{rs_e(prob)}</p>' if prob else rs_vazio("01.1")) + rs_kv(
        [("Por que agora", c["campo"]("01.1", "Por que agora")), ("Quem sente a dor", c["campo"]("01.1", "Quem sente a dor"))])
    dor = c["linhas"]("01.3", "dimensoes")
    if dor:
        corpo += "<h4 style='margin:14px 0 6px'>Tamanho da dor hoje</h4>" + rs_tabela(
            dor, ["Dimensão", "Indicador atual", "Ordem de grandeza", "Fonte"])
    sol = rs_kv([("O que a solução faz", c["campo"]("03.1", "O que a solução faz")),
                 ("Decisão apoiada", c["campo"]("03.1", "Decisão ou processo apoiado")),
                 ("Onde é consumida", c["campo"]("03.1", "Onde e como é consumida"))])
    return ("<h2>Para o sponsor: a dor, o valor, o escopo e o que se espera de você</h2>"
            f'<div class="grade">{rs_bloco("O problema", corpo, ("01.1", "01.3"), "abre")}'
            f'{rs_bloco("A solução", sol or rs_vazio("03.1"), ("03.1",), "abre")}</div>'
            f"{rs_valor(c)}{rs_releases(c)}<div class=grade>{rs_golive(c)}{rs_pede(c, comp) or ''}</div>")


# ---------------------------------------------------------------- aba Time técnico

def rs_aba_tecnico(c):
    d = c["d"]
    corpo = rs_kv([("Desenho", c["campo"]("04.1", "Desenho")), ("Aderência ao padrão", c["campo"]("04.1", "Aderência ao padrão"))])
    corpo += rs_tabela(c["linhas"]("04.1", "componentes"))
    arq = rs_bloco("Arquitetura", corpo or rs_vazio("04.1"), ("04.1",), "abre")
    dt = c["linhas"]("04.3", "decisoes")
    dec = rs_bloco("Decisões de arquitetura", rs_tabela(dt) or rs_vazio("04.3"), ("04.3",))

    origem = {l.get("ID", "").strip(): l for l in c["linhas"]("C", "origem")}
    dados = []
    for l in c["linhas"]("02.5", "dados"):
        o = origem.get(l.get("ID", "").strip(), {})
        dados.append({"ID": l.get("ID"), "Informação": l.get("Informação"), "Para qual RF": l.get("Para qual RF"),
                      "Frequência": l.get("Frequência"), "Onde existe hoje": o.get("Onde existe hoje", ""),
                      "Acesso": o.get("Forma de acesso", ""), "Classificação": o.get("Classificação", ""),
                      "Dados pessoais": o.get("Dados pessoais", ""), "Dono do dado": o.get("Dono do dado", "")})
    dados_b = rs_bloco("Do dado ao uso", rs_tabela(dados) or rs_vazio("02.5"), ("02.5", "Anexo C"))

    cards = []
    for chave, (nome, quando, blocos) in CANVAS.items():
        cv = d["canvas"].get(chave) or {}
        titulos = [b for b, _ in blocos]
        cheios = [b for b in titulos if (cv.get("blocos") or {}).get(b)]
        if _n(cv.get("aplicavel")) == "nao":
            cards.append(f'<div class="na"><b>{rs_e(nome)}</b><span class=conta>Não se aplica</span>'
                         f'<small>{rs_e(cv.get("motivo")) or "sem motivo registrado"}</small></div>')
            continue
        cl = "" if len(cheios) == len(titulos) else "parcial"
        esforco = (cv.get("blocos") or {}).get(titulos[-1], "")
        cards.append(f'<div class="{cl}"><b>{rs_e(nome)}</b><span class=conta>{len(cheios)} de {len(titulos)} blocos'
                     f'</span><small>{rs_e(esforco) if esforco else rs_e(quando)}</small></div>')
    canvas = rs_bloco("Canvas por especialidade", f'<div class="canvas">{"".join(cards)}</div>', ("04.2",))

    nfr = rs_bloco("Requisitos não funcionais", rs_tabela(c["linhas"]("02.4", "nfr")) or rs_vazio("02.4"), ("02.4",))
    ia = ""
    if rs_ia(c):
        campos = ["Tipo de IA", "Tarefa ou decisão apoiada", "Métrica técnica", "Limiar para ir à produção",
                  "Comparação com o jeito atual", "Conjunto de avaliação e quem valida", "Revisão humana",
                  "Limites e o que fazer quando falha", "Monitoramento e gatilho de revisão", "Custo por uso"]
        corpo = rs_kv([(k, c["campo"]("E", k)) for k in campos])
        if not c["campo"]("E", "Limiar para ir à produção"):
            corpo = '<p class="aviso">Há IA na solução e o limiar para ir à produção ainda não está no Anexo E.</p>' + corpo
        ia = rs_bloco("Requisitos de IA", corpo, ("04.4", "Anexo E"))
    custos = rs_bloco("Custos", rs_tabela(c["linhas"]("04.5", "custos")) or rs_vazio("04.5"), ("04.5", "Anexo D"))
    cut = rs_kv([(k, c["campo"]("05.5", k)) for k in ("Cutover (sequência, janela e dono)", "Contingência",
                                                       "Gatilhos de rollback", "Como voltar", "Tempo máximo para voltar",
                                                       "Quem decide e como comunica", "Solução atual disponível até")])
    cutb = rs_bloco("Cutover, contingência e rollback", cut or rs_vazio("05.5"), ("05.5",))
    return ("<h2>Para o time técnico: arquitetura, dados, canvas, custos e a virada</h2>"
            f"<div class=grade>{arq}{dec}</div>{dados_b}{canvas}<div class=grade>{nfr}{ia or cutb}</div>"
            f"{custos}{cutb if ia else ''}")


# ---------------------------------------------------------------- aba Revisor

def rs_aba_revisor(c, comp, gate, divergencias):
    d = c["d"]
    etapas = []
    linhas_ = [(num, f"{num} · {titulo}") for num, titulo, _ in ETAPAS]
    linhas_.insert(3, ("A1", "Anexo do Gate 1"))
    linhas_.append(("A2", "Anexos do Gate 2"))
    for num, titulo in linhas_:
        itens = comp[num]
        cheias = sum(1 for x in itens if x[3] == "ok")
        cobradas = sum(1 for x in itens if x[3] != "nc")
        faltam = sum(1 for x in itens if x[3] == "falta")
        tiles = "".join(f'<li class="{sit}"><b>{rs_e(sid)}</b>{rs_e(tit)}<small>{rs_e(nota)}</small></li>'
                        for sid, tit, _, sit, nota in itens)
        etapas.append(f'<div class="etapa"><div><b>{rs_e(titulo)}</b>'
                      f'<span class="conta{" falta" if faltam else ""}">{cheias} de {cobradas} com conteúdo</span></div>'
                      f'<ul class="tiles">{tiles}</ul></div>')
    nota = ("Completude, não qualidade: o \"bom quando\" de cada seção é conferido no checkpoint e no gate."
            + ("" if c["porte"] else " Sem porte no painel: todas as seções contam."))
    comp_b = rs_bloco("O que está preenchido", f'<p class=legenda>{rs_e(nota)}</p><div class="etapas">{"".join(etapas)}</div>',
                      ("01 a 05",))
    gates = []
    for g in ("1", "2"):
        nome, checklist = GATES[g]
        dec = d["gates"].get(g) or {}
        info = (d.get("gate") or {}).get(g, {}).get("decisao", {}) or dec
        estado = dec.get("Decisão") or ("próximo gate" if gate == g else "ainda não")
        extra = " · ".join(x for x in (info.get("Condições") and "condições: " + info["Condições"],
                                       dec.get("Quem decidiu"), dec.get("Data")) if x)
        gates.append(f'<div class="{"" if dec.get("Decisão") else "aberto"}"><small>{rs_e(nome)}</small>'
                     f'<strong>{rs_e(estado)}</strong><small>{rs_e(extra)}</small>'
                     f'<ol>{"".join(f"<li>{rs_e(x)}</li>" for x in checklist)}</ol></div>')
    gates_b = rs_bloco("Gates", f'<div class="gates">{"".join(gates)}</div>'
                       '<p class=legenda>A decisão é do sponsor e do revisor, marcada por eles no documento.</p>', ("Gates",))
    if divergencias:
        cons = "".join(f'<p class="aviso">{rs_e(x)}</p>' for x in divergencias)
    else:
        cons = '<p class="ok-txt">Escopo da R1 e dados batem entre 02.1, 02.2, 02.5 e Anexo C.</p>'
    cons_b = rs_bloco("Consistência", cons + '<p class=legenda>Só o que dá para conferir sem julgar o texto. '
                      'As demais checagens são feitas na revisão do gate.</p>', ("02.1", "02.2", "02.5", "Anexo C"))
    pend = sorted(c["linhas"]("A", "pendencias"), key=lambda p: _n(p.get("Bloqueante")) != "sim")
    pend_b = rs_bloco("Riscos e pendências", rs_tabela(pend) or '<p class="vazio">Nenhuma no Anexo A.</p>', ("Anexo A",))
    versoes = c["linhas"]("B", "versoes")
    log = "".join(f"<li><b>{rs_e(v.get('Versão'))}</b><span>{rs_e(v.get('Data'))}</span>"
                  f"<span>{rs_e(v.get('O que mudou'))}{' · ' + rs_e(v['Autor']) if v.get('Autor') else ''}</span></li>"
                  for v in reversed(versoes))
    mud = c["linhas"]("B", "mudancas")
    hist = (f'<ul class="log">{log}</ul>' if log else '<p class="vazio">Sem versões registradas.</p>')
    if mud:
        hist += "<h4 style='margin:14px 0 6px'>Pedidos de mudança</h4>" + rs_tabela(mud)
    hist_b = rs_bloco("Versões e mudanças", hist, ("Anexo B",))
    return ("<h2>Para o revisor: o que está preenchido, os gates, as pendências e o histórico</h2>"
            f"{comp_b}{gates_b}<div class=grade>{cons_b}{hist_b}</div>{pend_b}")


# ---------------------------------------------------------------- geração

def gerar_resumo(arquivo, saida):
    """Gera o resumo de `arquivo` (.docx do PRD) em `saida` (arquivo .html ou pasta) e devolve um relatório (dict)."""
    d = ler_prd(arquivo)
    c = rs_contexto(d)
    gate = rs_gate_alvo(d)
    comp = rs_completude(c)
    div = rs_divergencias(c)
    versao = d["painel"].get("Versão vigente") or ""
    nome = f"Resumo PRD {c['produto']}{' v' + versao if versao else ''}.html"
    destino = os.path.join(saida, nome) if os.path.isdir(saida) else saida
    titulo = html.escape(f"Resumo · PRD {c['produto']}{' v' + versao if versao else ''}")
    pagina = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
              f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titulo}</title>'
              f"<style>{RS_CSS}</style></head><body>{rs_topo(c, gate)}<main>"
              f'<section role="tabpanel" id="p-sponsor" aria-labelledby="t-sponsor">{rs_aba_sponsor(c, comp)}</section>'
              f'<section role="tabpanel" id="p-tecnico" aria-labelledby="t-tecnico">{rs_aba_tecnico(c)}</section>'
              f'<section role="tabpanel" id="p-revisor" aria-labelledby="t-revisor">'
              f"{rs_aba_revisor(c, comp, gate, div)}</section></main>"
              f"<footer>Gerado a partir de \"{html.escape(os.path.basename(arquivo))}\". O resumo mostra o que está "
              f"escrito no PRD; para mudar o que aparece aqui, mude o PRD e gere de novo.</footer>"
              f"<script>{RS_JS}</script></body></html>")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina)
    faltas = []
    total = completas = 0
    if gate:
        for num in RS_GATE_ETAPAS[gate]:
            for sid, tit, dono, sit, _ in comp[num]:
                if sit == "nc":
                    continue
                total += 1
                completas += sit == "ok"
                if sit == "falta":
                    faltas.append((sid, tit, dono))
    pend = c["linhas"]("A", "pendencias")
    return {"arquivo": os.path.basename(destino), "caminho": destino, "tamanho": os.path.getsize(destino),
            "abas": ["Sponsor", "Time técnico", "Revisor"], "gate": gate, "completas": completas, "total": total,
            "faltas": faltas, "divergencias": div, "assinado": d["assinado"],
            "versao_assinada": d["painel"].get("Versão assinada", ""), "porte": c["porte"],
            "pendencias": len(pend), "bloqueiam": sum(1 for p in pend if _n(p.get("Bloqueante")) == "sim")}
