---
name: ata-tipos
description: 'Tipos de reunião do Redator de Atas e a estrutura de cada um: como perguntar o tipo e sugerir pelo título e pelo conteúdo, as seções permitidas e a ordem para Homologação, Discovery, Refinamento, Alinhamento e Outro, o que entra em cada seção, as regras próprias de cada tipo (status só declarado na homologação, hipótese que não vira jornada no discovery, direcional junto do tema no refinamento, divergência neutra no alinhamento) e as seções que nunca entram sem pedido. Use para escolher o tipo, montar a ata e no comando tipo.'
---

## 1. Escolher o tipo

O tipo dito pelo usuário prevalece sobre qualquer sugestão e vale como definitivo. Sem tipo dito, pergunte numa única mensagem, antes de escrever:

```
Qual opção melhor descreve a reunião?
1. Homologação — validação de entregas
2. Discovery — entendimento de problema, solução e jornada
3. Refinamento — detalhamento de histórias, processos ou escopo
4. Alinhamento — sincronização entre times ou stakeholders
5. Outro — descreva em uma linha
Sugestão: 3, pelo título "Refinamento Painel Jatobá" e pelas regras detalhadas na conversa.
```

Sinais para a sugestão, pelo título e pelo conteúdo:

| Tipo | No título | No conteúdo |
|---|---|---|
| Homologação | homologação, UAT, validação, aceite, teste com usuário | funcionalidades demonstradas, "aprovado", "com ressalva", bugs |
| Discovery | discovery, imersão, entendimento, entrevista | dor, usuários, como é hoje, ideias e hipóteses |
| Refinamento | refinamento, refinement, grooming, detalhamento | regras, insumos, validações, critérios, desenho de tabela ou de história |
| Alinhamento | alinhamento, sync, status, kickoff, comitê | cronograma, decisões entre áreas, posições diferentes |

"Outro": use a estrutura de Outro (§6) e o que o usuário descreveu. Um tipo pedido pelo comando `tipo <tipo>` refaz a ata inteira na estrutura nova, com a mesma extração.

## 2. Regras comuns

- Cada seção entra **só quando a fonte a sustenta**. Seção sem conteúdo some; não escreva "não discutido".
- Use os títulos de seção exatamente como abaixo, em `##`, na ordem da tabela do tipo. Os temas dentro de Pontos Alinhados vão em `###`, numerados.
- Seção marcada como opcional entra só quando acrescenta informação útil e não repetida.
- **Nunca entram sem pedido explícito:** Resumo Executivo, Contexto (no Refinamento), Objetivo, Acordos Técnicos, Acordos Funcionais, Principais Dores, Itens Despriorizados, Critérios de Aceite, Fonte, Duração, Sprint e Status. Seção pedida pelo usuário entra e vai em `secoes_pedidas` na conferência.
- Uma informação aparece numa seção só. A decisão que já está no direcional do tema não se repete em Decisões Tomadas nem em Riscos.

## 3. Refinamento

| Ordem | Seção | O que entra |
|---|---|---|
| 1 | Participantes | Tabela Participante · Área, quando há área comprovada; senão, lista |
| 2 | Pontos Alinhados | Temas numerados, com o direcional junto do tema que o originou |
| 3 | Decisões Tomadas (opcional) | Só decisões que não ficaram claras nos direcionais dos temas |
| 4 | Riscos e Pontos de Atenção | Riscos, lacunas e definições pendentes discutidos |
| 5 | Próximos Passos | Tabela Ação · Responsável (· Prazo) |

Como organizar os temas:
- **Processo atual** e **Direcional acordado** como rótulos em negrito, quando houver contraste claro entre o hoje e o combinado. Se os bullets já explicam a limitação, não force "Problema discutido".
- **Partes da mesma solução ficam num bloco só:** pós-avaliação, tabela manual, upload, sistema de entrada e cálculo, por exemplo. Não crie uma seção por parte. Um tema ganha bloco próprio só quando tem regra própria detalhada (por exemplo, a regra de rateio).
- **Insumos em sub-bullets, com a origem** quando a fonte permitir: `[Base Cambuci]`, `[Tabela | Portal Araçá]`, `[Output Pós-avaliação]`.
- Preserve percentuais, exceções e a relação causal da regra (ex.: cliente de rede, nível N3, filial).
- Validação humana citada é regra: entra no tema.
- Alternativa de arquitetura ou de sistema só avaliada não ganha seção. Ela entra só se houver decisão, risco relevante ou próximo passo confirmado.
- Possibilidade "para depois" não entra como escopo.

## 4. Homologação

| Ordem | Seção | O que entra |
|---|---|---|
| 1 | Participantes | Como no Refinamento |
| 2 | Contexto (opcional) | O que foi homologado (produto, módulo, versão, ambiente), se dito e se não estiver no título |
| 3 | Funcionalidades Apresentadas | Tabela Funcionalidade · Status · Observação |
| 4 | Status de Homologação (opcional) | Só se houve um status geral declarado à parte; senão, ele fica na Conclusão |
| 5 | Bugs ou Ajustes Identificados | Um bullet por item: o que acontece, números do caso, causa e severidade só se ditas |
| 6 | Conclusão | O resultado geral, só como foi declarado, e a condição para seguir |
| 7 | Próximos Passos | Tabela |

- **Status só declarado.** "Aprovado", "Aprovado com ressalva" ou "Reprovado" só quando alguém com o papel de validar disse isso com clareza. Ressalva sempre com o conteúdo dela. Sem declaração: "Sem status declarado", com o que falta ("ainda não testado").
- **Severidade só dita.** "Bloqueante para o go-live, segundo o Otavio" entra, com o autor. "É um bug simples" fala de esforço, não de severidade.
- Sugestão de melhoria nova ("seria legal ter o alerta no Teams"), adiada: fora, ou uma linha na Conclusão se mudar o plano. Nunca como ajuste confirmado.
- A Conclusão diz se a entrega está homologada só como foi declarado ("ainda não: falta o alerta").

## 5. Discovery

| Ordem | Seção | O que entra |
|---|---|---|
| 1 | Participantes | Como no Refinamento |
| 2 | Contexto (opcional) | Por que o discovery existe, se dito |
| 3 | Dor ou Problema | A dor, com quem a relatou; números com a ressalva da fonte |
| 4 | Usuários Afetados | Só os que a reunião tratou como usuários |
| 5 | Jornada Atual e Proposta | Os passos de hoje como descritos; a jornada proposta só se foi descrita |
| 6 | Hipóteses de Solução | Cada hipótese com o autor e a dependência dita |
| 7 | Critérios Preliminares | Referências citadas, com quem citou e se falta validar |
| 8 | Premissas e Restrições | Dados, prazos e limites técnicos ditos |
| 9 | Dúvidas em Aberto | Perguntas sem resposta |
| 10 | Próximos Passos | Tabela |

- **Nada presumido.** Não complete jornada, persona, critério, impacto ou usuário pelo que costuma ser verdade. Usuário só citado ("possível usuário, não discutido") não entra como afetado; vira dúvida, se a reunião deixou a dúvida.
- **Hipótese não vira jornada proposta.** Sem jornada proposta descrita, a seção traz só a jornada atual, com o rótulo **Jornada atual**.
- Número de dor com a ressalva: "estimativa da área, não validada".

## 6. Alinhamento e Outro

**Alinhamento**

| Ordem | Seção | O que entra |
|---|---|---|
| 1 | Participantes | Como no Refinamento |
| 2 | Contexto (opcional) | Pano de fundo dito, quando ajuda a ler as decisões |
| 3 | Pontos Alinhados | Entendimentos comuns, sem escolha nova |
| 4 | Decisões Tomadas | Decisões, com quem decidiu quando isso importa ("TI corporativa, sem negociação") |
| 5 | Divergências Registradas | Cada posição com o autor e o argumento dito, em termo neutro, e quem decide e quando |
| 6 | Riscos e Pontos de Atenção | Riscos e impactos discutidos, com valores e autor |
| 7 | Próximos Passos | Tabela |

- Divergência só quando discutida claramente. Não diga quem tem razão nem escolha um lado. Posição não é decisão.
- Divergência e risco não se repetem: o argumento fica na divergência; o impacto com número fica em Riscos.

**Outro:** Participantes · Pontos Alinhados · Riscos e Pontos de Atenção · Próximos Passos, e as seções que o usuário pediu na descrição do tipo.
