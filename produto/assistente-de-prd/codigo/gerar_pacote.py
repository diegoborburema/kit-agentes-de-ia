"""Gera manifest.json e declarativeAgent_0.json do Assistente de PRD a partir de instrucoes.md.

Uso, na raiz do repositório:
    python produto/assistente-de-prd/codigo/gerar_pacote.py

As instruções vivem em codigo/instrucoes.md; o pacote nunca é editado à mão. testes/conferir_codigo.py confere que
o pacote está em dia.
"""
import json
import pathlib
import uuid

AGENTE = pathlib.Path(__file__).resolve().parents[1]
PACOTE = AGENTE / "pacote"
VERSAO = "1.0.0"
NOME = "Assistente de PRD"

DESCRICAO = (
    "Ajuda a escrever e revisar o PRD (Product Requirements Document) de um produto de dados ou de IA, novo ou "
    "evolução, em 5 etapas com checkpoints e 2 gates: Dor; Requisitos e critérios de aceite por release; Solução e "
    "benefícios (Gate 1 · Vale construir?); Refinamento técnico e custos, com canvas de engenharia de dados, ciência "
    "de dados, software, segurança e operação; Go-live e transição, com homologação, cutover, contingência e rollback "
    "(Gate 2 · PRD assinado). Você anexa o que já tem ou responde às perguntas. O agente preenche as seções do seu "
    "perfil (PM, especialista técnico ou revisor do gate), avalia cada uma pelo critério de qualidade, mostra o que "
    "falta com as perguntas agrupadas por quem responde e confere a consistência. Devolve o PRD em .docx a qualquer "
    "momento, a partir do template que vem com ele, e um resumo visual por público em HTML. Não decide gates nem "
    "inventa números."
)

INICIOS = [
    ("Começar um PRD", "Quero começar o PRD de um produto novo. Me pergunte o que precisar."),
    ("Preencher com meus arquivos", "Vou anexar o material que já tenho (discovery, PRD em andamento, arquitetura). "
                                    "Preencha e me diga o que falta para o próximo checkpoint."),
    ("Preencher tudo", "Vou anexar todo o material que tenho. Preencha tudo o que der, de todas as etapas, e me diga "
                       "o que validar com quem."),
    ("Refinamento técnico", "Sou da engenharia de dados. Vou anexar o PRD e a arquitetura para o refinamento técnico."),
    ("Revisar para o gate", "Sou o revisor do gate. Vou anexar o PRD para revisar."),
    ("Como funciona", "Explique em poucas linhas como você funciona, as etapas, os gates e os perfis."),
]

SKILLS = ["prd-etapas", "prd-negocio", "prd-tecnico", "prd-canvas", "prd-ia", "prd-perfis", "prd-docx", "prd-resumo"]


def montar():
    app = str(uuid.uuid5(uuid.NAMESPACE_URL, "kit-agentes-de-ia/assistente-de-prd"))
    gpt = str(uuid.uuid5(uuid.NAMESPACE_URL, "kit-agentes-de-ia/gpt/assistente-de-prd"))
    agente = {
        "version": "v1.8",
        "id": f"{app}.gpt.{gpt}",
        "actions": [],
        "conversation_starters": [{"text": t, "title": n} for n, t in INICIOS],
        "name": NOME,
        "description": DESCRICAO,
        "instructions": (AGENTE / "codigo/instrucoes.md").read_text(encoding="utf-8").strip(),
        "behavior_overrides": {"default_response_mode": "Think deeper",
                               "special_instructions": {"discourage_model_knowledge": True}},
        "capabilities": [{"name": "OneDriveAndSharePoint"}, {"name": "CodeInterpreter"}],
        "agent_skills": [{"folder": f"skills/{s}"} for s in SKILLS],
    }
    manifesto = {
        "version": VERSAO,
        "id": app,
        "developer": {"name": "Kit de agentes de IA (github.com/diegoborburema)",
                      "websiteUrl": "https://go.microsoft.com/fwlink/?linkid=2352565",
                      "privacyUrl": "https://go.microsoft.com/fwlink/?linkid=2138865",
                      "termsOfUseUrl": "https://go.microsoft.com/fwlink/?linkid=2138950"},
        "name": {"short": NOME, "full": NOME},
        "description": {"short": "Criado com o Construtor de Agentes do Microsoft 365 Copilot", "full": DESCRICAO},
        "icons": {"outline": "outline.png", "color": "color.png"},
        "accentColor": "#E3F1EE",
        "validDomains": ["*.botframework.com", "*.*.botframework.com", "copilotstudio.microsoft.com",
                         "copilotstudio.preview.microsoft.com"],
        "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.28/MicrosoftTeams.schema.json",
        "manifestVersion": "1.28",
        "copilotAgents": {"declarativeAgents": [{"id": f"{app}.gpt.{gpt}", "file": "declarativeAgent_0.json"}]},
    }
    return {"declarativeAgent_0.json": agente, "manifest.json": manifesto}


def texto(d):
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    for nome, d in montar().items():
        (PACOTE / nome).write_text(texto(d), encoding="utf-8", newline="\n")
        print("gravado:", PACOTE / nome)
