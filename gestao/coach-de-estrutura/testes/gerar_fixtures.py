"""Gera as fixtures do Coach de Estrutura: a análise esperada ao fim do Cenário A (13/11/2026) e as cópias dos planos de
13/11 e 04/12 do Coach de Gestão.

Uso, na raiz do repositório:
    python gestao/coach-de-estrutura/testes/gerar_fixtures.py

Usa o código de gestao/_codigo/ (o mesmo que vai na skill estrutura-pptx). O mapa do time não é fixture: ele chega
ditado na conversa (R-A1 do kit). Todos os nomes, fatos e números são fictícios.
"""
import pathlib
import shutil

RAIZ = pathlib.Path(__file__).resolve().parents[3]
SAIDA = pathlib.Path(__file__).resolve().parent / "fixtures"
ns = {}
for arq in ("pptx/ler_pauta.py", "pptx/gerar_pauta.py", "plano/plano.py", "plano/plano_pptx.py", "pessoas/ficha.py",
            "estrutura/estrutura.py", "estrutura/estrutura_pptx.py"):
    exec((RAIZ / "gestao/_codigo" / arq).read_text(encoding="utf-8"), ns)
g = lambda nome: ns[nome]

U = "[Usuário · 13/11]"


def M(pessoa, papel, frente, pct, autonomia, dono):
    return {"pessoa": pessoa, "papel": papel, "frente": frente, "pct": pct, "autonomia": autonomia, "dono": dono, "fonte": U}


MAPA = [M("Ana", "PO", "Tarumã", 50, "alta", True), M("Ana", "PO", "Painel Jatobá", 40, "alta", True),
        M("Ana", "PO", "Previsão de Ruptura", 20, "média", True), M("Bruno", "PO", "Quimera-7", 50, "alta", True),
        M("Bruno", "PO", "Integração Pitanga", 30, "média", True), M("Bruno", "PO", "Hub Logístico", 20, "média", False),
        M("Caio", "Analista", "Piloto do Ipê Triagem", 80, "baixa", True), M("Caio", "Analista", "Sustentação", 20, "média", True)]

ESTRUTURA_1311 = {
    "data": "2026-11-13", "usuario": "Lucas",
    "gatilho": "sinal do plano (Ana em 3 frentes, K5); Buriti 🔴; piloto da Triagem com o Caio",
    "plano": {"arquivo": "Plano 30-60-90 2026-11-13.pptx", "data": "2026-11-13"},
    "mapa": MAPA, "vagas": ["Analista Pleno", "Engenheiro de Dados"], "restricoes": [],
    "pontos_unicos": ["Tarumã e Painel Jatobá dependem só da Ana"],
    "diagnostico": [
        {"prioridade": "Tarumã", "risco": "Buriti 🔴", "causa": "foco", "secundaria": "capacidade",
         "evidencia": f"Ana em 3 frentes, 110% {U}; DL1, Buriti replanejado para 18/12 [Plano · 13/11]"},
        {"prioridade": "P2 Ipê-Roxo", "risco": "piloto da Triagem", "causa": "autonomia", "secundaria": "",
         "evidencia": f"Caio dono do piloto com autonomia baixa e sem apoio {U}"},
    ],
    "achados": ["Hub Logístico sem dono (o Bruno só apoia)", "Tarumã e Painel Jatobá dependem só da Ana"],
    "decisao": {"texto": "Pausar a Previsão de Ruptura até 18/12 e o Lucas apoiar o Caio no piloto por 4 semanas, 2 h por semana",
                "testes": [
                    {"id": "T1", "movimento": "Pausar a Previsão de Ruptura até 18/12", "nivel": 3,
                     "criterio": "Testes do Buriti concluídos até 11/12, para entrega em 18/12", "kpi": "DL1",
                     "inicio": "2026-11-16", "revisao": "2026-12-11"},
                    {"id": "T2", "movimento": "Apoio do Lucas ao Caio no piloto, 2 h por semana", "nivel": 4,
                     "ate": "2026-12-11", "escopo": "condução do piloto da Triagem", "saida": "piloto iniciado em 2 lojas",
                     "criterio": "Piloto da Triagem iniciado em 2 lojas até 11/12 (S4 do P2)", "kpi": "P2 S4",
                     "inicio": "2026-11-16", "revisao": "2026-12-11"}]},
    "transicao": ["S1 (16–20/11): conversa com a Ana sobre a pausa; conversa com o Caio sobre o apoio; Previsão de Ruptura pausada",
                  "S2 (23–27/11): primeira checagem do Buriti com a Ana; 2 h com o Caio no piloto",
                  "S3 (30/11–04/12): checagem dos testes do Buriti; 2 h com o Caio; lojas do piloto escolhidas",
                  "S4 (07–11/12): critérios de T1 e T2; revisão em 11/12"],
    "historico": [{"data": "2026-11-13", "registro": "Análise de 13/11/2026; teste de 16/11 a 11/12"}],
}

if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    for nome in ("Plano 30-60-90 2026-11-13.pptx", "Plano 30-60-90 2026-12-04.pptx"):
        shutil.copy(RAIZ / "gestao/coach-de-gestao/testes/fixtures" / nome, SAIDA / nome)
    erros = []
    assert not g("es_validar")(dict(ESTRUTURA_1311), erros) and not erros, erros
    g("gerar_estrutura")(ESTRUTURA_1311, SAIDA / "Estrutura 2026-11-13 (confidencial).pptx")
    for arq in sorted(SAIDA.iterdir()):
        print(arq.name)
