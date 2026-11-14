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
