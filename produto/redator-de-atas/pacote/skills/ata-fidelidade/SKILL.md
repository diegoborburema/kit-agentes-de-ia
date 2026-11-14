---
name: ata-fidelidade
description: 'Regras de fidelidade do Redator de Atas: o que é fonte, a leitura completa, como separar decisão, alinhamento, hipótese, recomendação, dúvida, risco, próximo passo e tema lateral nas falas, quem é responsável e o que é prazo, prova de presença e área dos participantes, números e correções, trecho não identificado, o que nunca entra na ata, a conferência para o usuário e a verificação final. Use em toda ata, do rascunho à entrega, e no comando evidência.'
---

## 1. Fonte

- **A reunião escolhida e nada mais:** a transcrição, as notas, os anexos dela, o chat da própria reunião e o que o usuário disser na conversa.
- **Não é fonte de fato:**
  - outra reunião, chat ou e-mail, mesmo do mesmo projeto;
  - o convite, como prova de presença;
  - o seu conhecimento geral;
  - o resumo gerado por IA (ex.: o recap inteligente do Teams). Ele serve só para achar o trecho na transcrição.
- **O que o usuário diz é fonte.** "O Gustavo estava, só ouvindo" faz do Gustavo um participante (`confirmados`). Número ou prazo que ele der vai em `extras` na conferência.

## 2. Leitura

1. Rode `ler` com todos os anexos (skill `ata-transcricao`).
2. Leia **todos** os blocos com `trecho`, do primeiro ao último.
3. Só depois extraia e escreva. A linha de status mostra `Leitura k/n blocos`.

Pela busca do Teams, sem anexo, a transcrição pode vir em trechos: a linha de status diz `Cobertura: parcial (busca)`, e a conferência pede o .docx para a versão final.

## 3. O que cada fala é

Antes de escrever, separe para você, sem mostrar, cada item com o tipo, o texto, quem, o prazo e os IDs das falas.

| Tipo | O que é | Sinais comuns na fala | Na ata |
|---|---|---|---|
| Decisão | Escolha fechada por quem pode decidir, sem objeção | "fechado", "então fica assim", "vamos seguir com", "está decidido", "de acordo" depois de uma proposta | Direcional acordado, ou Decisões Tomadas |
| Alinhamento | Entendimento comum de regra, processo ou escopo, sem escolha nova | explicação aceita ("é assim que funciona"), "isso", "exato" | Pontos Alinhados |
| Hipótese | Possibilidade não confirmada | "acho que", "provavelmente", "talvez", "pode ser", "a ideia seria", "poderíamos" | Escrita como hipótese, nunca como decisão |
| Recomendação | Opinião sobre o que seria bom | "o ideal seria", "eu sugiro", "seria legal" | Com autor, e só se mudar a execução; senão, fora |
| Dúvida | Pergunta sem resposta na reunião | "não sei", "precisa ver se", "quem vê isso?" | Riscos e Pontos de Atenção, ou Dúvidas em Aberto |
| Risco | Consequência negativa discutida | "o risco é", "se não…, …", "é bloqueante", "me preocupa" | Riscos e Pontos de Atenção |
| Próximo passo | Ação que alguém assumiu ou recebeu e aceitou | "eu fico com", "eu vejo", "deixa comigo", "consigo", pedido seguido de "pode deixar" | Próximos Passos |
| Lateral | Assunto sem detalhamento, direcional nem ação | menção de passagem, outro projeto, recado | Fora (comando `omitidos`) |

- **Na dúvida entre decisão e hipótese, é hipótese.** A conferência pergunta.
- **Alternativa só avaliada** (outra arquitetura, outro sistema) não ganha seção. Adiada ou descartada ("vamos deixar fora deste refinamento"): fora da ata e em `omitidos`.
- **"Fica como possibilidade para depois"** não é compromisso: fora, ou uma linha como hipótese se mudar a execução.
- **Correção vale a última.** Se um número ou uma regra aparece mais de uma vez, busque e use o que foi dito por último. "Na verdade, é 12%" substitui o 15% dito antes. O valor antigo não entra.

## 4. Responsável e prazo

**Responsável** é quem assumiu a ação ou quem a recebeu e aceitou, de forma explícita. Confirme com `buscar` antes de escrever.

| Na fala | Responsável |
|---|---|
| "Eu fico com o desenho e mando até quinta" | Quem falou |
| "Bruno e Caio, vocês conseguem…?" · "Consigo, junto com o Caio" · "Fechado" | Bruno e Caio, na mesma linha |
| "Eu levo para o Gustavo validar" | Quem falou (a ação é levar), não o Gustavo |
| "Eu posso ajudar, mas…" | Ninguém por isso; ajudar não é assumir |
| "Isso me lembra o problema do Tarumã" | Ninguém; comentar não é assumir |
| "Dá para trocar, é simples" | Ninguém; dizer que dá não é assumir |
| Pedido sem resposta ("Ana, você vê isso?" e silêncio) | Conferência: "atribuída à Ana, sem confirmação dela" |
| "Precisamos ver com o jurídico" · "quem vê?" · "a gente define no grupo" | Ninguém. Pendência em Riscos e Pontos de Atenção; a conferência pergunta quem assume |

- Responsável ausente da reunião só quando a ação foi atribuída a ele com todas as letras. A conferência pede a confirmação.
- Grupo como responsável ("time do Hub", "Trade") só quando dito assim.
- Ação sem dono que é só tema para avaliar: fora. Ação confirmada e indispensável sem dono: em Riscos e Pontos de Atenção, ou na tabela com "não informado", e na conferência.

**Prazo** só quando dito.
- Dia da semana ou "amanhã" vira data pela data da reunião, na próxima ocorrência depois dela. Exemplo: "até quinta", numa reunião de terça, 10/11, vira 12/11. A conferência mostra a conversão.
- "Semana que vem", "logo", "depois do go-live" e "até a próxima reunião" não viram data. Mantenha as palavras, se ajudarem.
- Dependência não é prazo.
- A coluna Prazo só existe com pelo menos um prazo dito.

## 5. Participantes e área

**Prova de presença:**
- ter falado na transcrição;
- constar como presente nas notas;
- ter iniciado a transcrição ou a gravação;
- identificar-se numa fala do dispositivo da sala ("aqui é o Marcos, de Vendas"): passe em `presentes` com o ID da fala;
- ter escrito no chat durante a reunião;
- ser confirmado pelo usuário.

**Não é prova:** ser convidado, ser citado ("eu levo para o Gustavo"), ser responsável por uma ação ou ter ido a outra reunião. Convidado sem prova vai para a conferência, nunca para a ata.

**Nomes**
- Em ordem natural, sem sufixo de localização nem "(Convidado)": "Andrade,Lucas,BR-São Paulo" vira Lucas Andrade.
- Escritos como na fonte, sem acrescentar acento.
- Só o primeiro nome quando a fonte só traz o primeiro nome.
- O usuário é participante se falou.

**Área**, só com evidência, nesta ordem:
1. o que o usuário disser;
2. o que a pessoa disser na reunião ("Ana, do time de Dados");
3. as notas ("Renata Okada (Trade Marketing)");
4. o departamento do diretório, quando a busca o trouxer, no nível útil (Dados, Produto, Trade Marketing).

Externo: a organização, quando dita ("Paula, da Parceiro+"). Nunca deduza a área do assunto que a pessoa tratou nem do papel dela na reunião. Sem evidência, a célula fica vazia. Sem nenhuma área comprovada, liste só os nomes.

## 6. Números, regras e termos

- Preserve exatamente: valores, percentuais, moedas, datas, unidades, exceções, condições de regra, sistemas, siglas, jargões, links e @menções.
- Não arredonde, não converta unidade e não faça conta (soma, diferença, percentual derivado), salvo se a conta foi dita.
- Mantenha as ressalvas da fonte: "cerca de", "estimado", "número da área, não validado", "segundo a Renata".
- Mantenha juntas a condição e a consequência de uma regra, por exemplo: cliente de rede → rateio entre as filiais pelo volume faturado; cliente direto → 100% para a filial que faturou.
- Validação humana citada (quem valida, quando e antes de quê) é regra de execução: não some.

## 7. Trecho não identificado

- Use `[trecho não identificado]` quando a fala é inaudível ou truncada **e** importa para a execução. Sem importância, omita.
- Nunca complete a lacuna. "A carga de outubro do… (inaudível)… fica para depois do fechamento do Hub" vira "Carga de outubro: [trecho não identificado]; fica para depois do fechamento do Hub".
- Referência ambígua ("isso", "ele") que muda a execução vai para a conferência.
- Decisão ou ação dita por falante não identificado vai para a conferência.

## 8. O que nunca entra na ata

- Saúde, vida pessoal, avaliação ou desempenho de pessoas, salário, desligamento e conflito pessoal, mesmo que ditos.
- Recados e assuntos sociais (confraternização, avisos gerais), piadas e comentários sobre pessoas ausentes.
- Mudança de equipe ("a Helena saiu do projeto"): fora. Entra só se a reunião a tratou como lacuna de execução; nesse caso, em termo neutro ("responsável pelos testes a definir"). Se alguém disse que não é tema da reunião, fica fora.

A conferência diz, em termo neutro, que um trecho pessoal ficou fora, sem o conteúdo.

## 9. Conferência para o usuário

Depois do `conferir` sem nada para corrigir, mostre abaixo da ata, depois de uma linha `---`, a **Conferência** com no máximo 6 pontos que só o usuário resolve. Cada ponto ocupa uma linha e traz uma sugestão. Prioridade:
1. ação confirmada sem responsável;
2. presença: convidados sem fala, dispositivo de sala, falante não identificado;
3. decisão incerta, que pode ser hipótese;
4. prazos convertidos, todos numa linha;
5. trecho não identificado que muda a execução;
6. trecho pessoal retirado; cobertura parcial.

Ponto sem resposta: vale a sugestão. A resposta é fonte: aplique e passe em `confirmados` ou `extras` no próximo `conferir`.

## 10. Verificação final

Antes de mostrar qualquer versão, confirme:
- Li todos os blocos, ou a linha de status diz que a cobertura é parcial.
- Todos os participantes comprovados estão na ata, e nenhum convidado entrou só pelo convite.
- Cada afirmação, área, ação, responsável, prazo, risco e decisão tem uma fala que a sustenta.
- Decisão, alinhamento, hipótese, dúvida e próximo passo estão separados; nenhum "acho que" virou decisão.
- Os valores corrigidos na reunião estão na última versão.
- Os temas sobrepostos foram consolidados sem perder regras, percentuais, origens de dados nem pendências.
- Nenhuma informação se repete entre as seções.
- O `conferir` não deixou nada no grupo "Corrija".
- A ata não tem ID de fala, HTML, marcas de fonte nem trecho pessoal.
