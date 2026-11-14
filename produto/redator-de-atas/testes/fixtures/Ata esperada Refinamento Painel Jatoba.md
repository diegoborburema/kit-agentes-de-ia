# Ata de Reunião | Refinamento Painel Jatobá – Pós-avaliação de promoções (Onda 2)

10/11/2026 · [Gravação da reunião](https://exemplo.sharepoint.com/sites/dados/gravacoes/refinamento-jatoba-2026-11-10)

## Participantes

| Participante | Área |
|---|---|
| Lucas Andrade | |
| Ana Souza | Dados |
| Bruno Prado | Engenharia de Dados |
| Caio Teles | Ciência de Dados |
| Renata Okada | Trade Marketing |
| Paula Reis | Parceiro+ |
| Marcos | Vendas |

## Pontos Alinhados

### 1. Pós-avaliação de promoções no Painel Jatobá

**Processo atual**
- Após o fim da promoção, o analista de Trade cruza à mão, em planilha, o sell-out da Base Cambuci com o faturamento por filial do Hub Logístico. O trabalho leva cerca de três dias por mês.
- Exceções (promoção cancelada, ação conjunta com outro fornecedor, troca de preço) são tratadas caso a caso, por e-mail, sem histórico.

**Direcional acordado**
- A pós-avaliação passa a ser calculada por promoção, a partir de três insumos:
  - Sell-out semanal [Base Cambuci]
  - Faturamento por filial [Hub Logístico]
  - Exceções mantidas pelo Trade [Tabela | Portal Araçá]
- Saída: pós-avaliação por promoção, com investimento, volume incremental e retorno, publicada no painel [Output Pós-avaliação].
- A tabela de exceções entra pelo Portal Araçá, no próprio cadastro da promoção, e não por planilha no SharePoint.
- Promoções com investimento abaixo de R$ 5 mil ficam fora da pós-avaliação. O corte ainda será validado com o Gustavo.
- O resultado abre por filial; vendedor não entra nesta onda.

### 2. Regra de rateio entre filiais

- Cliente de rede (nível N3 da hierarquia de clientes): o investimento é rateado entre as filiais que atendem a rede, na proporção do volume que cada filial faturou no período da promoção.
- Cliente direto, sem rede: 100% do investimento vai para a filial que faturou.
- Cliente que muda de rede durante a promoção (cerca de 2% dos casos): vale a rede do início da promoção.
- Como a hierarquia do Hub Logístico é a do mês corrente, será guardado um snapshot da hierarquia na data de início de cada promoção.

### 3. Tolerância e validação humana

- Divergência acima de 12% entre sell-out e faturamento vai para revisão humana antes da publicação.
- Todo resultado, mesmo dentro da tolerância, é validado pelo analista de Trade antes de ser publicado no painel, por exigência da diretoria.

### 4. Tabela de exceções

- Uma linha por exceção: código da promoção, tipo de exceção, período afetado, valor a desconsiderar e justificativa curta.
- Tipos: cancelamento, ação conjunta e troca de preço, sem a opção "outros".
- Validações no upload: o código da promoção deve existir no Portal Araçá e o período deve estar dentro da vigência da promoção. Se a validação falhar, o upload é recusado com a indicação da linha do erro.
- O campo de nome do promotor fica fora do desenho até a resposta do jurídico.

## Riscos e Pontos de Atenção

- **Dado pessoal na tabela de exceções:** falta definir com o jurídico se a tabela pode conter o nome do promotor. O layout só fecha depois dessa resposta.
- **Frequência do cálculo:** a hipótese é rodar semanalmente, mas isso depende de o Hub Logístico ter fechamento semanal; hoje o faturamento fecha só no mês. Para o Trade, a frequência mensal atende no início.
- **Carga de outubro:** [trecho não identificado]; fica para depois do fechamento do Hub Logístico.

## Próximos Passos

| Ação | Responsável | Prazo |
|---|---|---|
| Fechar o desenho da tabela de exceções (colunas e validações) e enviar à Renata | Ana Souza | 12/11 |
| Levantar as exceções dos últimos 3 meses, para exemplo e teste do upload | Renata Okada | 13/11 |
| Enviar o modelo de tabela de exceções usado em outro cliente | Paula Reis | |
| Confirmar se o campo customizado do Portal Araçá vem na API | Bruno Prado | |
| Verificar com o time do Hub Logístico se há fechamento semanal parcial | Bruno Prado | |
| Validar com o Gustavo o corte de R$ 5 mil | Lucas Andrade | |
| Estimar o esforço do cálculo, com snapshot e rateio | Bruno Prado, Caio Teles | 16/11 |
