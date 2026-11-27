# Gerado por ferramentas/montar_skills.py a partir de: produto/assistente-de-prd/codigo/estrutura.py produto/assistente-de-prd/codigo/prd_docx.py produto/assistente-de-prd/codigo/resumo_prd.py produto/assistente-de-prd/codigo/cli_resumo.py. Não edite aqui.

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

# ==== produto/assistente-de-prd/codigo/resumo_prd.py
# ---------------------------------------------------------------- PRD: resumo visual por público (HTML)
# Montado depois de estrutura.py e prd_docx.py (usa ler_prd, _n, SECOES, ETAPAS, CANVAS, GATES sem importar).
# Gera um HTML de um arquivo, com uma aba por público: Sponsor, Time técnico e Revisor. Mostra o que está escrito
# no PRD, sem reescrever e sem fazer contas: cada bloco cita a seção de origem. Números aparecem como estão no PRD;
# as barras só usam o valor lido para a proporção.
import html
import os
import re

# Seções que não contam como falta quando vazias, por porte ("–" não cobrar e "○" recomendada, em prd-etapas §2)
RS_NAO_COBRA = {"P": {"01.4": "não cobrada no P", "03.2": "não cobrada no P", "04.3": "não cobrada no P"},
                "M": {"03.2": "recomendada no M", "04.3": "recomendada no M"},
                "G": {}}
RS_CONDICIONAL = {"02.3": "só se o produto calcula ou mostra indicador"}
RS_GATE_ETAPAS = {"1": ("01", "02", "03", "A1"), "2": ("04", "05", "A2")}
RS_DONO_ANEXO = {"A": "PM", "C": "Engenharia de dados, com o negócio", "D": "Especialistas",
                 "E": "Ciência de dados, com o sponsor"}

RS_CSS = r"""/* VOICE: documento de trabalho, direto, como a página de gráficos de um bom jornal.
   IDEA: a folha que cada público leva para a reunião do PRD: o sponsor, o time técnico e o revisor do gate.
   PICTURE: no topo, a trilha das 5 etapas e dos 2 gates; em cada aba, o quadro principal primeiro.
   COLOUR and TYPE: azul-ardósia do template como campo dominante, petróleo de apoio, laranja-queimado só para o que
   falta; fonte do sistema.
   LAYOUT: faixa do topo de ponta a ponta; blocos em grade de duas colunas que viram uma no celular. */
:root{color-scheme:light dark;
 --bg:light-dark(#ffffff,#10171d);--ink:light-dark(#17262f,#e6edf1);--mut:light-dark(#5a6973,#98a8b2);
 --tinta:#1F3A4D;--pet:light-dark(#22717F,#4fb9c9);--acc:light-dark(#B4501E,#ff9a62);
 --line:light-dark(#dbe3e8,#26343d);--soft:light-dark(#f2f6f8,#17232b);--petsoft:light-dark(#e2f1f3,#123038);
 --accsoft:light-dark(#fbece3,#3a2418)}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Segoe UI",system-ui,-apple-system,Arial,sans-serif}
h1,h2,h3,h4{margin:0;line-height:1.2;text-wrap:balance}p{margin:0 0 .5em}
small{font-size:13px;color:var(--mut)}
.topo{background:var(--tinta);color:#fff}
.topo .in{max-width:1200px;margin:0 auto;padding:clamp(22px,4vw,40px) max(4vw,16px) 16px}
.marca{font-size:13px;opacity:.75;margin:0 0 6px}
h1{font-size:clamp(30px,5vw,44px);font-weight:700}
.meta{font-size:14px;opacity:.85;margin-top:8px}
.trilha{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 0;padding:0}
.trilha li{flex:1 1 120px;padding:9px 11px;border-top:4px solid rgba(255,255,255,.25);background:rgba(255,255,255,.06)}
.trilha li b{display:block;font-size:14px}.trilha li span{font-size:13px;opacity:.85}
.trilha .feito{border-color:#5fd0de}.trilha .atual{border-color:#ffb38a;background:rgba(255,179,138,.12)}
.trilha .gate{flex-basis:150px}
.abas{max-width:1200px;margin:0 auto;padding:0 max(4vw,16px);display:flex;gap:4px;flex-wrap:wrap}
.abas button{font:inherit;color:#fff;background:none;border:0;cursor:pointer;padding:12px 18px;min-height:44px;
 border-radius:8px 8px 0 0;font-weight:600;opacity:.8}
.abas button[aria-selected=true]{background:var(--bg);color:var(--ink);opacity:1}
.abas button:focus-visible{outline:3px solid #5fd0de;outline-offset:-3px}
main{max-width:1200px;margin:0 auto;padding:22px max(4vw,16px) 8px}
.js section[role=tabpanel][hidden]{display:none}
section[role=tabpanel]>h2{font-size:15px;color:var(--mut);font-weight:600;margin:0 0 14px}
.grade{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-bottom:18px}.grade>.bloco{margin:0}
.bloco{border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:18px}
.bloco.abre{border-color:transparent;background:var(--soft)}
.bloco>header{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin-bottom:12px}
.bloco>header h3{font-size:20px;flex:1 1 auto}
.secs{display:inline-flex;flex-wrap:wrap;gap:4px}
.sec{font-size:12px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:1px 8px;white-space:nowrap}
.frase{font-size:20px;line-height:1.4;font-weight:600}
.kv{display:grid;grid-template-columns:minmax(0,12em) minmax(0,1fr);gap:6px 14px;margin:0}
.kv dt{color:var(--mut);font-size:14px}.kv dd{margin:0;white-space:pre-line}
.vazio{color:var(--mut);font-style:italic}
.validar{display:inline-block;font-size:12px;font-weight:600;color:var(--acc);background:var(--accsoft);
 border-radius:999px;padding:0 8px;margin-left:4px;font-style:normal}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}
.kpis div{background:var(--bg);border-radius:8px;padding:12px}.kpis strong{display:block;font-size:22px;line-height:1.2}
.legenda{font-size:13px;color:var(--mut);margin:6px 0}.legenda i{display:inline-block;width:12px;height:12px;border-radius:2px;
 margin:0 4px 0 10px;vertical-align:-1px}
i.b{background:var(--pet)}i.c{background:var(--tinta);opacity:.55}
.ano{display:grid;grid-template-columns:3.8em minmax(0,1fr) 10em;gap:10px;align-items:center;padding:5px 0}
.ano i{display:block;height:13px;border-radius:0 3px 3px 0;margin:2px 0}
.num{text-align:right;font-variant-numeric:tabular-nums;font-size:13px;line-height:1.3}
.releases{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.releases>div{background:var(--soft);border-radius:8px;padding:12px 14px}
.releases h4{font-size:16px;margin-bottom:4px}.releases ul{list-style:none;margin:10px 0 0;padding:0}
.releases li{padding:8px 0;border-top:1px solid var(--line);font-size:15px}
.aceite{display:block;font-size:13px;color:var(--mut);margin-top:3px}.aceite.falta{color:var(--acc);font-weight:600}
.pri{display:inline-block;font-size:12px;font-weight:600;border-radius:4px;padding:0 6px;margin-right:6px;background:var(--line)}
.pri.must{background:var(--pet);color:#fff}.pri.should{background:var(--petsoft);color:var(--pet)}
.lista{list-style:none;margin:0;padding:0}.lista li{padding:8px 0;border-top:1px solid var(--line)}
.lista li:first-child{border-top:0}.lista b,.lista small{display:block}
.pede{border-color:var(--acc);border-width:2px}
.canvas{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.canvas>div{border-radius:8px;padding:12px 14px;background:var(--soft);border-left:4px solid var(--pet)}
.canvas .na{border-color:var(--line);opacity:.8}.canvas .parcial{border-color:var(--acc)}
.canvas b,.canvas small{display:block}.canvas .conta{font-size:13px;font-weight:600;color:var(--pet);margin:4px 0}
.canvas .parcial .conta{color:var(--acc)}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-size:13px;color:var(--mut);font-weight:600;border-bottom:2px solid var(--line);padding:6px 8px}
td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top;white-space:pre-line}
td.curto{white-space:nowrap}
.scroll{overflow-x:auto}
.etapas{display:grid;gap:14px}
.etapa{display:grid;grid-template-columns:minmax(0,12em) minmax(0,1fr);gap:8px 16px;padding-top:12px;border-top:1px solid var(--line)}
.etapa:first-child{border-top:0;padding-top:0}.etapa .conta{display:block;font-size:13px;font-weight:600;color:var(--pet)}
.etapa .conta.falta{color:var(--acc)}
.tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px}
.tiles li{padding:8px 10px;border-radius:8px;border:2px solid var(--line);font-size:14px}
.tiles li b{color:var(--mut);margin-right:6px;font-size:13px}.tiles li small{display:block;line-height:1.35;margin-top:2px}
.tiles .ok{border-color:var(--petsoft)}.tiles .ok small{color:var(--pet)}
.tiles .falta{border-color:var(--acc);background:var(--accsoft)}.tiles .falta small{color:var(--acc)}
.tiles .nc{border-style:dashed;opacity:.75}
.gates{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.gates>div{border-radius:8px;padding:12px 14px;background:var(--soft)}.gates strong{display:block;font-size:20px}
.gates .aberto strong{color:var(--acc)}.gates ol{margin:8px 0 0;padding-left:1.2em;font-size:14px;color:var(--mut)}
.aviso{border-left:4px solid var(--acc);background:var(--accsoft);padding:10px 14px;border-radius:0 8px 8px 0;margin-bottom:10px}
.ok-txt{color:var(--pet);font-weight:600}
.log{list-style:none;margin:0;padding:0}.log li{display:grid;grid-template-columns:4em 6.5em minmax(0,1fr);gap:8px;
 padding:6px 0;border-top:1px solid var(--line);font-size:14px}.log li:first-child{border-top:0}
footer{max-width:1200px;margin:0 auto;padding:10px max(4vw,16px) 30px;font-size:13px;color:var(--mut)}
@media (max-width:760px){.grade,.gates{grid-template-columns:1fr}.kv,.etapa{grid-template-columns:1fr}
 .bloco{padding:14px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.kpis strong{font-size:19px}table{font-size:13px}td,th{padding:6px 5px}
 .ano{grid-template-columns:3.2em minmax(0,1fr) 6.2em}}
@media print{.abas{display:none}section[role=tabpanel][hidden]{display:block!important}.topo{background:#fff;color:#000}}
"""

RS_JS = r"""document.documentElement.classList.add('js');
const abas=[...document.querySelectorAll('.abas button')];
function abrir(b){abas.forEach(x=>{const s=x===b;x.setAttribute('aria-selected',s);x.tabIndex=s?0:-1;
 document.getElementById(x.getAttribute('aria-controls')).hidden=!s});}
abas.forEach((b,i)=>{b.addEventListener('click',()=>abrir(b));
 b.addEventListener('keydown',e=>{const d={ArrowRight:1,ArrowLeft:-1}[e.key];if(d){const n=abas[(i+d+abas.length)%abas.length];
 abrir(n);n.focus();}});});
abrir(abas[0]);"""


def rs_e(t):
    """Escapa o texto e mostra "[validar: …]" como etiqueta."""
    t = html.escape(str(t or "").strip())
    return re.sub(r"\[validar:\s*([^\]]+)\]", r'<span class="validar">validar: \1</span>', t)


def rs_reais(t):
    """Valor em reais de um texto do PRD ("R$ 900 mil", "−R$ 208 mil", "R$ 3,6 milhões"), só para a proporção das
    barras. None se não houver valor."""
    m = re.search(r"([−-])?\s*R\$\s*([\d.]+(?:,\d+)?)\s*(mil|milh[õo]es|milh[ãa]o|mi|bi)?", str(t or ""))
    if not m:
        return None
    v = float(m.group(2).replace(".", "").replace(",", "."))
    suf = (m.group(3) or "").lower()
    v *= 1e3 if suf == "mil" else 1e6 if suf.startswith("mi") else 1e9 if suf == "bi" else 1
    return -v if m.group(1) else v


def rs_secs(*ids):
    return '<span class="secs">' + "".join(f'<span class="sec">{html.escape(i)}</span>' for i in ids if i) + "</span>"


def rs_bloco(titulo, corpo, secs=(), classe=""):
    return (f'<article class="bloco {classe}"><header><h3>{rs_e(titulo)}</h3>{rs_secs(*secs)}</header>'
            f"{corpo}</article>")


def rs_vazio(sid):
    return f'<p class="vazio">Ainda não preenchido no PRD ({html.escape(sid)}).</p>'


def rs_kv(pares):
    itens = [(k, v) for k, v in pares if v]
    if not itens:
        return ""
    return "<dl class=kv>" + "".join(f"<dt>{rs_e(k)}</dt><dd>{rs_e(v)}</dd>" for k, v in itens) + "</dl>"


def rs_tabela(linhas, colunas=None):
    if not linhas:
        return ""
    colunas = colunas or list(linhas[0])
    colunas = [c for c in colunas if any(l.get(c) for l in linhas)]
    cab = "".join(f"<th>{rs_e(c)}</th>" for c in colunas)
    def td(l, i, col):
        v = l.get(col, "")
        return f'<td class="curto">{rs_e(v)}</td>' if i == 0 and len(str(v)) <= 8 else f"<td>{rs_e(v)}</td>"

    corpo = "".join("<tr>" + "".join(td(l, i, col) for i, col in enumerate(colunas)) + "</tr>" for l in linhas)
    return f'<div class="scroll"><table><thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table></div>'


def rs_contexto(d):
    """Tudo o que as abas usam, lido uma vez."""
    S = d["secoes"]

    def campo(sid, rot):
        alvo = S.get(sid) or d["anexos"].get(sid) or {}
        for r, v in alvo.get("campos", {}).items():
            if _n(r) == _n(rot):
                return v
        return ""

    def linhas(sid, nome):
        alvo = S.get(sid) or d["anexos"].get(sid) or {}
        return [l for l in alvo.get("tabelas", {}).get(nome, []) if any(l.values())]

    porte = (d["painel"].get("Porte") or "").strip()[:1].upper()
    sponsor = (d["pessoas"].get("Sponsor") or {}).get("Nome", "")
    return {"d": d, "S": S, "campo": campo, "linhas": linhas, "porte": porte if porte in RS_NAO_COBRA else "",
            "sponsor": sponsor, "produto": d["painel"].get("Produto") or "PRD"}


def rs_gate_alvo(d):
    if d["assinado"]:
        return None
    if not (d["gates"].get("1") or {}).get("Decisão"):
        return "1"
    if not (d["gates"].get("2") or {}).get("Decisão"):
        return "2"
    return None


def rs_ia(c):
    tipo = c["campo"]("03.1", "Tipo de produto")
    return (_n(c["campo"]("04.4", "Há IA na solução?")) == "sim" or any(t in tipo for t in ("Modelo", "Agente"))
            or not c["d"]["anexos"].get("E", {}).get("vazia", True))


def rs_completude(c):
    """Por etapa: (sid, título, dono, situação) com situação ok, falta, nc (não cobrada ou condicional)."""
    nao = RS_NAO_COBRA.get(c["porte"], {})
    out = {}
    for num, _, _ in ETAPAS:
        itens = []
        for s in (x for x in SECOES if x["etapa"] == num):
            vazia = c["S"].get(s["id"], {}).get("vazia", True)
            if not vazia:
                sit, nota = "ok", "com conteúdo"
            elif s["id"] in nao:
                sit, nota = "nc", nao[s["id"]]
            elif s["id"] in RS_CONDICIONAL:
                sit, nota = "nc", RS_CONDICIONAL[s["id"]]
            else:
                sit, nota = "falta", f"vazia · {s['dono']}"
            itens.append((s["id"], s["titulo"], s["dono"], sit, nota))
        out[num] = itens
    for chave, ids in (("A1", ["A"]), ("A2", ["C", "D"] + (["E"] if rs_ia(c) else []))):
        itens = []
        for a in (x for x in ANEXOS if x["id"] in ids):
            vazia = c["d"]["anexos"].get(a["id"], {}).get("vazia", True)
            dono = RS_DONO_ANEXO[a["id"]]
            itens.append((f"Anexo {a['id']}", a["titulo"], dono, "falta" if vazia else "ok",
                          f"vazio · {dono}" if vazia else "com conteúdo"))
        out[chave] = itens
    return out


def rs_divergencias(c):
    """Checagens que dá para fazer sem julgar o texto: o escopo da R1 e os dados no Anexo C."""
    out = []
    rfs = c["linhas"]("02.1", "rfs")
    r1_rfs = {l["ID"].strip() for l in rfs if l.get("ID") and _n(l.get("Release")) == "r1"}
    r1 = next((l for l in c["linhas"]("02.2", "releases") if _n(l.get("Release")) == "r1"), None)
    if r1 and r1_rfs:
        mapa = set(re.findall(r"RF-\d+", r1.get("RFs incluídos", "")))
        so_rf, so_mapa = sorted(r1_rfs - mapa), sorted(mapa - r1_rfs)
        if so_rf:
            out.append(f"{', '.join(so_rf)} com release R1 na 02.1, mas fora da R1 no mapa de releases (02.2)")
        if so_mapa:
            out.append(f"{', '.join(so_mapa)} na R1 do mapa de releases (02.2), mas sem release R1 na 02.1")
    for l in rfs:
        if _n(l.get("Prioridade")) == "must" and l.get("Release") and _n(l["Release"]) != "r1":
            out.append(f"{l.get('ID')} é Must, mas está na {l['Release']} (02.1)")
    dados = {l["ID"].strip() for l in c["linhas"]("02.5", "dados") if l.get("ID")}
    origem = {l["ID"].strip() for l in c["linhas"]("C", "origem") if l.get("ID")}
    if origem and dados - origem:
        out.append(f"{', '.join(sorted(dados - origem))} na 02.5, mas sem origem no Anexo C")
    return out


# ---------------------------------------------------------------- topo

def rs_topo(c, gate):
    d = c["d"]
    p = d["painel"]
    meta = " · ".join(x for x in (p.get("Tipo"), f"Porte {p['Porte']}" if p.get("Porte") else "",
                                  f"Versão {p['Versão vigente']}" if p.get("Versão vigente") else "",
                                  f"Assinada: {p['Versão assinada']}" if p.get("Versão assinada") else "",
                                  f"Horizonte {p['Horizonte do business case']}" if p.get(
                                      "Horizonte do business case") else "") if x)
    atual = (p.get("Etapa atual") or "").strip()[:2]
    trilha = []
    for num, titulo, _ in ETAPAS:
        ck = d["checkpoints"].get(num) or {}
        cl = "feito" if ck.get("situacao") else "atual" if num == atual else ""
        estado = (f"{ck['situacao']}{' · ' + ck['data'] if ck.get('data') else ''}" if ck.get("situacao")
                  else "em andamento" if num == atual else "")
        trilha.append(f'<li class="{cl}"><b>{num} · {rs_e(titulo)}</b><span>{rs_e(estado)}</span></li>')
        if num in ("03", "05"):
            g = "1" if num == "03" else "2"
            dec = d["gates"].get(g) or {}
            nome = GATES[g][0]
            cl = "feito" if dec.get("Decisão") else "atual" if gate == g else ""
            estado = f"{dec['Decisão']}{' · ' + dec['Data'] if dec.get('Data') else ''}" if dec.get("Decisão") \
                else "próximo" if gate == g else ""
            trilha.append(f'<li class="gate {cl}"><b>{rs_e(nome)}</b><span>{rs_e(estado)}</span></li>')
    return (f'<header class="topo"><div class="in"><p class="marca">PRD · Product Requirements Document</p>'
            f"<h1>{rs_e(c['produto'])}</h1><p class=meta>{rs_e(meta)}</p>"
            f'<ol class="trilha">{"".join(trilha)}</ol></div>'
            '<nav class="abas" role="tablist" aria-label="Públicos">'
            '<button role="tab" id="t-sponsor" aria-controls="p-sponsor">Sponsor</button>'
            '<button role="tab" id="t-tecnico" aria-controls="p-tecnico">Time técnico</button>'
            '<button role="tab" id="t-revisor" aria-controls="p-revisor">Revisor</button></nav></header>')


# ---------------------------------------------------------------- aba Sponsor

def rs_valor(c):
    d = c["d"]
    bc = d["painel_bc"]
    tiles = "".join(f"<div><small>{rs_e(k)}</small><strong>{rs_e(v)}</strong></div>" for k, v in bc.items() if v)
    corpo = f'<div class="kpis">{tiles}</div>' if tiles else ""
    linhas_bc = c["linhas"]("04.6", "bc")
    anos = [k for k in (linhas_bc[0] if linhas_bc else {}) if k.startswith("Ano")]
    ben = next((l for l in linhas_bc if _n(l.get("Linha")).startswith("beneficio")), None)
    custos = [l for l in linhas_bc if _n(l.get("Linha")).startswith(("build", "run"))]
    if ben and anos:
        vals = []
        for a in anos:
            b = rs_reais(ben.get(a)) or 0
            cu = sum((rs_reais(l.get(a)) or 0) for l in custos)
            vals.append((a, b, cu, ben.get(a, ""), " + ".join(l.get(a, "") for l in custos if l.get(a))))
        topo_ = max([max(b, cu) for _, b, cu, _, _ in vals] + [1])
        barras = "".join(
            f'<div class="ano"><span>{rs_e(a)}</span><span><i class=b style="width:{b / topo_ * 100:.1f}%"></i>'
            f'<i class=c style="width:{cu / topo_ * 100:.1f}%"></i></span>'
            f'<span class=num>{rs_e(tb) or "—"}<br><small>{rs_e(tc) or "—"}</small></span></div>'
            for a, b, cu, tb, tc in vals)
        corpo += (f'<p class=legenda><i class=b></i>Benefício<i class=c></i>Build + run</p>{barras}')
    elif c["linhas"]("03.3", "valores"):
        corpo += rs_tabela(c["linhas"]("03.3", "valores"))
    kpis = c["linhas"]("03.3", "kpis")
    if kpis:
        corpo += "<h4 style='margin:16px 0 6px'>Como o benefício é medido</h4>" + rs_tabela(
            kpis, ["KPI", "Baseline", "Meta e prazo", "Método e responsável", "Release"])
    corpo += rs_kv([("Premissas", c["campo"]("03.3", "Premissas do benefício")),
                    ("Sensibilidade", c["campo"]("04.6", "Sensibilidade (benefício 30% menor)"))])
    return rs_bloco("Quanto vale", corpo or rs_vazio("03.3 e 04.6"), ("03.3", "04.5", "04.6"))


def rs_releases(c):
    rfs = c["linhas"]("02.1", "rfs")
    rels = c["linhas"]("02.2", "releases")
    nomes = [r.get("Release", "") for r in rels] or sorted({r.get("Release", "") for r in rfs if r.get("Release")})
    if not nomes and not rfs:
        return rs_bloco("O que entra em cada release", rs_vazio("02.1 e 02.2"), ("02.1", "02.2"))
    colunas = []
    for nome in nomes:
        r = next((x for x in rels if x.get("Release") == nome), {})
        itens = []
        for rf in (x for x in rfs if _n(x.get("Release")) == _n(nome)):
            pri = rf.get("Prioridade", "")
            crit = rf.get("Critério de aceite", "")
            aceite = (f'<span class="aceite">{rs_e(crit)}</span>' if crit else
                      '<span class="aceite falta">sem critério de aceite</span>' if _n(nome) == "r1" else "")
            itens.append(f'<li><span class="pri {_n(pri)}">{rs_e(pri) or "—"}</span><b>{rs_e(rf.get("ID"))}</b> '
                         f'{rs_e(rf.get("A solução deverá"))}{aceite}</li>')
        meta = " · ".join(x for x in (r.get("Data-alvo"), r.get("Critério de saída") and "saída: " + r["Critério de saída"]) if x)
        colunas.append(f'<div><h4>{rs_e(nome)}</h4><p>{rs_e(r.get("Objetivo"))}</p><small>{rs_e(meta)}</small>'
                       f'<ul>{"".join(itens)}</ul></div>')
    sem = [x for x in rfs if not x.get("Release")]
    corpo = f'<div class="releases">{"".join(colunas)}</div>'
    if sem:
        corpo += f'<p class="aviso">Sem release: {rs_e(", ".join(x.get("ID", "") for x in sem))} (02.1)</p>'
    fora = c["linhas"]("02.6", "fora")
    if fora:
        corpo += "<h4 style='margin:16px 0 6px'>Fora do escopo</h4><ul class=lista>" + "".join(
            f"<li><b>{rs_e(f.get('Item'))}</b><small>{rs_e(f.get('Motivo'))}"
            f"{' · reavaliar: ' + rs_e(f['Reavaliar quando']) if f.get('Reavaliar quando') else ''}</small></li>"
            for f in fora) + "</ul>"
    return rs_bloco("O que entra em cada release", corpo, ("02.1", "02.2", "02.6"))


def rs_golive(c):
    sid = "05.1" if not c["S"].get("05.1", {}).get("vazia", True) else "03.4"
    campos = ["Forma de lançamento", "O que a solução substitui", "Convivência com a solução atual",
              "Critério para desligar a solução atual", "Time do negócio na transição", "Dono da mudança"]
    corpo = rs_kv([(k, c["campo"](sid, k)) for k in campos])
    fases = [f for f in c["linhas"]("05.3", "fases") if _n(f.get("O que acontece")) != "n/a"]
    if fases:
        corpo += "<h4 style='margin:16px 0 6px'>Fases</h4><ul class=lista>" + "".join(
            f"<li><b>{rs_e(f.get('Fase'))} · {rs_e(f.get('Início e fim'))}</b>"
            f"<small>{rs_e(f.get('O que acontece'))}{' · saída: ' + rs_e(f['Critério de saída']) if f.get('Critério de saída') else ''}</small></li>"
            for f in fases) + "</ul>"
    corpo += rs_kv([("Gatilhos de rollback", c["campo"]("05.5", "Gatilhos de rollback")),
                    ("Solução atual disponível até", c["campo"]("05.5", "Solução atual disponível até"))])
    return rs_bloco("Como entra em produção", corpo or rs_vazio("03.4 e 05.1"), (sid, "05.3", "05.5"))


def rs_pede(c, comp):
    """O que o PRD pede do sponsor: pendências dele, seções vazias que ele preenche e o gate."""
    nome = c["sponsor"]
    itens = []
    for p in c["linhas"]("A", "pendencias"):
        if nome and _n(nome) in _n(p.get("Dono")):
            itens.append((p.get("Descrição", ""), f"{p.get('ID', '')} · {p.get('Tipo', '')}"
                          f"{' · prazo ' + p['Prazo'] if p.get('Prazo') else ''}"
                          f"{' · bloqueia' if _n(p.get('Bloqueante')) == 'sim' else ''}", p.get("Origem", "")))
    for itens_etapa in comp.values():
        for sid, tit, dono, sit, _ in itens_etapa:
            if sit == "falta" and "sponsor" in _n(dono):
                itens.append((f"Preencher {tit}", dono, sid))
    if not itens:
        return ""
    lis = "".join(f"<li><b>{rs_e(a)}</b><small>{rs_e(b)}{' · ' + rs_e(s) if s else ''}</small></li>"
                  for a, b, s in itens[:8])
    titulo = f"O que o PRD pede de {nome}" if nome else "O que o PRD pede do sponsor"
    return rs_bloco(titulo, f"<ul class=lista>{lis}</ul>", ("Anexo A",), "pede")


def rs_aba_sponsor(c, comp):
    prob = c["campo"]("01.1", "Problema ou oportunidade")
    corpo = (f'<p class="frase">{rs_e(prob)}</p>' if prob else rs_vazio("01.1")) + rs_kv(
        [("Por que agora", c["campo"]("01.1", "Por que agora")), ("Quem sente a dor", c["campo"]("01.1", "Quem sente a dor"))])
    dor = c["linhas"]("01.3", "dimensoes")
    if dor:
        corpo += "<h4 style='margin:14px 0 6px'>Tamanho da dor hoje</h4>" + rs_tabela(
            dor, ["Dimensão", "Indicador atual", "Ordem de grandeza", "Fonte"])
    sol = rs_kv([("O que a solução faz", c["campo"]("03.1", "O que a solução faz")),
                 ("Decisão apoiada", c["campo"]("03.1", "Decisão ou processo apoiado")),
                 ("Onde é consumida", c["campo"]("03.1", "Onde e como é consumida"))])
    return ("<h2>Para o sponsor: a dor, o valor, o escopo e o que se espera de você</h2>"
            f'<div class="grade">{rs_bloco("O problema", corpo, ("01.1", "01.3"), "abre")}'
            f'{rs_bloco("A solução", sol or rs_vazio("03.1"), ("03.1",), "abre")}</div>'
            f"{rs_valor(c)}{rs_releases(c)}<div class=grade>{rs_golive(c)}{rs_pede(c, comp) or ''}</div>")


# ---------------------------------------------------------------- aba Time técnico

def rs_aba_tecnico(c):
    d = c["d"]
    corpo = rs_kv([("Desenho", c["campo"]("04.1", "Desenho")), ("Aderência ao padrão", c["campo"]("04.1", "Aderência ao padrão"))])
    corpo += rs_tabela(c["linhas"]("04.1", "componentes"))
    arq = rs_bloco("Arquitetura", corpo or rs_vazio("04.1"), ("04.1",), "abre")
    dt = c["linhas"]("04.3", "decisoes")
    dec = rs_bloco("Decisões de arquitetura", rs_tabela(dt) or rs_vazio("04.3"), ("04.3",))

    origem = {l.get("ID", "").strip(): l for l in c["linhas"]("C", "origem")}
    dados = []
    for l in c["linhas"]("02.5", "dados"):
        o = origem.get(l.get("ID", "").strip(), {})
        dados.append({"ID": l.get("ID"), "Informação": l.get("Informação"), "Para qual RF": l.get("Para qual RF"),
                      "Frequência": l.get("Frequência"), "Onde existe hoje": o.get("Onde existe hoje", ""),
                      "Acesso": o.get("Forma de acesso", ""), "Classificação": o.get("Classificação", ""),
                      "Dados pessoais": o.get("Dados pessoais", ""), "Dono do dado": o.get("Dono do dado", "")})
    dados_b = rs_bloco("Do dado ao uso", rs_tabela(dados) or rs_vazio("02.5"), ("02.5", "Anexo C"))

    cards = []
    for chave, (nome, quando, blocos) in CANVAS.items():
        cv = d["canvas"].get(chave) or {}
        titulos = [b for b, _ in blocos]
        cheios = [b for b in titulos if (cv.get("blocos") or {}).get(b)]
        if _n(cv.get("aplicavel")) == "nao":
            cards.append(f'<div class="na"><b>{rs_e(nome)}</b><span class=conta>Não se aplica</span>'
                         f'<small>{rs_e(cv.get("motivo")) or "sem motivo registrado"}</small></div>')
            continue
        cl = "" if len(cheios) == len(titulos) else "parcial"
        esforco = (cv.get("blocos") or {}).get(titulos[-1], "")
        cards.append(f'<div class="{cl}"><b>{rs_e(nome)}</b><span class=conta>{len(cheios)} de {len(titulos)} blocos'
                     f'</span><small>{rs_e(esforco) if esforco else rs_e(quando)}</small></div>')
    canvas = rs_bloco("Canvas por especialidade", f'<div class="canvas">{"".join(cards)}</div>', ("04.2",))

    nfr = rs_bloco("Requisitos não funcionais", rs_tabela(c["linhas"]("02.4", "nfr")) or rs_vazio("02.4"), ("02.4",))
    ia = ""
    if rs_ia(c):
        campos = ["Tipo de IA", "Tarefa ou decisão apoiada", "Métrica técnica", "Limiar para ir à produção",
                  "Comparação com o jeito atual", "Conjunto de avaliação e quem valida", "Revisão humana",
                  "Limites e o que fazer quando falha", "Monitoramento e gatilho de revisão", "Custo por uso"]
        corpo = rs_kv([(k, c["campo"]("E", k)) for k in campos])
        if not c["campo"]("E", "Limiar para ir à produção"):
            corpo = '<p class="aviso">Há IA na solução e o limiar para ir à produção ainda não está no Anexo E.</p>' + corpo
        ia = rs_bloco("Requisitos de IA", corpo, ("04.4", "Anexo E"))
    custos = rs_bloco("Custos", rs_tabela(c["linhas"]("04.5", "custos")) or rs_vazio("04.5"), ("04.5", "Anexo D"))
    cut = rs_kv([(k, c["campo"]("05.5", k)) for k in ("Cutover (sequência, janela e dono)", "Contingência",
                                                       "Gatilhos de rollback", "Como voltar", "Tempo máximo para voltar",
                                                       "Quem decide e como comunica", "Solução atual disponível até")])
    cutb = rs_bloco("Cutover, contingência e rollback", cut or rs_vazio("05.5"), ("05.5",))
    return ("<h2>Para o time técnico: arquitetura, dados, canvas, custos e a virada</h2>"
            f"<div class=grade>{arq}{dec}</div>{dados_b}{canvas}<div class=grade>{nfr}{ia or cutb}</div>"
            f"{custos}{cutb if ia else ''}")


# ---------------------------------------------------------------- aba Revisor

def rs_aba_revisor(c, comp, gate, divergencias):
    d = c["d"]
    etapas = []
    linhas_ = [(num, f"{num} · {titulo}") for num, titulo, _ in ETAPAS]
    linhas_.insert(3, ("A1", "Anexo do Gate 1"))
    linhas_.append(("A2", "Anexos do Gate 2"))
    for num, titulo in linhas_:
        itens = comp[num]
        cheias = sum(1 for x in itens if x[3] == "ok")
        cobradas = sum(1 for x in itens if x[3] != "nc")
        faltam = sum(1 for x in itens if x[3] == "falta")
        tiles = "".join(f'<li class="{sit}"><b>{rs_e(sid)}</b>{rs_e(tit)}<small>{rs_e(nota)}</small></li>'
                        for sid, tit, _, sit, nota in itens)
        etapas.append(f'<div class="etapa"><div><b>{rs_e(titulo)}</b>'
                      f'<span class="conta{" falta" if faltam else ""}">{cheias} de {cobradas} com conteúdo</span></div>'
                      f'<ul class="tiles">{tiles}</ul></div>')
    nota = ("Completude, não qualidade: o \"bom quando\" de cada seção é conferido no checkpoint e no gate."
            + ("" if c["porte"] else " Sem porte no painel: todas as seções contam."))
    comp_b = rs_bloco("O que está preenchido", f'<p class=legenda>{rs_e(nota)}</p><div class="etapas">{"".join(etapas)}</div>',
                      ("01 a 05",))
    gates = []
    for g in ("1", "2"):
        nome, checklist = GATES[g]
        dec = d["gates"].get(g) or {}
        info = (d.get("gate") or {}).get(g, {}).get("decisao", {}) or dec
        estado = dec.get("Decisão") or ("próximo gate" if gate == g else "ainda não")
        extra = " · ".join(x for x in (info.get("Condições") and "condições: " + info["Condições"],
                                       dec.get("Quem decidiu"), dec.get("Data")) if x)
        gates.append(f'<div class="{"" if dec.get("Decisão") else "aberto"}"><small>{rs_e(nome)}</small>'
                     f'<strong>{rs_e(estado)}</strong><small>{rs_e(extra)}</small>'
                     f'<ol>{"".join(f"<li>{rs_e(x)}</li>" for x in checklist)}</ol></div>')
    gates_b = rs_bloco("Gates", f'<div class="gates">{"".join(gates)}</div>'
                       '<p class=legenda>A decisão é do sponsor e do revisor, marcada por eles no documento.</p>', ("Gates",))
    if divergencias:
        cons = "".join(f'<p class="aviso">{rs_e(x)}</p>' for x in divergencias)
    else:
        cons = '<p class="ok-txt">Escopo da R1 e dados batem entre 02.1, 02.2, 02.5 e Anexo C.</p>'
    cons_b = rs_bloco("Consistência", cons + '<p class=legenda>Só o que dá para conferir sem julgar o texto. '
                      'As demais checagens são feitas na revisão do gate.</p>', ("02.1", "02.2", "02.5", "Anexo C"))
    pend = sorted(c["linhas"]("A", "pendencias"), key=lambda p: _n(p.get("Bloqueante")) != "sim")
    pend_b = rs_bloco("Riscos e pendências", rs_tabela(pend) or '<p class="vazio">Nenhuma no Anexo A.</p>', ("Anexo A",))
    versoes = c["linhas"]("B", "versoes")
    log = "".join(f"<li><b>{rs_e(v.get('Versão'))}</b><span>{rs_e(v.get('Data'))}</span>"
                  f"<span>{rs_e(v.get('O que mudou'))}{' · ' + rs_e(v['Autor']) if v.get('Autor') else ''}</span></li>"
                  for v in reversed(versoes))
    mud = c["linhas"]("B", "mudancas")
    hist = (f'<ul class="log">{log}</ul>' if log else '<p class="vazio">Sem versões registradas.</p>')
    if mud:
        hist += "<h4 style='margin:14px 0 6px'>Pedidos de mudança</h4>" + rs_tabela(mud)
    hist_b = rs_bloco("Versões e mudanças", hist, ("Anexo B",))
    return ("<h2>Para o revisor: o que está preenchido, os gates, as pendências e o histórico</h2>"
            f"{comp_b}{gates_b}<div class=grade>{cons_b}{hist_b}</div>{pend_b}")


# ---------------------------------------------------------------- geração

def gerar_resumo(arquivo, saida):
    """Gera o resumo de `arquivo` (.docx do PRD) em `saida` (arquivo .html ou pasta) e devolve um relatório (dict)."""
    d = ler_prd(arquivo)
    c = rs_contexto(d)
    gate = rs_gate_alvo(d)
    comp = rs_completude(c)
    div = rs_divergencias(c)
    versao = d["painel"].get("Versão vigente") or ""
    nome = f"Resumo PRD {c['produto']}{' v' + versao if versao else ''}.html"
    destino = os.path.join(saida, nome) if os.path.isdir(saida) else saida
    titulo = html.escape(f"Resumo · PRD {c['produto']}{' v' + versao if versao else ''}")
    pagina = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
              f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titulo}</title>'
              f"<style>{RS_CSS}</style></head><body>{rs_topo(c, gate)}<main>"
              f'<section role="tabpanel" id="p-sponsor" aria-labelledby="t-sponsor">{rs_aba_sponsor(c, comp)}</section>'
              f'<section role="tabpanel" id="p-tecnico" aria-labelledby="t-tecnico">{rs_aba_tecnico(c)}</section>'
              f'<section role="tabpanel" id="p-revisor" aria-labelledby="t-revisor">'
              f"{rs_aba_revisor(c, comp, gate, div)}</section></main>"
              f"<footer>Gerado a partir de \"{html.escape(os.path.basename(arquivo))}\". O resumo mostra o que está "
              f"escrito no PRD; para mudar o que aparece aqui, mude o PRD e gere de novo.</footer>"
              f"<script>{RS_JS}</script></body></html>")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina)
    faltas = []
    total = completas = 0
    if gate:
        for num in RS_GATE_ETAPAS[gate]:
            for sid, tit, dono, sit, _ in comp[num]:
                if sit == "nc":
                    continue
                total += 1
                completas += sit == "ok"
                if sit == "falta":
                    faltas.append((sid, tit, dono))
    pend = c["linhas"]("A", "pendencias")
    return {"arquivo": os.path.basename(destino), "caminho": destino, "tamanho": os.path.getsize(destino),
            "abas": ["Sponsor", "Time técnico", "Revisor"], "gate": gate, "completas": completas, "total": total,
            "faltas": faltas, "divergencias": div, "assinado": d["assinado"],
            "versao_assinada": d["painel"].get("Versão assinada", ""), "porte": c["porte"],
            "pendencias": len(pend), "bloqueiam": sum(1 for p in pend if _n(p.get("Bloqueante")) == "sim")}

# ==== produto/assistente-de-prd/codigo/cli_resumo.py
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
