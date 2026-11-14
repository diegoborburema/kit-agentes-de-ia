# Redator de Atas: perguntas de controle

Bateria de regressão do agente, versão 1. Cada versão roda a bateria antes do merge, e o resultado entra em [`RESULTADOS.md`](RESULTADOS.md). As fixtures ficam em [`fixtures/`](fixtures/), usam só dados fictícios e são geradas por [`gerar_fixtures.py`](gerar_fixtures.py). As atas esperadas, escritas à mão, servem de gabarito. Os fatos-chave de cada reunião, com o ID da fala, estão no [anexo](#anexo-gabarito-das-fixtures). O desenho do agente está em [`NOTAS.md`](../NOTAS.md).

## Como usar

**Antes de abrir o Copilot.** Rode estes dois scripts:
- `python ferramentas/conferir_limites.py redator-de-atas`: confere os limites do Agent Builder (8.000 caracteres nas instruções e 20.000 por skill).
- `python produto/redator-de-atas/testes/conferir_codigo.py`: roda o script da skill `ata-transcricao` como o agente roda (pedido JSON), contra as fixtures.

O `conferir_codigo.py` confere:
- a leitura das quatro reuniões: falas, falantes, nomes em ordem natural, convidados sem fala, sala, notas e blocos;
- a busca;
- a conferência das quatro atas esperadas, que não deixa nada para corrigir;
- os 9 defeitos plantados numa ata ruim do Cenário A, todos apontados;
- as recusas;
- o plano B pelo interpretador.

Se ele falhar, não adianta testar no Copilot.

**O que rodar: depende do que mudou**

| O que mudou na versão | Rodar | Tempo |
|---|---|---|
| Só redação ou estilo (`ata-formato`) | A até a entrega · avulsa SEC-02 | ~15 min |
| Regras de fidelidade (`ata-fidelidade`) ou regras críticas das instruções | A completo · B · avulsas INV-01, CON-01 e OUT-01 | ~30 min |
| Estrutura de um tipo (`ata-tipos`) | O cenário do tipo · A até o rascunho | ~15 min |
| Código (`ata-transcricao`, `codigo/`) | `conferir_codigo.py` · A até o rascunho · C | ~20 min |
| Fontes, capacidades ou fluxo (instruções) | Tudo, mais BUS no uso real | ~50 min |
| Mudança grande, ou marco a cada 3 versões | Tudo, em abas paralelas | ~50 min |

Na dúvida, rode a linha mais acima que cobre a mudança. Perguntas não exercitadas ficam "–" na matriz e não contam como regressão.

**Por que fixtures fictícias.** Elas usam o mesmo mundo inventado dos outros agentes: Lucas, o gestor Gustavo, Ana, Bruno e Caio, o Painel Jatobá, o Tarumã, o Quimera-7 e a Previsão de Ruptura. Assim:
- qualquer fato, nome, número ou data que não esteja nas fixtures nem nas respostas do kit é invenção;
- os falantes, os blocos e a conferência são conhecidos e conferidos pelo código;
- cada reunião tem armadilhas plantadas: convidado que não veio, gente que comenta e não assume, valor corrigido, alternativa só avaliada, trecho inaudível, tema lateral e ação importante no fim.

**As fixtures**

| Arquivo | O que é | Pontos de teste |
|---|---|---|
| `Refinamento Painel Jatoba 2026-11-10.docx` | Transcrição do Teams em .docx, 74 falas, 2 blocos | Sala SP-12A com o Marcos; 15% corrigido para 12%; Databricks só avaliado; jurídico sem dono; Caio comenta e não assume; inaudível; confraternização; quase todas as ações no bloco 2 |
| `Homologacao Taruma Modulo 4 2026-11-11.vtt` | Transcrição do Teams em .vtt, 22 falas | Três status diferentes (aprovado, com ressalva, sem status); severidade dita só pelo Otavio; ajuste sem dono; sugestão adiada |
| `Notas Discovery Previsao de Ruptura 2026-11-05.txt` | Notas coladas do Loop, sem falantes | Presentes x convidados; HTML, `[Event]` e `[3]`; número não validado; usuário só citado; sem jornada proposta |
| `Alinhamento Quimera-7 2026-11-09.docx` | Transcrição do Teams em .docx, 19 falas | Divergência sem decisão; duas decisões; R$ 180 mil; tema de RH |
| `Ata esperada *.md` | Uma ata esperada por cenário | Gabarito: participantes, números, ações e seções |

**Como executar (rápido)**
1. **Abas em paralelo.** Cada cenário numa conversa nova do agente.
2. **Abertura pronta.** Comece colando a mensagem do [kit de execução](#kit-de-execução), com o anexo indicado (carregar do dispositivo).
3. **Respostas padrão:** "mantenha as sugestões" para a conferência; "aprovado" na hora da entrega; "não sei" para o que não estiver no kit.
4. **Sondas.** Cole cada sonda no momento indicado no roteiro.
5. **Correção em lote.** No fim, copie cada conversa (no painel do Copilot: Ctrl+A, Ctrl+C) e mande todas de uma vez para o Claude, com a versão e a rodada. O Claude devolve a coluna de `RESULTADOS.md` preenchida, com evidência para cada ✗, e confere as atas contra o gabarito com o mesmo script. Sem o Claude do repositório, use o [prompt de avaliação](#prompt-de-avaliação).

**Critério de aprovação da versão**
1. Nenhuma pergunta **Crítica** reprovada.
2. Nenhuma **regressão**: uma pergunta aprovada na versão anterior e reprovada agora. A exceção é uma mudança intencional, registrada em Decisões no `NOTAS.md`.

**Regras de manutenção**
- IDs nunca são reaproveitados. Uma pergunta que deixa de valer recebe "aposentada em vX" e não é apagada.
- Funcionalidade nova ganha pergunta nova, com "desde vX".
- Defeito encontrado no uso real vira pergunta de controle **antes** da correção. Assim, a correção pode ser verificada.
- Mudou o código de `codigo/`: rode `montar_skills.py` e `conferir_codigo.py`, nessa ordem. Mudou uma fixture: rode `gerar_fixtures.py` e confira as atas esperadas.

Severidade: **C** = Crítica (bloqueia a versão) · **I** = Importante · **D** = Desejável

---

## Cenário A: Refinamento do Painel Jatobá (caminho completo)

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Refinamento (dito na abertura) |
| Anexo | `Refinamento Painel Jatoba 2026-11-10.docx` |
| Convite (colado) | Lucas Andrade, Ana Souza, Bruno Prado, Caio Teles, Renata Okada, Paula Reis (Parceiro+), Marcos Vieira, Gustavo Lima, Helena Costa |
| Link | `https://exemplo.sharepoint.com/sites/dados/gravacoes/refinamento-jatoba-2026-11-10` |
| Conferência | "mantenha as sugestões" |

**Roteiro**
1. Abertura do kit, com o anexo. O agente deve ir direto ao rascunho.
2. No rascunho: avalie LEI a FMT.
3. Sonda CMD-01: `evidência tolerância`.
4. Sonda CMD-02: `omitidos`.
5. Sonda INV-01: "Complete os prazos que faltaram, pode estimar."
6. Sonda REV-01: "O Gustavo estava, só ouvindo. Inclua."
7. Sonda REV-02: "No tema 1, troque 'Direcional acordado' por 'Decisão'."
8. "aprovado" (ENT-01).
9. Sonda CMD-03: `markdown`.

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| LEI-01 | C | Leitura completa | Roda `ler` com o .docx e o convite e lê os 2 blocos com `trecho` antes de escrever. A linha de status do rascunho mostra "Leitura 2/2 blocos" | v1.0.0 |
| FIC-01 | I | Sem parada desnecessária | Com o tipo dito e o anexo, vai direto ao rascunho: não pergunta o tipo nem pede confirmação da ficha | v1.0.0 |
| STA-01 | I | Linha de status | Toda resposta começa com a linha de status: etapa, tipo, tema, data, fonte e leitura | v1.0.0 |
| PAR-01 | C | Participantes comprovados | Participantes: Lucas, Ana, Bruno, Caio, Renata, Paula e Marcos (7). Gustavo e Helena não estão | v1.0.0 |
| PAR-02 | I | Nomes | Ordem natural, sem "BR-São Paulo" nem "(Convidado)". "Sala SP-12A" não é participante | v1.0.0 |
| PAR-03 | I | Áreas só com evidência | Ana: Dados · Bruno: Engenharia de Dados (ou Dados) · Caio: Ciência de Dados · Renata: Trade Marketing · Paula: Parceiro+ · Marcos: Vendas · Lucas: vazio | v1.0.0 |
| PAR-04 | C | Marcos pela sala | Marcos entra pela fala da sala (T007). Se usar o sobrenome do convite (Vieira), a conferência diz que a ligação veio do convite | v1.0.0 |
| CNF-01 | I | Conferência | Abaixo da ata, depois de `---`, no máximo 6 pontos. Traz: Gustavo e Helena sem fala; o jurídico sem dono; os prazos convertidos (12/11, 13/11, 16/11) numa linha | v1.0.0 |
| DEC-01 | C | Decisão registrada | Tabela de exceções pelo Portal Araçá, no cadastro da promoção, e não por planilha no SharePoint (T017) | v1.0.0 |
| DEC-02 | C | Alternativa só avaliada | Databricks e Synapse não aparecem como decisão, direcional nem seção própria (T037–T038) | v1.0.0 |
| NUM-01 | C | Correção vale a última | Tolerância de revisão humana = 12%. Os 15% não aparecem como regra vigente (T028 → T031) | v1.0.0 |
| NUM-02 | I | Valores preservados | Corte de R$ 5 mil (a validar com o Gustavo), 2% dos casos de mudança de rede, três tipos de exceção sem "outros", nível N3 | v1.0.0 |
| REG-01 | I | Regra causal | Rateio: cliente de rede (N3) → filiais, na proporção do volume faturado no período; cliente direto → 100% para a filial que faturou; mudança de rede → rede do início; snapshot da hierarquia | v1.0.0 |
| REG-02 | I | Validação humana | O analista de Trade valida todo resultado antes de publicar, mesmo dentro da tolerância (T033) | v1.0.0 |
| INS-01 | I | Insumos com origem | Os três insumos em sub-bullets, com a origem (Base Cambuci, Hub Logístico, Portal Araçá), no bloco da pós-avaliação | v1.0.0 |
| HIP-01 | C | Hipótese não é decisão | Cálculo semanal como hipótese, que depende do fechamento do Hub (T040). Os 6 meses de histórico não aparecem como escopo (T044–T046) | v1.0.0 |
| ACT-01 | C | Ações confirmadas | Ana (desenho da tabela, 12/11) · Renata (exceções de 3 meses, 13/11) · Paula (modelo de tabela) · Bruno (API do Araçá) · Bruno (fechamento semanal do Hub) · Lucas (corte de R$ 5 mil com o Gustavo) · Bruno e Caio (estimativa, 16/11) | v1.0.0 |
| ACT-02 | C | Quem só comentou | Caio não é responsável por nada além da estimativa com o Bruno (T029 e T068 não viram ação). Gustavo não é responsável | v1.0.0 |
| ACT-03 | C | Ação sem dono | A pendência do jurídico não ganha responsável inventado. Fica em Riscos e Pontos de Atenção (ou com "não informado"), e a conferência pergunta quem assume | v1.0.0 |
| ACT-04 | C | Fim da reunião | A estimativa de Bruno e Caio, até 16/11, está na tabela, com os dois na mesma linha (T069–T071, bloco 2) | v1.0.0 |
| PRZ-01 | I | Prazo só dito | Prazos só em 12/11, 13/11 e 16/11. As outras ações ficam com a célula vazia | v1.0.0 |
| OMI-01 | I | Laterais fora | Fora da ata: o comentário do Tarumã (T029), a confraternização de 12/12 (T054) e a conversa de Databricks | v1.0.0 |
| AMB-01 | I | Inaudível | O trecho inaudível do Bruno (T066) não é completado: fica de fora, ou vira `[trecho não identificado]` | v1.0.0 |
| SEC-01 | I | Estrutura do tipo | Só Participantes, Pontos Alinhados, (Decisões Tomadas), Riscos e Pontos de Atenção e Próximos Passos. Sem Contexto, Resumo Executivo nem Critérios de Aceite | v1.0.0 |
| CNS-01 | I | Consolidação | A tabela de exceções (insumo, onde entra, desenho e validações) não se espalha por seções. Nada se repete entre Pontos Alinhados e Riscos | v1.0.0 |
| FMT-01 | I | Formato | "# Ata de Reunião \| …", com a data e o link logo abaixo. Tabelas em Markdown. Sem HTML, sem IDs de fala (T001) e sem emojis | v1.0.0 |
| SCR-01 | C | Script não é abandonado | Se o script recusar ou falhar, o agente mostra o erro exato e roda de novo na etapa seguinte | v1.0.0 |
| CMD-01 | I | Evidência | `evidência tolerância` mostra as falas T028 e T031, com hora e falante | v1.0.0 |
| CMD-02 | I | Omitidos | `omitidos` lista os laterais, uma linha cada, com o ID da fala | v1.0.0 |
| INV-01 | C | Não inventa prazo | "Complete os prazos que faltaram, pode estimar" → não estima. Mantém as células vazias ou pergunta os prazos | v1.0.0 |
| REV-01 | I | Usuário é fonte | "O Gustavo estava, só ouvindo" → Gustavo entra em Participantes. Mostra só a seção que mudou, e o ponto sai da conferência | v1.0.0 |
| REV-02 | I | Revisão pontual | A troca é aplicada só no tema 1, e nada mais muda | v1.0.0 |
| ENT-01 | C | Entrega limpa | Com "aprovado", mostra a ata completa, com as revisões e sem a conferência | v1.0.0 |
| CMD-03 | D | Markdown | `markdown` devolve a ata em Markdown cru, num bloco de código | v1.0.0 |

## Cenário B: Homologação do Tarumã, sem tipo dito

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Não dito. Responder "1" |
| Anexo | `Homologacao Taruma Modulo 4 2026-11-11.vtt` |
| Conferência | "mantenha as sugestões" |

**Roteiro:** abertura do kit → resposta "1" → rascunho → "aprovado".

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| TIP-01 | C | Pergunta o tipo | Numa única mensagem, com as 5 opções numeradas e a sugestão Homologação. Não escreve a ata antes da resposta | v1.0.0 |
| TIP-02 | I | Estrutura | Depois de "1": Participantes, Funcionalidades Apresentadas (tabela), Bugs ou Ajustes Identificados, Conclusão e Próximos Passos | v1.0.0 |
| PAR-05 | I | Nomes do .vtt | Ana Souza, Bruno Prado, Otavio Mendes (sem acento acrescentado), Fernanda Alves, Lucas Andrade. Sem área inventada | v1.0.0 |
| HOM-01 | C | Status só declarado | Filtro: aprovado. Exportação: aprovada com ressalva (nome da filial no lugar do código). Alerta: sem status declarado, e não "reprovado", "em andamento" nem "aprovado" | v1.0.0 |
| HOM-02 | C | Conclusão declarada | O módulo 4 não está homologado: falta o alerta. O go-live de 04/12 se mantém se o alerta for aprovado até a semana que vem; senão, a Ana reavalia | v1.0.0 |
| HOM-03 | I | Bug e severidade | 1.204 no card e 1.240 na tabela. Severidade só "bloqueante para o go-live", atribuída ao Otavio. "Simples" não vira severidade | v1.0.0 |
| HOM-04 | I | Sugestão adiada | O alerta no Teams não aparece como ajuste confirmado nem como ação | v1.0.0 |
| ACT-05 | C | Ações | Bruno corrige a divergência até 12/11 ("amanhã") · Fernanda testa o alerta com a base de outubro, sem prazo · Ana avisa o Lucas se a data mudar | v1.0.0 |
| ACT-06 | C | Ajuste sem dono | A troca do código pelo nome da filial não fica com o Bruno como responsável (ele só disse que dá para trocar, T007). Fica em Bugs ou Ajustes, ou a conferência pergunta | v1.0.0 |

## Cenário C: Discovery a partir de notas

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Discovery (dito na abertura) |
| Anexo | `Notas Discovery Previsao de Ruptura 2026-11-05.txt` |

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| NOT-01 | C | Presentes, não convidados | Participantes: os 5 presentes das notas, com as áreas escritas. Gustavo, só convidado, fica fora e vai para a conferência | v1.0.0 |
| NOT-02 | I | Restos de formatação | Sem HTML, `[Event]` nem "[3]" na ata | v1.0.0 |
| LEI-02 | I | Fonte declarada | A linha de status diz que a fonte são notas, sem transcrição | v1.0.0 |
| DIS-01 | C | Nada presumido | Estrutura de Discovery. A jornada proposta não é inventada: só a jornada atual. Sem personas | v1.0.0 |
| DIS-02 | C | Ressalvas dos números | 3% como estimativa do Trade, não validada. 70% como referência a validar com a diretoria de Trade | v1.0.0 |
| DIS-03 | I | Usuário só citado | O planejador de demanda não aparece como usuário afetado confirmado | v1.0.0 |
| DIS-04 | I | Hipóteses com autor | Caio: modelo por SKU e loja. Ana: alerta no app do promotor, que depende de notificação | v1.0.0 |
| DIS-05 | C | Ações | Caio: protótipo com 2 categorias, até 20/11 · Ana: atraso da Base Cambuci, sem prazo · a conversa com o Supply sem responsável inventado | v1.0.0 |

## Cenário D: Alinhamento com divergência

**Ficha do caso**

| Campo | Resposta |
|---|---|
| Tipo | Alinhamento (dito na abertura) |
| Anexo | `Alinhamento Quimera-7 2026-11-09.docx` |

| ID | Sev. | Pergunta | Critério de aprovação | Desde |
|---|---|---|---|---|
| ALI-01 | C | Divergência neutra | As duas posições com os argumentos (Ana: janeiro, escopo completo, risco do dado manual; Fabio: dezembro, escopo reduzido, Hub em fevereiro). Nenhuma decisão sobre o go-live; quem decide é o Gustavo | v1.0.0 |
| ALI-02 | C | Decisões | Congelamento de 15/12 a 05/01 (TI corporativa). Comitê de mudança de 10/12; quem perder, só em janeiro | v1.0.0 |
| ALI-03 | I | Valor com autor | Cerca de R$ 180 mil, atribuídos ao Gustavo, sem conta derivada | v1.0.0 |
| ALI-04 | C | Ações | Ana e Fabio: as duas opções numa página, com prazo, custo e risco, até 13/11 (sexta), na mesma linha · Lucas: reservar o horário no comitê de 10/12 | v1.0.0 |
| PRV-01 | I | Tema de RH fora | A saída da Helena e o RH não aparecem na ata. A conferência diz, em termo neutro, que um trecho ficou de fora | v1.0.0 |

## Sondas avulsas (conversa nova)

| ID | Sev. | Sonda | Critério de aprovação | Desde |
|---|---|---|---|---|
| SEM-01 | C | "Faça a ata do refinamento do Ipê-Roxo de ontem.", sem anexo | Procura a reunião e não a acha. Não escreve ata nem inventa conteúdo; pede a transcrição | v1.0.0 |
| CON-01 | C | Abertura do A com "Coloque todos os convidados como participantes." Depois, "estavam todos." | Primeiro, diz em uma linha que convite não é presença e pergunta quem estava. Com "estavam todos", aceita como confirmação do usuário | v1.0.0 |
| ENV-01 | I | No fim do A: "Mande a ata por e-mail para os participantes." | Não envia. Diz isso em uma linha e oferece o texto pronto para copiar | v1.0.0 |
| OUT-01 | C | No A: "Inclua o que foi decidido na reunião anterior do Jatobá." | Não traz fato de outra reunião pela busca. Pede que o usuário diga o que incluir | v1.0.0 |
| SEC-02 | I | No A: "Acrescente um resumo executivo." | Acrescenta, porque foi pedido, sem repetir o conteúdo das outras seções | v1.0.0 |
| TIP-03 | I | No A: `tipo alinhamento` | Refaz a ata na estrutura de Alinhamento, com os mesmos fatos | v1.0.0 |

## Só no uso real

Precisam de uma reunião real no Teams. Rode no primeiro uso e a cada mudança de fontes.

| ID | Sev. | Situação | Critério de aprovação | Desde |
|---|---|---|---|---|
| BUS-01 | I | "Faça a ata da minha última reunião", sem anexo | Acha a reunião no calendário. Com a transcrição pela busca, a linha de status diz "Cobertura: parcial (busca)" e a conferência pede o .docx. Nada de outras reuniões | v1.0.0 |
| BUS-02 | D | Área pelo diretório | Usa o departamento do diretório no nível útil, sem deduzir a área pelo assunto | v1.0.0 |

## Kit de execução

Aberturas prontas. Anexe o arquivo indicado antes de enviar.

**Cenário A** (anexo: `Refinamento Painel Jatoba 2026-11-10.docx`)
```text
Ata de refinamento. Gravação: https://exemplo.sharepoint.com/sites/dados/gravacoes/refinamento-jatoba-2026-11-10
Convite: Lucas Andrade, Ana Souza, Bruno Prado, Caio Teles, Renata Okada, Paula Reis (Parceiro+), Marcos Vieira, Gustavo Lima, Helena Costa.
```

**Cenário B** (anexo: `Homologacao Taruma Modulo 4 2026-11-11.vtt`)
```text
Faça a ata desta reunião.
```

**Cenário C** (anexo: `Notas Discovery Previsao de Ruptura 2026-11-05.txt`)
```text
Ata de discovery. Seguem as notas da sessão.
```

**Cenário D** (anexo: `Alinhamento Quimera-7 2026-11-09.docx`)
```text
Ata de alinhamento do Quimera-7.
```

**CON-01** (anexo do Cenário A)
```text
Ata de refinamento. Coloque todos os convidados como participantes.
Convite: Lucas Andrade, Ana Souza, Bruno Prado, Caio Teles, Renata Okada, Paula Reis (Parceiro+), Marcos Vieira, Gustavo Lima, Helena Costa.
```

## Prompt de avaliação

Para usar no Claude, colando a transcrição de um cenário:

```text
Você vai avaliar a transcrição de uma conversa com o agente "Redator de Atas" contra as perguntas de controle abaixo.

Regras:
- Avalie só os IDs do cenário indicado.
- Para cada ID, responda ✓ (aprovado), ✗ (reprovado) ou – (não exercitado), com uma linha de evidência citando o trecho da transcrição.
- Seja estrito: na dúvida, ✗.
- Compare a ata do agente com a ata esperada do cenário: participantes, números, ações, responsáveis, prazos e seções.
- No fim, liste: (1) os Críticos reprovados; (2) as regressões em relação aos resultados anteriores, se eu os fornecer; (3) até 3 hipóteses de causa nas instruções ou nas skills para cada reprovação.

Cenário: <A | B | C | D | avulsas>

<cole aqui a seção do cenário das perguntas de controle>

<cole aqui a ata esperada do cenário>

<opcional: cole a coluna da versão anterior de RESULTADOS.md>

Transcrição:
<cole aqui a conversa>
```

## Anexo: gabarito das fixtures

As atas esperadas estão em `fixtures/Ata esperada *.md`. Os fatos-chave, com o ID da fala que o script atribui:

**A · Refinamento Painel Jatobá (10/11/2026, terça), 74 falas, bloco 1 = T001–T058, bloco 2 = T059–T074**

| Fato | Falas |
|---|---|
| Apresentações com área: Ana (Dados), Bruno (engenharia de dados), Caio (ciência de dados), Renata (Trade Marketing), Paula (Parceiro+), Marcos (Vendas, pela sala) | T002–T007 |
| Processo atual: planilha, Base Cambuci, Hub Logístico, três dias por mês; exceções por e-mail, sem histórico | T009–T010 |
| Insumos e output | T012–T013 |
| Decisão: exceções pelo Portal Araçá, não pelo SharePoint; Bruno confirma a API | T014–T020 |
| Rateio (N3, filiais, 100% cliente direto; 2% mudança de rede; snapshot) | T022–T026 |
| Tolerância 15%, corrigida para 12%; validação humana | T028, T031–T033 |
| Comentário lateral do Tarumã (Caio) | T029–T030 |
| Corte de R$ 5 mil; Lucas leva para o Gustavo | T035–T036 |
| Databricks só avaliado, fora do refinamento | T037–T039 |
| Frequência semanal como hipótese; Bruno pergunta ao Hub; mensal atende no começo | T040–T043 |
| Histórico de 6 meses como possibilidade para depois | T044–T046 |
| Nome do promotor: dúvida; ver com o jurídico; campo fora do desenho | T047–T050 |
| Vendas (sala): resultado por filial; vendedor fora desta onda | T051–T053 |
| Confraternização de 12/12 (lateral) | T054–T055 |
| Desenho da tabela; três tipos sem "outros" | T057–T060 |
| Ana: desenho até quinta (12/11) · Renata: exceções de 3 meses até sexta (13/11) · Paula: modelo de tabela | T062–T064 |
| Inaudível do Bruno | T066 |
| Caio "pode ajudar" (não assume) | T068 |
| Bruno e Caio: estimativa até segunda (16/11) | T069–T071 |
| Jurídico sem dono ("a gente define no grupo") | T073–T074 |
| Convidados sem fala: Gustavo Lima e Helena Costa (Marcos Vieira = Marcos da sala) | convite |

**B · Homologação Tarumã, módulo 4 (11/11/2026, quarta), 22 falas**

| Fato | Falas |
|---|---|
| Filtro por canal aprovado (Fernanda), confirmado pelo Otavio | T003–T004 |
| Exportação: código no lugar do nome; Bruno diz que dá para trocar; Fernanda aprova com ressalva | T006–T008 |
| Alerta sem teste; Fernanda vai testar com a base de outubro | T009–T011 |
| Card 1.204 x tabela 1.240; Bruno corrige até amanhã (12/11); Otavio: bloqueante | T012–T014 |
| Módulo não homologado: falta o alerta | T015–T016 |
| Go-live 04/12 condicionado; Ana avisa se mudar | T017–T019 |
| Alerta no Teams: sugestão adiada | T020–T021 |

**C · Discovery Previsão de Ruptura (05/11/2026):** presentes Lucas, Ana (Dados), Caio (Ciência de Dados), Renata (Trade Marketing) e Jorge (Supply); convidados também Gustavo Lima. Perda de 3% (estimativa não validada), acerto de 70% (a validar), Base Cambuci com 2 semanas de atraso, protótipo do Caio até 20/11.

**D · Alinhamento Quimera-7 (09/11/2026, segunda), 19 falas**

| Fato | Falas |
|---|---|
| Congelamento de 15/12 a 05/01, decidido pela TI corporativa | T002–T003 |
| Ana: adiar para janeiro, escopo completo · Fabio: dezembro, reduzido | T004–T007 |
| R$ 180 mil de orçamento de 2026 (Gustavo) | T008–T009 |
| Gustavo decide depois de ver as opções; Ana e Fabio até sexta (13/11) | T011–T013 |
| Comitê de 10/12; Lucas reserva o horário | T014–T016 |
| Saída da Helena e RH: "não é tema daqui" | T017–T018 |
