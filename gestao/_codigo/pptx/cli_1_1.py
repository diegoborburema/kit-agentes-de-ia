# ---------------------------------------------------------------- linha de comando do Organizador de 1-1
# O agente grava o pedido em /mnt/data/pauta_pedido.json e roda este script. O script lê as pautas anexadas
# ou gera o .pptx da pauta nova, e imprime o resultado. O agente não escreve código de layout.
import json
import os
import sys

from pptx import Presentation


def _p11_base(argv):
    """(pasta de trabalho, caminho do pedido). O pedido pode vir como argumento ou em pauta_pedido.json."""
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "pauta_pedido.json")):
            return pasta, os.path.join(pasta, "pauta_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _p11_arquivo(base, nome):
    """Caminho de um anexo pelo nome; aceita diferença de maiúsculas."""
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _p11_txt(d):
    linhas = [f"Título: {d['titulo']} · {d['semana']}"]
    linhas += [f"Legenda {g}: {', '.join(itens)}" for g, itens in d["legenda"].items()]
    if not d["linhas"]:
        linhas.append("SEM TABELA. Textos do slide, de cima para baixo (monte as linhas e confirme com o usuário):")
        linhas += ["  " + t.replace("\n", " / ") for t in d["textos"]]
        return linhas
    linhas.append("Linhas (Categoria | Tema | Texto | Tipo | Status | Anotações):")
    for x in d["linhas"]:
        linhas.append("  " + " | ".join([x["categoria"], x["tema"], x["texto"].replace("\n", " / "), x["tipo"],
                                         x["status"] or "", x["anotacoes"].replace("\n", " / ")]))
    linhas.append("Combinados (Quem | O quê | Até | Feito):")
    linhas += ["  " + " | ".join([c["quem"], c["oque"], c["ate"], c["feito"] or "em aberto"]) for c in d["combinados"]]
    return linhas


def p11_ler(base, pedido):
    saida, texto = [], []
    for nome in pedido.get("arquivos", []):
        item = {"arquivo": nome}
        texto.append(f"\n=== {nome}")
        try:
            d = ler_pauta(_p11_arquivo(base, nome), completo=True)
        except FileNotFoundError as e:
            item["erro"] = str(e)
            texto.append(f"ERRO: {e}")
        except Exception as e:
            item["erro"] = f"{type(e).__name__}: {e}"
            texto.append(f"ERRO ao ler: {type(e).__name__}: {e}. Peça a pauta como imagem ou texto")
        else:
            item["pauta"] = d
            texto += _p11_txt(d)
        saida.append(item)
    json.dump(saida, open(os.path.join(base, "pauta_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(texto).strip())
    return 0


def _p11_validar(dados):
    erros = []
    for chave in ("direcao", "pessoa", "semana", "linhas"):
        if chave not in dados:
            erros.append(f"falta o campo {chave!r}")
    if dados.get("direcao") not in ("cima", "baixo"):
        erros.append('direcao deve ser "cima" ou "baixo"')
    for i, l in enumerate(dados.get("linhas", []), start=1):
        if l.get("secao") not in ORDEM:
            erros.append(f"linha {i}: secao {l.get('secao')!r} inválida (válidas: {', '.join(ORDEM)})")
    return erros


def p11_gerar(base, pedido):
    dados = pedido.get("pauta") or {}
    erros = _p11_validar(dados)
    if erros:
        print("NADA FOI GERADO. Corrija o pedido e rode de novo:\n" + "\n".join("- " + e for e in erros))
        return 1
    caminho = os.path.join(base, pedido.get("saida") or f"1-1 {dados['pessoa']}.pptx")
    try:
        n = gerar_pauta(json.loads(json.dumps(dados)), caminho)
    except Exception as e:
        print(f"NADA FOI GERADO. Erro na geração: {type(e).__name__}: {e}. Entregue só a tabela final")
        return 1

    # Conferência: o arquivo relido, para a entrega descrever só o que ele tem
    d = ler_pauta(caminho, completo=True)
    pedidas = [l["tema"] for l in sorted(dados["linhas"], key=lambda l: ORDEM.index(l["secao"]))
               if l.get("tema") or l.get("atualizacao") or l.get("puxar")]
    lidas = [l["tema"] for l in d["linhas"]]
    notas = ""
    prs = Presentation(caminho)
    if prs.slides[0].has_notes_slide:
        notas = prs.slides[0].notes_slide.notes_text_frame.text
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(caminho)} · {n} slide(s)" + (" · ATENÇÃO: mais de 2 slides, a pauta está longa demais" if n > 2 else ""),
            f"Linhas: {len(lidas)}" + (" (iguais às pedidas, na ordem)" if lidas == pedidas else f" ATENÇÃO: diferentes das pedidas {pedidas}"),
            f"Combinados: {len(d['combinados'])} em aberto + 3 linhas em branco"]
    conf += [f"Legenda {g}: {', '.join(itens)}" for g, itens in d["legenda"].items()]
    conf.append("Perguntas para levar nas notas: " + ("sim" if "Perguntas para levar" in notas else "NÃO"))
    json.dump({"arquivo": caminho, "slides": n, "conferencia": conf},
              open(os.path.join(base, "pauta_resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def p11_main(argv):
    base, pedido_caminho = _p11_base(argv)
    if not pedido_caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/pauta_pedido.json e rode o script de novo")
        return 2
    pedido = json.load(open(pedido_caminho, encoding="utf-8"))
    acao = pedido.get("acao")
    if acao == "ler":
        return p11_ler(base, pedido)
    if acao == "gerar":
        return p11_gerar(base, pedido)
    print(f'Ação desconhecida {acao!r}: use "ler" ou "gerar"')
    return 2


if __name__ == "__main__":
    _codigo_p11 = p11_main(sys.argv)
    if _codigo_p11:
        sys.exit(_codigo_p11)
