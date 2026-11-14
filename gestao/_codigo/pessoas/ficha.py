# ---------------------------------------------------------------- ficha da pessoa (.xlsx) e funções de texto
# Na versão pública, só as funções de texto (normalização, datas e termos sensíveis) são usadas, pelo Coach de
# Estrutura. O Coach de Pessoas, que grava a ficha, não faz parte do kit.
# Uma ficha por pessoa, com as abas Metas, Diário, Ausências, Interesses e Histórico. Datas no formato aaaa-mm-dd nos dicionários.
import datetime as _fi_dt
import re
import unicodedata

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

FI_ABAS = {
    "Metas": [("ciclo", "Ciclo", 22), ("id", "ID", 6), ("meta", "Meta", 40), ("metrica", "Métrica", 26),
              ("alvo", "Alvo", 16), ("prazo", "Prazo", 12), ("incluida", "Incluída em", 12),
              ("status", "Status factual", 14), ("status_texto", "Leitura factual", 44), ("fonte", "Fonte", 30)],
    "Diário": [("id", "ID", 6), ("data", "Data", 12), ("meta", "Meta ou tema", 14), ("situacao", "Situação", 30),
               ("comportamento", "Comportamento", 44), ("impacto", "Impacto", 32), ("tipo", "Tipo", 14),
               ("fonte", "Fonte", 26)],
    "Ausências": [("periodo", "Período", 18), ("de", "De (mês)", 10), ("ate", "Até (mês)", 10)],
    "Interesses": [("data", "Data", 12), ("interesse", "Interesse", 50), ("sigilo", "Sigilo", 8), ("fonte", "Fonte", 26)],
    "Histórico": [("data", "Data", 12), ("registro", "Registro", 70)],
}
FI_DATAS = {"prazo", "incluida", "data"}
FI_STATUS = ["atingida", "parcial", "não atingida", "sem dado", "sem critério"]
FI_TIPOS = ["resultado", "comportamento", "contexto"]
FI_MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# Termos que não entram na ficha: saúde e vida pessoal (motivo de ausência nunca é registrado)
FI_SAUDE = [r"licenca[ -]?medica", r"atestado", r"\bmedic[oa]s?\b", r"\bsaude\b", r"\bdoen",
            r"\bcirurgi", r"\binternacao", r"\binternad[oa]", r"\bhospita", r"tratamento medico", r"\bterapi",
            r"\bterapeut", r"\bpsicolog", r"\bpsiquiatr", r"\bdepress", r"\bansiedade\b", r"\bburnout\b",
            r"\bgravid", r"\bgesta[cn]", r"maternidade", r"paternidade", r"\bluto\b", r"\bfalec", r"\bdiagnost",
            r"\bremedio", r"\bmedicament", r"\bcovid", r"\bgripe\b"]
FI_PESSOAL = [r"problemas? em casa", r"problemas? pesso", r"vida pessoal", r"\bdivorci", r"\bseparacao\b",
              r"\bfamilia(r|res)?\b", r"\breligi"]


def fi_norm(texto):
    """Minúsculas, sem acentos: para comparar termos."""
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return t.lower()


def fi_sensivel(texto):
    """Termos de saúde ou de vida pessoal achados no texto (lista vazia quando não há)."""
    t = fi_norm(texto)
    return sorted({m.group(0) for p in FI_SAUDE + FI_PESSOAL for m in [re.search(p, t)] if m})


def fi_data(valor):
    """Data de uma célula ou de um texto (aaaa-mm-dd, dd/mm/aaaa, datetime) em aaaa-mm-dd; '' se vazia."""
    if valor in (None, ""):
        return ""
    if isinstance(valor, _fi_dt.datetime):
        return valor.date().isoformat()
    if isinstance(valor, _fi_dt.date):
        return valor.isoformat()
    t = str(valor).strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        return t
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", t)
    if m:
        a = int(m[3]) + (2000 if len(m[3]) == 2 else 0)
        return _fi_dt.date(a, int(m[2]), int(m[1])).isoformat()
    return t


def fi_br(iso):
    """aaaa-mm-dd → dd/mm/aaaa (o resto passa sem mudança)."""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(iso or ""))
    return f"{m[3]}/{m[2]}/{m[1]}" if m else str(iso or "")


def fi_ciclo_txt(ciclo):
    return f"{fi_br(ciclo['inicio'])}–{fi_br(ciclo['fim'])}"


def fi_ciclo_ler(texto):
    """'01/01/2026–31/12/2026' → {"inicio", "fim"}; None se não reconhecer."""
    datas = re.findall(r"\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}", str(texto or ""))
    return {"inicio": fi_data(datas[0]), "fim": fi_data(datas[1])} if len(datas) >= 2 else None


def fi_mes(valor):
    """'05/2026', '2026-05' ou 'mai/2026' → '2026-05'; '' se não reconhecer."""
    t = fi_norm(valor).strip()
    m = re.fullmatch(r"(\d{1,2})/(\d{4})", t) or None
    if m:
        return f"{m[2]}-{int(m[1]):02d}"
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", t)
    if m:
        return f"{m[1]}-{int(m[2]):02d}"
    m = re.fullmatch(r"([a-z]{3})[a-z]*/(\d{2,4})", t)
    if m and m[1] in FI_MESES:
        a = int(m[2]) + (2000 if len(m[2]) == 2 else 0)
        return f"{a}-{FI_MESES.index(m[1]) + 1:02d}"
    return ""


def fi_periodo_txt(de, ate):
    """('2026-05', '2026-06') → 'mai–jun/2026'."""
    a1, m1 = de.split("-")
    a2, m2 = ate.split("-")
    if de == ate:
        return f"{FI_MESES[int(m1) - 1]}/{a1}"
    if a1 == a2:
        return f"{FI_MESES[int(m1) - 1]}–{FI_MESES[int(m2) - 1]}/{a1}"
    return f"{FI_MESES[int(m1) - 1]}/{a1}–{FI_MESES[int(m2) - 1]}/{a2}"


def _fi_cabecalho(ws):
    """(linha do cabeçalho, {chave: coluna}) da aba, reconhecida pelos títulos das colunas."""
    titulos = {fi_norm(t): c for c, t, _ in FI_ABAS[ws.title]}
    for i in range(1, 6):
        mapa = {}
        for j, cel in enumerate(ws[i], start=1):
            chave = titulos.get(fi_norm(cel.value).strip()) if cel.value else None
            if chave:
                mapa[chave] = j
        if len(mapa) >= 2:
            return i, mapa
    return None, {}


def _fi_aba(wb, nome):
    alvo = fi_norm(nome)
    return next((ws for ws in wb.worksheets if fi_norm(ws.title) == alvo), None)


def fi_e_ficha(caminho):
    wb = openpyxl.load_workbook(caminho, read_only=True)
    return _fi_aba(wb, "Diário") is not None and _fi_aba(wb, "Metas") is not None


def ficha_ler(caminho):
    """Lê a ficha. Devolve {"pessoa", "metas", "diario", "ausencias", "interesses", "historico"}; cada item é um
    dicionário com as chaves de FI_ABAS. Datas em aaaa-mm-dd; o ciclo da meta em {"inicio", "fim"}."""
    wb = openpyxl.load_workbook(caminho, data_only=True)
    pessoa = ""
    saida = {"pessoa": "", "metas": [], "diario": [], "ausencias": [], "interesses": [], "historico": []}
    chaves = {"Metas": "metas", "Diário": "diario", "Ausências": "ausencias", "Interesses": "interesses",
              "Histórico": "historico"}
    for aba, chave in chaves.items():
        ws = _fi_aba(wb, aba)
        if ws is None:
            continue
        ws.title = aba  # o nome pode ter vindo sem acento
        linha, mapa = _fi_cabecalho(ws)
        if not linha:
            continue
        topo = str(ws.cell(1, 1).value or "")
        m = re.search(r"Ficha d[aoe]s? (.+?) ·", topo)
        pessoa = pessoa or (m[1].strip() if m else "")
        for r in ws.iter_rows(min_row=linha + 1, values_only=True):
            item = {}
            for k, j in mapa.items():
                v = r[j - 1] if j - 1 < len(r) else None
                item[k] = fi_data(v) if k in FI_DATAS else ("" if v is None else str(v).strip())
            if not any(item.values()):
                continue
            if chave == "metas":
                item["ciclo"] = fi_ciclo_ler(item.get("ciclo")) or item.get("ciclo")
            if chave == "ausencias":
                item["de"] = fi_mes(item.get("de")) or item.get("de", "")
                item["ate"] = fi_mes(item.get("ate")) or item.get("ate", "") or item["de"]
            if chave == "interesses":
                item["sigilo"] = fi_norm(item.get("sigilo")) in ("sim", "s", "x", "true", "1")
            saida[chave].append(item)
    saida["pessoa"] = pessoa
    return saida


def ficha_gravar(ficha, caminho):
    """Grava a ficha inteira em `caminho`. Cada aba leva a marca de confidencial na 1ª linha."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    chaves = {"Metas": "metas", "Diário": "diario", "Ausências": "ausencias", "Interesses": "interesses",
              "Histórico": "historico"}
    for aba, chave in chaves.items():
        ws = wb.create_sheet(aba)
        ws.cell(1, 1, f"CONFIDENCIAL · Ficha de {ficha['pessoa']} · não circule este arquivo")
        ws.cell(1, 1).font = Font(bold=True, color="B3261E")
        for j, (_, titulo, largura) in enumerate(FI_ABAS[aba], start=1):
            c = ws.cell(2, j, titulo)
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="523D6B")
            ws.column_dimensions[get_column_letter(j)].width = largura
        for i, item in enumerate(ficha.get(chave, []), start=3):
            for j, (k, _, _) in enumerate(FI_ABAS[aba], start=1):
                v = item.get(k, "")
                if k == "ciclo" and isinstance(v, dict):
                    v = fi_ciclo_txt(v)
                if k in ("de", "ate") and v:
                    v = f"{v[5:7]}/{v[:4]}"
                if k == "sigilo":
                    v = "sim" if v else "não"
                c = ws.cell(i, j)
                if k in FI_DATAS and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v or "")):
                    c.value = _fi_dt.date.fromisoformat(v)
                    c.number_format = "dd/mm/yyyy"
                else:
                    c.value = v if v != "" else None
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A3"
    wb.properties.creator = "Kit de agentes de IA"
    wb.save(caminho)
    return caminho
