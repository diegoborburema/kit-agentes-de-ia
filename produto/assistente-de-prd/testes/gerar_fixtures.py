"""Gera as fixtures fictícias do Assistente de PRD: o caso Radar de Ruptura, da Rede Quaresmeira.

Uso, na raiz do repositório:
    python produto/assistente-de-prd/testes/gerar_fixtures.py

O PRD em 6 versões é gravado pelo próprio script da skill prd-docx, a partir do template: as fixtures também
testam a gravação. O que só pessoas fazem (decidir um gate, assinar) é gravado aqui à parte, direto no .docx.
Os números são conhecidos e estão na bateria (PERGUNTAS-DE-CONTROLE.md): nada aqui deve ser mudado sem mudar lá.
"""
import copy
import pathlib
import runpy

from docx import Document
from docx.shared import Pt

AQUI = pathlib.Path(__file__).resolve().parent
PACOTE = AQUI.parent / "pacote/skills/prd-docx"
FIX = AQUI / "fixtures"
S = runpy.run_path(str(PACOTE / "scripts/prd_docx.py"), run_name="fixtures")
TEMPLATE = PACOTE / "assets/template-prd.docx"


# ---------------------------------------------------------------- material de apoio (texto livre)

def doc_livre(nome, titulo, partes):
    doc = Document()
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10.5)
    doc.add_heading(titulo, level=0)
    for cab, linhas in partes:
        doc.add_heading(cab, level=1)
        for l in linhas:
            if l.startswith("- "):
                doc.add_paragraph(l[2:], style="List Bullet")
            else:
                doc.add_paragraph(l)
    doc.save(FIX / nome)


def material():
    doc_livre("discovery-radar.docx", "Discovery · Painel de ruptura (Rede Quaresmeira)", [
        ("Contexto", [
            "Precisamos de um painel de ruptura para os gerentes de loja.",
            "A Rede Quaresmeira tem 42 lojas. Toda segunda-feira, cada gerente monta a lista de itens em falta na "
            "gôndola cruzando 3 relatórios do sistema da loja.",
            "Por que agora: a rede abre 12 lojas novas em 2027, e o processo manual não acompanha."]),
        ("Entrevistas (05 e 06/10/2026)", [
            "- 38 gerentes de loja gastam cerca de 3 h por semana montando a lista de faltas.",
            "- Os 6 compradores da central recebem as listas por e-mail e pedem a reposição.",
            "- Os gerentes descobrem a falta quando o cliente reclama."]),
        ("Números", [
            "Ruptura média de 7% dos itens do sortimento (auditoria de setembro de 2026).",
            "Benefício esperado, segundo a Marta Pacheco (diretora de operações de loja): \"reduzir a ruptura pela "
            "metade\"."]),
        ("Pedidos levantados", [
            "- Alerta diário de ruptura por loja",
            "- Lista de itens priorizada pelo impacto em vendas",
            "- Aviso no celular do gerente",
            "- Histórico de 2 anos por item e loja",
            "- Exportar a lista para Excel",
            "- Previsão de ruptura com 3 dias de antecedência"]),
        ("Dados citados", [
            "- Vendas por item, loja e dia (ERP)",
            "- Estoque do sistema da loja",
            "- Cadastro de lojas",
            "- Calendário de promoções (planilha)"]),
        ("Pontos em aberto", [
            "- O estoque do sistema da loja diverge da contagem física.",
            "- A planilha de promoções não tem dono.",
            "- A rede não tem app de celular para os gerentes."]),
    ])
    doc_livre("arquitetura-radar.docx", "Arquitetura proposta · Radar de Ruptura", [
        ("Desenho", [
            "Fontes: vendas no ERP, estoque no sistema da loja e promoções em planilha.",
            "Ingestão diária às 5h no lakehouse que já existe. Uma tabela de features nova alimenta a lista e, na "
            "R3, o modelo de previsão. O alerta e a lista saem no portal de relatórios que os gerentes já usam."]),
        ("Esforço e custos", [
            "- Engenharia de dados: 2 FTE por 3 meses.",
            "- Nuvem: R$ 4 mil por mês (processamento e armazenamento).",
            "- O custo por FTE não está neste documento."]),
    ])
    doc_livre("nota-modelo-radar.docx", "Nota do modelo · Previsão de ruptura", [
        ("Alvo", ["Ruptura de um item numa loja nos próximos 3 dias."]),
        ("Base de comparação", ["A regra atual: \"estoque abaixo de 2 dias de venda\"."]),
        ("Critério para ir à produção", ["Recall de 80% com precisão de 60%, num backtest de 6 meses."]),
        ("Operação", ["Retreino mensal.", "Esforço: 1 FTE por 2 meses."]),
    ])


# ---------------------------------------------------------------- o PRD, versão a versão

V02 = {
    "painel": {"Produto": "Radar de Ruptura", "Tipo": "Produto novo", "Porte": "M",
               "Horizonte do business case": "5 anos", "Etapa atual": "02"},
    "checkpoints": {"01": {"situacao": "Cumprido", "data": "30/10/2026"}},
    "pessoas": {"Sponsor": {"Nome": "Marta Pacheco", "Área": "Operações de loja"},
                "PM": {"Nome": "Caio Rezende", "Área": "Produto de dados"}},
    "campos": {
        "01.1": {"Problema ou oportunidade": "Os gerentes não sabem a tempo quais itens vão faltar na gôndola e "
                                             "gastam 3 h por semana montando a lista à mão.",
                 "Por que agora": "A rede abre 12 lojas novas em 2027, e o processo manual não acompanha.",
                 "Quem sente a dor": "38 gerentes de loja e os 6 compradores da central"},
        "01.4": {"Hipótese": "Se o gerente receber às 8h a lista dos itens com ruptura provável, priorizada pelo "
                             "impacto em vendas, conseguirá repor antes da falta, reduzindo a ruptura e as 3 h "
                             "semanais da lista manual.",
                 "Alternativas consideradas": "Não fazer: descartada pelas 12 lojas novas de 2027."}},
    "linhas": {
        "01.2/personas": [
            {"Persona": "Gerente de loja", "Volume": "38", "Como faz hoje": "Cruza 3 relatórios toda segunda",
             "Principal dor": "3 h por semana; descobre a falta pelo cliente", "Evidência": "Entrevistas de 05 e 06/10/2026"},
            {"Persona": "Comprador da central", "Volume": "6", "Como faz hoje": "Recebe as listas por e-mail",
             "Principal dor": "Lista chega tarde", "Evidência": "Entrevistas de 05 e 06/10/2026"}],
        "01.3/dimensoes": [
            {"Dimensão": "Operacional", "Indicador atual": "Ruptura média dos itens; tempo dos gerentes na lista",
             "Ordem de grandeza": "7% dos itens; 3 h por semana por gerente",
             "Fonte": "Auditoria de setembro de 2026; entrevistas de 05 e 06/10/2026"}]},
    "versao": {"numero": "0.2", "o_que_mudou": "Etapa 01 fechada", "autor": "Caio Rezende"},
}

V05 = {
    "painel": {"Etapa atual": "03"},
    "checkpoints": {"02": {"situacao": "Cumprido", "data": "10/11/2026"}},
    "linhas": {
        "02.1/rfs": [
            {"ID": "RF-01", "A solução deverá": "Enviar um alerta diário de ruptura por loja", "Prioridade": "Must",
             "Release": "R1", "Critério de aceite": "Pronto quando, nas 5 lojas do piloto, os itens com estoque zero "
             "às 7h aparecem no alerta das 8h, conferidos com a contagem física, com tolerância de 2 itens por loja."},
            {"ID": "RF-02", "A solução deverá": "Priorizar a lista pelo impacto em vendas", "Prioridade": "Must",
             "Release": "R1", "Critério de aceite": "Pronto quando, nas 5 lojas do piloto, os 10 primeiros itens "
             "da lista coincidem em pelo menos 8 com a conferência do gerente."},
            {"ID": "RF-03", "A solução deverá": "Mostrar o histórico de 2 anos por item e loja", "Prioridade": "Must",
             "Release": "R1", "Critério de aceite": "Pronto quando qualquer item de uma loja do piloto mostra 24 meses "
             "de vendas, conferidos com o ERP."},
            {"ID": "RF-04", "A solução deverá": "Exportar a lista para Excel", "Prioridade": "Could", "Release": "R1",
             "Critério de aceite": "Pronto quando a exportação tem as mesmas colunas e totais da tela."},
            {"ID": "RF-05", "A solução deverá": "Avisar o gerente no celular", "Prioridade": "Should",
             "Release": "R2"},
            {"ID": "RF-06", "A solução deverá": "Prever a ruptura com 3 dias de antecedência", "Prioridade": "Should",
             "Release": "R3"}],
        "02.2/releases": [
            {"Release": "R1", "Objetivo": "Alerta e lista priorizada nas 5 lojas do piloto",
             "RFs incluídos": "RF-01, RF-02, RF-03, RF-04", "Critério de saída": "4 semanas de uso com o aceite da Marta",
             "Data-alvo": "mar/2027"},
            {"Release": "R2", "Objetivo": "Aviso no celular", "RFs incluídos": "RF-05", "Data-alvo": "jun/2027"},
            {"Release": "R3", "Objetivo": "Previsão com 3 dias", "RFs incluídos": "RF-06", "Data-alvo": "set/2027"}],
        "02.3/indicadores": [
            {"Indicador": "Ruptura (%)", "Fórmula e janela": "Itens com estoque zero na gôndola ÷ itens do sortimento, "
             "por loja; média semanal", "Referência para conferir": "Auditoria mensal de ruptura",
             "Dono": "Marta Pacheco"}],
        "02.4/nfr": [
            {"Requisito": "Frequência de atualização", "Esperado": "Diária, até as 8h", "Release": "R1",
             "Como verificar": "Horário de chegada do alerta por 2 semanas"},
            {"Requisito": "Perfis de acesso", "Esperado": "O gerente vê só a própria loja; os compradores veem todas",
             "Release": "R1", "Como verificar": "Teste com um usuário de cada perfil"}],
        "02.5/dados": [
            {"ID": "D-01", "Informação": "Vendas por item, loja e dia", "Para qual RF": "RF-01, RF-02, RF-03",
             "Principais campos": "item, loja, dia, quantidade, valor", "Frequência": "Diária", "Histórico": "2 anos",
             "Release": "R1"},
            {"ID": "D-02", "Informação": "Estoque do sistema da loja", "Para qual RF": "RF-01",
             "Principais campos": "item, loja, quantidade", "Frequência": "Diária", "Histórico": "3 meses",
             "Release": "R1"},
            {"ID": "D-03", "Informação": "Cadastro de lojas", "Para qual RF": "RF-01",
             "Principais campos": "loja, gerente, região", "Frequência": "Mensal", "Histórico": "Atual",
             "Release": "R1"},
            {"ID": "D-04", "Informação": "Calendário de promoções", "Para qual RF": "RF-02",
             "Principais campos": "item, loja, início, fim", "Frequência": "Semanal", "Histórico": "1 ano",
             "Release": "R1"}],
        "02.6/fora": [
            {"Item": "Integração com fornecedores", "Motivo": "Fora do objetivo das 3 releases",
             "Reavaliar quando": "Depois da R3"},
            {"Item": "Pedido de reposição automático", "Motivo": "A decisão de repor continua com o gerente",
             "Reavaliar quando": "Depois do piloto"}],
        "03.3/kpis": [
            {"KPI": "Ruptura", "Tipo": "Receita", "Baseline": "7% dos itens (01.3)",
             "Meta e prazo": "3,5% em 12 meses depois da R1",
             "Método e responsável": "Auditoria mensal de ruptura; Marta Pacheco", "Release": "R1"}],
        "03.3/valores": [
            {"KPI": "Venda recuperada", "Ano 2": "R$ 900 mil", "Ano 3": "R$ 900 mil", "Ano 4": "R$ 900 mil",
             "Ano 5": "R$ 900 mil"}]},
    "campos": {
        "03.1": {"O que a solução faz": "Avisa o gerente, todo dia às 8h, quais itens estão ou vão ficar em falta na "
                                        "loja, em ordem de impacto em vendas.",
                 "Tipo de produto": "Data product",
                 "Decisão ou processo apoiado": "O que repor primeiro na loja, a cada manhã",
                 "Onde e como é consumida": "No portal de relatórios que os gerentes já usam, todo dia antes da "
                                            "abertura"},
        "03.3": {"Premissas do benefício": "R$ 900 mil por ano a partir do ano 2, informado pela Marta por e-mail "
                                           "em 20/10/2026; o ano 1 está sem valor."}},
    "versao": {"numero": "0.5", "o_que_mudou": "Etapa 02 fechada; etapa 03 em andamento", "autor": "Caio Rezende"},
}

V06 = {
    "painel": {"Etapa atual": "03"},
    "checkpoints": {"03": {"situacao": "Cumprido", "data": "18/11/2026"}},
    "pessoas": {"Revisor do gate": {"Nome": "Sérgio Lima", "Área": "Escritório de produto"},
                "Dono da mudança": {"Nome": "Marta Pacheco", "Área": "Operações de loja"}},
    "campos": {
        "03.4": {"Forma de lançamento": "Piloto e expansão",
                 "Convivência com a solução atual": "A lista manual continua por 4 semanas",
                 "Dono da mudança": "Marta Pacheco"}},
    "linhas": {
        "03.5/triagem": [
            {"Pergunta": "Envolve dados pessoais?", "Resposta": "Sim",
             "Ação": "O aviso no celular (R2) usa o telefone do gerente: definir base legal e minimização",
             "Responsável": "Rafaela Dutra"},
            {"Pergunta": "Todo dado tem um dono?", "Resposta": "Não",
             "Ação": "Definir o dono da planilha de promoções (D-04)", "Responsável": "Caio Rezende"},
            {"Pergunta": "Cria ou muda um indicador?", "Resposta": "Não"},
            {"Pergunta": "Usa IA (modelo, IA generativa ou agente)?", "Resposta": "Sim",
             "Ação": "Previsão de ruptura (R3): requisitos no Anexo E", "Responsável": "Tomás Brito"}]},
    "pendencias": [
        {"ID": "P-01", "Tipo": "Pendência", "Descrição": "Benefício do ano 1 a confirmar com a Marta",
         "Origem": "03.3", "Gate": "1", "Bloqueante": "Não", "Dono": "Marta Pacheco"},
        {"ID": "R-01", "Tipo": "Risco", "Descrição": "Estoque do sistema da loja diverge da contagem física",
         "Origem": "D-02", "Gate": "2", "Bloqueante": "Não", "Dono": "Lívia Andrade"}],
    "versao": {"numero": "0.6", "o_que_mudou": "Etapa 03 fechada; pronto para o Gate 1", "autor": "Caio Rezende"},
}

V07 = {
    "painel": {"Etapa atual": "04"},
    "pessoas": {"Engenharia de dados": {"Nome": "Lívia Andrade"}, "Ciência de dados": {"Nome": "Tomás Brito"},
                "Segurança": {"Nome": "Rafaela Dutra"}, "Operação": {"Nome": "Otto Siqueira"}},
    "linhas": {"A/pendencias": []},
    "pendencias": [
        {"ID": "C-01", "Tipo": "Condição de gate", "Descrição": "Confirmar o benefício do ano 1 antes do Gate 2",
         "Origem": "Gate 1", "Gate": "2", "Bloqueante": "Sim", "Dono": "Marta Pacheco", "Prazo": "15/12/2026"}],
    "versao": {"numero": "0.7", "o_que_mudou": "Gate 1: pronto com condições", "autor": "Caio Rezende"},
}
GATE1 = {"Decisão": "Pronto com condições", "Condições": "C-01 (Anexo A)",
         "Quem decidiu": "Marta Pacheco e Sérgio Lima", "Data": "20/11/2026"}

V09 = {
    "painel": {"Etapa atual": "05"},
    "painel_bc": {"Benefício no horizonte": "R$ 3,6 milhões", "Custo total no horizonte": "R$ 400 mil",
                  "Resultado líquido": "R$ 3,2 milhões", "ROI": "8,0 (800%)", "Payback": "15º mês"},
    "checkpoints": {"04": {"situacao": "Cumprido", "data": "04/12/2026"}},
    "campos": {
        "04.1": {"Desenho": "Vendas (ERP), estoque (sistema da loja) e promoções (planilha) entram às 5h no "
                            "lakehouse; a tabela de features alimenta a lista e, na R3, o modelo; o alerta e a lista "
                            "saem no portal de relatórios.",
                 "Aderência ao padrão": "Dentro do padrão; o único componente novo é a tabela de features (DT-01)."},
        "04.4": {"Há IA na solução?": "Sim", "Onde está": "Previsão de ruptura na R3; requisitos no Anexo E"},
        "03.3": {"Premissas do benefício": "R$ 900 mil por ano a partir do ano 2, informado pela Marta por e-mail "
                                           "em 20/10/2026; ano 1 sem benefício (piloto), confirmado pela Marta em "
                                           "02/12/2026."},
        "04.6": {"Payback": "15º mês: o acumulado fica positivo no 3º mês do ano 2 (−R$ 208 mil no ano 1; "
                            "+R$ 71 mil por mês no ano 2)",
                 "ROI no horizonte": "8,0 (800%): (R$ 3,6 milhões − R$ 400 mil) ÷ R$ 400 mil",
                 "Sensibilidade (benefício 30% menor)": "R$ 2,52 milhões de benefício: ainda paga o custo total "
                                                        "de R$ 400 mil"}},
    "linhas": {
        "03.3/valores": [{"KPI": "Venda recuperada", "Ano 1": "R$ 0", "Total": "R$ 3,6 milhões"}],
        "04.1/componentes": [
            {"Componente": "Ingestão diária", "Tecnologia": "Lakehouse da empresa", "Novo ou reuso": "Reuso",
             "Responsável": "Lívia Andrade"},
            {"Componente": "Tabela de features", "Tecnologia": "Lakehouse da empresa", "Novo ou reuso": "Novo",
             "Responsável": "Lívia Andrade"},
            {"Componente": "Lista e alerta", "Tecnologia": "Portal de relatórios", "Novo ou reuso": "Reuso",
             "Responsável": "Lívia Andrade"},
            {"Componente": "Modelo de previsão (R3)", "Tecnologia": "Lakehouse da empresa", "Novo ou reuso": "Novo",
             "Responsável": "Tomás Brito"}],
        "04.3/decisoes": [
            {"ID": "DT-01", "Decisão": "Tabela de features no lakehouse que já existe",
             "Alternativas": "Banco separado para o produto", "Racional": "Reuso da ingestão e menor custo"}],
        "04.5/custos": [
            {"Categoria": "Desenvolvimento – time interno", "Build": "R$ 160 mil", "Run no ano 1": "R$ 0",
             "Run por ano depois": "R$ 0", "Total no horizonte": "R$ 160 mil",
             "Premissa e fonte": "8 FTE-mês (6 da engenharia + 2 da ciência) × R$ 20 mil, da tabela de custos da área"},
            {"Categoria": "Nuvem – processamento", "Build": "R$ 0", "Run no ano 1": "R$ 48 mil",
             "Run por ano depois": "R$ 48 mil", "Total no horizonte": "R$ 240 mil",
             "Premissa e fonte": "R$ 4 mil × 12 (arquitetura), processamento e armazenamento"},
            {"Categoria": "TOTAL", "Build": "R$ 160 mil", "Run no ano 1": "R$ 48 mil", "Run por ano depois": "R$ 48 mil",
             "Total no horizonte": "R$ 400 mil", "Premissa e fonte": "As outras categorias: R$ 0"}],
        "04.6/bc": [
            {"Linha": "Benefício (03.3)", "Ano 1": "R$ 0", "Ano 2": "R$ 900 mil", "Ano 3": "R$ 900 mil",
             "Ano 4": "R$ 900 mil", "Ano 5": "R$ 900 mil", "Total": "R$ 3,6 milhões"},
            {"Linha": "Build (04.5)", "Ano 1": "R$ 160 mil", "Ano 2": "R$ 0", "Ano 3": "R$ 0", "Ano 4": "R$ 0",
             "Ano 5": "R$ 0", "Total": "R$ 160 mil"},
            {"Linha": "Run (04.5)", "Ano 1": "R$ 48 mil", "Ano 2": "R$ 48 mil", "Ano 3": "R$ 48 mil",
             "Ano 4": "R$ 48 mil", "Ano 5": "R$ 48 mil", "Total": "R$ 240 mil"},
            {"Linha": "Resultado líquido", "Ano 1": "−R$ 208 mil", "Ano 2": "R$ 852 mil", "Ano 3": "R$ 852 mil",
             "Ano 4": "R$ 852 mil", "Ano 5": "R$ 852 mil", "Total": "R$ 3,2 milhões"}],
        "C/origem": [
            {"ID": "D-01", "Onde existe hoje": "ERP", "Disponível hoje": "Sim", "Forma de acesso": "Ingestão diária",
             "Classificação": "Interna", "Dados pessoais": "Não", "Dono do dado": "Comercial", "Confirmado": "☒"},
            {"ID": "D-02", "Onde existe hoje": "Sistema da loja", "Disponível hoje": "Sim",
             "Forma de acesso": "Ingestão diária", "Classificação": "Interna", "Dados pessoais": "Não",
             "Dono do dado": "Operações de loja", "Confirmado": "☒"},
            {"ID": "D-03", "Onde existe hoje": "Cadastro corporativo", "Disponível hoje": "Sim",
             "Forma de acesso": "Ingestão mensal", "Classificação": "Interna", "Dados pessoais": "Sim (gerente)",
             "Dono do dado": "Operações de loja", "Confirmado": "☒"},
            {"ID": "D-04", "Onde existe hoje": "Planilha", "Disponível hoje": "Sim",
             "Forma de acesso": "Upload semanal", "Classificação": "Interna", "Dados pessoais": "Não",
             "Dono do dado": "Marketing", "Confirmado": "☒"}],
        "D/capacity": [
            {"Período": "Mês 1", "Engenharia": "2", "Ciência": "1", "Total": "3"},
            {"Período": "Mês 2", "Engenharia": "2", "Ciência": "1", "Total": "3"},
            {"Período": "Mês 3", "Engenharia": "2", "Total": "2"},
            {"Período": "TOTAL", "Engenharia": "6", "Ciência": "2", "Total": "8"}],
        "D/consolidacao": [
            {"Especialidade": "Engenharia de dados", "Interno ou externo": "Interno", "Total FTE-mês": "6",
             "Custo por FTE-mês": "R$ 20 mil", "Custo": "R$ 120 mil", "Fonte": "Tabela de custos da área"},
            {"Especialidade": "Ciência de dados", "Interno ou externo": "Interno", "Total FTE-mês": "2",
             "Custo por FTE-mês": "R$ 20 mil", "Custo": "R$ 40 mil", "Fonte": "Tabela de custos da área"}]},
    "canvas": {
        "eng": {"aplicavel": "Sim", "blocos": {
            "Fontes e acesso": "D-01 no ERP, D-02 no sistema da loja, D-03 no cadastro, D-04 em planilha; acessos "
                               "confirmados (Anexo C)",
            "Ingestão e frequência": "Diária às 5h; promoções por upload semanal",
            "Transformação e modelagem": "Tabela de features por item, loja e dia",
            "Qualidade e reconciliação": "Estoque conferido com a contagem física nas 5 lojas do piloto, tolerância "
                                         "de 2 itens por loja (R-01)",
            "Lineage e catálogo": "Tabelas no catálogo do lakehouse",
            "Ambientes": "Desenvolvimento, teste e produção do lakehouse",
            "Volume e desempenho": "Carga diária concluída até as 7h",
            "Operação e alertas": "Falha de carga avisa a engenharia às 6h",
            "Esforço e custo": "2 FTE por 3 meses; nuvem R$ 4 mil por mês"}},
        "cie": {"aplicavel": "Sim", "blocos": {
            "Decisão e variável-alvo": "Ruptura de um item numa loja nos próximos 3 dias (R3)",
            "Dados e features": "D-01, D-02 e D-04; 2 anos de histórico",
            "Base de comparação e métricas": "Regra atual (estoque abaixo de 2 dias de venda); recall e precisão",
            "Validação antes da produção": "Recall de 80% com precisão de 60% num backtest de 6 meses",
            "Explicabilidade e vieses": "Lista mostra o motivo do alerta; conferir lojas novas, com pouco histórico",
            "Monitoramento e retreino": "Recall mensal; retreino mensal",
            "Operação do modelo": "Roda no lakehouse depois da carga das 5h",
            "Esforço e custo": "1 FTE por 2 meses"}},
        "sw": {"aplicavel": "Não", "motivo": "O alerta e a lista saem no portal de relatórios que já existe"},
        "seg": {"aplicavel": "Sim", "blocos": {
            "Classificação dos dados": "Interna",
            "Dados pessoais": "Telefone corporativo do gerente (R2): base legal no contrato de trabalho; só o "
                              "telefone corporativo; mantido enquanto ele for gerente",
            "Modelo de acesso": "Gerente vê só a própria loja; compradores veem todas (02.4)",
            "Ameaças e controles": "Acesso indevido a outras lojas: filtro por perfil no portal",
            "Segredos e chaves": "No cofre do lakehouse",
            "Logs e auditoria": "Acessos ao portal registrados por 1 ano",
            "Terceiros": "Nenhum",
            "Aprovações necessárias": "Segurança da informação, antes do go-live",
            "Esforço e custo": "Dentro do time de engenharia"}},
        "op": {"aplicavel": "Sim", "blocos": {
            "Pipelines e agendamentos": "Carga às 5h; lista às 7h30; alerta às 8h",
            "Monitoramento e alertas": "Falha de carga ou alerta atrasado avisa a operação",
            "Dono operacional": "Otto Siqueira",
            "SLA": "Alerta até as 8h em 95% dos dias",
            "Runbook": "Reprocessar a carga; se passar das 9h, avisar os gerentes",
            "Suporte e escalonamento": "Central de suporte; escala para a engenharia",
            "Transferência de conhecimento": "2 sessões com a operação antes do go-live",
            "Esforço e custo de run": "Dentro do time de operação"}}},
    "linhas_e": None,
    "versao": {"numero": "0.9", "o_que_mudou": "Etapa 04 fechada", "autor": "Caio Rezende"},
}
V09_E = {"E": {
    "Tipo de IA": "Modelo preditivo",
    "Tarefa ou decisão apoiada": "Prever a ruptura de um item numa loja nos próximos 3 dias (R3)",
    "Entradas e saídas, com exemplos": "Entra: vendas, estoque e promoções do item na loja. Sai: probabilidade de "
                                       "ruptura em 3 dias (ex.: item 123, loja 7, 0,82)",
    "Métrica técnica": "Recall e precisão",
    "Métrica de negócio": "Ruptura (%)",
    "Limiar para ir à produção": "Recall de 80% com precisão de 60%",
    "Comparação com o jeito atual": "Regra atual: estoque abaixo de 2 dias de venda",
    "Conjunto de avaliação e quem valida": "Backtest de 6 meses; Tomás Brito",
    "Revisão humana": "O gerente decide a reposição; o modelo só ordena a lista",
    "Limites e o que fazer quando falha": "Itens novos, sem histórico, seguem a regra atual",
    "Monitoramento e gatilho de revisão": "Recall mensal abaixo de 80% dispara revisão",
    "Custo por uso": "Dentro da nuvem (04.5)"}}

V10 = {
    "painel": {"Etapa atual": "05"},
    "checkpoints": {"05": {"situacao": "Cumprido", "data": "14/12/2026"}},
    "campos": {
        "05.1": {"Forma de lançamento": "Piloto e expansão", "O que a solução substitui": "A lista manual de segunda-feira",
                 "Convivência com a solução atual": "4 semanas de lista manual em paralelo",
                 "Critério para desligar a solução atual": "2 conferências seguidas com até 2 itens de diferença por loja",
                 "Time do negócio na transição": "Gerentes das 5 lojas do piloto, 1 h por semana durante 4 semanas",
                 "Dono da mudança": "Marta Pacheco"},
        "05.2": {"Quem dá o aceite": "Marta Pacheco", "Homologadores": "Gerentes das 5 lojas do piloto",
                 "Período e ambiente": "2 semanas, no ambiente de teste com dados de produção",
                 "Critério de aceite da release": "RF-01 a RF-04 aprovados no roteiro"},
        "05.4": {"Quem decide e quando": "Marta Pacheco, na véspera do go-live"},
        "05.5": {"Cutover (sequência, janela e dono)": "Liberar o portal às 6h de uma segunda; Lívia Andrade",
                 "Contingência": "Se o alerta atrasar, enviar a lista das 7h30 por e-mail",
                 "Gatilhos de rollback": "Alerta depois das 9h em 2 dias seguidos, ou mais de 20% dos itens errados na "
                                         "conferência de 2 lojas",
                 "Como voltar": "Voltar para a lista manual no mesmo dia",
                 "Tempo máximo para voltar": "Mesmo dia",
                 "Quem decide e como comunica": "Marta Pacheco; grupo dos gerentes",
                 "Solução atual disponível até": "31/03/2027"},
        "05.6": {"Treinamento": "30 minutos por loja, na semana do go-live", "Canal de suporte": "Central de suporte",
                 "Métrica de adoção": "Lojas do piloto que abrem a lista até as 9h (premissa do benefício)"},
        "05.7": {"Escopo da R1": "RF-01, RF-02, RF-03 e RF-04 (02.1)", "Fora do escopo": "02.6",
                 "Indicadores acordados": "Ruptura (02.3 e 03.3)", "Aceite": "05.2", "Go-live": "05.1 e 05.3",
                 "Critérios de handover": "Canvas de Operação (04.2)", "Quem conduz a execução": "Caio Rezende",
                 "Datas": "R1 em mar/2027 (02.2)"}},
    "linhas": {
        "05.2/roteiro": [
            {"Caso": "H-01", "RF": "RF-01", "Como testar": "Comparar o alerta das 8h com a contagem física",
             "Resultado esperado": "Até 2 itens de diferença por loja", "Release": "R1"},
            {"Caso": "H-02", "RF": "RF-02", "Como testar": "Comparar os 10 primeiros itens com a conferência do gerente",
             "Resultado esperado": "Pelo menos 8 coincidem", "Release": "R1"},
            {"Caso": "H-03", "RF": "RF-03", "Como testar": "Consultar 24 meses de um item e conferir com o ERP",
             "Resultado esperado": "Mesmos números", "Release": "R1"},
            {"Caso": "H-04", "RF": "RF-04", "Como testar": "Exportar a lista e comparar com a tela",
             "Resultado esperado": "Mesmas colunas e totais", "Release": "R1"}],
        "05.3/fases": [
            {"Fase": "Homologação", "O que acontece": "Roteiro H-01 a H-04", "Início e fim": "04 a 15/01/2027",
             "Participantes": "Gerentes do piloto", "Critério de saída": "Aceite da Marta", "Responsável": "Caio Rezende"},
            {"Fase": "Go-live: onda 1", "O que acontece": "5 lojas do piloto", "Início e fim": "18/01/2027",
             "Participantes": "Gerentes do piloto", "Critério de saída": "4 semanas de uso",
             "Responsável": "Marta Pacheco"},
            {"Fase": "Convivência", "O que acontece": "Lista manual em paralelo", "Início e fim": "18/01 a 12/02/2027",
             "Participantes": "Gerentes do piloto", "Critério de saída": "05.1", "Responsável": "Marta Pacheco"}],
        "05.4/gonogo": [
            {"Critério": "Homologação da release aceita", "Como verificar": "Aceite da Marta", "Responsável": "Caio Rezende"},
            {"Critério": "Rollback ensaiado", "Como verificar": "Volta para a lista manual testada",
             "Responsável": "Lívia Andrade"}],
        "05.6/publicos": [
            {"Público": "Usuários finais", "O que muda": "A lista chega pronta às 8h", "Ação": "Treinamento de 30 min",
             "Canal": "Presencial", "Quando": "Semana do go-live", "Responsável": "Marta Pacheco"}]},
    "versao": {"numero": "1.0", "o_que_mudou": "Etapa 05 fechada; Gate 2", "autor": "Caio Rezende"},
}
GATE2 = {"Decisão": "Pronto", "Quem decidiu": "Marta Pacheco e Sérgio Lima", "Data": "15/12/2026"}


# ---------------------------------------------------------------- o que só pessoas gravam

def _decidir(caminho, n, valores, assinar=None):
    """Grava a decisão de um gate (e, no Gate 2, a versão assinada): o agente nunca faz isso."""
    doc = Document(caminho)
    mapa = S["_mapa"](doc)
    t_dec = mapa[f"gate{n}"][1]
    for row in t_dec.rows:
        rot = S["_texto_celula"](row.cells[0])
        if rot == "Decisão":
            S["_escrever_opcao"](row.cells[-1], S["DECISOES_GATE"], valores["Decisão"])
        elif rot in valores:
            S["_escrever"](row.cells[-1], valores[rot])
    nome_gate = S["GATES"][n][0]
    S["_gravar_linhas"](mapa["gates"][0], ["Gate", "Decisão", "Quem decidiu", "Data"], [],
                        [{"Gate": nome_gate, "Decisão": valores["Decisão"], "Quem decidiu": valores["Quem decidiu"],
                          "Data": valores["Data"]}], "gates")
    if assinar:
        for row in mapa["painel"][0].rows:
            if S["_texto_celula"](row.cells[0]) == "Versão assinada":
                S["_escrever"](row.cells[-1], assinar)
    doc.save(caminho)


def gerar():
    FIX.mkdir(exist_ok=True)
    material()
    hoje = {"0.2": "30/10/2026", "0.5": "10/11/2026", "0.6": "18/11/2026", "0.7": "20/11/2026", "0.9": "04/12/2026",
            "1.0": "14/12/2026"}
    anterior = TEMPLATE
    for v, ped in (("0.2", V02), ("0.5", V05), ("0.6", V06), ("0.7", V07), ("0.9", V09), ("1.0", V10)):
        ped = {k: val for k, val in copy.deepcopy(ped).items() if val is not None and k != "linhas_e"}
        if v == "0.7":
            ped["linhas"] = {}
        if v == "0.9":
            ped["campos"].update(V09_E)
        saida = FIX / f"prd-radar-v{v}.docx"
        S["gravar_prd"](ped, str(anterior), str(saida), hoje=hoje[v])
        if v == "0.7":
            _decidir(saida, "1", GATE1)
        if v == "1.0":
            _decidir(saida, "2", GATE2, assinar="1.0")
        anterior = saida
        print("gerada:", saida.name)


if __name__ == "__main__":
    gerar()
