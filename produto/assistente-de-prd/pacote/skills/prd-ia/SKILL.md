---
name: prd-ia
description: 'Requisitos de IA do PRD (Anexo E), para modelo preditivo, IA generativa e agente: quando o anexo se aplica, cada campo com o "bom quando" por tipo de IA, o limiar e o conjunto de avaliação antes do build, a revisão humana nas decisões de risco, os limites e o que fazer quando a IA falha, o monitoramento e o custo por uso. Use quando a solução tiver IA (03.1, 03.5 ou 04.4) e no refinamento de ciência de dados.'
---

## Quando se aplica

O Anexo E se aplica quando a solução tem **modelo preditivo** (previsão, classificação, recomendação), **IA generativa** (texto, resumo, resposta a perguntas, extração) ou **agente** (IA que executa passos ou usa ferramentas). Sinais: "Tipo de produto" = Modelo ou Agente na 03.1; "sim" na pergunta de IA da 03.5; "Há IA na solução?" = Sim na 04.4. Uma regra fixa ("estoque abaixo de 2 dias") não é IA: é regra de negócio (02.3), e o Anexo E fica N/A.

Quem preenche: o especialista de ciência de dados, ou o PM quando não houver um, marcando "validar com ciência de dados". O sponsor valida a métrica de negócio, o limiar e a revisão humana.

## Campos (rótulos do Anexo E, em `campos` com a chave `"E"`)

| Campo | Bom quando |
|---|---|
| Tipo de IA [Modelo preditivo · IA generativa · Agente · Regras] | Marcado; pode ser mais de um |
| Tarefa ou decisão apoiada | A decisão é a da 03.1, e fica claro o que a IA faz e o que a pessoa faz |
| Entradas e saídas, com exemplos | Um exemplo real (ou fictício, marcado) de entrada e da saída esperada |
| Métrica técnica | Uma métrica que mede a IA (recall e precisão, erro médio, % de respostas corretas com citação) |
| Métrica de negócio | A mesma do benefício (03.3) ou uma que leva a ela |
| Limiar para ir à produção | Um número, com a métrica e o conjunto em que é medido, **definido antes do build** e com dono |
| Comparação com o jeito atual | A base contra a qual a IA precisa ser melhor (regra atual, média, decisão humana, central de atendimento) |
| Conjunto de avaliação e quem valida | Como é montado (período, tamanho, casos difíceis), quem dá a resposta certa e quem valida o resultado |
| Revisão humana | O que a IA não decide sozinha; quem revisa, quando e com que poder de veto |
| Limites e o que fazer quando falha | O que fica de fora (dados, casos, perguntas), o que acontece quando a IA não sabe ou erra, e para onde a pessoa é encaminhada |
| Transparência para o usuário | O que o usuário vê sobre a origem e o porquê da resposta (fonte citada, motivo do alerta, aviso de IA) |
| Vieses e equidade | Que grupos ou casos conferir (lojas novas, clientes com pouco histórico, linguagem), e como |
| Monitoramento e gatilho de revisão | O que é medido em produção, com que frequência, e o número que dispara revisão ou retreino |
| Custo por uso | Inferência, tokens ou chamadas por mês, com fonte; vai para "Uso de IA" na 04.5. Sem fonte, linha a confirmar, sem valor |

## Por tipo de IA

**Modelo preditivo**
- Limiar: métrica técnica num conjunto fora do treino (backtest de um período, base separada), contra a base de comparação. Ex.: "recall de 80% com precisão de 60% num backtest de 6 meses, contra a regra atual".
- Revisão humana: normalmente a pessoa decide e o modelo ordena ou sugere. Diga isso.
- Monitoramento: a mesma métrica em produção, com frequência; drift dos dados de entrada.

**IA generativa** (respostas, resumos, extrações)
- Conjunto de avaliação: perguntas ou documentos reais, com a resposta certa dada por quem conhece o assunto (ex.: 50 perguntas reais com a resposta validada pela central). O agente pode sugerir **como** montar o conjunto; o tamanho e o limiar vêm do usuário.
- Métrica: % de respostas corretas e completas; % com a fonte citada certa; % de "não sei" quando a resposta não está na base.
- Limites: o que a IA não responde (fora da base, opinião, dado pessoal de outra pessoa) e o que diz nesses casos.
- Transparência: a resposta cita a fonte (documento, página).

**Agente** (executa passos ou usa ferramentas)
- Tudo da IA generativa, mais: a lista das ações que ele pode fazer sozinho e das que precisam de aprovação humana.
- Toda ação com efeito para outras pessoas (aprovar, mudar escala, enviar mensagem, mexer em dado) é **revisão humana**, a menos que o sponsor decida o contrário por escrito. Registre como requisito (02.1) e como limite.
- Registro: o que o agente fez, quando e por pedido de quem.

## Regras

- **Sem limiar, não há build.** Se o usuário disser que "ajusta depois do go-live", explique em uma linha que o limiar e o conjunto de avaliação vêm antes de construir, porque são o critério de aceite da IA (05.2) e do go/no-go (05.4). Pergunte a métrica, o limiar e o dono. Não invente o limiar nem proponha um número.
- **O número da fonte não muda.** Pedido para trocar o limiar "porque fica mais bonito" é recusado; o limiar muda só com uma fonte nova ou a decisão registrada do especialista e do sponsor.
- **Revisão humana não é opcional em decisão de risco**: decisão sobre pessoas, dinheiro, saúde, segurança ou direitos.
- O critério "Qualidade da IA atendida" do go/no-go (05.4) é o limiar deste anexo. O caso de homologação da IA (05.2) mede a métrica técnica no conjunto de avaliação.
- O benefício esperado (03.3) depende do limiar: se o limiar mudar, avise que a premissa do benefício pode mudar.

## Consistência

1. A decisão apoiada é a da 03.1, e o canvas de Ciência de dados cita os mesmos limiar e base de comparação.
2. Os dados de entrada existem na 02.5 e no Anexo C, com o histórico que o conjunto de avaliação precisa.
3. Dados pessoais na entrada ou na saída estão no canvas de Segurança; serviço externo de IA está em "Terceiros".
4. O custo por uso está na 04.5 ("Uso de IA").
5. A revisão humana aparece como requisito na 02.1 ou como limite aqui, e a explicabilidade bate com a 02.4.
