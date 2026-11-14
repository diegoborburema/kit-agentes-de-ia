# ---------------------------------------------------------------- leitura da reunião do Redator de Atas
# Lê transcrições do Teams (.docx e .vtt), texto colado ou notas (.txt e .md) e materiais de apoio (.docx e .pptx),
# só com a biblioteca padrão. Devolve os itens numerados (T001… falas, N001… linhas de notas, A001… apoio), os
# falantes com o nome em ordem natural e as marcas (externo, sala, não identificado), as listas de presentes e de
# convidados escritas nas notas, os eventos de transcrição e os blocos de leitura. O agente lê todos os blocos antes
# de escrever a ata.
import datetime as _dt
import html
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

AT_BLOCO = 8000  # caracteres por bloco de leitura; uma fala nunca é cortada

AT_MESES = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
            "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12, "january": 1, "february": 2, "march": 3,
            "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
            "december": 12}

AT_EXTERNO = re.compile(r"\s*\((?:convidad[oa]|guest|extern[oa]|external|visitante|unverified)\)", re.I)
AT_SALA = re.compile(r"\b(sala|room|audit[óo]rio|mtr|meeting room|teams room)\b", re.I)
AT_ANONIMO = re.compile(r"^(speaker|falante|participante|orador|locutor|unknown|desconhecido|usu[áa]rio|"
                        r"unidentified|n[ãa]o identificado)(\s*\d+)?$", re.I)
AT_LOCAL = re.compile(r"\s*\((?:[A-Z]{2}-[^)]*|[^)]*\b(?:BR|Brasil|Brazil|LATAM)\b[^)]*)\)\s*$")
AT_EVENTO = re.compile(r"^(?P<nome>.+?)\s+(?P<ev>iniciou a transcri\w+|parou a transcri\w+|interrompeu a transcri\w+|"
                       r"started transcription|stopped transcription|iniciou a grava\w+|started recording|"
                       r"stopped recording|parou a grava\w+)\.?\s*$", re.I)
AT_RUIDO = re.compile(r"^(transcri[çc][ãa]o|transcript|webvtt|note:?|kind:.*|language:.*|"
                      r"transcri[çc][ãa]o (iniciada|interrompida|encerrada)|grava[çc][ãa]o (iniciada|encerrada)|"
                      r"transcription (started|stopped))$", re.I)
AT_LISTA = re.compile(r"^\s*[-*•]?\s*(?:\*\*)?(?P<rot>presentes|participantes|participaram|presen[çc]a|attendees|"
                      r"convidados|convite|lista de convidados|invited|invitees|ausentes|ausências)(?:\*\*)?\s*:\s*"
                      r"(?:\*\*)?\s*(?P<lista>.+)$", re.I)

# Linhas de transcrição
AT_RE_SETA = re.compile(r"^\s*(\d{1,2}:\d{1,2}:\d{1,2}(?:[.,]\d+)?|\d{1,2}:\d{2}(?:[.,]\d+)?)\s*-->\s*"
                        r"(\d{1,2}:\d{1,2}:\d{1,2}(?:[.,]\d+)?|\d{1,2}:\d{2}(?:[.,]\d+)?)")
AT_RE_CAB = re.compile(r"^(?P<nome>[^\d\n:][^\n]{0,70}?)(?:\s{2,}|\t+)(?P<t>\d{1,2}:\d{2}(?::\d{2})?)\s*$")
AT_RE_COLCHETE = re.compile(r"^\s*\[(?P<t>\d{1,2}:\d{2}(?::\d{2})?)\]\s*(?P<nome>[^:\n]{2,70}?)\s*:\s*(?P<txt>.*)$")
AT_RE_HORA_NOME = re.compile(r"^\s*(?P<t>\d{1,2}:\d{2}(?::\d{2})?)\s+(?P<nome>[^:\n\d][^:\n]{1,69}?)\s*:\s*(?P<txt>.*)$")
AT_RE_NOME_HORA = re.compile(r"^\s*(?P<nome>[^:\n\d\[(][^:\n\[(]{1,69}?)\s*[\[(](?P<t>\d{1,2}:\d{2}(?::\d{2})?)[\])]\s*:?"
                             r"\s*(?P<txt>.*)$")
AT_RE_NOME_TXT = re.compile(r"^\s*(?P<nome>[A-ZÀ-Ý@][\w'.-]+(?:,?\s[A-ZÀ-Ý@][\w'.-]+){0,4})\s*:\s*(?P<txt>\S.*)$")


def at_sem_acento(texto):
    return unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode().lower()


def at_chave(nome):
    """Chave de comparação de nomes: minúsculas, sem acento, só letras e números."""
    return " ".join(re.sub(r"[^a-z0-9]+", " ", at_sem_acento(nome)).split())


def at_nome(bruto):
    """(nome em ordem natural, marca). Marca: '' · 'externo' · 'sala' · 'não identificado'.

    "Andrade,Lucas,BR-São Paulo" → Lucas Andrade · "Souza, Ana (BR-São Paulo)" → Ana Souza ·
    "Paula Reis (Convidado)" → Paula Reis, externo."""
    s = html.unescape(re.sub(r"<[^>]+>", "", bruto or "")).strip().strip(":").strip()
    marca = ""
    if AT_EXTERNO.search(s):
        marca = "externo"
        s = AT_EXTERNO.sub("", s).strip()
    s = AT_LOCAL.sub("", s).strip()
    s = re.sub(r"\s*[|]\s*[A-Z]{2}-[^|]+$", "", s).strip()
    partes = [p.strip() for p in s.split(",")]
    if len(partes) >= 2 and partes[0] and partes[1] and (
            len(partes) == 2 or re.match(r"^[A-Z]{2}(-|$)", partes[2]) or partes[2].upper() == partes[2]):
        s = f"{partes[1]} {partes[0]}"
    tokens = []
    for tk in s.split():
        tokens.append(tk.title() if tk.isalpha() and tk.isupper() and len(tk) > 3 else tk)
    s = " ".join(tokens)
    if AT_ANONIMO.match(s):
        marca = "não identificado"
    elif AT_SALA.search(s):
        marca = "sala"
    return s, marca


def at_seg(texto):
    """'1:02:03', '02:03' ou '0:0:5.320' → segundos."""
    if not texto:
        return None
    p = texto.replace(",", ".").split(":")
    try:
        p = [float(x) for x in p]
    except ValueError:
        return None
    while len(p) < 3:
        p.insert(0, 0.0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def at_hms(seg):
    if seg is None:
        return ""
    seg = int(seg)
    return f"{seg // 3600:02d}:{seg % 3600 // 60:02d}:{seg % 60:02d}"


def at_ler_texto(caminho):
    dados = open(caminho, "rb").read()
    for cod in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            texto = dados.decode(cod)
            if cod == "utf-16" and "\x00" in texto:
                continue
            return texto
        except UnicodeError:
            continue
    return dados.decode("utf-8", "ignore")


def at_docx_paragrafos(caminho):
    """Parágrafos de um .docx (texto das tabelas incluído), sem bibliotecas externas."""
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(caminho) as z:
        raiz = ET.fromstring(z.read("word/document.xml"))
    saida = []
    for p in raiz.iter(ns + "p"):
        partes = []
        for el in p.iter():
            if el.tag == ns + "t":
                partes.append(el.text or "")
            elif el.tag == ns + "tab":
                partes.append("\t")
            elif el.tag in (ns + "br", ns + "cr"):
                partes.append("\n")
        saida.extend("".join(partes).split("\n"))
    return saida


def at_pptx_textos(caminho):
    """Textos de um .pptx, um item por parágrafo, com o número do slide."""
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    saida = []
    with zipfile.ZipFile(caminho) as z:
        slides = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                        key=lambda n: int(re.findall(r"\d+", n)[-1]))
        for i, nome in enumerate(slides, 1):
            raiz = ET.fromstring(z.read(nome))
            for p in raiz.iter(ns + "p"):
                t = "".join(r.text or "" for r in p.iter(ns + "t")).strip()
                if t:
                    saida.append(f"Slide {i}: {t}")
    return saida


def at_limpar(texto, colapsar=True):
    """Tira HTML, entidades e marcas automáticas ([Event], referências truncadas). Devolve (texto, nº de remoções).
    Com colapsar=False, mantém os espaços repetidos (o .docx do Teams separa nome e hora com vários espaços)."""
    n = 0
    t = texto
    t, k = re.subn(r"</?[a-zA-Z][^>]*>", "", t)
    n += k
    t = html.unescape(t)
    t, k = re.subn(r"\[(?:Event|Evento)\]\s*", "", t, flags=re.I)
    n += k
    t, k = re.subn(r"【[^】]*】|†\S*|\bturn\d+\w*\b", "", t)
    n += k
    t = t.replace("\u00a0", " ")
    return (re.sub(r"[ \t]+", " ", t) if colapsar else t).strip(), n


def at_data_de(texto):
    """Primeira data reconhecível num texto (título, cabeçalho ou nome do arquivo), em ISO."""
    if not texto:
        return None
    m = re.search(r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})", texto)
    if m:
        try:
            return _dt.date(int(m[1]), int(m[2]), int(m[3])).isoformat()
        except ValueError:
            pass
    m = re.search(r"(\d{1,2}) de ([A-Za-zçÇ]+) de (\d{4})", texto)
    if m and at_sem_acento(m[2]) in AT_MESES:
        return _dt.date(int(m[3]), AT_MESES[at_sem_acento(m[2])], int(m[1])).isoformat()
    m = re.search(r"([A-Za-z]+) (\d{1,2}), (\d{4})", texto)
    if m and m[1].lower() in AT_MESES:
        return _dt.date(int(m[3]), AT_MESES[m[1].lower()], int(m[2])).isoformat()
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b", texto)
    if m:
        try:
            return _dt.date(int(m[3]), int(m[2]), int(m[1])).isoformat()
        except ValueError:
            pass
    return None


def at_titulo_limpo(titulo):
    t = re.sub(r"[-_ ]*20\d{6}_\d{4,6}[-_ ]*", " ", titulo or "")
    t = re.sub(r"[-–| ]*(Grava[çc][ãa]o de Reuni[ãa]o|Meeting Recording|Meeting Transcript|Transcri[çc][ãa]o( da reuni[ãa]o)?)"
               r"\s*$", "", t, flags=re.I)
    return re.sub(r"\s+", " ", t).strip(" -–|")


def at_parece_nome(nome):
    n = nome.strip()
    if not n or len(n) > 70 or re.search(r"\d{2,}", n) and not AT_SALA.search(n):
        return False
    if len(n.replace(",", " ").split()) > 7:
        return False
    if at_sem_acento(n.split()[0].strip(",")) in ("obs", "nota", "notas", "contexto", "pauta", "objetivo",
                                                   "agenda", "assunto", "data", "local", "link", "tema", "proximos",
                                                   "decisao", "decisoes", "duvida", "duvidas", "acao", "acoes"):
        return False
    return True


def at_cabecalho(linhas):
    """Título, data e duração no topo de uma transcrição exportada do Teams (antes da primeira fala)."""
    info = {"titulo": None, "data": None, "duracao": None}
    for ln in [l.strip() for l in linhas if l.strip()][:6]:
        s, _ = at_limpar(ln, colapsar=False)
        if AT_RE_CAB.match(s) or AT_EVENTO.match(s) or AT_RE_SETA.match(s):
            break
        if re.fullmatch(r"(\d+\s*h\s*)?(\d+\s*m(in)?\s*)?(\d+\s*s)?", s) and re.search(r"\d", s):
            info["duracao"] = re.sub(r"\s+", " ", s)
        elif info["titulo"] is None:
            s = re.sub(r"\s+", " ", s)
            info["titulo"] = at_titulo_limpo(s)
            info["data"] = at_data_de(s)
        elif at_data_de(s) and len(s) < 60:
            info["data"] = at_data_de(s)
    return info


def at_falas_de_linhas(linhas):
    """Reconhece o formato e devolve (formato, falas, eventos, removidos). Cada fala: falante bruto, hora e texto."""
    eventos, removidos = [], 0
    limpas = []
    for ln in linhas:
        ln = re.sub(r"^\s*<v\s+([^>]+)>", "\x01\\1\x02", ln).replace("</v>", "")
        s, k = at_limpar(ln, colapsar=False)
        removidos += k
        if not s:
            limpas.append("")
            continue
        m = AT_EVENTO.match(s)
        if m and at_parece_nome(m["nome"]):
            eventos.append({"bruto": m["nome"], "evento": m["ev"]})
            continue
        if AT_RUIDO.match(s):
            continue
        limpas.append(s)

    contagem = {
        "seta": sum(1 for s in limpas if AT_RE_SETA.match(s)),
        "cabecalho": sum(1 for s in limpas if AT_RE_CAB.match(s) and at_parece_nome(AT_RE_CAB.match(s)["nome"])),
        "colchete": sum(1 for s in limpas if AT_RE_COLCHETE.match(s)),
        "hora_nome": sum(1 for s in limpas if AT_RE_HORA_NOME.match(s)),
        "nome_hora": sum(1 for s in limpas if AT_RE_NOME_HORA.match(s)),
        "nome_texto": sum(1 for s in limpas if AT_RE_NOME_TXT.match(s) and at_parece_nome(AT_RE_NOME_TXT.match(s)["nome"])),
    }
    formato = max(contagem, key=contagem.get)
    if contagem[formato] < 3:
        return "notas", [], eventos, removidos

    falas = []
    atual = None

    def fechar():
        nonlocal atual
        if atual and atual["texto"].strip():
            falas.append(atual)
        atual = None

    if formato == "seta":
        i = 0
        while i < len(limpas):
            m = AT_RE_SETA.match(limpas[i])
            if not m:
                i += 1
                continue
            j = i + 1
            corpo = []
            while j < len(limpas) and not AT_RE_SETA.match(limpas[j]):
                prox = next((x for x in limpas[j + 1:] if x), "")
                id_deixa = re.fullmatch(r"[\w\-/.]+", limpas[j] or " ") and AT_RE_SETA.match(prox)
                if limpas[j] and not id_deixa:
                    corpo.append(limpas[j])
                j += 1
            nome, texto = "", ""
            if corpo:
                v = re.match(r"^\x01([^\x02]+)\x02(.*)$", corpo[0])
                if v:
                    nome, texto = v[1], " ".join([v[2]] + corpo[1:])
                elif len(corpo) >= 2 and at_parece_nome(corpo[0]) and not corpo[0].endswith((".", "?", "!")):
                    nome, texto = corpo[0], " ".join(corpo[1:])
                else:
                    mm = AT_RE_NOME_TXT.match(corpo[0])
                    if mm and at_parece_nome(mm["nome"]):
                        nome, texto = mm["nome"], " ".join([mm["txt"]] + corpo[1:])
                    else:
                        texto = " ".join(corpo)
            texto = texto.strip()
            if atual and atual["bruto"] == nome and nome:
                atual["texto"] += " " + texto
            else:
                fechar()
                atual = {"bruto": nome, "t": at_seg(m[1]), "texto": texto}
            i = j
        fechar()
    elif formato == "cabecalho":
        for s in limpas:
            m = AT_RE_CAB.match(s)
            if m and at_parece_nome(m["nome"]):
                fechar()
                atual = {"bruto": m["nome"].strip(), "t": at_seg(m["t"]), "texto": ""}
            elif atual is not None and s:
                atual["texto"] = (atual["texto"] + " " + s).strip()
        fechar()
    else:
        padrao = {"colchete": AT_RE_COLCHETE, "hora_nome": AT_RE_HORA_NOME, "nome_hora": AT_RE_NOME_HORA,
                  "nome_texto": AT_RE_NOME_TXT}[formato]
        for s in limpas:
            m = padrao.match(s)
            if m and at_parece_nome(m["nome"]):
                fechar()
                atual = {"bruto": m["nome"].strip(), "t": at_seg(m.groupdict().get("t")), "texto": m["txt"].strip()}
            elif atual is not None and s:
                atual["texto"] = (atual["texto"] + " " + s).strip()
        fechar()
    for f in falas:
        f["texto"] = re.sub(r"\s+", " ", f["texto"]).strip()
        f["bruto"] = re.sub(r"\s+", " ", f["bruto"]).strip()
    return formato, falas, eventos, removidos


def at_lista_nomes(texto):
    """'Ana Souza (Dados), Bruno Prado e Renata Okada (Trade)' → [(nome, área ou None)]."""
    saida = []
    for parte in re.split(r"\s*[;,]\s*|\s+e\s+", texto.strip().rstrip(".")):
        parte = parte.strip(" -*")
        if not parte:
            continue
        area = None
        m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", parte)
        if m and not AT_EXTERNO.search(parte) and not AT_LOCAL.search(parte):
            parte, area = m[1].strip(), m[2].strip()
        m = re.match(r"^(.+?)\s+[–—-]\s+(.+)$", parte)
        if m and area is None:
            parte, area = m[1].strip(), m[2].strip()
        nome, marca = at_nome(parte)
        if nome:
            saida.append({"nome": nome, "area": area, "marca": marca})
    return saida


def at_ler_arquivo(caminho):
    """Lê um anexo. Devolve dict com tipo (transcrição, notas ou apoio), formato, cabeçalho, falas, linhas e listas."""
    nome = os.path.basename(caminho)
    ext = os.path.splitext(nome)[1].lower()
    info = {"arquivo": nome, "tipo": None, "formato": None, "titulo": None, "data": None, "duracao": None,
            "falas": [], "linhas": [], "eventos": [], "presentes": [], "convidados": [], "ausentes": [],
            "removidos": 0, "avisos": []}
    if ext == ".pptx":
        info.update(tipo="apoio", formato="pptx", linhas=at_pptx_textos(caminho))
        return info
    if ext == ".docx":
        linhas = at_docx_paragrafos(caminho)
        formato_arq = "docx"
    elif ext in (".vtt", ".txt", ".md", ".srt", ".csv", ".text", ""):
        linhas = at_ler_texto(caminho).splitlines()
        formato_arq = ext.lstrip(".") or "texto"
    else:
        raise ValueError(f'"{nome}": formato {ext} não suportado. Peça a transcrição em .docx ou .vtt, ou notas em .txt')
    formato, falas, eventos, removidos = at_falas_de_linhas(linhas)
    cab = at_cabecalho(linhas) if formato_arq == "docx" else {"titulo": None, "data": None, "duracao": None}
    info.update(cab)
    info["data"] = info["data"] or at_data_de(nome)
    if not info["titulo"]:
        base = re.sub(r"[-_ ]*20\d{2}[-_.]?\d{2}[-_.]?\d{2}.*$", "", os.path.splitext(nome)[0]).strip(" -_")
        info["titulo"] = (base + " (nome do arquivo)") if base else None
    info["removidos"] = removidos
    info["eventos"] = eventos
    for ln in linhas:
        s, _ = at_limpar(ln)
        m = AT_LISTA.match(s)
        if m:
            rot = at_sem_acento(m["rot"])
            destino = ("convidados" if rot.startswith(("convid", "convite", "lista", "invit")) else
                       "ausentes" if rot.startswith("ausen") else "presentes")
            info[destino].extend(at_lista_nomes(m["lista"]))
    if formato == "notas":
        info.update(tipo="notas", formato=formato_arq)
        for ln in linhas:
            s, k = at_limpar(ln)
            info["removidos"] += k
            if s and not AT_RUIDO.match(s):
                info["linhas"].append(s)
        if ext == ".docx" and not info["presentes"] and not info["convidados"]:
            info["tipo"] = "apoio"
        return info
    info.update(tipo="transcrição", formato={"seta": "vtt" if ext == ".vtt" else "docx (blocos com seta)",
                                               "cabecalho": "docx do Teams", "colchete": "texto [hh:mm]",
                                               "hora_nome": "texto hh:mm nome", "nome_hora": "texto nome (hh:mm)",
                                               "nome_texto": "texto nome: fala"}[formato])
    info["falas"] = falas
    if not any(f.get("t") is not None for f in falas):
        info["avisos"].append("transcrição sem hora nas falas")
    if not info["duracao"] and falas and falas[-1].get("t") is not None:
        info["duracao"] = at_hms(falas[-1]["t"]) + " (até a última fala)"
    return info


def at_ler(caminhos, convidados=None, tamanho=AT_BLOCO):
    """Lê todos os anexos e monta a leitura: itens numerados, falantes, listas, eventos e blocos."""
    leitura = {"arquivos": [], "itens": [], "falantes": [], "presentes": [], "convidados": [], "ausentes": [],
               "eventos": [], "blocos": [], "titulo": None, "data": None, "duracao": None}
    cont = {"T": 0, "N": 0, "A": 0}
    por_nome = {}
    for c in caminhos:
        a = at_ler_arquivo(c)
        resumo = {k: a[k] for k in ("arquivo", "tipo", "formato", "titulo", "data", "duracao", "removidos", "avisos")}
        resumo["falas"] = len(a["falas"])
        resumo["linhas"] = len(a["linhas"])
        leitura["arquivos"].append(resumo)
        if a["tipo"] in ("transcrição", "notas"):
            for k in ("titulo", "data", "duracao"):
                leitura[k] = leitura[k] or a[k]
        for f in a["falas"]:
            nome, marca = at_nome(f["bruto"]) if f["bruto"] else ("[falante não identificado]", "não identificado")
            cont["T"] += 1
            item = {"id": f"T{cont['T']:03d}", "arquivo": a["arquivo"], "hora": at_hms(f.get("t")),
                    "falante": nome, "marca": marca, "texto": f["texto"]}
            leitura["itens"].append(item)
            reg = por_nome.setdefault(at_chave(nome), {"nome": nome, "brutos": [], "marca": marca, "falas": 0,
                                                       "palavras": 0, "primeira": None, "ultima": None, "ids": []})
            if f["bruto"] and f["bruto"] not in reg["brutos"]:
                reg["brutos"].append(f["bruto"])
            reg["falas"] += 1
            reg["palavras"] += len(f["texto"].split())
            reg["primeira"] = reg["primeira"] or item["hora"]
            reg["ultima"] = item["hora"] or reg["ultima"]
            reg["ids"].append(item["id"])
        prefixo = "A" if a["tipo"] == "apoio" else "N"
        for ln in a["linhas"]:
            cont[prefixo] += 1
            leitura["itens"].append({"id": f"{prefixo}{cont[prefixo]:03d}", "arquivo": a["arquivo"], "hora": "",
                                     "falante": "", "marca": "", "texto": ln})
        for ev in a["eventos"]:
            nome, _ = at_nome(ev["bruto"])
            leitura["eventos"].append({"nome": nome, "evento": ev["evento"], "arquivo": a["arquivo"]})
        for k in ("presentes", "convidados", "ausentes"):
            for p in a[k]:
                p = dict(p, arquivo=a["arquivo"])
                if at_chave(p["nome"]) not in {at_chave(x["nome"]) for x in leitura[k]}:
                    leitura[k].append(p)
    for nome in convidados or []:
        n, marca = at_nome(nome)
        if at_chave(n) not in {at_chave(x["nome"]) for x in leitura["convidados"]}:
            leitura["convidados"].append({"nome": n, "area": None, "marca": marca, "arquivo": "pedido"})
    leitura["falantes"] = sorted(por_nome.values(), key=lambda r: r["ids"][0])
    leitura["blocos"] = at_blocos(leitura["itens"], tamanho)
    return leitura


def at_linha_item(it):
    hora = f" {it['hora']}" if it.get("hora") else ""
    quem = f" {it['falante']}:" if it.get("falante") else ""
    return f"{it['id']}{hora}{quem} {it['texto']}"


def at_blocos(itens, tamanho=AT_BLOCO):
    blocos, atual, chars = [], [], 0
    for i, it in enumerate(itens):
        n = len(at_linha_item(it)) + 1
        if atual and chars + n > tamanho:
            blocos.append(atual)
            atual, chars = [], 0
        atual.append(i)
        chars += n
    if atual:
        blocos.append(atual)
    saida = []
    for k, idx in enumerate(blocos, 1):
        prim, ult = itens[idx[0]], itens[idx[-1]]
        horas = [itens[i]["hora"] for i in idx if itens[i]["hora"]]
        saida.append({"n": k, "de": prim["id"], "ate": ult["id"], "indices": idx,
                      "inicio": horas[0] if horas else "", "fim": horas[-1] if horas else ""})
    return saida


def at_falantes_pessoas(leitura):
    """Falantes que provam presença de uma pessoa (sem sala e sem não identificado)."""
    return [f for f in leitura["falantes"] if f["marca"] in ("", "externo")]


def at_buscar(leitura, termos, falante=None, todos=False, limite=12):
    """Itens que contêm os termos (sem acento e sem maiúsculas), com o vizinho anterior e o seguinte."""
    chaves = [at_sem_acento(t) for t in termos if t and t.strip()]
    itens = leitura["itens"]
    acertos = []
    for i, it in enumerate(itens):
        if falante and at_chave(falante) not in at_chave(it.get("falante", "")):
            continue
        texto = at_sem_acento(it["texto"] + " " + it.get("falante", ""))
        n = sum(1 for c in chaves if c in texto)
        if n and (not todos or n == len(chaves)):
            acertos.append((n, i))
    acertos.sort(key=lambda x: (-x[0], x[1]))
    escolhidos = sorted(i for _, i in acertos[:limite])
    mostrar = set()
    for i in escolhidos:
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(itens) and itens[j]["arquivo"] == itens[i]["arquivo"]:
                mostrar.add(j)
    return [dict(itens[j], acerto=j in escolhidos) for j in sorted(mostrar)], len(acertos)
