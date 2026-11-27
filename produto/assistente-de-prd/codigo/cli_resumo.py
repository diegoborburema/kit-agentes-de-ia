# ---------------------------------------------------------------- PRD: linha de comando do resumo
# O agente grava {"arquivo": "<PRD>.docx"} em /mnt/data/prd_resumo.json (em Python, com json.dump) e roda este
# script. Ele gera "Resumo PRD <produto> v<versão>.html" na mesma pasta e imprime o relatório para o agente
# repassar. Sem "arquivo", usa o PRD mais recente da pasta. O agente não escreve HTML.
import glob
import json
import os
import sys


def _rcli_pasta(argv):
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "prd_resumo.json")):
            return pasta, os.path.join(pasta, "prd_resumo.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _rcli_eh_prd(caminho):
    try:
        d = ler_prd(caminho)
    except Exception:
        return False
    return "01.1" in d["secoes"] and "05.7" in d["secoes"]


def _rcli_achar(pasta, nome=None):
    if nome:
        for c in (nome, os.path.join(pasta, nome)):
            if os.path.isfile(c):
                return c
        for f in os.listdir(pasta):
            if f.lower() == os.path.basename(nome).lower():
                return os.path.join(pasta, f)
        raise FileNotFoundError(f'"{nome}" não está em {pasta}: peça para o usuário anexar o PRD (.docx) na conversa')
    docs = sorted((f for f in glob.glob(os.path.join(pasta, "*.docx")) if not os.path.basename(f).startswith("~$")),
                  key=os.path.getmtime, reverse=True)
    for f in docs:
        if _rcli_eh_prd(f):
            return f
    raise FileNotFoundError("não há PRD (.docx) deste template nesta conversa: peça para o usuário anexar o PRD")


def _rcli_relatorio(r, origem):
    out = [f'Resumo gerado: {r["arquivo"]} ({max(r["tamanho"] // 1024, 1)} KB), a partir de "{os.path.basename(origem)}".',
           "Abas: " + ", ".join(r["abas"])]
    if r["divergencias"]:
        out.append("O PRD se contradiz (aviso na aba Revisor):")
        out += [f"  - {x}" for x in r["divergencias"]]
    if r["assinado"]:
        out.append(f'PRD assinado (versão {r["versao_assinada"]}): o que mudar agora entra como pedido de mudança '
                   "(Anexo B).")
    elif r["gate"]:
        porte = f" no porte {r['porte']}" if r["porte"] else ""
        out.append(f'Gate {r["gate"]}: {r["completas"]} de {r["total"]} seções e anexos cobrados{porte} com conteúdo '
                   "(completude, não qualidade).")
        out += [f"  - {sid} {tit}: vazia ({dono})" for sid, tit, dono in r["faltas"][:5]]
        if len(r["faltas"]) > 5:
            out.append(f"  - e mais {len(r['faltas']) - 5} (aba Revisor)")
    else:
        out.append("Gates 1 e 2 decididos; a versão assinada ainda não está no painel.")
    out.append(f'Anexo A: {r["pendencias"]} item(ns), {r["bloqueiam"]} bloqueante(s).')
    return "\n".join(out)


def resumo_main(argv):
    pasta, pedido = _rcli_pasta(argv)
    nome = None
    if pedido:
        with open(pedido, encoding="utf-8") as f:
            nome = json.load(f).get("arquivo")
    try:
        origem = _rcli_achar(pasta, nome)
        r = gerar_resumo(origem, pasta)
    except FileNotFoundError as e:
        print(f"ERRO (nada foi gerado): {e}")
        return 1
    except Exception as e:
        print(f"ERRO (nada foi gerado): {type(e).__name__}: {e}. Se o arquivo não for um PRD deste template, "
              "diga isso ao usuário")
        return 1
    print(_rcli_relatorio(r, origem))
    return 0


if __name__ == "__main__":
    _codigo_resumo = resumo_main(sys.argv)
    if _codigo_resumo:
        sys.exit(_codigo_resumo)
