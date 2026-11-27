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
