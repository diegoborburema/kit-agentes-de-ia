# ---------------------------------------------------------------- PRD: linha de comando
# O agente grava o pedido em /mnt/data/prd_pedido.json (em Python, com json.dump) e roda este script.
# Ações: "ler" (um PRD anexado) e "gravar" (no PRD em andamento ou no template que vem com a skill).
import glob
import json
import os
import sys


def _prd_base(argv):
    """(pasta de trabalho, caminho do pedido)."""
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "prd_pedido.json")):
            return pasta, os.path.join(pasta, "prd_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _prd_arquivo(base, nome):
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _prd_template():
    aqui = os.path.dirname(os.path.abspath(globals().get("__file__", "") or "."))
    candidatos = [os.path.join(aqui, "..", "assets", "template-prd.docx")]
    candidatos += glob.glob("/home/oai/skills/**/prd-docx/assets/template-prd.docx", recursive=True)
    for c in candidatos:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("template-prd.docx não encontrado na pasta assets da skill prd-docx")


def _prd_curto(v, n=220):
    v = str(v).replace("\n", " / ")
    return v if len(v) <= n else v[:n - 1] + "…"


def prd_resumo_texto(d):
    """A leitura em texto, etapa por etapa, só com o que tem conteúdo."""
    out = []
    p = d["painel"]
    out.append("PAINEL: " + " · ".join(f"{k}: {v}" for k, v in p.items() if v) if any(p.values())
               else "PAINEL: vazio")
    if d.get("assinado"):
        out.append("PRD ASSINADO: só pedidos de mudança (Anexo B)")
    ck = [f"{e} {v['situacao']}" for e, v in d["checkpoints"].items() if v.get("situacao")]
    out.append("Checkpoints: " + (", ".join(ck) if ck else "nenhum registrado"))
    gt = [f"Gate {g}: {v.get('Decisão')}" for g, v in d["gates"].items() if v.get("Decisão")]
    out.append("Gates: " + (", ".join(gt) if gt else "nenhuma decisão registrada"))
    pessoas = [f"{k}: {v['Nome']}" for k, v in d["pessoas"].items() if v.get("Nome")]
    if pessoas:
        out.append("Pessoas: " + "; ".join(pessoas))
    for num, titulo, _ in ETAPAS:
        out.append(f"\n== {num} · {titulo}")
        for s in (x for x in SECOES if x["etapa"] == num):
            sec = d["secoes"].get(s["id"], {})
            if sec.get("vazia", True):
                out.append(f"{s['id']} {s['titulo']}: VAZIA")
                continue
            out.append(f"{s['id']} {s['titulo']}:")
            for k, v in sec["campos"].items():
                if v:
                    out.append(f"  {k}: {_prd_curto(v)}")
            for nome, linhas in sec["tabelas"].items():
                for l in linhas:
                    out.append(f"  [{nome}] " + " | ".join(f"{k}: {_prd_curto(v, 90)}" for k, v in l.items() if v))
        if num == "04":
            for chave, c in d["canvas"].items():
                nome = CANVAS[chave][0]
                if c["vazio"]:
                    out.append(f"Canvas {nome}: VAZIO")
                    continue
                out.append(f"Canvas {nome} (aplicável: {c['aplicavel'] or '?'}{'; ' + c['motivo'] if c['motivo'] else ''}):")
                for b, v in c["blocos"].items():
                    out.append(f"  {b}: {_prd_curto(v) if v else '(vazio)'}")
    out.append("\n== Anexos")
    for a in ANEXOS:
        sec = d["anexos"].get(a["id"], {})
        n_linhas = sum(len(l) for l in sec.get("tabelas", {}).values())
        n_campos = sum(1 for v in sec.get("campos", {}).values() if v)
        out.append(f"Anexo {a['id']} {a['titulo']}: " + ("VAZIO" if sec.get("vazia", True) else
                                                         f"{n_linhas} linha(s), {n_campos} campo(s)"))
        for nome, linhas in sec.get("tabelas", {}).items():
            for l in linhas:
                out.append(f"  [{nome}] " + " | ".join(f"{k}: {_prd_curto(v, 90)}" for k, v in l.items() if v))
        for k, v in sec.get("campos", {}).items():
            if v:
                out.append(f"  {k}: {_prd_curto(v)}")
    return "\n".join(out)


def prd_ler(base, pedido):
    nome = pedido.get("arquivo") or (pedido.get("arquivos") or [None])[0]
    if not nome:
        print('Pedido sem "arquivo": diga qual PRD ler')
        return 2
    try:
        d = ler_prd(_prd_arquivo(base, nome))
    except FileNotFoundError as e:
        print(f"ERRO: {e}")
        return 1
    except Exception as e:
        print(f"ERRO ao ler {nome}: {type(e).__name__}: {e}. Se não for um PRD deste template, leia o arquivo "
              "como material de apoio")
        return 1
    json.dump(d, open(os.path.join(base, "prd_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"=== {nome}\n" + prd_resumo_texto(d))
    return 0


def prd_gravar(base, pedido):
    try:
        origem = _prd_arquivo(base, pedido["base"]) if pedido.get("base") else _prd_template()
    except FileNotFoundError as e:
        print(f"NADA FOI GRAVADO: {e}")
        return 1
    produto = (pedido.get("painel") or {}).get("Produto")
    if not produto and pedido.get("base"):
        try:
            produto = ler_prd(origem)["painel"].get("Produto")
        except Exception:
            produto = None
    produto = produto or "sem nome"
    numero = (pedido.get("versao") or {}).get("numero", "")
    saida = os.path.join(base, pedido.get("saida") or f"PRD {produto}{' v' + numero if numero else ''}.docx")
    try:
        feito = gravar_prd(pedido, origem, saida)
    except PedidoInvalido as e:
        print(f"NADA FOI GRAVADO. Corrija o pedido e rode de novo: {e}")
        return 1
    except Exception as e:
        print(f"NADA FOI GRAVADO. Erro na gravação: {type(e).__name__}: {e}. Entregue o conteúdo por seção, "
              "pronto para colar")
        return 1
    d = ler_prd(saida)
    cheias = [s for s, v in d["secoes"].items() if not v["vazia"]]
    vazias = [s for s, v in d["secoes"].items() if v["vazia"]]
    canvas = [CANVAS[k][0] for k, v in d["canvas"].items() if not v["vazio"]]
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(saida)} · versão vigente: {d['painel'].get('Versão vigente') or '—'}",
            "Gravado: " + "; ".join(feito) if feito else "Gravado: nada (template vazio)",
            f"Seções com conteúdo ({len(cheias)}): {', '.join(cheias) or '—'}",
            f"Seções vazias ({len(vazias)}): {', '.join(vazias) or '—'}",
            f"Canvas com conteúdo: {', '.join(canvas) or '—'}",
            "Decisões de gate: " + (", ".join(f"Gate {g}: {v.get('Decisão')}" for g, v in d["gates"].items()
                                              if v.get("Decisão")) or "em branco")]
    json.dump({"arquivo": saida, "conferencia": conf}, open(os.path.join(base, "prd_resultado.json"), "w",
                                                              encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def prd_main(argv):
    base, caminho = _prd_base(argv)
    if not caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/prd_pedido.json (em Python, com json.dump) e "
              "rode o script de novo")
        return 2
    pedido = json.load(open(caminho, encoding="utf-8"))
    acao = pedido.get("acao")
    if acao == "ler":
        return prd_ler(base, pedido)
    if acao == "gravar":
        return prd_gravar(base, pedido)
    print(f'Ação desconhecida {acao!r}: use "ler" ou "gravar"')
    return 2


if __name__ == "__main__":
    _codigo_prd = prd_main(sys.argv)
    if _codigo_prd:
        sys.exit(_codigo_prd)
