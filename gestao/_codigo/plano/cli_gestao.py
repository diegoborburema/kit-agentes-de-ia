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
