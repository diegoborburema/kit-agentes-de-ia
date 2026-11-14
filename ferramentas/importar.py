#!/usr/bin/env python3
"""
Importa para este repositório o pacote .zip exportado do Agent Builder (Microsoft 365 Copilot).

Uso, na raiz do repositório:
    python ferramentas/importar.py "caminho/para/Agente.zip"                    # agente que já existe aqui
    python ferramentas/importar.py "caminho/para/Agente.zip" --tema produto     # agente novo (produto ou gestao)
    Opcional: --slug nome-da-pasta

O que faz:
  1. Lê o manifest.json do pacote e descobre o nome do agente.
  2. Substitui <tema>/<slug>/pacote/ pelo conteúdo do zip (o export é a referência).
  3. Reformata os .json (indentação e acentos legíveis) para o diff do Git ser útil.
     O conteúdo não muda, só a formatação.
  4. Gera <tema>/<slug>/agente.md, uma visão legível das instruções e configurações.
  5. Cria <tema>/<slug>/NOTAS.md a partir de metodo/modelos/NOTAS.md, se ainda não existir.

Usa só a biblioteca padrão (Python 3.8+).
"""
import argparse
import json
import re
import shutil
import sys
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath

RAIZ = Path(__file__).resolve().parent.parent


def slugify(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t or "agente"


def ler_json(dados):
    return json.loads(dados.decode("utf-8-sig"))


def escrever_texto(caminho, texto):
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def escrever_json(caminho, obj):
    escrever_texto(caminho, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def membros_seguros(zf):
    for info in zf.infolist():
        if info.is_dir():
            continue
        p = PurePosixPath(info.filename.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts:
            sys.exit(f"Caminho inválido dentro do zip: {info.filename}")
        yield info, p


def celula(texto):
    return str(texto).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def cerca(texto):
    n = 3
    while "~" * n in texto:
        n += 1
    return "~" * n


def gerar_resumo(manifest, agente):
    nome = agente.get("name") or manifest.get("name", {}).get("short", "")
    caps = agente.get("capabilities", [])
    skills = agente.get("agent_skills", [])
    modo = agente.get("behavior_overrides", {}).get("default_response_mode", "padrão")
    instr = agente.get("instructions", "").rstrip()
    f = cerca(instr)

    L = [
        f"# {nome}",
        "",
        "> Gerado por `importar.py` a partir de `pacote/`. Não edite à mão: "
        "as mudanças são feitas no Copilot e reimportadas.",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| Versão do pacote | {celula(manifest.get('version', ''))} |",
        f"| Schema do agente | {celula(agente.get('version', ''))} |",
        f"| Modo de resposta | {celula(modo)} |",
        f"| Ações | {len(agente.get('actions', []))} |",
    ]
    especiais = agente.get("behavior_overrides", {}).get("special_instructions")
    if especiais is not None:
        so_fontes = "sim" if especiais.get("discourage_model_knowledge") else "não"
        L.append(f"| Só fontes configuradas | {so_fontes} |")
    L += [
        "",
        "## Descrição",
        "",
        agente.get("description", "").strip(),
        "",
        "## Capacidades e conhecimento",
        "",
    ]
    if caps:
        for c in caps:
            extras = {k: v for k, v in c.items() if k != "name"}
            linha = f"- {c.get('name', '?')}"
            if extras:
                linha += f": `{json.dumps(extras, ensure_ascii=False)}`"
            L.append(linha)
    else:
        L.append("- nenhuma")
    L += ["", "## Skills", ""]
    if skills:
        for s in skills:
            pasta = s.get("folder", "")
            L.append(f"- [{PurePosixPath(pasta).name}](pacote/{pasta}/SKILL.md)")
    else:
        L.append("- nenhuma")
    L += ["", "## Instruções", "", f"{f}markdown", instr, f, "", "## Prompts iniciais", ""]
    starters = agente.get("conversation_starters", [])
    if starters:
        L += ["| Título | Mensagem |", "|---|---|"]
        L += [f"| {celula(s.get('title', ''))} | {celula(s.get('text', ''))} |" for s in starters]
    else:
        L.append("- nenhum")
    return "\n".join(L) + "\n", nome


def main():
    ap = argparse.ArgumentParser(description="Importa um pacote .zip exportado do Agent Builder.")
    ap.add_argument("zip", help="arquivo .zip exportado do Copilot")
    ap.add_argument("--slug", help="nome da pasta do agente (padrão: derivado do nome do agente)")
    ap.add_argument("--tema", help="pasta do tema para agente novo: produto ou gestao")
    a = ap.parse_args()

    zp = Path(a.zip)
    if not zp.is_file():
        sys.exit(f"Arquivo não encontrado: {zp}")

    with zipfile.ZipFile(zp) as zf:
        membros = list(membros_seguros(zf))
        por_nome = {str(p): info for info, p in membros}
        if "manifest.json" not in por_nome:
            sys.exit("manifest.json não está na raiz do zip. É mesmo um pacote exportado do Copilot?")
        manifest = ler_json(zf.read(por_nome["manifest.json"]))
        decl = manifest.get("copilotAgents", {}).get("declarativeAgents", [])
        if not decl:
            sys.exit("O manifest não declara nenhum agente (copilotAgents.declarativeAgents).")

        slug = a.slug or slugify(manifest.get("name", {}).get("short", "") or zp.stem)
        existentes = [p for p in RAIZ.glob(f"*/{slug}") if p.is_dir() and p.parent.name not in ("ferramentas", "metodo")]
        if existentes:
            destino = existentes[0]
        elif a.tema:
            destino = RAIZ / a.tema / slug
        else:
            sys.exit(f"Agente novo ({slug}): diga em que tema ele entra, com --tema produto ou --tema gestao.")
        pacote = destino / "pacote"

        versao_anterior = None
        if (pacote / "manifest.json").exists():
            versao_anterior = json.loads(
                (pacote / "manifest.json").read_text(encoding="utf-8-sig")
            ).get("version")
            shutil.rmtree(pacote)
        pacote.mkdir(parents=True)

        for info, p in membros:
            alvo = pacote.joinpath(*p.parts)
            alvo.parent.mkdir(parents=True, exist_ok=True)
            dados = zf.read(info)
            if p.suffix.lower() == ".json":
                escrever_json(alvo, ler_json(dados))
            else:
                alvo.write_bytes(dados)

    for antigo in destino.glob("agente*.md"):
        antigo.unlink()

    nome = slug
    for i, d in enumerate(decl):
        arq = pacote.joinpath(*PurePosixPath(d["file"]).parts)
        agente = json.loads(arq.read_text(encoding="utf-8"))
        texto, nome = gerar_resumo(manifest, agente)
        escrever_texto(destino / ("agente.md" if len(decl) == 1 else f"agente-{i + 1}.md"), texto)

    notas = destino / "NOTAS.md"
    if not notas.exists():
        modelo = RAIZ / "metodo" / "modelos" / "NOTAS.md"
        base = modelo.read_text(encoding="utf-8") if modelo.exists() else "# {{NOME}}: notas\n"
        escrever_texto(notas, base.replace("{{NOME}}", nome))
        print(f"Criado {notas.relative_to(RAIZ)} a partir do modelo.")

    versao = manifest.get("version", "?")
    if versao_anterior is None:
        print(f"Agente novo: {nome} (v{versao}) em {destino.relative_to(RAIZ).as_posix()}/")
    elif versao_anterior == versao:
        print(f"Atenção: a versão continua v{versao}. Confira se exportou a versão certa.")
    else:
        print(f"{nome}: v{versao_anterior} -> v{versao}")
    print()
    print("Próximos passos:")
    print("  1. Revisar o diff (principalmente agente.md)")
    print("  2. Rodar os casos de teste de NOTAS.md e registrar o motivo em Decisões")
    print(f'  3. git add {destino.relative_to(RAIZ).as_posix()} && git commit -m "{slug}: v{versao}: <motivo da mudança>"')


if __name__ == "__main__":
    main()
