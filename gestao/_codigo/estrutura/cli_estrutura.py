# ---------------------------------------------------------------- linha de comando do Coach de Estrutura
# O agente grava o pedido em /mnt/data/estrutura_pedido.json e roda este script. Ações: ler (plano do Coach de Gestão,
# análise anterior), carga (soma por pessoa e lentes) e gerar (o arquivo confidencial).
import json
import os
import sys

from pptx import Presentation


def _ec_base(argv):
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "estrutura_pedido.json")):
            return pasta, os.path.join(pasta, "estrutura_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _ec_arquivo(base, nome):
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _ec_txt_carga(mapa, restricoes):
    carga, lentes = es_carga(mapa, restricoes), es_lentes(mapa)
    linhas = ["CARGA (números do script: use estes)"]
    for p, c in carga.items():
        linhas.append(f"  {p}: {c['soma']:g}% em {len(c['frentes'])} frentes ({', '.join(c['frentes'])})"
                      + (f" · disponível {c['disponivel']:g}%" + (f" até {pl_dm(c['ate'])}" if c.get("ate") else "") if c["disponivel"] < 100 else "")
                      + (f" · ACIMA de {c['disponivel']:g}%" if c["acima"] else "") + (" · 3 ou mais frentes" if c["tres_ou_mais"] else ""))
    linhas.append("LENTES")
    linhas.append("  Frentes sem dono: " + (", ".join(lentes["sem_dono"]) or "nenhuma"))
    linhas.append("  Frentes com mais de um dono: " + (", ".join(lentes["varios_donos"]) or "nenhuma"))
    linhas.append("  Dono com autonomia baixa e sem apoio na frente: "
                  + ("; ".join(f"{p} em {f}" for p, f in lentes["autonomia_baixa_sem_apoio"]) or "nenhum"))
    por = {}
    for f, p in lentes["uma_pessoa"].items():
        por.setdefault(p, []).append(f)
    linhas.append("  Frentes com uma pessoa só: " + ("; ".join(f"{p}: {', '.join(fs)}" for p, fs in por.items()) or "nenhuma"))
    return linhas


def ec_ler(base, pedido):
    saida, texto = [], []
    for nome in pedido.get("arquivos", []):
        item = {"arquivo": nome}
        texto.append(f"\n=== {nome}")
        try:
            caminho = _ec_arquivo(base, nome)
        except FileNotFoundError as e:
            item["erro"] = str(e)
            texto.append(f"ERRO: {e}")
            saida.append(item)
            continue
        if caminho.lower().endswith(".pptx"):
            e = ler_estrutura(caminho)
            if e is not None:
                item["estrutura"] = e
                texto.append(f"Análise de estrutura de {pl_dma(e['data'])} · gatilho: {e.get('gatilho', '–')}")
                texto += [f"  {l['pessoa']} | {l.get('papel', '')} | {l['frente']} | {float(l.get('pct') or 0):g}% | "
                          f"{l.get('autonomia') or '–'} | {'dono' if l.get('dono') else 'apoio'}" for l in e.get("mapa", [])]
                texto += _ec_txt_carga(e.get("mapa", []), e.get("restricoes", []))
                dec = e.get("decisao") or {}
                texto.append(f"Decisão: {dec.get('texto', '–')}")
                for t in dec.get("testes", []):
                    r = t.get("resultado")
                    texto.append(f"  {t['id']} · nível {t['nivel']} · {t['movimento']} · critério: {t['criterio']} · teste "
                                 f"{pl_dm(t['inicio'])}–{pl_dm(t['revisao'])} · "
                                 + (("atingido" if r["atingido"] else "não atingido") + f" em {pl_dm(r['data'])}" if r else "em teste"))
                texto += [f"Histórico: {pl_dm(h['data'])} · {h['registro']}" for h in e.get("historico", [])]
            else:
                dados, colunas = ler_plano(caminho)
                if dados is not None:
                    item["plano"] = dados
                    ag = dados.get("agenda", {})
                    texto.append(f"Plano 30-60-90 de {pl_dma(dados['data'])} · ciclo {dados.get('ciclo', 1)}, semana {dados.get('semana', 1)} de 4")
                    texto += [f"  {p['id']} {p.get('nome')} · resultado {p.get('resultado', '–')} · dono {p.get('dono') or 'SEM DONO'} · "
                              f"S1–S4: " + " | ".join(p.get("entregaveis", {}).get(f"S{k}") or "–" for k in range(1, 5))
                              for p in dados.get("prioridades", [])]
                    texto += [f"  {d['id']} delegação · {d.get('quem')} · {d.get('frente', '')} · {d.get('oque')} · checar em "
                              f"{pl_dm(d['checar']) if d.get('checar') else '–'}" for d in ag.get("delegacoes", [])]
                    texto += [f"  {k['id']} {k.get('nome')} · {k.get('tipo')} · baseline {k.get('baseline') or 'a levantar'} · status "
                              f"{PL_KPI_STATUS.get(k.get('status') or 'sem_dado')}" for k in dados.get("kpis", [])]
                    texto += [f"  Movimento: {m['nome']} (dono: {m.get('dono') or '–'})" for m in dados.get("retrato", {}).get("movimentos", [])]
                    _, _, sinais = pl_consistencia(dados)
                    texto += [f"Sinal de estrutura do plano: {x}" for x in sinais]
                else:
                    item["erro"] = "pptx sem dados de plano nem de análise"
                    texto.append("Este .pptx não é um plano do Coach de Gestão nem uma análise de estrutura: peça as prioridades em texto")
        else:
            item["erro"] = "formato não lido pelo script"
            texto.append("Formato não lido pelo script")
        saida.append(item)
    json.dump(saida, open(os.path.join(base, "estrutura_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(texto).strip())
    return 0


def _ec_partida(base, pedido):
    if pedido.get("estrutura"):
        return dict(pedido["estrutura"])
    e = ler_estrutura(_ec_arquivo(base, pedido["partida"]))
    if e is None:
        raise ValueError(f"{pedido['partida']} não é uma análise do Coach de Estrutura")
    return e


def ec_carga(base, pedido):
    if pedido.get("mapa") is not None:
        mapa, restr = pedido["mapa"], pedido.get("restricoes", [])
    else:
        e = _ec_partida(base, pedido)
        mapa = e.get("mapa", [])
        restr = pedido.get("restricoes", e.get("restricoes", []))
    print("\n".join(_ec_txt_carga(mapa, restr)))
    return 0


def ec_gerar(base, pedido):
    erros, log = [], []
    try:
        e = _ec_partida(base, pedido)
    except (FileNotFoundError, ValueError, KeyError) as x:
        print(f"NADA FOI GERADO: {x}")
        return 1
    if pedido.get("partida") and pedido.get("atualizar"):
        for k, v in pedido["atualizar"].items():
            e[k] = v
            log.append(f"Atualizado: {k}")
        e["data"] = pedido.get("data") or e["data"]
    if pedido.get("revisao"):
        e, log2 = es_revisar(e, pedido["revisao"], erros)
        log += log2
    if not e.get("data"):
        erros.append("Falta a data da análise")
    avisos = es_validar(e, erros)
    if erros:
        print("NADA FOI GERADO. Resolva com o usuário e rode de novo:\n" + "\n".join("- " + x for x in erros))
        return 1
    caminho = os.path.join(base, pedido.get("saida") or f"Estrutura {e['data']} (confidencial).pptx")
    avisos += gerar_estrutura(e, caminho)
    relido = ler_estrutura(caminho)
    prs = Presentation(caminho)
    marcados = sum(1 for s in prs.slides if any(sh.has_text_frame and ES_MARCA in sh.text_frame.text for sh in s.shapes))
    carga = es_carga(e.get("mapa", []), e.get("restricoes", []))
    dec = e.get("decisao") or {}
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(caminho)} · {len(prs.slides)} slides · \"Confidencial\" em {marcados} de {len(prs.slides)} · "
            + ("releitura sem diferença" if relido == json.loads(json.dumps(e, ensure_ascii=False)) else "ATENÇÃO: a releitura difere"),
            f"Mapa: {len(e.get('mapa', []))} linhas, {len(carga)} pessoas · carga: "
            + ", ".join(f"{p} {c['soma']:g}%" + (" (acima)" if c["acima"] else "") for p, c in carga.items()),
            f"Diagnóstico: {len(e.get('diagnostico', []))} prioridade(s) em risco · " + "; ".join(
                f"{d['prioridade']}: {d['causa']}" + (f" + {d['secundaria']}" if d.get("secundaria") else "") for d in e.get("diagnostico", [])),
            f"Decisão: {dec.get('texto') or 'Manter'}",
            "Testes: " + ("; ".join(f"{t['id']} {t['movimento']} · revisão em {pl_dm(t['revisao'])}"
                                    + (f" · {'atingido' if t['resultado']['atingido'] else 'não atingido'}" if t.get("resultado") else "")
                                    for t in dec.get("testes", [])) or "nenhum"),
            f"Histórico: {len(e.get('historico', []))} registro(s)"]
    if log:
        conf += ["Mudanças:"] + [f"- {x}" for x in log]
    if avisos:
        conf += ["Avisos:"] + [f"- {x}" for x in avisos]
    conf.append("Avise em uma linha: o arquivo é confidencial e não deve circular.")
    json.dump({"arquivo": caminho, "conferencia": conf, "estrutura": e}, open(os.path.join(base, "estrutura_resultado.json"), "w",
                                                                              encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def ec_main(argv):
    base, pedido_caminho = _ec_base(argv)
    if not pedido_caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/estrutura_pedido.json e rode o script de novo")
        return 2
    pedido = json.load(open(pedido_caminho, encoding="utf-8"))
    acoes = {"ler": ec_ler, "carga": ec_carga, "gerar": ec_gerar}
    if pedido.get("acao") not in acoes:
        print(f"Ação desconhecida {pedido.get('acao')!r}: use {', '.join(acoes)}")
        return 2
    try:
        return acoes[pedido["acao"]](base, pedido)
    except (FileNotFoundError, ValueError) as x:
        print(f"ERRO: {x}")
        return 1


if __name__ == "__main__":
    _codigo = ec_main(sys.argv)
    if _codigo:
        sys.exit(_codigo)
