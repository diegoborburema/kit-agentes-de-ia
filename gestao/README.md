# Gestão: da estratégia à semana

Três agentes que trabalham em sequência para quem lidera um time:

```
Coach de Gestão          Coach de Estrutura           Organizador de 1:1
o que entregar     →     quem entrega e com que   →   acompanhamento
em 30, 60 e 90 dias      carga                        semana a semana
```

1. **[Coach de Gestão](coach-de-gestao/):** transforma os desafios e o alinhamento estratégico da área num plano de 30, 60 e 90 dias, com resultados, marcos e uma entrega por semana. Revisa toda sexta e vira o ciclo a cada 4 semanas.
2. **[Coach de Estrutura](coach-de-estrutura/):** lê o plano e ajuda a dividir as frentes entre as pessoas do time. Soma a carga de cada uma, aponta o que está em risco e propõe do ajuste mais leve ao mais pesado, com um teste de 4 semanas.
3. **[Organizador de 1:1](organizador-1-1/):** prepara a pauta de cada 1:1, com o gestor ou com um liderado, e acompanha os combinados até serem feitos.

Cada um entrega um bloco de texto para o próximo (por exemplo, os "pontos para os 1-1s"), que você cola na conversa seguinte. Eles não leem os arquivos uns dos outros sozinhos: quem conecta é você.

> **Dados de pessoas.** Estes agentes lidam com informações sobre pessoas do seu time: quem faz o quê, carga, temas de conversa. Use só num ambiente aprovado pela sua empresa (por exemplo, o Microsoft 365 Copilot corporativo), siga as regras dela e a LGPD, e não leve esses dados para uma ferramenta que a empresa não autorizou. Nenhum deles avalia pessoas: nota, ranking, promoção e qualquer decisão sobre alguém ficam com você.

## Arquivos de teste

Todo nome de pessoa, projeto, sistema, empresa e número nos testes é **fictício**: o "Núcleo de Dados", o Recomendador, o Ipê Triagem, a Base Sabiá, os valores e as pessoas (Ana, Bruno, Caio, Gustavo e o usuário Lucas).

## Código compartilhado

[`_codigo/`](_codigo/) guarda o código que os três usam: leitura e geração das pautas em .pptx (`pptx/`), o plano 30-60-90 (`plano/`), o mapa do time (`estrutura/`) e funções de texto (`pessoas/ficha.py`). O script de cada skill é montado a partir daqui por [`ferramentas/montar_skills.py`](../ferramentas/montar_skills.py). Se você só quer usar os agentes, não precisa abrir esta pasta.
