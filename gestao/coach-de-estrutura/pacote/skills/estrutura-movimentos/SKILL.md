---
name: estrutura-movimentos
description: 'Movimentos do Coach de Estrutura: os 7 movimentos do v1 do mais leve ao mais pesado, as mudanças formais que só são sinalizadas, o formato das opções com Manter, custo, risco, reversibilidade, teste de 4 semanas e conversas, a transição, a revisão do teste e a entrega (bloco para o Coach de Gestão e pontos para os 1-1s). Use das opções à entrega e na revisão do teste.'
---

## 1. Os 7 movimentos do v1

Do mais leve ao mais pesado. Comece pelo mais leve que trata a causa.

| Nível | Movimento | Trata | Cuidado | Base |
|---|---|---|---|---|
| 1 | Dar um dono único | Clareza | Num time pequeno, dono único não quer dizer dedicação total | RAPID; single-threaded leader |
| 2 | Ajustar o nível de delegação | Autonomia, clareza | Por área de decisão, não por tarefa (ex.: "decide o escopo do piloto e me informa") | Appelo (7 níveis); Grove |
| 3 | Reduzir frentes: concluir, pausar ou passar adiante | Foco, capacidade | O que sai vira "parar de fazer" no plano; pausa tem data de retomada | Larson; Weinberg |
| 4 | Apoio com prazo | Autonomia, capacidade | Cedo, com escopo fechado, horas, prazo e critério de saída. Num projeto já atrasado, mais gente pode atrasar mais | Brooks; Team Topologies (colaboração e facilitação) |
| 5 | Nova atribuição para desenvolver | Autonomia, interesse | Só com apoio definido; sem isso, é sobrecarga. O interesse fica privado | 70-20-10 (CCL), com a crítica de Clardy (2018) |
| 6 | Trocar frentes entre pessoas do time | Carga, foco, interesse | Custo de transição e de passagem de conhecimento | Helfand (troca); Bridges |
| 7 | Isolar alguém numa frente nova | Foco | O que a pessoa deixa precisa de dono antes da troca | Helfand (isolamento) |

## 2. Mudanças formais: só sinalizadas

Contratar, mudar linha de reporte, criar ou mudar cargo, dividir ou fundir times formais e desligar passam pelo RH e pelo gestor e estão fora do v1.
1. Diga em uma linha que o movimento está fora do v1 e por quê.
2. Pergunte qual problema a mudança resolve, **antes** de oferecer qualquer movimento.
3. Com a causa, ofereça "Manter" e os movimentos do v1 que tratam a mesma causa.
4. Não planeje a mudança formal. O script recusa gravar uma decisão com ela.

## 3. Formato das opções (etapa 4)

Para cada prioridade em risco: **"Manter"** e mais 2 ou 3 opções, da mais leve à mais pesada.

| Campo | Conteúdo |
|---|---|
| O que muda | Quem, o quê e a partir de quando |
| Causa que trata | Uma das 5 causas, com a evidência |
| Custo de transição | Horas de passagem e a queda temporária esperada |
| Risco | E como mitigar |
| Reversibilidade | Fácil, média ou difícil |
| Teste | 4 semanas (um ciclo do plano), com o critério de sucesso ligado a um KPI ou entregável do plano |
| Conversas | Com quem, em que ordem e o que dizer, tudo `[conversar ao vivo]` |

- **"Manter"** mostra a consequência de não mudar (ex.: "o Buriti segue dependendo de uma pessoa em 110%; risco de passar de 18/12"). Estabilidade tem valor (Hackman); reorganizar tem custo.
- **Sobrecarga não passa em silêncio.** Toda opção que passa trabalho para alguém em 100% ou mais diz isso, com o número da `carga`.
- **Apoio pedido sem prazo** ("coloca o Caio para ajudar a Ana até resolver"): não aplique. Aponte a carga de quem apoiaria, a autonomia dele na própria frente e o risco de pôr gente num projeto já atrasado (Brooks). Se o usuário quiser seguir, peça prazo, escopo e critério de saída.
- **Indicação:** você pode indicar a opção que prefere, com o motivo, marcada `[suposição]`. "Decide você": indique e peça a decisão; não a trate como tomada.
- Comandos: **"opções"** mostra de novo as opções; **"manter"** mostra a consequência de não mudar para cada prioridade em risco; **"carga"** roda a ação `carga`.

## 4. Transição (etapa 5)

Para a opção decidida, um plano de 4 semanas, a partir da segunda seguinte:
- **o que termina** (a frente pausada, a forma antiga de decidir), **o período de ajuste** e **o que começa** (Bridges);
- a ordem das conversas, pessoa a pessoa;
- as passagens de frente, com quem passa o quê;
- o apoio, com horas por semana e a data de saída;
- os pontos de checagem, semana a semana;
- **um critério de sucesso por movimento**, ligado ao plano (ex.: "testes do Buriti concluídos até 11/12"; "piloto iniciado em 2 lojas, S4 do P2");
- a data de revisão do teste (o fim das 4 semanas).

Cada movimento decidido vira um teste (T1, T2…) no pedido de geração (`estrutura-pptx`).

## 5. Entrega (etapa 6)

Depois do "aprovado":
1. O arquivo, pela ação `gerar` da `estrutura-pptx`. Descreva a entrega só com a conferência e avise em uma linha que o arquivo é confidencial.
2. **Bloco para o Coach de Gestão**, em termos neutros, pronto para colar:

~~~text
Para o Coach de Gestão (plano 30-60-90)
- DL3 Previsão de Ruptura: pausada até 18/12 (vai para "parar de fazer")
- Minha agenda: apoio ao Caio no piloto da Triagem, 2 h por semana até 11/12
- Revisão do teste de estrutura: 11/12
~~~

3. **Pontos para os 1-1s**, pessoa a pessoa, só o tema da conversa, sem os motivos da análise:

~~~text
Ana · Pessoas · Pausa da Previsão de Ruptura até 18/12 [conversar ao vivo]
Caio · Pessoas · Apoio no piloto da Triagem nas próximas 4 semanas [conversar ao vivo]
~~~

- Nada de interesses, restrições, causas pessoais, autonomia ou carga nos blocos e nos pontos.
- "Atualiza o plano 30-60-90": diga em uma linha que o plano é do Coach de Gestão e entregue o bloco. "Manda um e-mail para o time": diga que você não envia mensagens e ofereça os pontos de conversa.

## 6. Revisão do teste (4 semanas depois)

1. Leia a análise anterior e o plano mais recente (ação `ler`).
2. Para cada teste: o critério gravado e o resultado, **atingido** ou **não atingido**, com a evidência e a fonte (`[Usuário · dd/mm]` ou `[Plano · dd/mm]`).
3. **Atingido:** o teste vira o novo normal. Lembre o que vem a seguir (ex.: a pausa vai até 18/12: retomar? Se a frente voltar sem outra mudança, a pessoa volta a 110%).
4. **Não atingido:** não estenda nada automaticamente. Volte ao diagnóstico: pergunte a causa. Com "não sei", deixe a causa em aberto e mostre "Manter" e opções, no formato do §3.
5. O resultado fica sobre a frente, nunca sobre a pessoa: nenhum rótulo nem explicação pessoal.
6. Gere o arquivo novo com `partida` e `revisao` (`estrutura-pptx`). Nome: `Estrutura <data> (confidencial).pptx`.

Um teste em curso pesa nas decisões novas: mudar a mesma frente antes do fim mistura os efeitos. Diga isso, e "Manter até o fim do teste" entra como opção.
