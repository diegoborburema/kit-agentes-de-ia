# ---------------------------------------------------------------- linha de comando do Redator de Atas
# O agente grava o pedido em /mnt/data/ata_pedido.json e roda este script. Ações: ler (os anexos da reunião),
# trecho (um bloco de leitura), buscar (os trechos que sustentam um item) e conferir (a ata contra a fonte).
# O agente não lê a transcrição nem confere a ata por conta própria.
import json
import os
import sys

_CA_LEITURA = "ata_leitura.json"


def _ca_base(argv):
    """(pasta de trabalho, caminho do pedido). O pedido pode vir como argumento ou em ata_pedido.json."""
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "ata_pedido.json")):
            return pasta, os.path.join(pasta, "ata_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _ca_arquivo(base, nome):
    """Caminho de um anexo pelo nome; aceita diferença de maiúsculas e de acentos."""
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    alvo = at_sem_acento(os.path.basename(nome))
    for f in os.listdir(base):
        if at_sem_acento(f) == alvo:
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _ca_dm(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}" if iso and len(iso) == 10 else (iso or "")


def _ca_ler(base, pedido):
    arquivos = pedido.get("arquivos") or []
    if not arquivos:
        print("NADA FOI LIDO: o pedido não tem arquivos. Liste em \"arquivos\" os anexos da reunião, pelo nome.")
        return 0
    caminhos, faltam = [], []
    for nome in arquivos:
        try:
            caminhos.append(_ca_arquivo(base, nome))
        except FileNotFoundError as e:
            faltam.append(str(e))
    if faltam:
        print("NADA FOI LIDO:")
        for f in faltam:
            print("  - " + f)
        print("Arquivos nesta pasta: " + (", ".join(sorted(x for x in os.listdir(base) if not x.startswith(("ata_", "."))))
                                         or "nenhum"))
        return 0
    try:
        tamanho = max(2000, int(pedido.get("tamanho") or AT_BLOCO))
    except (TypeError, ValueError):
        tamanho = AT_BLOCO
    leitura = at_ler(caminhos, pedido.get("convidados"), tamanho)
    if pedido.get("data_reuniao"):
        leitura["data"] = pedido["data_reuniao"]
    json.dump(leitura, open(os.path.join(base, _CA_LEITURA), "w", encoding="utf-8"), ensure_ascii=False)

    falas = sum(a["falas"] for a in leitura["arquivos"])
    pessoas = at_falantes_pessoas(leitura)
    cab = [leitura["titulo"] or "(sem título no arquivo)", _ca_dm(leitura["data"]) or "data não encontrada"]
    if leitura["duracao"]:
        cab.append(leitura["duracao"])
    print(f"LEITURA: {' · '.join(cab)} · {len(caminhos)} arquivo(s) · {falas} falas · {len(pessoas)} falantes · "
          f"{len(leitura['blocos'])} bloco(s)")
    for a in leitura["arquivos"]:
        desc = {"transcrição": f"transcrição ({a['formato']}) · {a['falas']} falas",
                "notas": f"notas sem falantes ({a['formato']}) · {a['linhas']} linhas",
                "apoio": f"material de apoio ({a['formato']}) · {a['linhas']} trechos"}[a["tipo"]]
        extra = []
        if a["titulo"]:
            extra.append(f'título "{a["titulo"]}"')
        if a["data"]:
            extra.append(_ca_dm(a["data"]))
        if a["duracao"]:
            extra.append(a["duracao"])
        if a["removidos"]:
            extra.append(f"{a['removidos']} marcas automáticas ou trechos em HTML removidos")
        print(f'  "{a["arquivo"]}": {desc}' + (" · " + " · ".join(extra) if extra else ""))
        for av in a["avisos"]:
            print(f"    aviso: {av}")
    if leitura["falantes"]:
        print("Falantes (nome | como aparece | falas | palavras | primeira–última fala | marca):")
        for f in leitura["falantes"]:
            marca = {"": "", "externo": "externo",
                     "sala": "sala: não é pessoa; veja nas falas se alguém se identifica",
                     "não identificado": "não identificado: não vira participante"}[f["marca"]]
            print(f"  {f['nome']} | {', '.join(f['brutos']) or '–'} | {f['falas']} | {f['palavras']} | "
                  f"{f['primeira'] or '–'}–{f['ultima'] or '–'} | {marca}")
    if leitura["presentes"]:
        print("Presentes escritos nas notas (provam presença): " + ", ".join(
            p["nome"] + (f" ({p['area']})" if p.get("area") else "") for p in leitura["presentes"]))
    if leitura["eventos"]:
        print("Eventos: " + "; ".join(f"{e['nome']} {e['evento']}" for e in leitura["eventos"]))
    if leitura["convidados"] or leitura["ausentes"]:
        provas = [f["nome"] for f in pessoas] + [p["nome"] for p in leitura["presentes"]] + \
                 [e["nome"] for e in leitura["eventos"]]
        sem = [c["nome"] for c in leitura["convidados"] + leitura["ausentes"] if not ac_casar(c["nome"], provas)]
        print(f"Convidados: {len(leitura['convidados'])} · sem fala nem presença escrita: "
              + (", ".join(dict.fromkeys(sem)) if sem else "nenhum") + " (convite não é presença)")
    n = len(leitura["blocos"])
    if n:
        print(f"Próximo passo: leia os blocos 1 a {n} com {{\"acao\": \"trecho\", \"bloco\": N}}, todos, antes de "
              f"escrever a ata.")
    else:
        print("Nenhum texto lido nos arquivos.")
    return 0


def _ca_carregar(base):
    caminho = os.path.join(base, _CA_LEITURA)
    if not os.path.exists(caminho):
        return None
    return json.load(open(caminho, encoding="utf-8"))


def _ca_trecho(base, pedido):
    leitura = _ca_carregar(base)
    if leitura is None:
        print('NADA FOI LIDO: rode antes {"acao": "ler"} com os anexos da reunião.')
        return 0
    n = len(leitura["blocos"])
    try:
        k = int(pedido.get("bloco", 1))
    except (TypeError, ValueError):
        k = 1
    if not 1 <= k <= n:
        print(f"Bloco {k} não existe: a leitura tem {n} bloco(s).")
        return 0
    b = leitura["blocos"][k - 1]
    horas = f" · {b['inicio']}–{b['fim']}" if b["inicio"] else ""
    print(f"BLOCO {k}/{n} · {b['de']}–{b['ate']}{horas}")
    for i in b["indices"]:
        print(at_linha_item(leitura["itens"][i]))
    print(f"Fim do bloco {k}/{n}." + (f" Leia o bloco {k + 1} antes de escrever." if k < n else
                                       " Leitura completa."))
    return 0


def _ca_buscar(base, pedido):
    leitura = _ca_carregar(base)
    if leitura is None:
        print('NADA FOI LIDO: rode antes {"acao": "ler"} com os anexos da reunião.')
        return 0
    termos = pedido.get("termos") or []
    if isinstance(termos, str):
        termos = [termos]
    itens, total = at_buscar(leitura, termos, pedido.get("falante"), bool(pedido.get("todos")))
    filtro = f" · falante {pedido['falante']}" if pedido.get("falante") else ""
    print(f"BUSCA {', '.join(repr(t) for t in termos)}{filtro} · {total} fala(s) com os termos"
          + (f" (mostrando as 12 com mais termos)" if total > 12 else ""))
    if not itens:
        print("Nada na fonte com esses termos. Sem trecho, o item não entra na ata como fato.")
    for it in itens:
        print(("» " if it["acerto"] else "  ") + at_linha_item(it))
    return 0


def _ca_conferir(base, pedido):
    ata = pedido.get("ata")
    if not ata and pedido.get("ata_arquivo"):
        ata = open(_ca_arquivo(base, pedido["ata_arquivo"]), encoding="utf-8").read()
    if not ata:
        print('NADA FOI CONFERIDO: mande o texto da ata em "ata" ou o arquivo em "ata_arquivo".')
        return 0
    leitura = _ca_carregar(base)
    tipo = pedido.get("tipo") or "outro"
    pontos = ac_conferir(ata, leitura, tipo, pedido.get("confirmados"), pedido.get("presentes"),
                         pedido.get("extras", ""), pedido.get("secoes_pedidas"))
    nome_tipo = AC_NOME_TIPO.get(at_sem_acento(tipo).strip(), tipo)
    grupos = [("corrigir", "Corrija pela fonte antes de mostrar"), ("perguntar", "Leve à conferência do usuário"),
              ("saber", "Para saber")]
    print(f"CONFERÊNCIA ({nome_tipo}): {sum(1 for p in pontos if p['acao'] == 'corrigir')} para corrigir · "
          f"{sum(1 for p in pontos if p['acao'] == 'perguntar')} para o usuário")
    if leitura is None or not leitura.get("itens"):
        print("Sem leitura da transcrição nesta conversa: conferidos só título, seções e formato. Participantes, "
              "responsáveis e números não foram conferidos contra a fonte.")
    for acao, rot in grupos:
        lista = [p for p in pontos if p["acao"] == acao]
        if lista:
            print(f"{rot} ({len(lista)}):")
            for p in lista:
                print(f"  - [{p['cat']}] {p['texto']}")
    if not pontos:
        print("Nenhum ponto: participantes, responsáveis, números, seções e formato batem com a fonte.")
    return 0


def main(argv=None):
    argv = sys.argv if argv is None else argv
    base, caminho = _ca_base(argv)
    if caminho is None:
        print(f'NADA FOI FEITO: grave o pedido em {os.path.join(base, "ata_pedido.json")} e rode de novo.')
        return 0
    pedido = json.load(open(caminho, encoding="utf-8-sig"))
    acao = (pedido.get("acao") or "").strip().lower()
    acoes = {"ler": _ca_ler, "trecho": _ca_trecho, "buscar": _ca_buscar, "conferir": _ca_conferir}
    if acao not in acoes:
        print(f'NADA FOI FEITO: ação "{acao}" desconhecida. Use: ler, trecho, buscar ou conferir.')
        return 0
    return acoes[acao](base, pedido)


if __name__ == "__main__":
    sys.exit(main())
