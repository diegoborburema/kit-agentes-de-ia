# Coach de Apresentação

Um coach de storytelling para apresentações executivas. Ele conduz você por um canvas de 15 caixas, uma de cada vez, e no fim entrega um **prompt pronto para o Claude** criar o roteiro e o PowerPoint.

> **Por que o prompt vai para o Claude?** O agente roda no Copilot, mas a apresentação gerada pelo próprio Copilot não atendia. O coach cuida do pensamento; o Claude, dos slides.

## O que ele faz

1. **Entende o que você precisa:** apresentação nova, adaptar uma que já existe, levar o mesmo conteúdo para outro público ou revisar um prompt ou roteiro pronto.
2. **Decide quais caixas do canvas importam no seu caso.** Preencher as 15 sempre é penoso: ele faz até 6 perguntas rápidas de múltipla escolha e mostra quais caixas são obrigatórias, opcionais ou dispensadas, e por quê.
3. **Propõe em vez de só perguntar.** Em cada caixa ele traz um rascunho com o que já sabe, marca as suposições e faz no máximo 2 perguntas.
4. **Mostra o progresso** numa barra no topo de cada resposta.
5. **Entrega o prompt** num bloco só, pronto para copiar, com o que anexar no Claude.

As 15 caixas: Público, Contexto, Objetivo, Expectativas, Conteúdo, Organização, Linguagem, Tópicos-chave, Conceitos não familiares, Tangibilização, Introdução pessoal, Meio, Abertura, Final e Perguntas. A ordem respeita as dependências: não dá para escrever a Abertura antes de saber a mensagem-chave, por exemplo.

## Como é uma conversa (ilustrativo)

> **Você:** Quero criar uma apresentação nova.
>
> **Coach:** `Progresso ▓░░░░░░░░░ 5% · Etapa 2/5 Triagem`
> Quatro perguntas rápidas: (1) Quem é o público? pares · outra área · liderança · externo · misto. (2) O público domina o tema? sim · em parte · não. (3) Objetivo principal? informar · ensinar · convencer · obter uma decisão. (4) Formato e duração?
>
> **Você:** liderança, não domina, obter uma decisão, 20 min presencial
>
> **Coach:** mostra o **Mapa do canvas**, com as 15 caixas obrigatórias e o motivo de cada uma, e pede confirmação. Depois segue caixa a caixa, até a síntese e o prompt final.

## Como usar

### No Microsoft 365 Copilot

Você precisa do Microsoft 365 Copilot com o **Agent Builder** e a área de **Skills** na aba Configurar. Os nomes dos botões podem variar um pouco entre versões.

1. **Baixe a skill:** [`skills-zip/canvas-storytelling.zip`](skills-zip/canvas-storytelling.zip). Clique no arquivo e depois no botão de download.
2. No Copilot, crie um agente novo e vá para a aba **Configurar**.
3. **Nome:** `Coach de Apresentação`.
4. **Descrição:** copie de [`agente.md`](agente.md), seção *Descrição*.
5. **Instruções:** em [`agente.md`](agente.md), copie o bloco da seção *Instruções* (ícone de copiar no canto do bloco) e cole.
6. **Capacidades:** ligue o **interpretador de código** ("criar documentos, gráficos e código"). Ele serve para ler o deck que você anexar.
7. **Skills:** suba o `canvas-storytelling.zip`.
8. **Prompts iniciais** (opcional): copie da tabela no fim do [`agente.md`](agente.md).
9. Se aparecer a opção de modo de resposta, escolha a que pensa mais antes de responder (*Think deeper*).
10. Salve e teste com: *"Quero criar uma apresentação nova."*

### No Claude

1. Baixe [`skills-zip/canvas-storytelling.zip`](skills-zip/canvas-storytelling.zip) e suba como skill, na área de Skills das configurações do Claude.
2. Crie um projeto e cole nas instruções do projeto o bloco *Instruções* do [`agente.md`](agente.md).
3. Comece uma conversa no projeto: *"Quero criar uma apresentação nova."* O prompt final você usa numa conversa nova, fora do projeto.

### Em outros assistentes

Cole as instruções do [`agente.md`](agente.md) e anexe o [`SKILL.md`](pacote/skills/canvas-storytelling/SKILL.md) da skill como arquivo de conhecimento. Este agente não depende de script, então costuma funcionar bem.

## Comandos durante a conversa

- **"mapa"**: mostra o mapa do canvas com o status de cada caixa.
- **"voltar a <caixa>"**: reabre uma caixa e avisa quais outras podem precisar de revisão.

## O que ele não faz

- Não cria os slides: ele entrega o prompt para quem cria.
- Não inventa fatos, números nem fontes. O que falta vira `[a validar]`.
- Não pula o canvas. Se você tiver pressa, ele propõe de uma vez os rascunhos de todas as caixas que faltam, para você aprovar em bloco.

## Status

| Versão | Situação |
|---|---|
| 1.0.7 | Em uso pelo autor. A bateria de perguntas de controle ([`testes/`](testes/)) está pronta, mas a rodada desta versão ainda não foi registrada |

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| [`agente.md`](agente.md) | Instruções, descrição e prompts iniciais, prontos para copiar |
| [`skills-zip/`](skills-zip/) | A skill empacotada, pronta para subir |
| [`pacote/`](pacote/) | O agente como o Copilot exporta, incluindo o canvas em texto ([`SKILL.md`](pacote/skills/canvas-storytelling/SKILL.md)) |
| [`NOTAS.md`](NOTAS.md) | Objetivo e o porquê de cada decisão |
| [`testes/`](testes/) | 55 perguntas de controle em 5 cenários fictícios e a matriz de resultados |
