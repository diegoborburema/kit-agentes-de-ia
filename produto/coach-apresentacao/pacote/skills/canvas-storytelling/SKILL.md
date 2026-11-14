---
name: canvas-storytelling
description: 'Canvas de Apresentação: as 15 caixas do canvas, as dependências entre elas, as regras de triagem (obrigatória, opcional, dispensada), os formatos do mapa e da síntese e o modelo do prompt final para o Claude. Use em qualquer pedido de criar, adaptar ou revisar uma apresentação.'
---

## 1. Caixas do canvas

As caixas têm números em até três trilhas: **vd** = Conteúdo, **az** = Pessoas, **rx** = Pessoal.

| Caixa | vd | az | rx | Pergunta | Critério de qualidade |
|---|---|---|---|---|---|
| Público | – | 0 | – | Quem é o público? | Senioridade, background e proximidade com o apresentador; o que já sabem; o que valorizam ou rejeitam |
| Contexto | – | 0 | – | Onde estamos? | Onde e como a apresentação acontece: formato, duração, presencial ou remoto, clima (rotina, intimista, evento). O que no ambiente pode dar cor |
| Objetivo | 0 | 1 | 0 | Por que essa apresentação está acontecendo? | O que se quer atingir e o que se quer transmitir, em uma frase verificável |
| Expectativas | 0 | 1 | – | O que o público deseja ouvir? | Por que o público reservou esse tempo; o que espera; se há um "elefante na sala" |
| Conteúdo | 1 | 2 | – | O que quero falar e mostrar? | Todas as ideias, sem filtro: quantidade antes de qualidade |
| Introdução pessoal | 1* | 3 | 2 | Quem é você? | Como o apresentador quer ser apresentado (por alguém ou por si mesmo) e quando: no início ou logo após a abertura, com o interesse já desperto |
| Organização | 2 | – | – | Como essas informações se conversam? | Ideias agrupadas em ordem lógica ou cronológica; o que não serve ao objetivo sai |
| Linguagem | – | 2 | 1 | Como me comunicar com esse público? | Formalidade, jargão permitido e proibido, profundidade técnica |
| Tópicos-chave | 3 | 2 | 1 | Que frase todos devem levar na cabeça? | Interseção entre o que o público mais quer ouvir e o que o apresentador mais quer falar; resulta em uma frase |
| Conceitos não familiares | 4 | 3 | – | Algo precisa ser explicado? | Termos e conceitos que parte do público pode não conhecer e que precisam ser explicados antes de usados |
| Tangibilização | 5 | 3 | 2 | Como introduzir os novos conceitos? | Uma história, metáfora ou exemplo para cada conceito; onde entra emoção |
| Meio | 6 | 4 | 3 | Como persuadir e transmitir conhecimento? | Conteúdo e organização numa forma que faça sentido, em 3 partes, nem mais nem menos; algo que renove a atenção a cada 4–5 min |
| Abertura | 7 | 4 | 3 | Como despertar o interesse? | Agradecimento e apresentação; tema e objetivo; um recurso de impacto (vídeo, atuação, história, pergunta, dado ou frase) |
| Final | 8 | 4 | 3 | Qual é a chamada de ação? | Conclusão; repete a frase dos Tópicos-chave; próximo passo, reflexão ou provocação; deixa claro que o objetivo foi cumprido |
| Perguntas | 9 | 4 | 3 | Que perguntas podem surgir? | Perguntas prováveis e como respondê-las; perguntas interessantes que um aliado na audiência poderia fazer |

## 2. Dependências

Regra: uma caixa só pode ser trabalhada quando, em cada trilha em que aparece, todas as caixas de número menor estão resolvidas. Resolvida = concluída, opcional não preenchida ou dispensada.

\* Exceção: o vd 1 da Introdução pessoal não bloqueia as caixas verdes seguintes. Aplicada ao pé da letra, a regra cria um ciclo: pela trilha vd, a Introdução vem antes de Tópicos-chave; pela az, depois.

Ordem resultante (caixas do mesmo nível podem ir juntas):

1. Público, Contexto
2. Objetivo, Expectativas
3. Conteúdo, Linguagem
4. Organização
5. Tópicos-chave
6. Conceitos não familiares, Introdução pessoal
7. Tangibilização
8. Meio
9. Abertura
10. Final
11. Perguntas

Ao reabrir uma caixa ("voltar a"), avise que as caixas de níveis posteriores que dependem dela podem precisar de revisão.

## 3. Triagem

**Núcleo, sempre obrigatório:** Público, Objetivo, Expectativas, Conteúdo, Organização, Tópicos-chave, Meio, Abertura, Final.

Perguntas de triagem. Faça só as que não puderem ser inferidas do que o usuário já disse ou anexou, como múltipla escolha:
- **T1.** Relação com o público: pares da mesma área · outra área · liderança · externo · misto. O público te conhece? sim · em parte · não
- **T2.** O público domina o tema? sim · em parte · não
- **T3.** Objetivo principal: informar · ensinar · convencer · obter uma decisão
- **T4.** Formato: duração aproximada · reunião de rotina, reunião importante ou evento/auditório · presencial ou remoto
- **T5.** Há resistência, tema sensível ou decisão difícil em jogo? sim · não · não sei
- **T6.** Haverá espaço para perguntas do público? sim · não · não sei

Regras das caixas condicionais:

| Caixa | Obrigatória | Opcional | Dispensada |
|---|---|---|---|
| Contexto | Formato fora da rotina (evento, auditório, remoto com muita gente, espaço curto numa agenda maior) ou tipo "outro público" | Demais casos | Reunião recorrente com o mesmo grupo |
| Linguagem | Público de outra área, externo, misto ou liderança; ou tipo "outro público" | Pares da mesma área | Nunca |
| Conceitos não familiares | O público não domina o tema | Domina em parte | Domina |
| Tangibilização | O público não domina o tema, ou o objetivo é convencer ou obter uma decisão | Domina em parte e o objetivo é informar ou ensinar | Domina e o objetivo é informar |
| Introdução pessoal | O público não conhece o apresentador | Conhece em parte | Conhece bem |
| Perguntas | O objetivo é obter uma decisão, há resistência ou tema sensível, ou haverá perguntas | Demais casos | Nunca |

"Não sei" conta como o caso mais exigente.

Ajustes por tipo de atividade:
- **Nova apresentação:** as regras acima.
- **Adaptar existente:** extraia Conteúdo e Organização do arquivo e peça validação; depois de validadas, contam como concluídas. Meio, Abertura e Final partem da estrutura atual.
- **Outro público:** Público, Contexto, Expectativas e Linguagem são obrigatórias; Conteúdo vem do material existente; Conceitos e Tangibilização são avaliados para o novo público; Tópicos-chave é revalidado.
- **Revisar prompt ou roteiro:** classifique cada caixa obrigatória como ✓ presente, ◐ fraca ou ○ ausente no material. As ✓ contam como concluídas; o canvas percorre só as ◐ e ○.

Ajustes por duração:
- **Até 10 min:** Introdução pessoal em no máximo uma frase; o Meio dispensa a renovação de atenção.
- **Acima de 30 min:** Perguntas é obrigatória; o Meio indica o recurso de renovação de atenção de cada parte.

## 4. Formatos

**Mapa do canvas**

| Nível | Caixa | Classificação | Motivo | Status |
|---|---|---|---|---|

Status: ✓ concluída · ◐ em andamento · ○ pendente · — dispensada

**Síntese**
- Para quem:
- Por quê:
- Mensagem-chave (frase dos Tópicos-chave):
- Arco: Abertura → Meio (partes 1, 2 e 3) → Final
- O que precisa acontecer depois:
- Lacunas `[a validar]`:

## 5. Modelo do prompt final (para o Claude)

Preencha cada seção com o conteúdo aprovado, por extenso: o Claude não terá acesso a esta conversa. Retire as seções de caixas dispensadas ou de opcionais não preenchidas. Por padrão, mantenha o passo 3 do Processo (pausa para aprovação do roteiro); retire-o só se o usuário pedir execução direta.

~~~text
# Papel
Você é especialista em storytelling executivo e design de apresentações. Sua tarefa é criar uma apresentação em PowerPoint (.pptx) a partir do briefing abaixo, construído com o Canvas de Apresentação.

# Briefing
## Público
## Contexto
## Objetivo
## O que o público espera ouvir
## Conteúdo disponível
(fatos e dados com fonte; hipóteses marcadas como hipóteses)
## Organização das ideias
## Linguagem
## Mensagem-chave
(a frase que todos devem levar na cabeça)
## Conceitos a explicar e como tangibilizar cada um
## Introdução pessoal
(quem apresenta, como e em que momento)
## Estrutura definida
- Abertura:
- Meio, parte 1:
- Meio, parte 2:
- Meio, parte 3:
- Final e chamada de ação:
## Perguntas prováveis e respostas
## Execução
- Duração e formato:
- Idioma:
- Template: [anexado / não anexado]
- Lacunas [a validar]:

# Regras
1. Tudo serve à mensagem-chave: ela aparece na abertura e é repetida no final.
2. A abertura desperta interesse antes de qualquer contexto.
3. O meio tem 3 partes. [Se a duração passar de 10 min: renove a atenção a cada 4–5 min com história, pergunta ao público, dado surpreendente ou mudança de formato.]
4. O final retoma a ideia central e fecha com a chamada de ação.
5. Um slide, uma ideia. Título afirmativo: a conclusão do slide, não o tema.
6. Texto visível mínimo; o detalhe vai para as notas do apresentador.
7. Diferencie fatos (com fonte), hipóteses e recomendações. Não invente números nem fontes: use [a validar].
8. Explique cada conceito da lista antes de usá-lo, com a tangibilização indicada.
9. As perguntas prováveis viram slides de apoio no apêndice.
10. Defina o número de slides de forma coerente com a duração (referência: 1 a 2 minutos por slide).

# Processo
1. Proponha a arquitetura narrativa: o arco, o número de slides e o tempo de cada seção.
2. Monte o roteiro slide a slide numa tabela: nº · título afirmativo · mensagem · conteúdo visível · visual e layout · notas do apresentador · tempo · fonte.
3. Pare e aguarde minha aprovação do roteiro.
4. Com o roteiro aprovado, crie o arquivo .pptx. Com template anexado, use os layouts, as cores e as fontes dele; sem template, use um design limpo e corporativo, com hierarquia visual clara e variedade de layouts com propósito.
5. Antes de entregar, confira: a mensagem-chave está na abertura e no final; cada slide tem uma só ideia; os tempos somam a duração; nenhum número está sem fonte ou sem a marcação [a validar].
~~~

## 6. Checagem antes de entregar o prompt
- Todas as caixas obrigatórias estão no prompt, com o conteúdo aprovado e sem resumir.
- Fatos, hipóteses e lacunas estão claramente separados.
- O prompt não depende desta conversa para ser entendido.
- O prompt está num único bloco de código.
