# Gerado por ferramentas/montar_skills.py a partir de: produto/assistente-de-prd/codigo/estrutura.py produto/assistente-de-prd/codigo/prd_docx.py produto/assistente-de-prd/codigo/cli_prd.py. Não edite aqui.

# ==== produto/assistente-de-prd/codigo/estrutura.py
# ---------------------------------------------------------------- PRD: estrutura do documento
# Fonte única das seções do PRD. Gera o template (gerar_template.py) e guia a leitura e a gravação (prd_docx.py).
# Cada seção tem um ID ("01.1"), um título e blocos:
#   ("campos", [rótulo ou (rótulo, [opções])])          -> tabela de 2 colunas: rótulo | valor
#   ("tabela", nome, [colunas], linhas_fixas, n_vazias) -> tabela com cabeçalho; a 1ª coluna das linhas fixas é a chave
#   ("grade", canvas)                                    -> quadro de um canvas (etapa 04)
# A orientação ("guia") sai em cinza itálico no template e nunca conta como conteúdo.

HORIZONTE_PADRAO = 5
ANOS = [f"Ano {i}" for i in range(1, HORIZONTE_PADRAO + 1)]

ETAPAS = [
    ("01", "Dor", "Qual problema, de quem e de que tamanho, sem falar da solução."),
    ("02", "Requisitos e critérios de aceite por release",
     "O que a solução precisa fazer em cada release, e como saber que está pronta."),
    ("03", "Solução e benefícios", "Que produto, para quem, e quanto ele vale em cada release."),
    ("04", "Refinamento técnico e custos", "Como construir, com que riscos e quanto custa."),
    ("05", "Go-live e transição", "Como a solução entra em produção e como voltar se der errado."),
]

OPCOES_LANCAMENTO = ["Big bang", "Por ondas", "Piloto e expansão"]
SIM_NAO_NAOSEI = ["Sim", "Não", "Não sei"]

SECOES = [
    # ---------------------------------------------------------------- 01 Dor
    {"id": "01.1", "titulo": "Problema e contexto", "etapa": "01", "dono": "PM, com o sponsor",
     "guia": "Bom quando descreve a dor e quem a sente sem citar a solução, o \"por que agora\" tem um gatilho com "
             "data ou evento e quem sente a dor tem área e volume.",
     "blocos": [("campos", ["Problema ou oportunidade", "Por que agora", "Prioridade estratégica",
                            "Quem sente a dor"])]},
    {"id": "01.2", "titulo": "Como é hoje", "etapa": "01", "dono": "PM",
     "guia": "Uma linha por persona: volume, o passo a passo atual em uma frase e uma evidência com data.",
     "blocos": [("tabela", "personas", ["Persona", "Volume", "Como faz hoje", "Principal dor", "Evidência"], [], 3)]},
    {"id": "01.3", "titulo": "Tamanho da dor", "etapa": "01", "dono": "PM, com o sponsor",
     "guia": "Pelo menos uma dimensão com baseline numérico, unidade e fonte. É o tamanho do problema hoje, "
             "não o benefício.",
     "blocos": [("tabela", "dimensoes", ["Dimensão", "Indicador atual", "Ordem de grandeza", "Fonte"],
                 ["Financeira", "Operacional", "Risco ou compliance"], 0)]},
    {"id": "01.4", "titulo": "Hipótese e alternativas", "etapa": "01", "dono": "PM",
     "guia": "Hipótese: \"Se [capacidade], [usuário] conseguirá [resultado], reduzindo [dor]\". No porte G, as "
             "alternativas (processo, ferramenta de mercado, não fazer) têm o motivo do descarte.",
     "blocos": [("campos", ["Hipótese", "Alternativas consideradas"])]},
    # ---------------------------------------------------------------- 02 Requisitos por release
    {"id": "02.1", "titulo": "Requisitos funcionais e critérios de aceite", "etapa": "02", "dono": "PM, com o negócio",
     "guia": "Todo Must na R1; Could na R1 só com motivo; Won't vai para o fora do escopo. Todo RF da release que "
             "vai ser construída tem critério verificável (\"pronto quando…\", com dado, caso e tolerância).",
     "blocos": [("tabela", "rfs", ["ID", "A solução deverá", "Prioridade", "Release", "Critério de aceite"], [], 5)]},
    {"id": "02.2", "titulo": "Mapa de releases", "etapa": "02", "dono": "PM, com o sponsor",
     "guia": "Os RFs da 02.1 agrupados em quantas releases o produto precisar (R1 = MVP). Cada release entrega "
             "valor sozinha e tem um critério de saída.",
     "blocos": [("tabela", "releases", ["Release", "Objetivo", "RFs incluídos", "Critério de saída", "Data-alvo"],
                 [], 3)]},
    {"id": "02.3", "titulo": "Indicadores e regras de negócio", "etapa": "02", "dono": "PM, com o sponsor",
     "guia": "Só se o produto calcula ou mostra indicadores: numerador, denominador e janela; um relatório "
             "contra o qual conferir; o dono é uma pessoa.",
     "blocos": [("tabela", "indicadores", ["Indicador", "Fórmula e janela", "Referência para conferir", "Dono"],
                 [], 2)]},
    {"id": "02.4", "titulo": "Requisitos não funcionais", "etapa": "02", "dono": "PM",
     "guia": "Frequência e perfis de acesso em todo porte; no G, toda categoria com forma de verificação.",
     "blocos": [("tabela", "nfr", ["Requisito", "Esperado", "Release", "Como verificar"],
                 ["Frequência de atualização", "Disponibilidade", "Perfis de acesso", "Desempenho",
                  "Explicabilidade"], 0)]},
    {"id": "02.5", "titulo": "Dados necessários", "etapa": "02", "dono": "PM, com o negócio",
     "guia": "Todo RF da R1 que depende de dado tem pelo menos um D-nn. Origem, acesso e cuidados ficam no "
             "Anexo C.",
     "blocos": [("tabela", "dados", ["ID", "Informação", "Para qual RF", "Principais campos", "Frequência",
                                     "Histórico", "Release"], [], 4)]},
    {"id": "02.6", "titulo": "Fora do escopo", "etapa": "02", "dono": "PM, com o sponsor",
     "guia": "Os pedidos que apareceram e não entraram, cada um com o motivo. Vazio é ◐: o que não está escrito "
             "vira discussão depois.",
     "blocos": [("tabela", "fora", ["Item", "Motivo", "Reavaliar quando"], [], 3)]},
    # ---------------------------------------------------------------- 03 Solução e benefícios
    {"id": "03.1", "titulo": "Visão da solução", "etapa": "03", "dono": "PM",
     "guia": "A saída em linguagem de negócio; a decisão apoiada é específica; o consumo tem ferramenta, "
             "frequência e momento do processo.",
     "blocos": [("campos", ["O que a solução faz",
                            ("Tipo de produto", ["Dashboard", "Modelo", "Data product", "API", "Aplicação",
                                                 "Automação", "Agente"]),
                            "Decisão ou processo apoiado", "Onde e como é consumida"])]},
    {"id": "03.2", "titulo": "Jornada e protótipo", "etapa": "03", "dono": "PM",
     "guia": "No porte G, protótipo testado com usuários e aprendizados registrados.",
     "blocos": [("campos", ["Jornada TO-BE", "Protótipo", ("Teste com usuários", ["Sim", "Não", "N/A"]),
                            "Aprendizados"])]},
    {"id": "03.3", "titulo": "Benefícios por release", "etapa": "03", "dono": "Sponsor, com o PM",
     "guia": "Todo KPI tem baseline (da 01.3), meta com prazo, método e quem mede. Os valores por ano vêm do "
             "sponsor ou de uma fonte, nunca de estimativa.",
     "blocos": [("tabela", "kpis", ["KPI", "Tipo", "Baseline", "Meta e prazo", "Método e responsável", "Release"],
                 [], 2),
                ("tabela", "valores", ["KPI"] + ANOS + ["Total"], ["TOTAL"], 2),
                ("campos", ["Premissas do benefício", "Benefícios não financeiros", "Validação do sponsor"])]},
    {"id": "03.4", "titulo": "Estratégia de lançamento (preliminar)", "etapa": "03", "dono": "Sponsor, com o PM",
     "guia": "As premissas de adoção do benefício batem com ela. O detalhe vem na 05.1.",
     "blocos": [("campos", [("Forma de lançamento", OPCOES_LANCAMENTO), "Convivência com a solução atual",
                            "Dono da mudança"])]},
    {"id": "03.5", "titulo": "Triagem de governança", "etapa": "03", "dono": "PM",
     "guia": "Todo \"sim\" ou \"não sei\" tem ação e responsável. Vira insumo do canvas de Segurança e do Anexo E.",
     "blocos": [("tabela", "triagem", ["Pergunta", "Resposta", "Ação", "Responsável"],
                 ["Envolve dados pessoais?", "Todo dado tem um dono?", "Cria ou muda um indicador?",
                  "Usa IA (modelo, IA generativa ou agente)?"], 0)]},
    # ---------------------------------------------------------------- 04 Refinamento técnico e custos
    {"id": "04.1", "titulo": "Arquitetura e componentes", "etapa": "04", "dono": "Especialistas técnicos",
     "guia": "Desenho de fontes, ingestão, transformação, modelo e consumo. Todo desvio do padrão da empresa "
             "tem uma decisão registrada (04.3).",
     "blocos": [("campos", ["Desenho", "Aderência ao padrão"]),
                ("tabela", "componentes", ["Componente", "Tecnologia", "Novo ou reuso", "Responsável"], [], 4)]},
    {"id": "04.2", "titulo": "Canvas por especialidade", "etapa": "04", "dono": "Cada especialista, no seu canvas",
     "guia": "Um quadro por especialidade. Cada bloco fica preenchido ou \"N/A\" com motivo. O bloco de esforço "
             "e custo alimenta a 04.5.",
     "blocos": [("grade", "eng"), ("grade", "cie"), ("grade", "sw"), ("grade", "seg"), ("grade", "op")]},
    {"id": "04.3", "titulo": "Decisões de arquitetura", "etapa": "04", "dono": "Especialistas técnicos",
     "guia": "Obrigatório no porte G; recomendado no M.",
     "blocos": [("tabela", "decisoes", ["ID", "Decisão", "Alternativas", "Racional"], [], 2)]},
    {"id": "04.4", "titulo": "Requisitos de IA", "etapa": "04", "dono": "Ciência de dados ou PM",
     "guia": "Quando a solução tem modelo preditivo, IA generativa ou agente, os requisitos ficam no Anexo E.",
     "blocos": [("campos", [("Há IA na solução?", ["Sim", "Não"]), "Onde está"])]},
    {"id": "04.5", "titulo": "Custos", "etapa": "04", "dono": "Especialistas técnicos, com o PM",
     "guia": "Toda linha com premissa e fonte, ou \"0\" com motivo. O custo por FTE só entra com fonte. Total no "
             "horizonte = build + run no ano 1 + run por ano × (horizonte − 1).",
     "blocos": [("tabela", "custos", ["Categoria", "Build", "Run no ano 1", "Run por ano depois",
                                      "Total no horizonte", "Premissa e fonte"],
                 ["Desenvolvimento – time interno", "Desenvolvimento – fornecedor", "Nuvem – processamento",
                  "Nuvem – armazenamento", "Licenças", "Aquisição de dados", "Uso de IA (inferência ou tokens)",
                  "Sustentação", "Evolução e retreino", "Go-live e convivência", "Adoção e mudança", "TOTAL"], 0)]},
    {"id": "04.6", "titulo": "Business case", "etapa": "04", "dono": "PM, com o revisor",
     "guia": "Só quando 03.3 e 04.5 estão com ✓. Resultado líquido = benefício − build − run, por ano; ROI = "
             "(benefício − custo total) ÷ custo total; payback = mês em que o acumulado fica positivo.",
     "blocos": [("tabela", "bc", ["Linha"] + ANOS + ["Total"],
                 ["Benefício (03.3)", "Build (04.5)", "Run (04.5)", "Resultado líquido"], 0),
                ("campos", ["Payback", "ROI no horizonte", "Sensibilidade (benefício 30% menor)"])]},
    # ---------------------------------------------------------------- 05 Go-live e transição
    {"id": "05.1", "titulo": "Estratégia de go-live", "etapa": "05", "dono": "Sponsor, com o PM",
     "guia": "A convivência tem duração e critério de desligamento mensurável; o time do negócio tem papéis, "
             "horas por semana e período.",
     "blocos": [("campos", [("Forma de lançamento", OPCOES_LANCAMENTO), "O que a solução substitui",
                            "Convivência com a solução atual", "Critério para desligar a solução atual",
                            "Time do negócio na transição", "Operação assistida", "Janelas a evitar",
                            "Dono da mudança"])]},
    {"id": "05.2", "titulo": "Homologação por release", "etapa": "05", "dono": "PM, com o sponsor",
     "guia": "O aceite é de uma pessoa nomeada. O roteiro tem um caso por RF da release, a partir dos critérios "
             "da 02.1.",
     "blocos": [("campos", ["Quem dá o aceite", "Homologadores", "Período e ambiente",
                            "Critério de aceite da release"]),
                ("tabela", "roteiro", ["Caso", "RF", "Como testar", "Resultado esperado", "Release"], [], 4)]},
    {"id": "05.3", "titulo": "Fases da transição", "etapa": "05", "dono": "PM, com os especialistas",
     "guia": "Toda fase que se aplica tem datas, participantes e critério de saída; a que não se aplica fica "
             "\"N/A\".",
     "blocos": [("tabela", "fases", ["Fase", "O que acontece", "Início e fim", "Participantes", "Critério de saída",
                                     "Responsável"],
                 ["Homologação", "Operação assistida", "Go-live: onda 1", "Go-live: onda n", "Convivência",
                  "Hypercare", "Handover", "Desligamento da solução atual"], 0)]},
    {"id": "05.4", "titulo": "Go/no-go", "etapa": "05", "dono": "PM",
     "guia": "Todo critério tem responsável, e a decisão tem quem e quando.",
     "blocos": [("tabela", "gonogo", ["Critério", "Como verificar", "Responsável"],
                 ["Homologação da release aceita", "Dados reconciliados com a fonte", "Acessos concedidos",
                  "Suporte e runbook prontos", "Comunicação feita", "Rollback ensaiado",
                  "Qualidade da IA atendida (quando houver)"], 0),
                ("campos", ["Quem decide e quando"])]},
    {"id": "05.5", "titulo": "Cutover, contingência e rollback", "etapa": "05", "dono": "Especialistas, com o PM",
     "guia": "Contingência é seguir sem voltar atrás; rollback é voltar. Os gatilhos são mensuráveis e a "
             "solução atual fica disponível até uma data definida.",
     "blocos": [("campos", ["Cutover (sequência, janela e dono)", "Contingência", "Gatilhos de rollback",
                            "Como voltar", "Tempo máximo para voltar", "Quem decide e como comunica",
                            "Solução atual disponível até"])]},
    {"id": "05.6", "titulo": "Comunicação, treinamento e adoção", "etapa": "05", "dono": "Dono da mudança",
     "guia": "Todo público tem ação, data relativa ao go-live e responsável. A métrica de adoção é a mesma "
             "premissa do benefício (03.3).",
     "blocos": [("tabela", "publicos", ["Público", "O que muda", "Ação", "Canal", "Quando", "Responsável"],
                 ["Usuários finais", "Gestores dos usuários", "Áreas impactadas", "Suporte"], 0),
                ("campos", ["Treinamento", "Material de apoio", "Canal de suporte", "Métrica de adoção"])]},
    {"id": "05.7", "titulo": "Acordo de entrega", "etapa": "05", "dono": "PM, com o revisor",
     "guia": "Cita os IDs e as seções, sem reescrever o conteúdo.",
     "blocos": [("campos", ["Escopo da R1", "Fora do escopo", "Indicadores acordados", "Aceite", "Go-live",
                            "Critérios de handover", "Quem conduz a execução", "Datas"])]},
]

CANVAS = {
    "eng": ("Engenharia de dados", "Quase sempre", [
        ("Fontes e acesso", "De onde vem cada D-nn, e o acesso já existe?"),
        ("Ingestão e frequência", "Como e de quanto em quanto tempo os dados chegam?"),
        ("Transformação e modelagem", "Que tabelas e regras saem da ingestão?"),
        ("Qualidade e reconciliação", "Contra o que os números são conferidos, e com que tolerância?"),
        ("Lineage e catálogo", "Onde o dado fica documentado e rastreável?"),
        ("Ambientes", "Desenvolvimento, teste e produção existem, com quais acessos?"),
        ("Volume e desempenho", "Quanto dado, e quanto tempo cada carga pode levar?"),
        ("Operação e alertas", "O que é monitorado e quem recebe o alerta?"),
        ("Esforço e custo", "FTE por período, build e run, com fonte.")]),
    "cie": ("Ciência de dados", "Só com modelo", [
        ("Decisão e variável-alvo", "O que o modelo prevê, para qual decisão, com que horizonte?"),
        ("Dados e features", "Que dados entram, com qual histórico?"),
        ("Base de comparação e métricas", "Contra o que o modelo é comparado; métrica técnica e de negócio."),
        ("Validação antes da produção", "Como e com qual limiar o modelo é aprovado?"),
        ("Explicabilidade e vieses", "O que o usuário vê sobre o porquê; que grupos conferir."),
        ("Monitoramento e retreino", "O que dispara a revisão ou o retreino?"),
        ("Operação do modelo", "Quem opera, onde roda, como é versionado?"),
        ("Esforço e custo", "FTE por período, build e run, com fonte.")]),
    "sw": ("Software", "Com aplicação, API ou automação", [
        ("Arquitetura da aplicação", "Front-end, back-end e serviços."),
        ("Integrações e APIs", "Com quais sistemas conversa, e como?"),
        ("Autenticação e autorização", "Como implementa os perfis da 02.4?"),
        ("Não funcionais atendidos", "Como atende a 02.4 (desempenho, disponibilidade)?"),
        ("Testes", "Unitários, de integração e de carga."),
        ("Esteira e ambientes", "Como o código chega à produção?"),
        ("Observabilidade", "Logs, métricas e alertas."),
        ("Esforço e custo", "FTE por período, build e run, com fonte.")]),
    "seg": ("Segurança", "Sempre (simplificado no porte P)", [
        ("Classificação dos dados", "A classificação mais alta entre os D-nn."),
        ("Dados pessoais", "Base legal, minimização e retenção."),
        ("Modelo de acesso", "Perfis da 02.4 e menor privilégio."),
        ("Ameaças e controles", "O que pode dar errado e o que impede."),
        ("Segredos e chaves", "Onde ficam e quem acessa."),
        ("Logs e auditoria", "O que é registrado e por quanto tempo."),
        ("Terceiros", "Fornecedores e serviços externos que tocam o dado."),
        ("Aprovações necessárias", "Quem precisa aprovar antes do go-live."),
        ("Esforço e custo", "FTE por período, build e run, com fonte.")]),
    "op": ("Operação e sustentação", "Sempre (simplificado no porte P)", [
        ("Pipelines e agendamentos", "O que roda, quando e em que ordem."),
        ("Monitoramento e alertas", "O que é acompanhado e quem é avisado."),
        ("Dono operacional", "Uma pessoa ou um time nomeado."),
        ("SLA", "Parte da disponibilidade da 02.4."),
        ("Runbook", "O que fazer em cada falha conhecida."),
        ("Suporte e escalonamento", "Quem atende e para quem escala."),
        ("Transferência de conhecimento", "Como e quando o time de operação aprende."),
        ("Esforço e custo de run", "FTE e custos por ano, com fonte.")]),
}

PAINEL_CAMPOS = ["Produto", ("Tipo", ["Produto novo", "Evolução"]), ("Porte", ["P", "M", "G"]),
                 "Horizonte do business case", "Etapa atual", "Versão vigente", "Versão assinada"]
PAINEL_BC = ["Benefício no horizonte", "Custo total no horizonte", "Resultado líquido", "ROI", "Payback"]
PESSOAS = ["Sponsor", "PM", "Engenharia de dados", "Ciência de dados", "Software", "Segurança", "Operação",
           "Revisor do gate", "Dono da mudança"]

GATES = {
    "1": ("Gate 1 · Vale construir?", [
        "O problema descreve a dor sem citar a solução, com quem sente e volume (01.1)",
        "O tamanho da dor tem baseline com fonte (01.3)",
        "Todo RF da R1 com prioridade e critério de aceite verificável (02.1)",
        "Mapa de releases com objetivo e critério de saída (02.2)",
        "Dados da R1 mapeados (02.5)",
        "Fora do escopo preenchido (02.6)",
        "Visão da solução com decisão apoiada e consumo (03.1)",
        "Benefício com baseline, meta, prazo, método e responsável (03.3)",
        "Estratégia de lançamento preliminar e dono da mudança (03.4)",
        "Triagem de governança com ações (03.5)",
        "Riscos e dependências conhecidos no Anexo A"]),
    "2": ("Gate 2 · PRD assinado", [
        "Condições do Gate 1 resolvidas",
        "Arquitetura e componentes, com os desvios decididos (04.1 e 04.3)",
        "Canvas aplicáveis completos (04.2)",
        "Requisitos de IA com limiar e conjunto de avaliação, quando há IA (Anexo E)",
        "Custos com premissa e fonte (04.5)",
        "Business case fechado (04.6)",
        "Estratégia de go-live e fases com critério de saída (05.1 e 05.3)",
        "Homologação da R1 com roteiro e aceite nomeado (05.2)",
        "Go/no-go com responsáveis e quem decide (05.4)",
        "Cutover, contingência e rollback com gatilhos mensuráveis (05.5)",
        "Comunicação e métrica de adoção (05.6)",
        "Acordo de entrega (05.7)",
        "Pessoas completas"]),
}
DECISOES_GATE = ["Pronto", "Pronto com condições", "Não pronto"]

ANEXOS = [
    {"id": "A", "titulo": "Riscos, dependências e pendências",
     "guia": "Só o que o PM aceitar, com dono e prazo quando informados. Tipo: risco, dependência, pendência ou "
             "condição de gate.",
     "blocos": [("tabela", "pendencias", ["ID", "Tipo", "Descrição", "Origem", "Gate", "Bloqueante", "Dono",
                                          "Prazo"], [], 3)]},
    {"id": "B", "titulo": "Versões e pedidos de mudança",
     "guia": "A versão é registrada a cada gravação. Depois do PRD assinado, toda mudança vira um pedido.",
     "blocos": [("tabela", "versoes", ["Versão", "Data", "O que mudou", "Autor"], [], 1),
                ("tabela", "mudancas", ["ID", "Data", "Pedido", "Impacto", "Decisão"], [], 1)]},
    {"id": "C", "titulo": "Dados: origem, acesso e cuidados",
     "guia": "Uma linha por D-nn da 02.5. O negócio informa o que souber; a engenharia confirma.",
     "blocos": [("tabela", "origem", ["ID", "Onde existe hoje", "Disponível hoje", "Forma de acesso",
                                      "Classificação", "Dados pessoais", "Dono do dado", "Confirmado"], [], 4)]},
    {"id": "D", "titulo": "Capacity e custos por especialidade",
     "guia": "FTE por período e especialidade. O custo por FTE só entra com fonte.",
     "blocos": [("tabela", "capacity", ["Período", "Engenharia", "Ciência", "Software", "Segurança", "Operação",
                                        "Total"], ["TOTAL"], 3),
                ("tabela", "consolidacao", ["Especialidade", "Interno ou externo", "Total FTE-mês",
                                            "Custo por FTE-mês", "Custo", "Fonte"],
                 ["Engenharia de dados", "Ciência de dados", "Software", "Segurança", "Operação"], 0)]},
    {"id": "E", "titulo": "Requisitos de IA",
     "guia": "Para modelo preditivo, IA generativa ou agente. Bom quando o limiar e o conjunto de avaliação "
             "existem antes do build, com dono, e toda decisão de risco tem revisão humana.",
     "blocos": [("campos", [("Tipo de IA", ["Modelo preditivo", "IA generativa", "Agente", "Regras"]),
                            "Tarefa ou decisão apoiada", "Entradas e saídas, com exemplos", "Métrica técnica",
                            "Métrica de negócio", "Limiar para ir à produção", "Comparação com o jeito atual",
                            "Conjunto de avaliação e quem valida", "Revisão humana",
                            "Limites e o que fazer quando falha", "Transparência para o usuário",
                            "Vieses e equidade", "Monitoramento e gatilho de revisão", "Custo por uso"])]},
]


def rotulo(campo):
    return campo[0] if isinstance(campo, tuple) else campo


def opcoes(campo):
    return campo[1] if isinstance(campo, tuple) else None


def secao(sid):
    """A seção ou o anexo pelo ID ("01.1", "A")."""
    for s in SECOES + ANEXOS:
        if s["id"] == sid:
            return s
    raise KeyError(sid)

# ==== produto/assistente-de-prd/codigo/prd_docx.py
# ---------------------------------------------------------------- PRD: leitura e gravação do .docx
# Montado depois de estrutura.py (usa SECOES, CANVAS, ANEXOS, GATES, rotulo, opcoes, secao sem importar).
# Este módulo só lê e grava dados. Quem julga a qualidade de cada seção é o agente.
import copy
import re
import unicodedata
from datetime import date

from docx import Document
from docx.oxml.ns import qn
from docx.shared import RGBColor

GUIA_COR = "808080"
MARCADO, VAZIO_OP = "☒", "☐"


class PedidoInvalido(Exception):
    """Erro no pedido de gravação: nada é gravado."""


def _n(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9.%/ ]", " ", t)).strip()


def _eh_guia(run):
    try:
        cor = run.font.color.rgb if run.font.color is not None and run.font.color.type is not None else None
    except Exception:
        cor = None
    return bool(run.italic) and cor is not None and str(cor).upper() == GUIA_COR


def _texto_celula(cel, pular=0):
    """Texto de uma célula sem a orientação em cinza; `pular` ignora os primeiros parágrafos (título do bloco)."""
    linhas = []
    for p in cel.paragraphs[pular:]:
        t = "".join(r.text for r in p.runs if not _eh_guia(r)).strip()
        if t:
            linhas.append(t)
    return "\n".join(linhas)


def _opcao_valor(texto):
    """'☒ Sim   ☐ Não' -> 'Sim'; só caixas vazias -> ''; texto livre -> o próprio texto."""
    if VAZIO_OP not in texto and MARCADO not in texto:
        return texto
    marcadas = re.findall(r"☒\s*([^☐☒]+)", texto)
    return "; ".join(m.strip() for m in marcadas)


def _nivel(par):
    try:
        nome = (par.style.name or "").lower()
    except Exception:
        nome = ""
    m = re.search(r"(heading|t[ií]tulo)\s*(\d)", nome)
    if m:
        return int(m.group(2))
    ppr = par._p.pPr
    ol = ppr.find(qn("w:outlineLvl")) if ppr is not None else None
    return int(ol.get(qn("w:val"))) + 1 if ol is not None else None


_CANVAS_POR_NOME = {_n(v[0]): k for k, v in CANVAS.items()}


def _mapa(doc):
    """{chave: [tabelas na ordem]}. Chaves: painel, checkpoints, gates, painel_bc, pessoas, '01.1'…,
    'canvas:eng'…, 'gate1', 'gate2', 'A'…'E'. A chave vem do título (Heading) que precede a tabela."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    mapa, atual = {}, None
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            par = Paragraph(el, doc)
            nivel = _nivel(par)
            if not nivel:
                continue
            t = par.text.strip()
            n = _n(t)
            if nivel == 1:
                m = re.match(r"^anexo ([a-e])\b", n)
                g = re.match(r"^gate ([12])\b", n)
                atual = (m.group(1).upper() if m else f"gate{g.group(1)}" if g else
                         "painel" if n.startswith("painel") else None)
            elif nivel == 2:
                m = re.match(r"^(\d\d\.\d)\b", t)
                sub = {"checkpoints": "checkpoints", "gates": "gates", "business case": "painel_bc",
                       "pessoas": "pessoas"}
                atual = m.group(1) if m else sub.get(n, atual)
            elif nivel == 3 and n.startswith("canvas"):
                nome = _n(t.split("·", 1)[-1])
                atual = f"canvas:{_CANVAS_POR_NOME.get(nome, nome)}"
        elif el.tag == qn("w:tbl") and atual:
            mapa.setdefault(atual, []).append(Table(el, doc))
    return mapa


def _blocos_de(sid):
    """Blocos de tabela (campos e tabela) de uma seção ou anexo, na ordem do documento."""
    return [b for b in secao(sid)["blocos"] if b[0] in ("campos", "tabela")]


# ---------------------------------------------------------------- leitura

def _ler_campos(t):
    out = {}
    for row in t.rows:
        rot = _texto_celula(row.cells[0])
        if rot:
            out[rot] = _opcao_valor(_texto_celula(row.cells[-1]))
    return out


def _ler_tabela(t, fixas):
    cab = [_texto_celula(c) for c in t.rows[0].cells]
    linhas = []
    for row in t.rows[1:]:
        vals = [_opcao_valor(_texto_celula(c)) for c in row.cells]
        d = dict(zip(cab, vals))
        chave_fixa = vals and _n(vals[0]) in {_n(f) for f in fixas}
        conteudo = any(v for v in (vals[1:] if chave_fixa else vals))
        if conteudo:
            linhas.append(d)
    return linhas


def _ler_grade(t, chave):
    blocos = {}
    for row in t.rows:
        for cel in row.cells:
            if not cel.paragraphs or not cel.paragraphs[0].text.strip():
                continue
            titulo = cel.paragraphs[0].text.strip()
            blocos[titulo] = _texto_celula(cel, pular=1)
    return blocos


def ler_prd(caminho):
    """Lê o PRD e devolve um dicionário com o painel, as seções, os canvas, os gates e os anexos."""
    doc = Document(caminho)
    mapa = _mapa(doc)
    if not any(k in mapa for k in ("01.1", "painel")):
        raise ValueError("o arquivo não segue o template do PRD (não achei o painel nem a seção 01.1)")
    d = {"painel": {}, "checkpoints": {}, "gates": {}, "painel_bc": {}, "pessoas": {}, "secoes": {}, "canvas": {},
         "gate": {}, "anexos": {}}
    if mapa.get("painel"):
        d["painel"] = _ler_campos(mapa["painel"][0])
    if mapa.get("checkpoints"):
        d["checkpoints"] = {l["Etapa"][:2]: {"situacao": l.get("Situação", ""), "data": l.get("Data", "")}
                            for l in _ler_tabela(mapa["checkpoints"][0], [])}
    if mapa.get("gates"):
        d["gates"] = {l["Gate"][5:6]: {k: v for k, v in l.items() if k != "Gate"}
                      for l in _ler_tabela(mapa["gates"][0], [])}
    if mapa.get("painel_bc"):
        d["painel_bc"] = {k: v for k, v in _ler_campos(mapa["painel_bc"][0]).items() if v}
    if mapa.get("pessoas"):
        d["pessoas"] = {l["Papel"]: {k: v for k, v in l.items() if k != "Papel" and v}
                        for l in _ler_tabela(mapa["pessoas"][0], [])}
    for s in SECOES + ANEXOS:
        tabelas, blocos = mapa.get(s["id"], []), _blocos_de(s["id"])
        sec = {"campos": {}, "tabelas": {}}
        for b, t in zip(blocos, tabelas):
            if b[0] == "campos":
                sec["campos"].update(_ler_campos(t))
            else:
                sec["tabelas"][b[1]] = _ler_tabela(t, b[3])
        sec["vazia"] = not any(sec["campos"].values()) and not any(sec["tabelas"].values())
        (d["anexos"] if len(s["id"]) == 1 else d["secoes"])[s["id"]] = sec
    for chave in CANVAS:
        ts = mapa.get(f"canvas:{chave}", [])
        if len(ts) >= 2:
            ap = _ler_campos(ts[0])
            blocos = _ler_grade(ts[1], chave)
            d["canvas"][chave] = {"aplicavel": ap.get("Aplicável?", ""),
                                  "motivo": ap.get("Motivo, se não se aplica", ""), "blocos": blocos,
                                  "vazio": not any(blocos.values()) and not ap.get("Aplicável?")}
    if "04.2" in d["secoes"]:   # a 04.2 só tem os canvas: está vazia se todos estiverem
        d["secoes"]["04.2"]["vazia"] = all(c["vazio"] for c in d["canvas"].values())
    for n in ("1", "2"):
        ts = mapa.get(f"gate{n}", [])
        if ts:
            d["gate"][n] = {"checklist": _ler_tabela(ts[0], GATES[n][1]),
                            "decisao": _ler_campos(ts[1]) if len(ts) > 1 else {}}
    d["assinado"] = bool(d["painel"].get("Versão assinada"))
    return d


# ---------------------------------------------------------------- gravação

def _limpar(cel, manter=0):
    """Apaga o conteúdo da célula, mantendo os `manter` primeiros parágrafos."""
    for p in cel.paragraphs[max(manter, 1):]:
        p._p.getparent().remove(p._p)
    if manter == 0:
        p = cel.paragraphs[0]
        for r in list(p.runs):
            r._r.getparent().remove(r._r)


def _escrever(cel, texto, manter=0):
    _limpar(cel, manter)
    linhas = str(texto).split("\n") if texto is not None else [""]
    if manter == 0:
        cel.paragraphs[0].add_run(linhas[0])
        linhas = linhas[1:]
    for l in linhas:
        cel.add_paragraph(l)


def _escrever_opcao(cel, ops, valor):
    escolhidas = {_n(v) for v in (valor if isinstance(valor, list) else re.split(r";|,", str(valor)))
                  if str(v).strip()}
    desconhecidas = escolhidas - {_n(o) for o in ops}
    if desconhecidas:
        raise PedidoInvalido(f"opção desconhecida {sorted(desconhecidas)}; válidas: {', '.join(ops)}")
    _escrever(cel, "   ".join(f"{MARCADO if _n(o) in escolhidas else VAZIO_OP} {o}" for o in ops))


def _campos_por_rotulo(t):
    return {_n(_texto_celula(row.cells[0])): row for row in t.rows}


def _gravar_campos(t, lista, valores, onde):
    linhas = _campos_por_rotulo(t)
    por_rotulo = {_n(rotulo(c)): c for c in lista}
    for rot, val in valores.items():
        c = por_rotulo.get(_n(rot))
        row = linhas.get(_n(rot))
        if c is None or row is None:
            raise PedidoInvalido(f"{onde}: campo {rot!r} não existe; campos: {', '.join(rotulo(x) for x in lista)}")
        if opcoes(c):
            _escrever_opcao(row.cells[-1], opcoes(c), val)
        else:
            _escrever(row.cells[-1], val)


def _nova_linha(t, antes=None):
    modelo = t.rows[-1]._tr if antes is None else t.rows[1]._tr
    nova = copy.deepcopy(modelo)
    if antes is None:
        t._tbl.append(nova)
    else:
        antes._tr.addprevious(nova)
    from docx.table import _Row
    row = _Row(nova, t)
    for cel in row.cells:
        _escrever(cel, "")
    return row


def _gravar_linhas(t, colunas, fixas, linhas, onde):
    cab = [_n(_texto_celula(c)) for c in t.rows[0].cells]
    for l in linhas:
        extra = [k for k in l if _n(k) not in cab]
        if extra:
            raise PedidoInvalido(f"{onde}: coluna(s) {extra} não existe(m); colunas: {', '.join(colunas)}")
        chave = _n(l.get(colunas[0], ""))
        alvo = None
        for row in t.rows[1:]:
            if chave and _n(_texto_celula(row.cells[0])) == chave:
                alvo = row
                break
        if alvo is None:
            vazias = [row for row in t.rows[1:] if not any(_texto_celula(c) for c in row.cells)]
            total = next((row for row in t.rows[1:] if _n(_texto_celula(row.cells[0])) == "total"), None)
            alvo = vazias[0] if vazias else _nova_linha(t, antes=total) if total else _nova_linha(t)
        for k, v in l.items():
            _escrever(alvo.cells[cab.index(_n(k))], v)


def _gravar_grade(t, chave, blocos, onde):
    por_titulo = {}
    for row in t.rows:
        for cel in row.cells:
            if cel.paragraphs and cel.paragraphs[0].text.strip():
                por_titulo[_n(cel.paragraphs[0].text)] = cel
    for titulo, texto in blocos.items():
        cel = por_titulo.get(_n(titulo))
        if cel is None:
            validos = ", ".join(b for b, _ in CANVAS[chave][2])
            raise PedidoInvalido(f"{onde}: bloco {titulo!r} não existe; blocos: {validos}")
        _escrever(cel, texto, manter=2)


PROIBIDOS_PAINEL = {_n("Versão assinada")}


def gravar_prd(pedido, base, saida, hoje=None):
    """Grava o pedido em `base` (PRD em andamento ou template) e salva em `saida`. Devolve a lista do que foi
    gravado. Valida tudo antes: um erro no pedido levanta PedidoInvalido e nada é salvo."""
    doc = Document(base)
    mapa = _mapa(doc)
    lido = ler_prd(base)
    hoje = hoje or date.today().strftime("%d/%m/%Y")
    feito = []
    conteudo = any(pedido.get(k) for k in ("campos", "linhas", "canvas", "painel", "checkpoints", "pessoas",
                                           "pendencias", "painel_bc"))
    if lido["assinado"] and conteudo:
        raise PedidoInvalido("PRD ASSINADO: o conteúdo acordado não é reescrito. Registre a mudança em "
                             "\"mudancas\" (Anexo B) e grave só ela")

    painel = pedido.get("painel") or {}
    if any(_n(k) in PROIBIDOS_PAINEL for k in painel):
        raise PedidoInvalido("painel: \"Versão assinada\" é preenchida por quem assina, nunca pelo agente")
    if painel:
        _gravar_campos(mapa["painel"][0], PAINEL_CAMPOS, painel, "painel")
        feito.append(f"painel: {', '.join(painel)}")
    if pedido.get("painel_bc"):
        _gravar_campos(mapa["painel_bc"][0], PAINEL_BC, pedido["painel_bc"], "painel_bc")
        feito.append("painel: business case")
    for etapa, v in (pedido.get("checkpoints") or {}).items():
        num = str(etapa)[:2].zfill(2)
        nome = next((f"{n} · {t}" for n, t, _ in ETAPAS if n == num), None)
        if not nome:
            raise PedidoInvalido(f"checkpoints: etapa {etapa!r} não existe (01 a 05)")
        _gravar_linhas(mapa["checkpoints"][0], ["Etapa", "Situação", "Data"], [],
                       [{"Etapa": nome, "Situação": v.get("situacao", ""), "Data": v.get("data", hoje)}],
                       "checkpoints")
        feito.append(f"checkpoint {num}")
    for papel, v in (pedido.get("pessoas") or {}).items():
        _gravar_linhas(mapa["pessoas"][0], ["Papel", "Nome", "Área"], PESSOAS, [dict(v, Papel=papel)], "pessoas")
        feito.append(f"pessoas: {papel}")

    for sid, valores in (pedido.get("campos") or {}).items():
        try:
            blocos = _blocos_de(sid)
        except KeyError:
            raise PedidoInvalido(f"campos: seção {sid!r} não existe")
        indices = [i for i, b in enumerate(blocos) if b[0] == "campos"]
        if not indices:
            raise PedidoInvalido(f"campos: a seção {sid} não tem campos, só tabela (use \"linhas\")")
        restantes = dict(valores)
        for i in indices:
            lista = blocos[i][1]
            parte = {k: v for k, v in restantes.items() if _n(k) in {_n(rotulo(c)) for c in lista}}
            if parte:
                _gravar_campos(mapa[sid][i], lista, parte, sid)
                for k in parte:
                    restantes.pop(k)
        if restantes:
            todos = [rotulo(c) for i in indices for c in blocos[i][1]]
            raise PedidoInvalido(f"{sid}: campo(s) {list(restantes)} não existe(m); campos: {', '.join(todos)}")
        feito.append(f"{sid}: {len(valores)} campo(s)")

    for alvo, linhas in (pedido.get("linhas") or {}).items():
        sid, _, nome = alvo.partition("/")
        try:
            blocos = _blocos_de(sid)
        except KeyError:
            raise PedidoInvalido(f"linhas: seção {sid!r} não existe")
        idx = next((i for i, b in enumerate(blocos) if b[0] == "tabela" and b[1] == nome), None)
        if idx is None:
            nomes = [b[1] for b in blocos if b[0] == "tabela"]
            raise PedidoInvalido(f"linhas: tabela {alvo!r} não existe; tabelas de {sid}: {', '.join(nomes) or '—'}")
        b = blocos[idx]
        _gravar_linhas(mapa[sid][idx], b[2], b[3], linhas, alvo)
        feito.append(f"{alvo}: {len(linhas)} linha(s)")

    for chave, v in (pedido.get("canvas") or {}).items():
        if chave not in CANVAS:
            raise PedidoInvalido(f"canvas {chave!r} não existe; canvas: {', '.join(CANVAS)}")
        ts = mapa[f"canvas:{chave}"]
        cab = {}
        if "aplicavel" in v:
            cab["Aplicável?"] = v["aplicavel"]
        if v.get("motivo"):
            cab["Motivo, se não se aplica"] = v["motivo"]
        if cab:
            _gravar_campos(ts[0], [("Aplicável?", ["Sim", "Não"]), "Motivo, se não se aplica"], cab, chave)
        if v.get("blocos"):
            _gravar_grade(ts[1], chave, v["blocos"], f"canvas {chave}")
        feito.append(f"canvas {chave}: {len(v.get('blocos') or {})} bloco(s)")

    if pedido.get("pendencias"):
        b = _blocos_de("A")[0]
        _gravar_linhas(mapa["A"][0], b[2], b[3], pedido["pendencias"], "pendencias")
        feito.append(f"Anexo A: {len(pedido['pendencias'])} pendência(s)")
    if pedido.get("mudancas"):
        if any(str(v).strip() for m in pedido["mudancas"] for k, v in m.items() if _n(k) == _n("Decisão")):
            raise PedidoInvalido("mudancas: a \"Decisão\" de um pedido de mudança é preenchida por quem decide, "
                                 "nunca pelo agente")
        b = _blocos_de("B")[1]
        _gravar_linhas(mapa["B"][1], b[2], b[3], pedido["mudancas"], "mudancas")
        feito.append(f"Anexo B: {len(pedido['mudancas'])} pedido(s) de mudança")

    versao = pedido.get("versao") or {}
    if versao.get("numero"):
        b = _blocos_de("B")[0]
        _gravar_linhas(mapa["B"][0], b[2], b[3], [{"Versão": versao["numero"], "Data": hoje,
                                                    "O que mudou": versao.get("o_que_mudou", ""),
                                                    "Autor": versao.get("autor", "")}], "versão")
        if not lido["assinado"]:
            _gravar_campos(mapa["painel"][0], PAINEL_CAMPOS, {"Versão vigente": versao["numero"]}, "painel")
        feito.append(f"versão {versao['numero']}")

    produto = painel.get("Produto") or lido["painel"].get("Produto")
    if produto:
        doc.core_properties.title = f"PRD · {produto}"
    doc.save(saida)
    return feito

# ==== produto/assistente-de-prd/codigo/cli_prd.py
# ---------------------------------------------------------------- PRD: linha de comando
# O agente grava o pedido em /mnt/data/prd_pedido.json (em Python, com json.dump) e roda este script.
# Ações: "ler" (um PRD anexado) e "gravar" (no PRD em andamento ou no template que vem com a skill).
import glob
import json
import os
import sys


def _prd_base(argv):
    """(pasta de trabalho, caminho do pedido)."""
    if len(argv) > 1 and argv[1].endswith(".json") and os.path.exists(argv[1]):
        return os.path.dirname(os.path.abspath(argv[1])), os.path.abspath(argv[1])
    for pasta in ("/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(pasta, "prd_pedido.json")):
            return pasta, os.path.join(pasta, "prd_pedido.json")
    return ("/mnt/data" if os.path.isdir("/mnt/data") else os.getcwd()), None


def _prd_arquivo(base, nome):
    if os.path.isabs(nome) and os.path.exists(nome):
        return nome
    if os.path.exists(os.path.join(base, nome)):
        return os.path.join(base, nome)
    for f in os.listdir(base):
        if f.lower() == os.path.basename(nome).lower():
            return os.path.join(base, f)
    raise FileNotFoundError(f'"{nome}" não está em {base}: peça para o usuário anexar o arquivo na conversa')


def _prd_template():
    aqui = os.path.dirname(os.path.abspath(globals().get("__file__", "") or "."))
    candidatos = [os.path.join(aqui, "..", "assets", "template-prd.docx")]
    candidatos += glob.glob("/home/oai/skills/**/prd-docx/assets/template-prd.docx", recursive=True)
    for c in candidatos:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("template-prd.docx não encontrado na pasta assets da skill prd-docx")


def _prd_curto(v, n=220):
    v = str(v).replace("\n", " / ")
    return v if len(v) <= n else v[:n - 1] + "…"


def prd_resumo_texto(d):
    """A leitura em texto, etapa por etapa, só com o que tem conteúdo."""
    out = []
    p = d["painel"]
    out.append("PAINEL: " + " · ".join(f"{k}: {v}" for k, v in p.items() if v) if any(p.values())
               else "PAINEL: vazio")
    if d.get("assinado"):
        out.append("PRD ASSINADO: só pedidos de mudança (Anexo B)")
    ck = [f"{e} {v['situacao']}" for e, v in d["checkpoints"].items() if v.get("situacao")]
    out.append("Checkpoints: " + (", ".join(ck) if ck else "nenhum registrado"))
    gt = [f"Gate {g}: {v.get('Decisão')}" for g, v in d["gates"].items() if v.get("Decisão")]
    out.append("Gates: " + (", ".join(gt) if gt else "nenhuma decisão registrada"))
    pessoas = [f"{k}: {v['Nome']}" for k, v in d["pessoas"].items() if v.get("Nome")]
    if pessoas:
        out.append("Pessoas: " + "; ".join(pessoas))
    for num, titulo, _ in ETAPAS:
        out.append(f"\n== {num} · {titulo}")
        for s in (x for x in SECOES if x["etapa"] == num):
            sec = d["secoes"].get(s["id"], {})
            if sec.get("vazia", True):
                out.append(f"{s['id']} {s['titulo']}: VAZIA")
                continue
            out.append(f"{s['id']} {s['titulo']}:")
            for k, v in sec["campos"].items():
                if v:
                    out.append(f"  {k}: {_prd_curto(v)}")
            for nome, linhas in sec["tabelas"].items():
                for l in linhas:
                    out.append(f"  [{nome}] " + " | ".join(f"{k}: {_prd_curto(v, 90)}" for k, v in l.items() if v))
        if num == "04":
            for chave, c in d["canvas"].items():
                nome = CANVAS[chave][0]
                if c["vazio"]:
                    out.append(f"Canvas {nome}: VAZIO")
                    continue
                out.append(f"Canvas {nome} (aplicável: {c['aplicavel'] or '?'}{'; ' + c['motivo'] if c['motivo'] else ''}):")
                for b, v in c["blocos"].items():
                    out.append(f"  {b}: {_prd_curto(v) if v else '(vazio)'}")
    out.append("\n== Anexos")
    for a in ANEXOS:
        sec = d["anexos"].get(a["id"], {})
        n_linhas = sum(len(l) for l in sec.get("tabelas", {}).values())
        n_campos = sum(1 for v in sec.get("campos", {}).values() if v)
        out.append(f"Anexo {a['id']} {a['titulo']}: " + ("VAZIO" if sec.get("vazia", True) else
                                                         f"{n_linhas} linha(s), {n_campos} campo(s)"))
        for nome, linhas in sec.get("tabelas", {}).items():
            for l in linhas:
                out.append(f"  [{nome}] " + " | ".join(f"{k}: {_prd_curto(v, 90)}" for k, v in l.items() if v))
        for k, v in sec.get("campos", {}).items():
            if v:
                out.append(f"  {k}: {_prd_curto(v)}")
    return "\n".join(out)


def prd_ler(base, pedido):
    nome = pedido.get("arquivo") or (pedido.get("arquivos") or [None])[0]
    if not nome:
        print('Pedido sem "arquivo": diga qual PRD ler')
        return 2
    try:
        d = ler_prd(_prd_arquivo(base, nome))
    except FileNotFoundError as e:
        print(f"ERRO: {e}")
        return 1
    except Exception as e:
        print(f"ERRO ao ler {nome}: {type(e).__name__}: {e}. Se não for um PRD deste template, leia o arquivo "
              "como material de apoio")
        return 1
    json.dump(d, open(os.path.join(base, "prd_leitura.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"=== {nome}\n" + prd_resumo_texto(d))
    return 0


def prd_gravar(base, pedido):
    try:
        origem = _prd_arquivo(base, pedido["base"]) if pedido.get("base") else _prd_template()
    except FileNotFoundError as e:
        print(f"NADA FOI GRAVADO: {e}")
        return 1
    produto = (pedido.get("painel") or {}).get("Produto")
    if not produto and pedido.get("base"):
        try:
            produto = ler_prd(origem)["painel"].get("Produto")
        except Exception:
            produto = None
    produto = produto or "sem nome"
    numero = (pedido.get("versao") or {}).get("numero", "")
    saida = os.path.join(base, pedido.get("saida") or f"PRD {produto}{' v' + numero if numero else ''}.docx")
    try:
        feito = gravar_prd(pedido, origem, saida)
    except PedidoInvalido as e:
        print(f"NADA FOI GRAVADO. Corrija o pedido e rode de novo: {e}")
        return 1
    except Exception as e:
        print(f"NADA FOI GRAVADO. Erro na gravação: {type(e).__name__}: {e}. Entregue o conteúdo por seção, "
              "pronto para colar")
        return 1
    d = ler_prd(saida)
    cheias = [s for s, v in d["secoes"].items() if not v["vazia"]]
    vazias = [s for s, v in d["secoes"].items() if v["vazia"]]
    canvas = [CANVAS[k][0] for k, v in d["canvas"].items() if not v["vazio"]]
    conf = ["CONFERÊNCIA DO ARQUIVO (descreva a entrega só com o que está aqui)",
            f"Arquivo: {os.path.basename(saida)} · versão vigente: {d['painel'].get('Versão vigente') or '—'}",
            "Gravado: " + "; ".join(feito) if feito else "Gravado: nada (template vazio)",
            f"Seções com conteúdo ({len(cheias)}): {', '.join(cheias) or '—'}",
            f"Seções vazias ({len(vazias)}): {', '.join(vazias) or '—'}",
            f"Canvas com conteúdo: {', '.join(canvas) or '—'}",
            "Decisões de gate: " + (", ".join(f"Gate {g}: {v.get('Decisão')}" for g, v in d["gates"].items()
                                              if v.get("Decisão")) or "em branco")]
    json.dump({"arquivo": saida, "conferencia": conf}, open(os.path.join(base, "prd_resultado.json"), "w",
                                                              encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(conf))
    return 0


def prd_main(argv):
    base, caminho = _prd_base(argv)
    if not caminho:
        print("Pedido não encontrado: grave o pedido em /mnt/data/prd_pedido.json (em Python, com json.dump) e "
              "rode o script de novo")
        return 2
    pedido = json.load(open(caminho, encoding="utf-8"))
    acao = pedido.get("acao")
    if acao == "ler":
        return prd_ler(base, pedido)
    if acao == "gravar":
        return prd_gravar(base, pedido)
    print(f'Ação desconhecida {acao!r}: use "ler" ou "gravar"')
    return 2


if __name__ == "__main__":
    _codigo_prd = prd_main(sys.argv)
    if _codigo_prd:
        sys.exit(_codigo_prd)
