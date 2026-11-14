# ---------------------------------------------------------------- conferência da ata contra a fonte
# Confere o rascunho da ata contra a leitura da reunião: quem está em Participantes sem prova de presença e quem
# falou e ficou de fora; responsáveis que não aparecem na fonte; números e datas da ata que não estão na fonte ou que
# foram corrigidos na reunião; prazos convertidos de dia da semana; seções fora da estrutura do tipo; título e
# restos de formatação. Cada ponto vem com o que fazer: corrigir pela fonte, levar ao usuário ou só saber.
import datetime as _dt
import re

AC_SECOES = {
    "refinamento": ["participantes", "pontos alinhados", "decisoes tomadas", "riscos e pontos de atencao",
                    "proximos passos"],
    "homologacao": ["participantes", "contexto", "funcionalidades apresentadas", "status de homologacao",
                    "bugs ou ajustes identificados", "conclusao", "proximos passos"],
    "discovery": ["participantes", "contexto", "dor ou problema", "usuarios afetados", "jornada atual e proposta",
                  "jornada atual", "jornada proposta", "hipoteses de solucao", "criterios preliminares",
                  "premissas e restricoes", "duvidas em aberto", "proximos passos"],
    "alinhamento": ["participantes", "contexto", "contexto ou pano de fundo", "pano de fundo", "pontos alinhados",
                    "decisoes tomadas", "divergencias registradas", "riscos e pontos de atencao", "proximos passos"],
    "outro": None,
}
AC_NOME_TIPO = {"refinamento": "Refinamento", "homologacao": "Homologação", "discovery": "Discovery",
                "alinhamento": "Alinhamento", "outro": "Outro"}
AC_PROIBIDAS = ["resumo executivo", "resumo", "acordos tecnicos", "acordos funcionais", "principais dores",
                "itens despriorizados", "criterios de aceite", "fonte", "fontes", "duracao", "objetivo", "sprint",
                "status", "observacoes"]
AC_DIAS = {"segunda": 0, "segunda-feira": 0, "terca": 1, "terca-feira": 1, "quarta": 2, "quarta-feira": 2,
           "quinta": 3, "quinta-feira": 3, "sexta": 4, "sexta-feira": 4, "sabado": 5, "domingo": 6}
AC_CORRECAO = re.compile(r"\b(na verdade|corrigindo|me corrigindo|corrige|corrijo|errei|me enganei|confundi|"
                         r"retificando|desculp\w*,? (?:e|era|sao)|nao e (?:\d|isso)|alias)\b")
AC_STATUS_HOMOLOG = re.compile(r"\b(aprovad[oa]s?|reprovad[oa]s?|ressalvas?|homologad[oa]s?)\b")
AC_SEM_DONO = re.compile(r"^(nao informado|n/?i|a definir|tbd|-+|–|—|\?)$")
AC_UNIDADES = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7,
               "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14, "catorze": 14,
               "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19}
AC_DEZENAS = {"vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70,
              "oitenta": 80, "noventa": 90, "cem": 100}
AC_POR_EXTENSO = re.compile(r"\b(?:(" + "|".join(AC_DEZENAS) + r")(?: e (" + "|".join(AC_UNIDADES) + r"))?|("
                            + "|".join(AC_UNIDADES) + r"))(?= (?:por cento|mil)\b)")


def ac_extenso(texto):
    """'cem por cento' → '100 por cento'; 'cinco mil' → '5 mil'. Só antes de 'por cento' e de 'mil'."""
    def troca(m):
        if m[3]:
            return str(AC_UNIDADES[m[3]])
        return str(AC_DEZENAS[m[1]] + (AC_UNIDADES[m[2]] if m[2] else 0))
    return AC_POR_EXTENSO.sub(troca, at_sem_acento(texto))


def ac_secao_chave(titulo):
    t = at_sem_acento(re.sub(r"^#+\s*", "", titulo))
    t = re.sub(r"[*_`]", "", t)
    t = re.sub(r"^\s*\d+\s*[.)-]?\s*", "", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return " ".join(t.split())


def ac_tabelas(linhas):
    """Tabelas Markdown de um trecho: lista de (cabeçalho, linhas), cada linha como dict coluna → valor."""
    tabelas, atual = [], []
    for ln in linhas + [""]:
        if ln.strip().startswith("|"):
            atual.append(ln.strip())
            continue
        if len(atual) >= 2:
            celulas = [[c.strip() for c in re.split(r"(?<!\\)\|", l.strip("|"))] for l in atual]
            cab = [ac_secao_chave(c) for c in celulas[0]]
            corpo = [c for c in celulas[1:] if not all(re.fullmatch(r":?-{2,}:?", x or "---") for x in c)]
            tabelas.append((cab, [dict(zip(cab, c)) for c in corpo]))
        atual = []
    return tabelas


def ac_partes(ata):
    """Título, linhas e seções (## …) da ata."""
    linhas = ata.replace("\r", "").split("\n")
    titulo = next((l.strip() for l in linhas if l.strip()), "")
    secoes, atual = [], None
    for ln in linhas:
        if re.match(r"^##\s+\S", ln) and not ln.startswith("###"):
            atual = {"titulo": ln[2:].strip(), "chave": ac_secao_chave(ln[2:]), "linhas": []}
            secoes.append(atual)
        elif atual is not None:
            atual["linhas"].append(ln)
    return titulo, linhas, secoes


def ac_nomes_participantes(secao):
    nomes = []
    for cab, linhas in ac_tabelas(secao["linhas"]):
        col = next((c for c in cab if c.startswith(("participante", "nome", "quem"))), cab[0] if cab else None)
        for l in linhas:
            if l.get(col):
                nomes.append(re.sub(r"[*_`]", "", l[col]).strip())
    if not nomes:
        for ln in secao["linhas"]:
            m = re.match(r"^\s*[-*•]\s+(.+)$", ln)
            if m:
                nomes.append(re.split(r"\s+[–—-]\s+|\s*\(|\s*\|", re.sub(r"[*_`]", "", m[1]))[0].strip())
    return [n for n in nomes if n]


def ac_casar(nome, candidatos):
    """Candidato que é a mesma pessoa que `nome` (nome completo, contido, ou primeiro nome único), ou None."""
    k = at_chave(nome).split()
    if not k:
        return None
    for c in candidatos:
        if at_chave(c).split() == k:
            return c
    for c in candidatos:
        kc = at_chave(c).split()
        if len(k) >= 2 and set(k) <= set(kc) or len(kc) >= 2 and set(kc) <= set(k):
            return c
    mesmos = [c for c in candidatos if at_chave(c).split()[:1] == k[:1]]
    if len(k) == 1 and len(mesmos) == 1:
        return mesmos[0]
    if len(k) >= 2 and len(mesmos) == 1 and len(at_chave(mesmos[0]).split()) == 1:
        return mesmos[0]
    return None


def ac_valores(texto):
    """Números da ata ou da fonte: lista de (tipo, valor, texto). Tipos: pct, num, data (dia, mês)."""
    t = ac_extenso(texto)
    saida = []
    for m in re.finditer(r"(?<![\w/])(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?(?![\w/])", t):
        d, mth = int(m[1]), int(m[2])
        if 1 <= d <= 31 and 1 <= mth <= 12:
            saida.append(("data", (d, mth), m[0]))
    t2 = re.sub(r"(?<![\w/])\d{1,2}/\d{1,2}(?:/\d{2,4})?(?![\w/])", " ", t)
    for m in re.finditer(r"(?<![\w.,-])(\d+(?:[.,]\d+)?)\s?(%|por cento)", t2):
        saida.append(("pct", float(m[1].replace(",", ".")), m[0]))
    t3 = re.sub(r"(?<![\w.,-])\d+(?:[.,]\d+)?\s?(%|por cento)", " ", t2)
    for m in re.finditer(r"(?<![\w-])(?:R\$\s?)?(\d{1,3}(?:\.\d{3})+|\d+(?:,\d+)?)(?:\s?(mil|milh[õo]es|milh[ãa]o|mi|bi|k))?"
                         r"(?![\w-])", t3):
        bruto = m[1]
        val = float(bruto.replace(".", "")) if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", bruto) else \
            float(bruto.replace(",", "."))
        mult = (m[2] or "").lower()
        val *= 1000 if mult in ("mil", "k") else 1e6 if mult.startswith(("milh", "mi")) else 1e9 if mult == "bi" else 1
        if val >= 10 or "," in bruto or mult:
            saida.append(("num", val, m[0].strip()))
    return saida


def ac_datas_relativas(itens, data_reuniao):
    """Datas que a fonte diz por dia da semana ou por 'amanhã': {(dia, mês): [(palavra, id)]}."""
    if not data_reuniao:
        return {}
    base = _dt.date.fromisoformat(data_reuniao)
    saida = {}
    for it in itens:
        t = at_sem_acento(it["texto"])
        for m in re.finditer(r"\b(segunda(?:-feira)?|terca(?:-feira)?|quarta(?:-feira)?|quinta(?:-feira)?|"
                             r"sexta(?:-feira)?|sabado|domingo|amanha)\b", t):
            p = m[1]
            if p == "amanha":
                d = base + _dt.timedelta(days=1)
            else:
                delta = (AC_DIAS[p] - base.weekday()) % 7 or 7
                d = base + _dt.timedelta(days=delta)
            saida.setdefault((d.day, d.month), []).append((p, it["id"]))
    return saida


def ac_conferir(ata, leitura=None, tipo="outro", confirmados=None, presentes=None, extras="", secoes_pedidas=None):
    """Pontos da conferência: lista de dicts {acao: corrigir|perguntar|saber, cat, texto}."""
    pontos = []

    def ponto(acao, cat, texto):
        pontos.append({"acao": acao, "cat": cat, "texto": texto})

    tipo_k = at_sem_acento(tipo or "outro").strip()
    tipo_k = tipo_k if tipo_k in AC_SECOES else "outro"
    titulo, linhas, secoes = ac_partes(ata)
    pedidas = {ac_secao_chave(s) for s in (secoes_pedidas or [])}

    # Título e formato
    if not re.match(r"^(#\s*)?(\*\*)?Ata de Reuni[ãa]o \| \S", titulo):
        ponto("corrigir", "Formato", f'a ata deve começar com "# Ata de Reunião | <tema>" (está "{titulo[:60]}")')
    if not secoes:
        ponto("corrigir", "Formato", 'nenhuma seção em "## ": use ## para as seções e ### para os temas')
    corpo = "\n".join(linhas)
    for padrao, rot in ((r"</?[a-zA-Z][^>]*>", "HTML"), (r"\[(?:Event|Evento)\]", "[Event]"),
                        (r"【|†|\bturn\d+|\bcite\w*\b|(?<!\])\[\d{1,3}\](?!\()", "referência automática"), (r"&nbsp;|&amp;|&lt;", "entidade HTML"),
                        (r"(?<![\w-])[TNA]\d{3}(?![\w-])", "ID interno de fala (T001…)")):
        achados = re.findall(padrao, corpo)
        if achados:
            ponto("corrigir", "Formato", f"{rot} na ata ({len(achados)}x, ex.: {achados[0]}): tire")

    # Seções
    permitidas = AC_SECOES[tipo_k]
    vistas = set()
    for s in secoes:
        k = s["chave"]
        if k in vistas:
            ponto("corrigir", "Seções", f'seção "{s["titulo"]}" repetida: junte num bloco só')
        vistas.add(k)
        if k in pedidas:
            continue
        if k in AC_PROIBIDAS:
            ponto("corrigir", "Seções", f'"{s["titulo"]}" não entra sem pedido do usuário: tire')
        elif permitidas is not None and k not in permitidas:
            ponto("corrigir", "Seções", f'"{s["titulo"]}" não faz parte da estrutura de {AC_NOME_TIPO[tipo_k]}: '
                                        f"tire, ou leve o conteúdo para a seção certa")
    sec = {s["chave"]: s for s in secoes}

    sem_fonte = leitura is None or not leitura.get("itens")
    itens = [] if sem_fonte else leitura["itens"]
    fonte_txt = at_sem_acento("\n".join(it["texto"] + " " + it.get("falante", "") for it in itens) + "\n" + (extras or ""))

    # Participantes
    part = sec.get("participantes")
    nomes_ata = ac_nomes_participantes(part) if part else []
    if not part:
        ponto("corrigir", "Participantes", "falta a seção Participantes")
    if not sem_fonte:
        falantes = [f["nome"] for f in at_falantes_pessoas(leitura)]
        notas = [p["nome"] for p in leitura.get("presentes", [])]
        eventos = [e["nome"] for e in leitura.get("eventos", [])]
        conf = [at_nome(c)[0] for c in (confirmados or [])]
        por_fonte, turnos_fonte = [], set()
        for p in presentes or []:
            nome, turno = (p.get("nome"), p.get("turno")) if isinstance(p, dict) else (p, None)
            it = next((x for x in itens if x["id"] == turno), None)
            if it and at_chave(nome) and at_chave(nome).split()[0] in at_chave(it["texto"]):
                por_fonte.append(nome)
                turnos_fonte.add(turno)
            else:
                ponto("corrigir", "Participantes", f'{nome}: o turno {turno or "(sem turno)"} não traz esse nome; '
                                                   f"presença pela fonte precisa do ID da fala em que a pessoa aparece")
        provas = falantes + notas + eventos + conf + por_fonte
        for n in nomes_ata:
            if not ac_casar(n, provas):
                ponto("corrigir", "Participantes", f"{n} está em Participantes sem prova de presença (não falou, não "
                                                   f"está como presente no material e não foi confirmado): tire")
        for f in at_falantes_pessoas(leitura):
            if not ac_casar(f["nome"], nomes_ata):
                ponto("corrigir", "Participantes", f'{f["nome"]} falou ({f["falas"]} falas, {f["ids"][0]}) e não está '
                                                   f"em Participantes: inclua")
        for p in leitura.get("presentes", []):
            if not ac_casar(p["nome"], nomes_ata):
                ponto("corrigir", "Participantes", f'{p["nome"]} consta como presente em {p["arquivo"]} e não está '
                                                   f"em Participantes: inclua")
        for f in leitura["falantes"]:
            if f["marca"] in ("sala", "não identificado") and not turnos_fonte & set(f["ids"]):
                ponto("perguntar", "Participantes", f'{f["nome"]} ({f["marca"]}) tem {f["falas"]} falas '
                                                    f'({", ".join(f["ids"][:3])}): se alguém se identifica na fala, '
                                                    f"passe em presentes com o turno; senão, pergunte quem era")
        faltam = [c["nome"] for c in leitura.get("convidados", []) if not ac_casar(c["nome"], provas)]
        faltam += [a["nome"] for a in leitura.get("ausentes", []) if not ac_casar(a["nome"], provas)
                   and a["nome"] not in faltam]
        if faltam:
            ponto("perguntar", "Participantes", "convidados sem fala nem confirmação: " + ", ".join(faltam)
                  + ". Ficam fora da ata; pergunte só se algum esteve presente sem falar")

    # Próximos passos
    pp = sec.get("proximos passos")
    if pp:
        tabs = ac_tabelas(pp["linhas"])
        if not tabs:
            ponto("corrigir", "Próximos passos", "Próximos Passos deve ser uma tabela Ação | Responsável (| Prazo)")
        for cab, linhas_t in tabs:
            c_acao = next((c for c in cab if c.startswith("acao")), None)
            c_resp = next((c for c in cab if c.startswith("responsave")), None)
            c_prazo = next((c for c in cab if c.startswith("prazo")), None)
            if not c_acao or not c_resp:
                ponto("corrigir", "Próximos passos", "a tabela precisa das colunas Ação e Responsável")
                continue
            if c_prazo and linhas_t and all(AC_SEM_DONO.match(at_sem_acento(l.get(c_prazo, "") or "-").strip())
                                            for l in linhas_t):
                ponto("corrigir", "Próximos passos", "coluna Prazo sem nenhum prazo comprovado: tire a coluna")
            for l in linhas_t:
                acao = re.sub(r"[*_`]", "", l.get(c_acao, "")).strip()
                resp = re.sub(r"[*_`]", "", l.get(c_resp, "")).strip()
                if not acao:
                    continue
                if not resp or AC_SEM_DONO.match(at_sem_acento(resp).strip()):
                    ponto("perguntar", "Próximos passos", f'"{acao[:70]}" sem responsável: mantenha só se for '
                                                          f'indispensável ("não informado") e pergunte quem assume')
                    continue
                if sem_fonte:
                    continue
                for r in [x.strip() for x in re.split(r",|;|/|\s+e\s+", resp) if x.strip()]:
                    if r.startswith("@"):
                        continue
                    if ac_casar(r, nomes_ata):
                        continue
                    primeiro = at_chave(r).split()[0] if at_chave(r) else ""
                    if primeiro and re.search(rf"\b{re.escape(primeiro)}\b", fonte_txt):
                        ponto("perguntar", "Próximos passos", f'{r} é responsável por "{acao[:60]}" e não está em '
                                                              f"Participantes: confirme que a ação foi atribuída a ele(a) "
                                                              f"na reunião")
                    else:
                        ponto("corrigir", "Próximos passos", f'responsável "{r}" não aparece na fonte: tire, ou '
                                                             f"confirme com o usuário")

    # Status de homologação
    if tipo_k == "homologacao" and not sem_fonte:
        for m in sorted(set(AC_STATUS_HOMOLOG.findall(at_sem_acento(corpo)))):
            raiz = m[:5]
            if raiz not in fonte_txt:
                ponto("corrigir", "Status", f'"{m}" na ata, mas ninguém declarou isso na fonte: use só o status '
                                            f"declarado")

    # Números e datas
    if not sem_fonte:
        data_reuniao = leitura.get("data")
        ignorar = set()
        if data_reuniao:
            d = _dt.date.fromisoformat(data_reuniao)
            ignorar.add(("data", (d.day, d.month)))
        texto_ata = "\n".join(l for s in secoes if s["chave"] != "participantes" for l in s["linhas"])
        valores_fonte = {}
        por_item = []
        for it in itens:
            vs = ac_valores(it["texto"])
            por_item.append(vs)
            for tp, v, _ in vs:
                valores_fonte.setdefault((tp, v), []).append(it["id"])
        for tp, v, _ in ac_valores(extras or ""):
            valores_fonte.setdefault((tp, v), []).append("usuário")
        relativas = ac_datas_relativas(itens, data_reuniao)
        vistos = set()
        idx = {it["id"]: i for i, it in enumerate(itens)}
        for tp, v, bruto in ac_valores(texto_ata):
            if (tp, v) in vistos or (tp, v) in ignorar:
                continue
            vistos.add((tp, v))
            if tp == "data":
                if (tp, v) in valores_fonte:
                    continue
                if v in relativas:
                    palavra, onde = relativas[v][0]
                    palavra = {"amanha": "amanhã", "terca": "terça", "terca-feira": "terça-feira",
                               "sabado": "sábado"}.get(palavra, palavra)
                    ponto("perguntar", "Números e datas", f'{bruto} = "{palavra}" em {onde}, convertido pela data da '
                                                          f'reunião ({data_reuniao[8:10]}/{data_reuniao[5:7]}): '
                                                          f"mostre a conversão na conferência")
                else:
                    ponto("corrigir", "Números e datas", f"{bruto} não aparece na fonte: tire, ou confirme com o "
                                                         f"usuário (se veio dele, passe em extras)")
                continue
            onde = valores_fonte.get((tp, v))
            if not onde:
                ponto("corrigir", "Números e datas", f'"{bruto}" não aparece na fonte: tire, ou confirme com o '
                                                     f"usuário (se veio dele, passe em extras)")
                continue
            for oid in onde:
                if oid not in idx:
                    continue
                i = idx[oid]
                for j in range(i + 1, min(i + 4, len(itens))):
                    if itens[j]["arquivo"] != itens[i]["arquivo"]:
                        break
                    tj = at_sem_acento(itens[j]["texto"])
                    outros = [(t2, v2, b2) for t2, v2, b2 in por_item[j] if t2 == tp and v2 != v]
                    if AC_CORRECAO.search(tj) and outros:
                        ponto("corrigir", "Números e datas", f'"{bruto}" aparece em {oid}, mas {itens[j]["id"]} '
                                                             f'corrige para "{outros[0][2]}": use o valor corrigido')
                        break

    palavras = len(re.findall(r"\w+", corpo))
    if palavras > 1100:
        ponto("saber", "Formato", f"ata com {palavras} palavras: veja se há temas sobrepostos para juntar ou laterais "
                                  f"para omitir")
    return pontos
