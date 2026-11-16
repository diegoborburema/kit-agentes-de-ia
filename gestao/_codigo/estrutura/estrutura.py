# ---------------------------------------------------------------- estrutura do time: carga, lentes e regras (Coach de Estrutura)
# O mapa do time é uma lista de linhas pessoa × frente. As contas (carga, frentes sem dono, uma pessoa só, autonomia
# baixa sem apoio) e as recusas (rótulo, mudança formal, saúde, apoio sem prazo) saem daqui, não do modelo.
import copy
import re

ES_AUTONOMIA = ["baixa", "média", "alta"]
ES_NIVEIS = {1: "Dar um dono único", 2: "Ajustar o nível de delegação", 3: "Reduzir frentes (concluir, pausar ou passar adiante)",
             4: "Apoio com prazo", 5: "Nova atribuição para desenvolver", 6: "Trocar frentes entre pessoas do time",
             7: "Isolar alguém numa frente nova"}
ES_CAUSAS = ["capacidade", "autonomia", "clareza", "coordenação", "foco"]
ES_FORMAL = [r"\bcontrat", r"linha de reporte", r"passa\w* a reportar", r"\breportar (ao|a|para)\b", r"\bpromov", r"\bcargo\b",
             r"\bdemit", r"\bdeslig", r"\bfundir\b", r"\bdividir o time\b", r"\bnovo time\b", r"\btransferir para outra area\b"]
ES_ROTULOS = [r"\bfrac[oa]s?\b", r"\balto potencial\b", r"\bbaixo potencial\b", r"\bbaixo desempenho\b", r"\bpreguic",
              r"\bacomodad", r"\bdificil de lidar\b", r"\bincompetent", r"\bdespreparad", r"\bestrela\b", r"\bfora de serie\b"]


def _es_norm(texto):
    return fi_norm(texto)


def es_achar(padroes, texto):
    t = _es_norm(texto)
    return sorted({m.group(0) for p in padroes for m in [re.search(p, t)] if m})


def es_carga(mapa, restricoes=()):
    """Por pessoa: frentes, soma de %, disponibilidade (100 ou a restrição) e os sinais."""
    disp = {r["pessoa"]: r for r in restricoes}
    por = {}
    for l in mapa:
        p = por.setdefault(l["pessoa"], {"frentes": [], "soma": 0, "papel": l.get("papel", "")})
        p["frentes"].append(l["frente"])
        p["soma"] += float(l.get("pct") or 0)
    for pessoa, p in por.items():
        r = disp.get(pessoa)
        p["disponivel"] = float(r["disponivel_pct"]) if r else 100.0
        p["ate"] = r.get("ate") if r else None
        p["acima"] = p["soma"] > p["disponivel"]
        p["tres_ou_mais"] = len(p["frentes"]) >= 3
    return por


def es_lentes(mapa):
    """Cobertura, concentração e autonomia, a partir do mapa."""
    frentes = {}
    for l in mapa:
        frentes.setdefault(l["frente"], []).append(l)
    sem_dono = [f for f, ls in frentes.items() if not any(l.get("dono") for l in ls)]
    varios = [f for f, ls in frentes.items() if sum(1 for l in ls if l.get("dono")) > 1]
    uma_pessoa = {f: ls[0]["pessoa"] for f, ls in frentes.items() if len({l["pessoa"] for l in ls}) == 1}
    sem_apoio = [(l["pessoa"], l["frente"]) for l in mapa if l.get("dono") and l.get("autonomia") == "baixa"
                 and len({x["pessoa"] for x in frentes[l["frente"]]}) == 1]
    return {"sem_dono": sem_dono, "varios_donos": varios, "uma_pessoa": uma_pessoa, "autonomia_baixa_sem_apoio": sem_apoio}


def es_validar(e, erros):
    """Confere o que vai para o arquivo. Devolve a lista de avisos (o que foi tirado)."""
    avisos = []
    for i, l in enumerate(e.get("mapa", []), start=1):
        for c in ("pessoa", "frente"):
            if not l.get(c):
                erros.append(f"Mapa, linha {i}: falta {c}")
        if l.get("autonomia") and l["autonomia"] not in ES_AUTONOMIA:
            erros.append(f"Mapa, linha {i}: autonomia {l['autonomia']!r} (baixa, média ou alta)")
        try:
            float(l.get("pct") or 0)
        except (TypeError, ValueError):
            erros.append(f"Mapa, linha {i}: % {l.get('pct')!r} não é número")
    for r in e.get("restricoes", []):
        if set(r) - {"pessoa", "disponivel_pct", "ate", "fonte"}:
            erros.append(f"Restrição de {r.get('pessoa')}: só pessoa, disponivel_pct, ate e fonte (sem o motivo)")
    dec = e.get("decisao") or {}
    for t in dec.get("testes", []):
        for c in ("id", "movimento", "nivel", "criterio", "inicio", "revisao"):
            if not t.get(c):
                erros.append(f"Teste {t.get('id', '?')}: falta {c}")
        if t.get("nivel") and int(t["nivel"]) not in ES_NIVEIS:
            erros.append(f"Teste {t.get('id')}: nível {t['nivel']} (1 a 7)")
        if int(t.get("nivel") or 0) == 4:
            for c in ("ate", "escopo", "saida"):
                if not t.get(c):
                    erros.append(f"Teste {t.get('id')}: apoio sem {'prazo (ate)' if c == 'ate' else c}: apoio só com prazo, escopo e critério de saída")
    for d in e.get("diagnostico", []):
        if d.get("causa") not in ES_CAUSAS or (d.get("secundaria") and d["secundaria"] not in ES_CAUSAS):
            erros.append(f"Diagnóstico de {d.get('prioridade')}: causa ({', '.join(ES_CAUSAS)})")
        if not d.get("evidencia"):
            erros.append(f"Diagnóstico de {d.get('prioridade')}: sem evidência")
    if "interesses" in e:
        e.pop("interesses")
        avisos.append("Interesses de desenvolvimento não são gravados no arquivo (ficam na conversa ou "
                      "são ditados de novo): tirados do pedido")
    textos = []

    def junta(x):
        if isinstance(x, dict):
            for v in x.values():
                junta(v)
        elif isinstance(x, list):
            for v in x:
                junta(v)
        elif isinstance(x, str):
            textos.append(x)
    junta({k: v for k, v in e.items() if k != "historico"})
    tudo = " · ".join(textos)
    if fi_sensivel(tudo):
        erros.append(f"Termo de saúde ou de vida pessoal ({', '.join(fi_sensivel(tudo))}): restrição entra só como % e data, sem motivo")
    if es_achar(ES_ROTULOS, tudo):
        erros.append(f"Rótulo sobre pessoa ({', '.join(es_achar(ES_ROTULOS, tudo))}): use o fato observável na frente")
    formal = es_achar(ES_FORMAL, " · ".join([dec.get("texto", "")] + [t.get("movimento", "") for t in dec.get("testes", [])]))
    if formal:
        erros.append(f"Mudança formal na decisão ({', '.join(formal)}): fora do v1, passa pelo RH e pelo gestor; só sinalize")
    return avisos


def es_revisar(e, rev, erros):
    """Revisão do teste: o resultado de cada teste em aberto, com fonte. Devolve a estrutura nova e o log."""
    n = copy.deepcopy(e)
    log = []
    res = rev.get("resultados", {})
    for t in n.get("decisao", {}).get("testes", []):
        if t.get("resultado"):
            continue
        r = res.get(t["id"])
        if not r or "atingido" not in r or not r.get("fonte"):
            erros.append(f"Teste {t['id']} sem resultado (atingido true/false, evidência e fonte)")
            continue
        t["resultado"] = {"atingido": bool(r["atingido"]), "evidencia": r.get("evidencia", ""), "fonte": r["fonte"],
                          "data": rev["data"]}
        log.append(f"{t['id']} {'atingido' if r['atingido'] else 'NÃO atingido'}: {r.get('evidencia', '')} {r['fonte']}")
    n.setdefault("historico", []).append({"data": rev["data"], "registro": "Revisão do teste: " + "; ".join(log)})
    n["data"] = rev["data"]
    return n, log
