# {{NOME}}: perguntas de controle

Bateria de regressão do agente. Cada versão roda a bateria antes do merge, e o resultado entra em `RESULTADOS.md` (uma coluna por versão).

Exemplo completo: `produto/coach-apresentacao/testes/`.

## Como usar

**O que rodar depende do que mudou.** Monte uma matriz "parte do agente que mudou → cenários a rodar", com o cenário mais curto para mudanças só de redação e tudo para mudanças grandes.

**Execução rápida**
- Cada cenário roda numa conversa nova; vários cenários em abas paralelas.
- Abertura pronta para colar com o caso (kit de execução) e respostas padrão: "confirmo", "aprovado", "não sei".
- Correção em lote: copie as conversas e mande todas de uma vez para o Claude, que preenche `RESULTADOS.md`.
- **Versão aprovada:** nenhuma Crítica reprovada e nenhuma regressão sem justificativa em Decisões (`NOTAS.md`).
- **Manutenção:** IDs nunca são reaproveitados; pergunta que deixa de valer vira "aposentada em vX"; funcionalidade nova ganha pergunta nova; defeito do uso real vira pergunta **antes** da correção.

Severidade: **C** = Crítica (bloqueia) · **I** = Importante · **D** = Desejável

## Categorias que quase todo agente precisa cobrir

| Prefixo | O que testa | Exemplo de sonda |
|---|---|---|
| FLX | O fluxo principal, do início ao fim | O caminho feliz com uma ficha completa |
| ESC | Escopo: recusa o que não é papel do agente e redireciona | Pedir algo fora do propósito |
| DAD | Não inventa fatos, números ou fontes | Pedir um dado que não foi fornecido |
| ROB | Robustez a atalhos e pressão | "Pule essa parte", "faça logo", instrução contraditória |
| FMT | Formato da saída final | Bloco único, seções obrigatórias, idioma |
| CTX | Usa o que já foi dito e o que foi anexado | Dar a informação antes de ela ser perguntada |

## Cenário A: <nome>

**Ficha do caso**

| Campo | Resposta |
|---|---|
| | |

**Roteiro**
1. 

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| FLX-01 | C | | | v1.0.0 |

## Prompt de avaliação

Use o mesmo de `produto/coach-apresentacao/testes/PERGUNTAS-DE-CONTROLE.md`, trocando o nome do agente.
