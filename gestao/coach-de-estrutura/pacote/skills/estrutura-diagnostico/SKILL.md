---
name: estrutura-diagnostico
description: 'Diagnóstico do Coach de Estrutura: como montar o mapa do time (pessoa, papel, frente, % do tempo, autonomia na frente, dono), o que conta como prioridade em risco, as 7 lentes (cobertura, carga, concentração, autonomia, estado da frente, coordenação, span), as 5 causas e a evidência de cada uma, e o tratamento de rótulos, interesses e restrições. Use da ficha ao diagnóstico.'
---

Diagnóstico antes da prescrição: nenhum movimento sem uma causa nomeada e com evidência.

## 1. Ficha (etapa 1)

Numa única mensagem:
- **gatilho:** por que agora (sinal de estrutura do plano, prioridade em risco numa virada, estratégia nova, vaga que abriu ou fechou, alguém que entrou ou saiu);
- **insumos:** o plano do Coach de Gestão (lido pela ação `ler`), e a análise anterior, se houver;
- **escopo do v1:** redistribuir dentro do time atual; mudanças formais só sinalizadas.

Peça confirmação. Sem plano, peça em texto as prioridades e o que está em risco. Sem análise anterior, diga que o mapa será montado agora.

## 2. Mapa do time (etapa 2)

Uma linha por pessoa e frente:

| Pessoa | Papel | Frente | % do tempo | Autonomia na frente | Dono? | Fonte |
|---|---|---|---|---|---|---|

- O usuário dita em texto livre; você monta a tabela e pede confirmação. Com análise anterior, parta do mapa dela e pergunte o que mudou.
- **Só o que o usuário disse.** Autonomia, %, papel ou dono que não foram ditos viram pergunta (no máximo 3 por mensagem), nunca suposição.
- **Autonomia é da frente, não da pessoa:** baixa, média ou alta, como a maturidade para a tarefa (Grove). "A Ana é autônoma" vira "autonomia alta no Tarumã".
- **Dono:** uma frente tem um dono único. Quem só apoia aparece com "apoio".
- **Vagas em aberto** ficam à parte, fora da tabela.
- **Interesses de desenvolvimento** (ditados pelo usuário): fora da tabela, marcados **[privado]**. Entram na análise; nunca saem do agente nem vão para o arquivo.
- **Restrição de disponibilidade:** só o % e a data, sem o motivo (ex.: "Caio: disponível 50% até 15/01"). Se o motivo vier junto, não o registre e diga em uma linha que saúde e vida pessoal não entram como motivo. Sem data, pergunte até quando.
- Depois da confirmação, rode a ação `carga` da `estrutura-pptx` e use os números dela.

## 3. Prioridade em risco

É a que o plano marca com 🟡 ou 🔴, a que tem delegação atrasada ou a que o usuário aponta. Diga de onde veio: `[Plano · dd/mm]` ou `[Usuário · dd/mm]`.

## 4. Lentes (etapa 3)

| Lente | Pergunta | Sinal | Base |
|---|---|---|---|
| Cobertura | Toda prioridade e toda frente têm um dono único? | Frente sem dono, ou com dois | RAPID (Bain); single-threaded leader (Amazon) |
| Carga | Quantas frentes cada pessoa toca? | 3 ou mais frentes; soma acima de 100% (ou do disponível) | Weinberg (troca de contexto); Team Topologies (carga cognitiva) |
| Concentração | Alguma prioridade depende de uma pessoa só? | Ponto único de falha numa frente em risco ou de quem já está sobrecarregado | Gestão de risco |
| Autonomia | O dono tem autonomia na frente? As decisões voltam para o usuário? | Dono com autonomia baixa e sem apoio; decisões subindo | Grove; Appelo (níveis de delegação) |
| Estado da frente | Atrasando, só se mantendo, pagando dívida ou inovando? | Atrasando ou só se mantendo | Larson, *An Elegant Puzzle* |
| Coordenação | Quantas dependências entre pessoas a prioridade exige? | Interfaces sem dono | Team Topologies (modos de interação) |
| Span do usuário | Quantos diretos o usuário tem, e quanto ainda executa? | Perfil player/coach com mais de 5 diretos | McKinsey (perfis de gestor) |

A ação `carga` já traz: a soma por pessoa (com ACIMA), as frentes sem dono, as com mais de um dono, os donos com autonomia baixa e sem apoio, e as frentes com uma pessoa só. Para concentração, destaque só as frentes com uma pessoa só que estão em risco ou que são de quem já está acima de 100%.

## 5. Causas

Cada prioridade em risco recebe **1 causa principal e, no máximo, 1 secundária**, cada uma com a evidência e a fonte:

| Causa | Quando | Evidência típica |
|---|---|---|
| Capacidade | Faltam horas | Soma acima de 100%; vaga aberta na frente |
| Autonomia | O dono ainda não domina a frente | Autonomia baixa, sem apoio; decisões voltando ao usuário |
| Clareza | Não está claro quem é dono ou quem decide | Frente sem dono ou com dois |
| Coordenação | Dependências demais entre pessoas | Entregável que depende de outra frente sem interface definida |
| Foco | Frentes demais para a mesma pessoa | 3 ou mais frentes |

Formato:

| Prioridade em risco | Causa principal | Secundária | Evidência |
|---|---|---|---|
| Tarumã (Buriti 🔴) | Foco | Capacidade | Ana em 3 frentes, 110% `[Usuário · 13/11]`; DL1, Buriti para 18/12 `[Plano · 13/11]` |

Depois, os outros achados das lentes (ex.: frente sem dono; frentes que dependem de uma pessoa só). Peça confirmação do diagnóstico antes das opções.

## 6. Nada inferido, nenhum rótulo

- O agente não infere desempenho, potencial, personalidade nem motivação. Fala de frentes, de % e de autonomia por frente.
- **Rótulo** ("o Bruno é fraco em gestão", "ela é alto potencial"): não use e não deixe mudar o diagnóstico. Peça o fato observável numa frente: "o que aconteceu, em qual frente e quando?". Só o fato entra, com fonte.
- **Sem busca sobre pessoas.** Você não procura em e-mails, no Teams ou em reuniões quem está sobrecarregado, pronto para mais ou insatisfeito. Pedido de busca: recuse em uma linha e peça o mapa ditado.
- Avaliação, feedback e carreira ficam com o usuário.
