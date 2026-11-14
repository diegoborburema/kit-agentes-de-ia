# Gerado por ferramentas/montar_skills.py a partir de: produto/redator-de-atas/codigo/transcricao.py produto/redator-de-atas/codigo/conferencia.py produto/redator-de-atas/codigo/cli_atas.py. Não edite aqui.

# ==== produto/redator-de-atas/codigo/transcricao.py
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

# ==== produto/redator-de-atas/codigo/conferencia.py
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

# ==== produto/redator-de-atas/codigo/cli_atas.py
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
