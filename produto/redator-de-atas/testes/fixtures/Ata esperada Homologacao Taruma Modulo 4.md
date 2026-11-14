# Ata de Reunião | Homologação Tarumã – Módulo 4

11/11/2026

## Participantes

- Lucas Andrade
- Ana Souza
- Fernanda Alves
- Otavio Mendes
- Bruno Prado

## Funcionalidades Apresentadas

| Funcionalidade | Status | Observação |
|---|---|---|
| Filtro por canal (atacado, varejo e e-commerce, combinado com o filtro de filial) | Aprovado | Testado pela Fernanda com a carteira dela |
| Exportação para Excel (tabela com os filtros aplicados) | Aprovado com ressalva | O arquivo deve trazer o nome da filial em vez do código |
| Alerta de ruptura por e-mail (estoque projetado do SKU na loja abaixo de 3 dias de cobertura dispara e-mail ao vendedor) | Sem status declarado | Ainda não testado: a base de teste não tinha ruptura |

## Bugs ou Ajustes Identificados

- **Total de lojas divergente:** o card de total mostra 1.204 lojas e a tabela, 1.240. Causa apontada: contagem de loja inativa. Para o Otavio, é bloqueante para o go-live, porque a diretoria olha o card.
- **Exportação:** trocar o código da filial pelo nome no arquivo exportado.

## Conclusão

- O módulo 4 ainda não está homologado: falta validar o alerta de ruptura.
- O go-live de 04/12 se mantém se o alerta for aprovado até a semana que vem; caso contrário, a Ana reavalia a data.

## Próximos Passos

| Ação | Responsável | Prazo |
|---|---|---|
| Corrigir a divergência do total de lojas entre o card e a tabela | Bruno Prado | 12/11 |
| Testar o alerta de ruptura com a base de outubro e dar retorno | Fernanda Alves | |
| Avisar o Lucas se a data de go-live mudar | Ana Souza | |
