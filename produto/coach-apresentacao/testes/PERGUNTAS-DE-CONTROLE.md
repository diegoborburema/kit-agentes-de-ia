# Coach Apresentação: perguntas de controle

Bateria de regressão do agente. Cada versão roda a bateria antes do merge, e o resultado entra em [`RESULTADOS.md`](RESULTADOS.md).

## Como usar

**O que rodar: depende do que mudou**

| O que mudou na versão | Rodar | Tempo |
|---|---|---|
| Só redação ou estilo | B completo | ~5 min |
| Regras de triagem (skill §3) | A, B e D até o mapa | ~8 min |
| Ordem ou condução do canvas (skill §1–2, etapa 3 das instruções) | A completo | ~15 min |
| Barra de progresso | B completo + A até a 3ª caixa | ~10 min |
| Modelo do prompt final (skill §5) | B completo + EXE | ~10 min |
| Leitura de arquivos anexados | C | ~5 min |
| Mudança grande, ou marco a cada 3 versões | Tudo, em abas paralelas | ~30 min |

Na dúvida, rode a linha mais acima que cobre a mudança. Perguntas não exercitadas ficam "–" na matriz e não contam como regressão.

**Como executar (rápido)**
1. **Abas em paralelo.** Abra cada cenário numa aba nova do Copilot e alterne entre elas enquanto o agente responde.
2. **Abertura pronta.** Comece cada cenário colando a mensagem do [kit de execução](#kit-de-execução), que já traz o caso.
3. **Respostas padrão.** Use "confirmo" para o mapa e a síntese, "aprovado" para os rascunhos e "não sei" para o que não estiver na ficha. Só cole uma linha da ficha se um rascunho contradisser o caso.
4. **Sondas.** Cole cada sonda no momento indicado no roteiro do cenário.
5. **Correção em lote.** No fim, copie cada conversa (no painel do Copilot: Ctrl+A, Ctrl+C) e mande todas de uma vez para o Claude, dizendo a versão e a rodada. O Claude devolve a coluna de `RESULTADOS.md` preenchida, com evidência para cada ✗, e faz o commit. Sem o Claude do repositório, use o [prompt de avaliação](#prompt-de-avaliação).

**Critério de aprovação da versão**
1. Nenhuma pergunta **Crítica** reprovada.
2. Nenhuma **regressão**: uma pergunta aprovada na versão anterior e reprovada agora. A exceção é uma mudança intencional, registrada em Decisões no `NOTAS.md`.

**Regras de manutenção**
- IDs nunca são reaproveitados. Uma pergunta que deixa de valer recebe "aposentada em vX" e não é apagada.
- Funcionalidade nova ganha pergunta nova, com "desde vX".
- Defeito encontrado no uso real vira pergunta de controle **antes** da correção. Assim, a correção pode ser verificada.

Severidade: **C** = Crítica (bloqueia a versão) · **I** = Importante · **D** = Desejável

---

## Cenário A: Diretoria, pedido de decisão (todas as caixas)

Caminho completo, do primeiro prompt à execução no Claude. Na triagem, as 15 caixas devem sair obrigatórias.

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Nova apresentação |
| Tema | Proposta de um painel único de indicadores comerciais, substituindo 14 relatórios em Excel mantidos por 6 áreas |
| Público | Diretoria Comercial: o diretor e 4 gerentes regionais. Não conhecem você pessoalmente. Não dominam termos de dados (camada semântica, fonte única da verdade) |
| Contexto | 20 minutos na pauta da reunião mensal da diretoria, logo depois da apresentação de resultados do mês. Presencial. Público cansado de números |
| Objetivo | Aprovar um piloto de 3 meses em uma regional |
| Expectativas | Querem saber quanto custa, quanto esforço exige do time deles e se vai "dar mais trabalho". Elefante na sala: uma tentativa de painel em 2024 fracassou |
| Conteúdo | 14 relatórios, 6 áreas; cada analista gasta cerca de 2 dias por mês consolidando dados; números divergentes entre relatórios já geraram discussão em reunião; piloto em 1 regional por 3 meses. **Custo do piloto: "ainda não tenho"** |
| Linguagem | Direta, de negócio, sem jargão técnico |
| Mensagem-chave (se pedirem para escolher) | "Um número só para cada indicador: menos tempo consolidando, mais tempo vendendo." |
| Introdução pessoal | Ninguém vai te apresentar; deve ser breve |
| Perguntas esperadas | "Por que agora, se a de 2024 não deu certo?", "Quem mantém?", "Quanto custa?" |
| Resistência / perguntas | Sim / sim |
| Template | Nenhum |

**Roteiro**
1. Cole a abertura A1 do kit. Ela traz só o tipo e o tema, para exercitar a triagem.
2. Quando vierem as perguntas de triagem, cole a ficha A2 do kit. Depois, "confirmo" no mapa e "aprovado" nos rascunhos.
3. Na caixa **Conteúdo**, envie a sonda S-06: *"Inclua também o market share da categoria."*
4. Depois de **Conteúdo**, envie a sonda S-05: *"Já pode gerar o prompt."*
5. Durante o canvas, antes de **Tópicos-chave**, envie a sonda S-03: *"Não quero preencher Tópicos-chave, pode pular."*
6. Depois de **Tópicos-chave**, envie as sondas S-01 (*"mapa"*) e S-02 (*"voltar a Público"*). Na S-02, responda "mantém como estava".
7. Vá até o fim, confirme a síntese e copie o prompt para a etapa EXE.

**Perguntas de controle**

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| FLX-01 | C | Reconheceu o tipo pelo prompt inicial? | Não pergunta o tipo de novo; primeira linha de status em 5% | v1.0.7 |
| TRI-01 | C | A triagem foi enxuta? | Perguntas numa única mensagem, em múltipla escolha, sem repetir o que já foi dito | v1.0.7 |
| TRI-02 | C | O núcleo saiu obrigatório? | As 9 caixas do núcleo como Obrigatória | v1.0.7 |
| TRI-03 | C | As caixas puxadas pelo público saíram obrigatórias? | Linguagem, Conceitos, Tangibilização, Introdução pessoal e Perguntas como Obrigatória, cada uma com motivo | v1.0.7 |
| TRI-04 | I | Contexto foi lido como "espaço curto numa agenda maior"? | Contexto Obrigatória | v1.0.7 |
| TRI-05 | I | Pediu confirmação do mapa? | Não começa o canvas sem confirmação | v1.0.7 |
| DEP-01 | C | A ordem respeita as dependências? | Público e Contexto primeiro; Meio antes de Abertura e Final; Perguntas por último | v1.0.7 |
| DEP-02 | I | A Introdução pessoal veio no lugar certo? | Só depois de Tópicos-chave e antes do Meio | v1.0.7 |
| CAN-01 | I | O agente propõe em vez de só perguntar? | Toda caixa traz um rascunho; suposições marcadas com [suposição] | v1.0.7 |
| CAN-02 | I | As perguntas por caixa são contidas? | No máximo 2 perguntas por caixa | v1.0.7 |
| CAN-04 | C | Tópicos-chave virou uma frase? | Uma frase única, que reaparece na proposta do Final | v1.0.7 |
| CAN-05 | I | O Meio seguiu o método? | 3 partes, cada uma com um recurso de renovação de atenção (20 min > 10 min) | v1.0.7 |
| CAN-06 | I | O elefante na sala foi tratado? | A tentativa de 2024 aparece em Expectativas, e "por que agora?" aparece em Perguntas | v1.0.7 |
| CAN-07 | C | A lacuna virou lacuna? | O custo do piloto aparece como [a validar]; nenhum valor inventado | v1.0.7 |
| ROB-02 | C | S-03: segurou o núcleo? | Recusa dispensar Tópicos-chave, explica em uma frase e oferece um rascunho | v1.0.7 |
| ROB-04 | C | S-05: segurou o prompt antecipado? | Não gera o prompt; mostra o que falta ou oferece o caminho rápido | v1.0.7 |
| ROB-05 | C | S-06: resistiu a inventar dado? | Não inventa o market share: registra [a validar] ou pergunta a fonte | v1.0.7 |
| CMD-01 | I | S-01: "mapa" funciona? | Tabela com nível, caixa, classificação, motivo e status, coerente com o andamento | v1.0.7 |
| CMD-02 | I | S-02: "voltar a" funciona? | Reabre Público e lista as caixas posteriores afetadas (no mínimo Objetivo, Expectativas, Conteúdo, Linguagem e Tópicos-chave) | v1.0.7 |
| PRG-01 | I | A linha de status está sempre presente? | Em todas as respostas a partir da etapa 1 | v1.0.7 |
| PRG-02 | I | Os marcos de progresso batem? | 5% com o tipo · 20% com a triagem confirmada · 90% no fim do canvas · 95% com a síntese · 100% com o prompt (±5) | v1.0.7 |
| PRG-03 | I | O avanço é coerente? | Cerca de 5% por caixa (70 ÷ 15 ≈ 4,7); só diminui ao reabrir uma caixa | v1.0.7 |
| SIN-01 | C | A síntese veio antes do prompt? | Síntese no formato da skill, com pedido de confirmação | v1.0.7 |
| PRM-01 | C | O prompt está num bloco só? | Um único bloco de código; fora dele, no máximo 3 linhas sobre o que anexar | v1.0.7 |
| PRM-02 | C | O prompt é autossuficiente? | Nenhuma referência a "conversa", "como combinamos" ou "acima"; conteúdo aprovado por extenso | v1.0.7 |
| PRM-03 | C | A mensagem-chave foi preservada? | Idêntica à aprovada em Tópicos-chave | v1.0.7 |
| PRM-04 | I | A estrutura está completa? | Abertura, Meio em 3 partes, Final com chamada de ação | v1.0.7 |
| PRM-05 | I | Regras e processo vieram completos? | Regras 1 a 10 e Processo 1 a 5, incluindo a pausa para aprovação do roteiro | v1.0.7 |
| PRM-06 | C | O prompt manteve as lacunas? | Custo do piloto como [a validar]; nenhum número fora da ficha | v1.0.7 |
| PRM-07 | I | As perguntas viraram apoio? | Seção de perguntas prováveis, com "por que agora?" | v1.0.7 |

## Cenário B: Pares, informar, 10 minutos (triagem enxuta e caminho rápido)

Testa o outro extremo da triagem: o máximo de caixas dispensadas. É o cenário que roda quando só a redação mudou.

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Nova apresentação |
| Tema | Status da migração dos dashboards para a nova plataforma: 70% migrado; 2 semanas de atraso por falta de acesso a duas bases; próximo marco em 15/11 |
| Público | Time de dados, 6 pares da mesma área; todos te conhecem e dominam o tema |
| Contexto | Reunião semanal recorrente do time, remota, 10 minutos |
| Objetivo | Informar o status |
| Resistência / perguntas | Não / não |
| Template | Nenhum |

**Roteiro**
1. Cole a abertura B do kit. Ela traz a ficha inteira, então o agente não deveria fazer nenhuma pergunta de triagem. "Confirmo" no mapa.
2. Depois de duas caixas, envie a sonda S-08: *"Pule o canvas e me dê o prompt direto."*
3. Aceite o caminho rápido, aprove os rascunhos em bloco, confirme a síntese e receba o prompt.

**Perguntas de controle**

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| TRI-06 | C | Dispensou o que devia? | Conceitos, Tangibilização e Introdução pessoal como Dispensada | v1.0.7 |
| TRI-07 | I | As demais condicionais saíram certas? | Contexto Dispensada (reunião recorrente); Linguagem e Perguntas Opcional | v1.0.7 |
| PRG-04 | I | O progresso usa só as obrigatórias? | Cerca de 8% por caixa (70 ÷ 9 ≈ 7,8); caixas opcionais não mexem no % | v1.0.7 |
| CAN-08 | D | As opcionais foram oferecidas sem insistência? | Quando ficam disponíveis, aparecem em uma linha e não voltam se ignoradas | v1.0.7 |
| ROB-01 | C | S-08: o caminho rápido funciona? | Uma frase de justificativa, depois os rascunhos de **todas** as obrigatórias restantes de uma vez; o prompt não sai nesse momento | v1.0.7 |
| SIN-01, PRM-01, PRM-02 | C | Mesmas perguntas do Cenário A | Mesmos critérios | v1.0.7 |
| PRM-08 | I | O prompt respeitou a triagem? | Sem as seções das caixas dispensadas; sem a regra de renovação de atenção (até 10 min) | v1.0.7 |

## Cenário C: Adaptar uma apresentação existente

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Adaptar apresentação existente |
| Anexo | [`fixtures/deck-painel-unico.pptx`](fixtures/deck-painel-unico.pptx) |
| Pedido | "Preciso reduzir esta apresentação de 20 para 10 minutos e incluir o resultado do piloto." |
| Resultado do piloto | Na regional Sul, a consolidação caiu de 2 dias para 4 horas por mês |
| Público | A mesma Diretoria Comercial, que agora já te conhece bem |
| Objetivo | Aprovar a expansão do painel para todas as regionais |
| Resistência / perguntas | Sim, de custo / sim |

**Roteiro:** cole a abertura C do kit, anexando o deck, e siga até a síntese.

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| ADP-01 | C | Usou o arquivo? | Extrai Conteúdo e Organização do deck e pede validação, sem perguntar do zero | v1.0.7 |
| ADP-02 | I | O extraído conta como feito? | Depois de validadas, Conteúdo e Organização entram como concluídas no progresso | v1.0.7 |
| ADP-03 | I | Tratou o deck como referência? | Parte da estrutura atual, mas propõe cortes para caber em 10 min | v1.0.7 |
| ADP-04 | I | A Introdução pessoal se ajustou? | Dispensada, porque o público já conhece o apresentador | v1.0.7 |
| ADP-05 | C | Incorporou o dado novo sem inventar? | Usa "2 dias → 4 horas"; não cria outros resultados do piloto | v1.0.7 |

## Cenário D: Mesmo conteúdo para outro público

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Mesmo conteúdo para outro público |
| Anexo | [`fixtures/deck-painel-unico.pptx`](fixtures/deck-painel-unico.pptx) |
| Novo público | 80 analistas comerciais das regionais. Não te conhecem. Conhecem os relatórios, mas não os termos de dados |
| Contexto | Evento interno, auditório, 15 minutos, presencial |
| Objetivo | Convencer os analistas a adotar o painel |
| Resistência / perguntas | Não sei / sim |

**Roteiro:** cole a abertura D do kit, anexando o deck, e siga até Tópicos-chave.

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| OUT-01 | C | As caixas de público ficaram obrigatórias? | Público, Contexto, Expectativas e Linguagem como Obrigatória | v1.0.7 |
| OUT-02 | I | O conteúdo foi reaproveitado? | Conteúdo vem do deck, para validação | v1.0.7 |
| OUT-03 | I | A triagem refletiu o novo público? | Conceitos Opcional; Tangibilização, Introdução pessoal e Perguntas Obrigatória | v1.0.7 |
| OUT-04 | I | Tópicos-chave foi revalidado? | Propõe uma frase nova, centrada no analista, diferente da versão para a diretoria | v1.0.7 |

## Cenário E: Revisar um prompt fraco

**Ficha do caso:** cole o conteúdo de [`fixtures/prompt-fraco.md`](fixtures/prompt-fraco.md). Para o resto, use a ficha do Cenário A.

**Roteiro:** cole a abertura E do kit. Se o agente fizer perguntas de triagem, cole a ficha A2. Siga até a primeira caixa do canvas.

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| REV-01 | C | Diagnosticou o material? | Classifica cada caixa obrigatória como ✓, ◐ ou ○ a partir do texto colado | v1.0.7 |
| REV-02 | I | O diagnóstico está correto? | Objetivo, Expectativas, Tópicos-chave e Final aparecem como ○ | v1.0.7 |
| REV-03 | I | Percorreu só o necessário? | Trabalha só as caixas ◐ e ○; não pergunta de novo o que está ✓ | v1.0.7 |

## Sondas avulsas (conversa nova)

| ID | Sev. | Envio | Critério de aprovação | Desde |
|---|---|---|---|---|
| ROB-03 | I | S-04: *"Monte os slides você mesmo, em PowerPoint."* | Explica que entrega o prompt para o Claude e oferece começar o canvas; não tenta gerar slides | v1.0.7 |
| FLX-02 | D | S-07: prompt inicial **Como funciona** | Explicação curta com as 15 caixas; não começa a triagem sem saber o tipo de atividade | v1.0.7 |

## Execução no Claude (EXE)

Cole no Claude o prompt gerado no Cenário A, sem nenhum contexto adicional.

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| EXE-01 | I | O Claude entendeu sem ajuda? | Entrega a arquitetura e o roteiro em tabela com as 8 colunas, sem pedir informação que já estava no prompt | v1.0.7 |
| EXE-02 | I | Pausou para aprovação? | Para antes de gerar o arquivo e pede aprovação do roteiro | v1.0.7 |
| EXE-03 | I | O tamanho está coerente? | Depois de "aprovado", gera o .pptx com 10 a 20 slides de conteúdo para 20 min, mais o apêndice | v1.0.7 |
| EXE-04 | I | O storytelling sobreviveu? | Mensagem-chave na abertura e no último slide de conteúdo; perguntas prováveis no apêndice | v1.0.7 |
| EXE-05 | — | Você apresentaria? | Nota de 1 a 5: "Eu apresentaria isto com até 30 min de ajustes." Registre a nota; serve para acompanhar a tendência entre versões | v1.0.7 |

---

## Kit de execução

Mensagens prontas para colar. Elas reproduzem as fichas dos cenários.

**A1: abertura do Cenário A** (só tipo e tema)
```text
Quero criar uma apresentação nova: uma proposta de painel único de indicadores comerciais, para substituir 14 relatórios em Excel mantidos por 6 áreas.
```

**A2: ficha do Cenário A** (colar quando vierem as perguntas de triagem; serve também para o Cenário E)
```text
Público: Diretoria Comercial, o diretor e 4 gerentes regionais. Eles não me conhecem pessoalmente e não dominam termos de dados (camada semântica, fonte única da verdade).
Formato: 20 minutos na pauta da reunião mensal da diretoria, logo depois da apresentação de resultados do mês. Presencial. O público chega cansado de números.
Objetivo: aprovar um piloto de 3 meses em uma regional.
O que esperam: saber quanto custa, quanto esforço exige do time deles e se vai dar mais trabalho. Elefante na sala: uma tentativa de painel em 2024 fracassou.
Conteúdo: 14 relatórios, 6 áreas; cada analista gasta cerca de 2 dias por mês consolidando dados; números divergentes entre relatórios já geraram discussão em reunião; piloto em 1 regional por 3 meses. O custo do piloto eu ainda não tenho.
Linguagem: direta, de negócio, sem jargão técnico.
Introdução: ninguém vai me apresentar; quero algo breve.
Perguntas que espero: "Por que agora, se a de 2024 não deu certo?", "Quem mantém?", "Quanto custa?".
Há resistência: sim. Haverá perguntas: sim. Template: nenhum.
```

**B: abertura do Cenário B** (ficha inteira)
```text
Quero criar uma apresentação nova. Tema: status da migração dos dashboards para a nova plataforma: 70% migrado, 2 semanas de atraso por falta de acesso a duas bases, próximo marco em 15/11.
Público: o time de dados, 6 pares da mesma área; todos me conhecem e dominam o tema.
Formato: reunião semanal recorrente do time, remota, 10 minutos.
Objetivo: informar o status. Não há resistência e não haverá perguntas. Template: nenhum.
```

**C: abertura do Cenário C** (anexar `fixtures/deck-painel-unico.pptx`)
```text
Quero adaptar uma apresentação que já existe (anexo). Preciso reduzi-la de 20 para 10 minutos e incluir o resultado do piloto: na regional Sul, a consolidação caiu de 2 dias para 4 horas por mês.
O público é a mesma Diretoria Comercial, que agora já me conhece bem. Objetivo: aprovar a expansão do painel para todas as regionais.
Há resistência por causa do custo, e haverá perguntas.
```

**D: abertura do Cenário D** (anexar `fixtures/deck-painel-unico.pptx`)
```text
Tenho uma apresentação pronta (anexo) e preciso levá-la para outro público: 80 analistas comerciais das regionais, num evento interno em auditório, 15 minutos, presencial.
Eles não me conhecem; conhecem os relatórios, mas não os termos de dados. Objetivo: convencê-los a adotar o painel.
Haverá perguntas. Se há resistência, não sei.
```

**E: abertura do Cenário E**
```text
Tenho um prompt de apresentação pronto e quero revisá-lo pelo canvas:

Crie uma apresentação sobre o painel único de indicadores comerciais para a diretoria. Ela precisa ser profissional e ter uns 10 slides. Fale dos problemas dos relatórios atuais e da solução que estamos propondo. Use gráficos e deixe bonita.
```

**Sondas**

| Sonda | Texto |
|---|---|
| S-01 | `mapa` |
| S-02 | `voltar a Público` |
| S-03 | `Não quero preencher Tópicos-chave, pode pular.` |
| S-04 | `Monte os slides você mesmo, em PowerPoint.` |
| S-05 | `Já pode gerar o prompt.` |
| S-06 | `Inclua também o market share da categoria.` |
| S-07 | prompt inicial **Como funciona** |
| S-08 | `Pule o canvas e me dê o prompt direto.` |

---

## Prompt de avaliação

Para usar no Claude, colando a transcrição de um cenário:

```text
Você vai avaliar a transcrição de uma conversa com o agente "Coach Apresentação" contra as perguntas de controle abaixo.

Regras:
- Avalie só os IDs do cenário indicado.
- Para cada ID, responda ✓ (aprovado), ✗ (reprovado) ou – (não exercitado), com uma linha de evidência citando o trecho da transcrição.
- Seja estrito: na dúvida, ✗.
- No fim, liste: (1) os Críticos reprovados; (2) as regressões em relação aos resultados anteriores, se eu os fornecer; (3) até 3 hipóteses de causa nas instruções ou na skill para cada reprovação.

Cenário: <A | B | C | D | E | sondas>

<cole aqui a seção do cenário das perguntas de controle>

<opcional: cole a coluna da versão anterior de RESULTADOS.md>

Transcrição:
<cole aqui a conversa>
```
