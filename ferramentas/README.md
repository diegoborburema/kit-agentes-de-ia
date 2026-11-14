# Ferramentas

Scripts de apoio ao [método](../metodo/). Todos usam só Python 3, sem instalar nada, e rodam na pasta principal do repositório.

| Script | O que faz |
|---|---|
| [`importar.py`](importar.py) | Traz para o repositório o pacote .zip exportado do Copilot e gera o `agente.md` |
| [`conferir_limites.py`](conferir_limites.py) | Confere os limites do Agent Builder em todos os agentes: instruções, tamanho e nome das skills |
| [`montar_skills.py`](montar_skills.py) | Monta o script de uma skill a partir do código separado em `codigo/` |
| [`empacotar_skills.py`](empacotar_skills.py) | Gera os .zip das skills (`skills-zip/`), prontos para subir no Agent Builder |
| [`sonda-skills/`](sonda-skills/) | Uma skill de diagnóstico do ambiente onde rodam os scripts das skills |

## Sonda de skills

Antes de colocar código numa skill, vale saber o que o ambiente do Agent Builder oferece. A sonda mostra:
- a versão do Python e as bibliotecas instaladas (python-pptx, python-docx, openpyxl);
- onde ficam os arquivos da skill;
- se o script enxerga os arquivos anexados na conversa;
- se consegue gravar um arquivo para download;
- se o interpretador de código consegue ler os arquivos da skill.

Ela só lê e imprime o ambiente e grava um .pptx de teste. Não acessa a rede.

**Como usar**

1. Baixe [`sonda-skills.zip`](sonda-skills.zip).
2. No Agent Builder, crie um agente de teste (aba **Configurar**):
   - **Nome:** `Sonda de skills`
   - **Descrição:** `Agente de teste que roda a skill sonda-skills para diagnosticar o ambiente de scripts das skills.`
   - **Instruções:**
     ```text
     Você é um agente de teste. Quando o usuário escrever "rodar sonda", invoque a skill sonda-skills e siga exatamente os passos dela, na ordem. Mostre as saídas completas, sem resumir nem interpretar. Para qualquer outro pedido, diga em uma linha que este agente só roda a sonda.
     ```
   - **Conhecimento:** nenhum. **Capacidades:** interpretador de código ligado.
   - **Skills:** suba o `sonda-skills.zip`.
3. Numa conversa com o agente, anexe qualquer .pptx e escreva **"rodar sonda"**.
4. Guarde a saída completa: ela decide como empacotar o código das suas skills (dentro do `SKILL.md` ou em `scripts/`).
