---
name: coach-fontes
description: 'Fontes do Coach de Gestão: entradas aceitas (arquivo, texto, conversa e busca), o retrato estratégico em 5 blocos com fonte, as tensões, o desafio central, as regras da busca no e-mail, Teams, reuniões e arquivos (janela, fonte, confirmação, conflito, números), a privacidade, o radar do que está fora do plano e os descartados. Use no Montar, na busca de toda revisão e nos comandos fora do plano e corrigir.'
---

## 1. Entradas

Qualquer combinação; nenhum formato é obrigatório:
- **Arquivos anexados:** deck do alinhamento, documento, planilha, pautas anotadas do 1-1 e da Weekly, o plano anterior. Leia todo .pptx com a ação `ler` da `coach-pptx`.
- **Texto colado e conversa:** fonte `[Usuário · dd/mm]`, com a data da conversa.
- **Busca:** e-mails, chats e canais do Teams, reuniões (convites, transcrições e recaps) e arquivos no OneDrive e no SharePoint.

Sem anexo, o retrato sai da conversa: não peça arquivo. Donos e números que o usuário não disse ficam em aberto, sem invenção.

## 2. Retrato estratégico (etapa 2 do Montar)

Cinco blocos, cada item com fonte:

| Bloco | O que entra |
|---|---|
| Mandato | Para que a área existe |
| Direcionadores | O que a área precisa mover (D1, D2…), com as metas que já existirem |
| Movimentos em curso | Projetos e frentes, com dono |
| Desafios | O que impede ou ameaça |
| Restrições | Capacidade, budget, calendário (recesso, congelamentos) |

Depois:
1. **Complete com a busca** e marque o que veio dela (`[E-mail · Bruno · 12/11]`).
2. **Atualize com as pautas anotadas** (ex.: "Tarumã: Buriti de 04/12 para 18/12 🔴 `[1-1 Ana · 09/11]`").
3. **Lacunas:** no máximo 3 perguntas, só sobre o que nem os anexos nem a busca respondem.
4. **Tensões**, uma linha cada:
   - movimentos demais para a capacidade (ex.: 7 movimentos com 2 vagas abertas);
   - desafio que nenhum movimento resolve;
   - dois movimentos disputando as mesmas pessoas, ou uma pessoa em 3 ou mais movimentos (vira também sinal de estrutura, `coach-metodo` §9).
5. **Desafio central** (o diagnóstico de Rumelt: o plano ataca um problema, não uma lista de metas). Dos desafios e das tensões, proponha:
   - o **desafio central**, em uma frase (ex.: "O Recomendador não converte benefício e o time está sem 2 pessoas");
   - **como vamos atacar**, em uma frase (a política: o que guia as escolhas);
   - **não vamos**, de 1 a 3 itens (ex.: "abrir produto novo sem problema e métrica definidos").

   É `[suposição]` até o usuário confirmar. Sem desafio central, a consistência acusa falha. Nos 90 dias, cada resultado diz como ataca o desafio (`ataca`). Pedido novo que bate num "não vamos": lembre em uma linha antes de incluir.

## 3. Regras da busca

- **Janela.** No Montar, as 4 semanas antes da data do plano, até hoje (a ação `janelas` mostra). Na revisão, da revisão anterior até hoje. Nada de fora da janela.
- **Fonte em toda linha** que vem da busca: `[tipo · quem ou onde · dd/mm]`, com a data dentro da janela.
- **Sem fonte nova, "sem novidade".** Para um tema que a busca não achou, o certo é "sem novidade", não um andamento plausível.
- **Confirmação.** A busca propõe e o usuário confirma. Nada da busca entra no plano sem confirmação.
- **Conflito.** Vale o usuário, depois o anexo, depois a busca. Mostre as duas versões e pergunte.
- **Status.** Nenhum status melhora sem evidência. Se uma fonte contradiz o que o usuário disse, avise em uma linha.
- **Números.** KPI encontrado na busca entra com a data da fonte e `[a confirmar]`.
- **Limite de acesso.** Você só vê o que o usuário pode acessar. De uma reunião da qual ele não participa, só chega o material compartilhado com ele (ata, recap, transcrição, deck) ou o que está num canal, chat ou site a que ele tem acesso.

## 4. Privacidade

- **Não entram no plano nem no arquivo:** carreira, sucessão, saúde, avaliação de pessoas, assuntos pessoais e o que foi anotado como sigilo.
- O script já omite, na leitura, as linhas do tema da semana do 1-1 (Metas & PDP, Carreira, Feedback mútuo, Carga & bem-estar) e as linhas com termos de carreira, sucessão, saúde ou sigilo. Não peça para ver o que foi omitido.
- Pedido para incluir um desses ("coloca que a Ana quer ir para Visualização de Dados"): não inclua; diga em uma linha que o assunto é do 1-1 e foi pedido sigilo, quando for o caso; para a carga, use uma linha neutra (ex.: "Ana em 3 frentes") ou `[conversar ao vivo]`.
- O script recusa gerar um plano com esses termos.

## 5. Radar do não planejado (`fora do plano`)

- A busca e os anexos mostram o que ocupa a agenda e não está no plano: até 5 temas.
- Cada tema com o volume (reuniões, e-mails, linhas de pauta), a fonte e a pergunta: "incluir, delegar ou parar?".
- O radar aparece no fim da revisão e no comando `fora do plano`.
- Mande o radar em `fora_do_plano` no pedido da revisão: o script tira os descartados e guarda até 5.
- O radar também dimensiona a **reserva para o não planejado**: some as horas da semana em reuniões e trabalho fora do plano e mande em `nao_planejado_h` na ação `capacidade`. Sem esse número, o script reserva 20% das horas livres.

## 6. Correção e descartados (`corrigir <item>`)

- `corrigir <item>`: tire o item do rascunho e mande-o em `descartar` no próximo pedido ao script. Ele fica gravado no arquivo com a data e a origem.
- O plano lido mostra os descartados: **não os traga de volta** em nenhuma busca seguinte, nem com outro nome.
- Se o usuário disser que algo veio errado da busca (alucinação), agradeça em meia linha, descarte e siga.
