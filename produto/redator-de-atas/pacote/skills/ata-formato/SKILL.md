---
name: ata-formato
description: 'Formato e estilo da ata do Redator de Atas: título e linha de data e link, Markdown que funciona no Loop, no Teams e no e-mail, tabelas de participantes e de próximos passos, seleção e síntese (o que entra, o que é lateral, como consolidar temas sobrepostos), linguagem executiva, o bloco de conferência abaixo da ata, a lista de omitidos, a revisão, a entrega e o comando markdown, com um exemplo completo. Use para escrever e revisar qualquer versão da ata.'
---

## 1. Cabeçalho

```
# Ata de Reunião | <tema>

<dd/mm/aaaa> · [<rótulo do link>](<link>)
```

- **Tema:** o assunto da reunião em poucas palavras, com o nome do projeto ou do produto como a fonte o escreve (ex.: "Refinamento Painel Jatobá – Pós-avaliação de promoções (Onda 2)"). Tire do título do arquivo os sufixos automáticos ("-20261110_140112-Gravação de Reunião").
- **Linha abaixo do título:** a data da reunião e, quando houver, o link útil (gravação, Loop ou documento da reunião) dado pelo usuário ou achado na própria reunião. Sem link, só a data. Não acrescente duração, horário, fonte, objetivo nem sprint.

## 2. Participantes

Com pelo menos uma área comprovada, use uma tabela, sem bullets:

```
| Participante | Área |
|---|---|
| Lucas Andrade | |
| Ana Souza | Dados |
```

Sem nenhuma área comprovada, use uma lista simples. A ordem é a da primeira fala ou a das notas; o usuário pode pedir outra.

## 3. Pontos Alinhados e demais seções

- Temas em `### 1. <tema>`, numerados, na ordem lógica da execução: cenário atual, regra, insumos, decisão, pendência.
- Bullets curtos, de no máximo duas linhas. Sub-bullets só para listar insumos, tipos ou regras de um item. No máximo dois níveis.
- Rótulos em negrito no início do bullet ou numa linha própria, só quando organizam a leitura: **Processo atual**, **Direcional acordado**, ou o nome do risco em Riscos e Pontos de Atenção.
- Parágrafo corrido só quando uma explicação causal não cabe em bullets.

## 4. Próximos Passos

```
| Ação | Responsável | Prazo |
|---|---|---|
| Fechar o desenho da tabela de exceções e enviar à Renata | Ana Souza | 12/11 |
| Estimar o esforço do cálculo | Bruno Prado, Caio Teles | 16/11 |
```

- Ação começa com verbo no infinitivo e diz o entregável quando ele foi dito.
- Todos os responsáveis da ação na mesma linha, separados por vírgula, com nome e sobrenome como em Participantes. @menção da fonte é mantida como está.
- A coluna Prazo só existe se houver pelo menos um prazo dito; prazo em `dd/mm`. Célula sem prazo fica vazia.
- Uma linha por ação. Duas ações da mesma pessoa são duas linhas.

## 5. Seleção e síntese

- **Uma versão publicável e enxuta.** Normalmente Participantes, Pontos Alinhados, Riscos e Pontos de Atenção e Próximos Passos, conforme o tipo (skill `ata-tipos`).
- **O que entra:** os temas que tiveram detalhamento, direcional ou ação concreta.
- **O que fica fora:** assunto só mencionado ou sem consequência para a execução, recado, conversa social, alternativa adiada. Guarde a lista para o comando `omitidos`.
- **Consolide:** temas sobrepostos, ou o mesmo tema discutido em dois momentos da reunião, viram um bloco só, orientado à execução. Não crie uma seção para cada assunto citado.
- **Sem repetição:** a mesma informação não aparece em Pontos Alinhados, Decisões Tomadas e Riscos.
- **Preserve o que muda a execução:** etapas, regras, valores, percentuais, exceções, sistemas, origens de dados, exemplos e validações humanas.

## 6. Linguagem

- Executiva, neutra, concisa, em voz ativa, em português do Brasil.
- Preserve as formulações importantes do negócio, as siglas, os nomes de sistemas, os jargões, os links e as @menções. Tire a oralidade ("né", "tipo", "então, assim") e as repetições.
- Não atribua falas literais, salvo quando a formulação exata importa; atribua posição e autoria quando importam ("segundo o Otavio", "proposta da Ana").
- Sem emojis, sem HTML, sem IDs de fala (T001), sem marcas de fonte e sem notas de rodapé.

## 7. Markdown para Loop, Teams e e-mail

- `#` só no título; `##` para as seções; `###` para os temas.
- Tabelas simples: cabeçalho, separador `|---|` e uma linha por item. Sem células mescladas, sem quebra de linha dentro da célula e sem listas na célula.
- Listas com `-`. Negrito com `**`. Links como `[rótulo](url)`.
- A resposta renderizada copia bem para o Outlook e para o Teams. O comando `markdown` devolve o texto cru num bloco de código, para colar no Loop ou em outro editor que entende Markdown.

## 8. Rascunho, conferência e revisão

**Rascunho:** a linha de status, a ata completa, uma linha `---` e o bloco:

```
**Conferência** (não faz parte da ata)
1. Gustavo Lima e Helena Costa estavam no convite e não falaram. Ficaram fora da ata. Algum esteve presente? Sugestão: manter fora.
2. "Ver com o jurídico se a tabela pode ter nome de promotor" está sem responsável. Quem assume? Sugestão: manter como pendência em Riscos.
3. Prazos convertidos pela data da reunião (ter 10/11): quinta = 12/11, sexta = 13/11, segunda = 16/11.
```

- No máximo 6 pontos, só os que o usuário resolve (skill `ata-fidelidade` §9). Sem pontos: "Conferência: nada a confirmar."
- No fim, em uma linha: "Responda os pontos ou diga **aprovado**. `omitidos` mostra o que ficou de fora."

**Revisão:** aplique só o que foi pedido e as respostas da conferência. Mostre só as seções que mudaram, com o título da seção, e a conferência que restar. Mudança que afeta a fonte (incluir participante, número, prazo) passa pelo `conferir` antes de aparecer.

**Omitidos:** uma linha por tema, com o ID da primeira fala: `Duplicidade de filial no Tarumã (comentário, T029)`. `incluir <tema>` traz o tema de volta, no bloco certo.

## 9. Entrega

Com "aprovado", "pode fechar" ou equivalente:
1. a linha de status;
2. a ata completa, limpa, sem a conferência e sem comentários antes ou depois, pronta para copiar;
3. no fim, uma linha: "Pronta para colar no Loop, no Teams ou no e-mail. `markdown` traz o texto cru."

## 10. Exemplo

Reunião fictícia, só para mostrar a forma:

```
# Ata de Reunião | Refinamento Integração Pitanga – Carga de devoluções

03/11/2026 · [Loop da reunião](https://exemplo.sharepoint.com/loop/pitanga-devolucoes)

## Participantes

| Participante | Área |
|---|---|
| Lucas Andrade | |
| Caio Teles | Ciência de Dados |
| Lúcia Prates | Logística |

## Pontos Alinhados

### 1. Carga diária de devoluções

**Processo atual**
- As devoluções chegam por e-mail da transportadora e são lançadas à mão pela Logística, uma vez por semana.

**Direcional acordado**
- A carga passa a ser diária, a partir de dois insumos:
  - Notas de devolução [Portal Ingá]
  - Motivos de devolução [Tabela | Logística]
- Devolução sem motivo entra como "a classificar" e não bloqueia a carga.
- Antes do fechamento do mês, a Logística valida as devoluções acima de R$ 20 mil.

## Riscos e Pontos de Atenção

- **Histórico:** o Portal Ingá só guarda 90 dias. A carga do histórico anterior depende de exportação manual, ainda sem dono.

## Próximos Passos

| Ação | Responsável | Prazo |
|---|---|---|
| Enviar a tabela de motivos de devolução | Lúcia Prates | 06/11 |
| Testar a leitura das notas do Portal Ingá | Caio Teles | |
```
