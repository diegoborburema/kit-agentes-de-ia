"""Gera as fixtures do Coach de Gestão: o alinhamento estratégico, o plano do ciclo 1 (13/11), o mesmo plano depois de
1 revisão (20/11, para o 2º escorregão) e de 3 revisões (04/12), e um plano feito à mão, sem dados. Copia o 1-1 da Ana de 09/11 e a weekly do time de 18/11 das
fixtures do Organizador de Weekly.

Uso, na raiz do repositório:
    python gestao/coach-de-gestao/testes/gerar_fixtures.py

Usa o código de gestao/_codigo/ (o mesmo que vai na skill coach-pptx): o plano de 04/12 sai de 3 revisões feitas pelo
próprio código. Todos os nomes, fatos e números são fictícios.
"""
import copy
import pathlib
import shutil

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

RAIZ = pathlib.Path(__file__).resolve().parents[3]
SAIDA = pathlib.Path(__file__).resolve().parent / "fixtures"
ns = {}
for arq in ("pptx/ler_pauta.py", "pptx/gerar_pauta.py", "plano/plano.py", "plano/plano_pptx.py"):
    exec((RAIZ / "gestao/_codigo" / arq).read_text(encoding="utf-8"), ns)
g = lambda nome: ns[nome]

ALINHAMENTO = [
    ("Núcleo de Dados · Produtos", ["Alinhamento 2027"]),
    ("Mandato", ["Levar dados confiáveis às decisões de Compras, Lojas e Logística"]),
    ("Direcionadores", ["D1. Capturar o benefício prometido: Recomendador com R$ 3 MM de out a dez/26 (R$ 1,0 MM/mês); "
                        "ainda sem conversão em out/26",
                        "D2. Produtos usados no rito do negócio: NPS 40 em 2027; 60% dos produtos usados no rito mensal",
                        "D3. Toda demanda nova com problema e métrica definidos"]),
    ("Movimentos", ["Quimera-7 (Bruno)", "Tarumã (Ana)", "Ipê-Roxo: automação de atendimento com o Ipê Triagem (Caio)",
                    "Painel Jatobá (Ana)", "Integração Pitanga (Bruno)", "Previsão de Ruptura: discovery a partir de 16/11 (Ana)",
                    "Vagas em aberto: Analista Pleno e Engenheiro de Dados (Lucas)"]),
    ("Desafios", ["O Recomendador não converte benefício", "Os dados das lojas chegam atrasados",
                  "O time está sobrecarregado, com 2 vagas abertas", "As áreas de negócio não usam os produtos no rito mensal"]),
    ("Restrições", ["Sem verba para ferramenta nova até jan/27", "Recesso de 21/12 a 01/01"]),
]

F_ALI = "[Alinhamento · slide {}]"
PLANO_1311 = {
    "usuario": "Lucas", "data": "2026-11-13",
    "retrato": {
        "mandato": [{"texto": ALINHAMENTO[1][1][0], "fonte": F_ALI.format(2)}],
        "direcionadores": [{"id": "D1", "texto": "Capturar o benefício prometido", "fonte": F_ALI.format(3)},
                           {"id": "D2", "texto": "Produtos usados no rito do negócio", "fonte": F_ALI.format(3)},
                           {"id": "D3", "texto": "Toda demanda nova com problema e métrica definidos", "fonte": F_ALI.format(3)}],
        "movimentos": [{"nome": n, "dono": d, "fonte": F_ALI.format(4)} for n, d in (
            ("Quimera-7", "Bruno"), ("Tarumã", "Ana"), ("Ipê-Roxo", "Caio"), ("Painel Jatobá", "Ana"),
            ("Integração Pitanga", "Bruno"), ("Previsão de Ruptura", "Ana"), ("Vagas em aberto", "Lucas"))],
        "desafios": [{"texto": t, "fonte": F_ALI.format(5)} for t in ALINHAMENTO[4][1]],
        "restricoes": [{"texto": t, "fonte": F_ALI.format(6)} for t in ALINHAMENTO[5][1]],
        "desafio_central": {"texto": "O Recomendador não converte benefício e o time está sem 2 pessoas",
                            "politica": "Converter o Recomendador antes de abrir frente nova e completar o time",
                            "nao_vamos": ["Abrir produto novo sem problema e métrica definidos", "Contar com ferramenta nova até jan/27"],
                            "fonte": F_ALI.format(5)},
    },
    "resultados": [
        {"id": "R1", "prioridade": "Quimera-7", "texto": "Recomendador convertendo benefício", "kpis": ["K1"], "dono": "Bruno",
         "direcionador": "D1", "data": "2027-02-05", "fonte": F_ALI.format(3), "compromisso": "comprometido",
         "ataca": "Ataca a conversão do Recomendador"},
        {"id": "R2", "prioridade": "Ipê-Roxo", "texto": "Ipê Triagem resolvendo chamados", "kpis": ["K2"], "dono": "Caio",
         "direcionador": "D1", "data": "2027-02-05", "fonte": F_ALI.format(4), "compromisso": "aspiracional"},
        {"id": "R3", "prioridade": "Vagas em aberto", "texto": "Time completo", "kpis": ["K3"], "dono": "Lucas",
         "direcionador": "D1", "data": "2027-02-05", "fonte": F_ALI.format(5), "compromisso": "comprometido",
         "ataca": "Tira a sobrecarga que trava a conversão"},
    ],
    "marcos": [
        {"id": "M1", "resultado": "R1", "texto": "Primeira conversão apurada (nov) na Base Sabiá", "data": "2026-12-18"},
        {"id": "M2", "resultado": "R1", "texto": "Plano de conversão rodando em 2 lojas", "data": "2027-01-08"},
        {"id": "M3", "resultado": "R2", "texto": "Piloto da Triagem em 2 lojas", "data": "2026-12-18"},
        {"id": "M4", "resultado": "R2", "texto": "Lojas do piloto treinadas", "data": "2027-01-08"},
        {"id": "M5", "resultado": "R3", "texto": "Analista Pleno contratado", "data": "2026-12-18"},
        {"id": "M6", "resultado": "R3", "texto": "Proposta aceita pelo Engenheiro de Dados", "data": "2027-01-08"},
    ],
    "prioridades": [
        {"id": "P1", "nome": "Quimera-7", "resultado": "R1", "dono": "Bruno", "kpis": ["K4"],
         "feito_quando": "Leitura de conversão de nov apurada", "fecha_100": True, "entregaveis": {
             "S1": "Plano de conversão acordado com Compras", "S2": "Carga do Recomendador com TI (25/11)",
             "S3": "1º relatório de recomendações aplicadas", "S4": "Leitura de conversão de nov"}},
        {"id": "P2", "nome": "Ipê-Roxo", "resultado": "R2", "dono": "Caio", "kpis": ["K6"],
         "feito_quando": "Piloto iniciado em 2 lojas", "fecha_100": True, "entregaveis": {
             "S1": "Forma de medir os chamados resolvidos definida", "S2": "2 lojas do piloto escolhidas",
             "S3": "Roteiro de treinamento", "S4": "Piloto iniciado em 2 lojas"}},
        {"id": "P3", "nome": "Vagas em aberto", "resultado": "R3", "dono": "Lucas", "kpis": ["K7"],
         "feito_quando": "Proposta feita ao Engenheiro de Dados", "fecha_100": True, "entregaveis": {
             "S1": "Decisão do Analista Pleno", "S2": "Proposta aceita pelo Analista Pleno",
             "S3": "Vaga de Engenheiro de Dados aberta", "S4": "Proposta ao Engenheiro de Dados"}},
    ],
    "kpis": [
        {"id": "K1", "tipo": "resultado", "nome": "Benefício capturado do Recomendador (R$ MM/mês)", "fonte_dado": "Analista de Benefícios",
         "baseline": "R$ 0,0 (out/26)", "metas": {"60": "R$ 0,25 MM", "90": "R$ 1,0 MM"}, "frequencia": "Mensal", "dono": "Bruno",
         "status": "vermelho", "fonte": F_ALI.format(3), "par": "K5"},
        {"id": "K2", "tipo": "resultado", "nome": "% de chamados resolvidos pela Triagem", "fonte_dado": "A definir (A2)",
         "baseline": "", "metas": {"90": "40%"}, "frequencia": "Mensal", "dono": "Caio", "status": "sem_dado",
         "par": "% de chamados reabertos depois da Triagem"},
        {"id": "K3", "tipo": "resultado", "nome": "Vagas preenchidas", "fonte_dado": "RH", "baseline": "0 de 2",
         "metas": {"90": "2 de 2"}, "frequencia": "Semanal", "dono": "Lucas", "status": "amarelo"},
        {"id": "K4", "tipo": "direcionador", "nome": "% de lojas do piloto com recomendação aplicada", "fonte_dado": "Relatório do Recomendador",
         "baseline": "", "metas": {"30": "60%"}, "frequencia": "Semanal", "dono": "Bruno", "status": "sem_dado"},
        {"id": "K6", "tipo": "direcionador", "nome": "Chamados do piloto atendidos pela Triagem por semana", "fonte_dado": "A definir (A2)",
         "baseline": "", "metas": {}, "frequencia": "Semanal", "dono": "Caio", "status": "sem_dado"},
        {"id": "K7", "tipo": "direcionador", "nome": "Candidatos na etapa final", "fonte_dado": "RH", "baseline": "2",
         "metas": {}, "frequencia": "Semanal", "dono": "Lucas", "status": "verde"},
        {"id": "K5", "tipo": "saude", "nome": "Pessoas do time em mais de 2 frentes", "fonte_dado": "Alinhamento, slide 4",
         "baseline": "1 (Ana)", "metas": {"90": "0"}, "frequencia": "Mensal", "dono": "Lucas", "status": "amarelo"},
    ],
    "agenda": {
        "atividades": [
            {"id": "A1", "liga": "P1", "texto": "Alinhar com Compras o plano de conversão do Recomendador",
             "feito_quando": "Plano aceito por e-mail", "esforco_h": 3},
            {"id": "A2", "liga": "P2", "texto": "Definir com o Caio como medir os chamados resolvidos",
             "feito_quando": "Forma de medir registrada", "esforco_h": 1, "levanta": ["K2", "K6"]},
            {"id": "A3", "liga": "P3", "texto": "Decidir o Analista Pleno entre as 2 finalistas",
             "feito_quando": "Decisão comunicada ao RH", "esforco_h": 2},
            {"id": "A4", "liga": "P3", "texto": "Escrever a descrição da vaga de Engenheiro de Dados",
             "feito_quando": "Descrição enviada ao RH", "esforco_h": 2},
            {"id": "A5", "liga": "Budget 2027", "texto": "Fechar o pedido de 2 licenças de BI",
             "feito_quando": "Pedido lançado no budget", "esforco_h": 1},
            {"id": "A6", "liga": "P2", "texto": "Revisar com o Caio o escopo do piloto", "feito_quando": "Escopo registrado",
             "esforco_h": 1},
        ],
        "delegacoes": [
            {"id": "DL1", "quem": "Ana", "frente": "Tarumã", "oque": "Buriti, replanejamento para 18/12", "checar": "2026-11-20",
             "fonte": "[1-1 Ana · 09/11]"},
            {"id": "DL2", "quem": "Bruno", "frente": "Quimera-7", "liga": "P1", "oque": "Carga do Recomendador com TI",
             "checar": "2026-11-25"},
            {"id": "DL3", "quem": "Ana", "frente": "Previsão de Ruptura", "oque": "Discovery Previsão de Ruptura, kick-off em 16/11",
             "checar": "2026-11-20", "fonte": "[1-1 Ana · 09/11]"},
        ],
        "frentes": [{"nome": "Budget 2027", "direcionador": "D1"}],
        "pedidos": [{"id": "PG1", "tipo": "Ajuda", "texto": "Patrocínio do plano de conversão do Recomendador junto à diretoria de Compras"}],
        "parar": [{"id": "PF1", "texto": "Acompanhar o Tarumã no detalhe (delegado à Ana)"}],
    },
    "riscos": [
        {"id": "RB1", "texto": "TI não fazer a carga do Recomendador em 25/11", "resultado": "R1",
         "mitigacao": "DL2: Bruno confirma a janela com TI até 20/11"},
        {"id": "RB2", "texto": "A finalista do Analista Pleno recusar a proposta", "resultado": "R3",
         "mitigacao": "A3: decidir com a 2ª finalista como reserva"},
    ],
    "fora_do_plano": [],
    "descartados": [],
}


def A(id_, liga, texto, feito, h):
    return {"id": id_, "liga": liga, "texto": texto, "feito_quando": feito, "esforco_h": h}


def ST(s, **extra):
    return dict({"status": s}, **extra)


REV_2011 = {
    "data": "2026-11-20",
    "status": {"A1": ST("feito", fonte="[E-mail · Compras · 18/11]"), "A2": ST("não feito"), "A3": ST("feito"),
               "A4": ST("não feito"), "A5": ST("parcial", nota="pedido escrito, falta lançar"),
               "A6": ST("cancelado", motivo="o escopo do piloto vai ao MOR de dezembro"),
               "DL1": ST("checar depois", para="2026-11-27", nota="Buriti 🟡", fonte="[Anotações weekly do time · 18/11]"),
               "DL2": ST("checar depois", para="2026-11-25", nota="Recomendador 🟢, carga em 25/11",
                         fonte="[Anotações weekly do time · 18/11]"),
               "DL3": ST("checar depois", para="2026-12-04", nota="discovery em andamento; use case para o MOR",
                         fonte="[Anotações weekly do time · 18/11]"),
               "PG1": ST("aberto"), "PF1": ST("mantido")},
    "atividades": [A("A2", "P2", "Definir com o Caio como medir os chamados resolvidos", "Forma de medir registrada", 1),
                   A("A4", "P3", "Escrever a descrição da vaga de Engenheiro de Dados", "Descrição enviada ao RH", 2),
                   A("A5", "Budget 2027", "Fechar o pedido de 2 licenças de BI", "Pedido lançado no budget", 1),
                   A(None, "P2", "Escolher com o Caio as 2 lojas do piloto", "Lojas registradas", 1),
                   A(None, "P3", "Fechar a proposta do Analista Pleno com o RH", "Proposta enviada", 1)],
    "fora_do_plano": [{"tema": "Hub Logístico", "volume": "1 linha na weekly do time", "fonte": "[Anotações weekly do time · 18/11]",
                       "pergunta": "incluir, delegar ou parar?"}],
    "confianca": {"R1": 5, "R2": 6, "R3": 7},
    "vitorias": ["Plano de conversão aceito por Compras", "Analista Pleno decidido"],
}
REV_2711 = {
    "data": "2026-11-27",
    "status": {"A2": ST("feito"), "A4": ST("feito"), "A5": ST("feito"), "A7": ST("feito"), "A8": ST("feito"),
               "DL1": ST("checar depois", para="2026-12-04"), "DL2": ST("concluída", nota="carga em 25/11"),
               "DL3": ST("checar depois", para="2026-12-04"), "PG1": ST("aberto"), "PF1": ST("mantido")},
    "atividades": [A(None, "P2", "Revisar o roteiro de treinamento com o Caio", "Roteiro aprovado", 2),
                   A(None, "P3", "Abrir a vaga de Engenheiro de Dados com o RH", "Vaga publicada", 1),
                   A(None, "P1", "Ler o 1º relatório de recomendações com o Bruno", "Relatório lido e comentado", 1),
                   A(None, "Budget 2027", "Fechar o budget 2027 da área", "Budget enviado ao Gustavo", 3),
                   A(None, "P1", "Validar com Compras o plano de conversão nas 2 lojas", "Lojas confirmadas", 1)],
    "kpis": {"K3": {"valor": "1 de 2", "data": "2026-11-27", "fonte": "[Usuário · 27/11]", "status": "amarelo"}},
    "mudancas": [{"op": "concluir", "id": "M5", "data": "2026-11-27", "fonte": "[Usuário · 27/11]"}],
    "descartar": [{"texto": "Comitê Araçá", "origem": "radar"}],
    "fora_do_plano": [{"tema": "Hub Logístico", "volume": "2 reuniões", "fonte": "[Reunião · Hub Logístico · 25/11]",
                       "pergunta": "incluir, delegar ou parar?"}],
    "confianca": {"R1": 5, "R2": 6, "R3": 8},
    "vitorias": ["Analista Pleno contratado"],
}
REV_0412 = {
    "data": "2026-12-04",
    "status": {"A9": ST("feito"), "A10": ST("feito"), "A11": ST("feito"), "A12": ST("feito"),
               "A13": ST("parcial", nota="1 de 2 lojas confirmada"),
               "DL1": ST("checar depois", para="2026-12-11"), "DL3": ST("checar depois", para="2026-12-11"),
               "PG1": ST("aberto"), "PF1": ST("mantido")},
    "atividades": [A("A13", "P1", "Validar com Compras o plano de conversão nas 2 lojas", "Lojas confirmadas", 1),
                   A(None, "P3", "Mandar a proposta ao Engenheiro de Dados", "Proposta enviada", 1),
                   A(None, "P2", "Acompanhar o início do piloto da Triagem", "Piloto iniciado", 2),
                   A(None, "P1", "Ler a conversão de nov com o Bruno", "Leitura registrada", 1),
                   A(None, "Budget 2027", "Revisar o budget 2027 com o Gustavo", "Budget aprovado", 1)],
    "confianca": {"R1": 6, "R2": 4, "R3": 8},
    "vitorias": ["Vaga de Engenheiro de Dados publicada"],
}


def plano_1311():
    p = copy.deepcopy(PLANO_1311)
    p["janelas"] = g("pl_janelas")(p["data"])
    p["ciclo"], p["semana"] = 1, 1
    return p


def plano_revisado(revisoes):
    p = plano_1311()
    for rev in revisoes:
        p, log, erros, avisos = g("pl_revisar")(p, rev)
        assert not erros, erros
    return p


def plano_2011():
    return plano_revisado([REV_2011])


def plano_0412():
    return plano_revisado([REV_2011, REV_2711, REV_0412])


def alinhamento():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for titulo, itens in ALINHAMENTO:
        s = prs.slides.add_slide(prs.slide_layouts[1])
        s.shapes.title.text = titulo
        corpo = s.placeholders[1].text_frame
        for i, t in enumerate(itens):
            par = corpo.paragraphs[0] if i == 0 else corpo.add_paragraph()
            par.text = t
    prs.save(SAIDA / "Alinhamento Nucleo 2027 ficticio.pptx")


SEM_DADOS = [
    ("30 dias", [("verde", "Quimera-7: plano de conversão com Compras"), ("amarelo", "Ipê-Roxo: piloto da Triagem"),
                 ("vermelho", "Vagas em aberto")]),
    ("60 dias", [("verde", "Primeira conversão apurada · 18/12"), ("amarelo", "Piloto em 2 lojas · 18/12"),
                 ("vermelho", "Analista Pleno contratado"), (None, "Proposta ao Engenheiro de Dados")]),
    ("90 dias", [(None, "Recomendador convertendo benefício"), (None, "Time completo")]),
]


def plano_sem_dados():
    cores = {"verde": "89A647", "amarelo": "FFD54F", "vermelho": "FA7676"}
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    tf = s.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.6)).text_frame
    tf.text = "Meu plano 30-60-90 (nov/26)"
    for n, (titulo, itens) in enumerate(SEM_DADOS):
        x = 0.5 + n * 4.2
        tf = s.shapes.add_textbox(Inches(x), Inches(1.2), Inches(3.8), Inches(0.5)).text_frame
        tf.text = titulo
        tf.paragraphs[0].runs[0].font.bold = True
        tf = s.shapes.add_textbox(Inches(x), Inches(1.9), Inches(3.8), Inches(4.5)).text_frame
        tf.word_wrap = True
        for i, (cor, texto) in enumerate(itens):
            par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if cor:
                r = par.add_run()
                r.text = "● "
                r.font.color.rgb = RGBColor.from_string(cores[cor])
            r = par.add_run()
            r.text = texto
            r.font.size = Pt(16)
    prs.save(SAIDA / "Plano 30-60-90 sem dados.pptx")


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    alinhamento()
    g("gerar_plano")(plano_1311(), SAIDA / "Plano 30-60-90 2026-11-13.pptx")
    g("gerar_plano")(plano_2011(), SAIDA / "Plano 30-60-90 2026-11-20.pptx")
    g("gerar_plano")(plano_0412(), SAIDA / "Plano 30-60-90 2026-12-04.pptx")
    plano_sem_dados()
    # "1-1 Ana 2026-11-09 anotada.pptx" e "Weekly time 2026-11-18 anotada.pptx" vêm prontos em fixtures/
    # (gerados pelo Organizador de Weekly, que não está na versão pública)
    for arq in sorted(SAIDA.iterdir()):
        print(arq.name)
