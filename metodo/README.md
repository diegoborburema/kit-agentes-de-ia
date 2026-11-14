# O método: agente tratado como produto

Um agente de IA muda o tempo todo: uma frase nas instruções, uma regra nova na skill. Sem método, ninguém sabe o que mudou, por que mudou, nem se a mudança quebrou algo que funcionava. Aqui cada agente é tratado como um produto: **tem versão, tem o porquê de cada decisão e tem uma bateria de testes que roda antes de cada versão nova.**

Esta parte é para quem quer criar ou manter os próprios agentes. Para só usar um agente, você não precisa dela.

## As três camadas de cada agente

| Camada | O que é | Quem escreve |
|---|---|---|
| `pacote/` | O agente exatamente como o Copilot exporta (o conteúdo do .zip, com o JSON indentado) | O export. Não se edita à mão |
| `agente.md` | Instruções e configurações em texto legível | Gerado a partir do pacote |
| `NOTAS.md` | Objetivo e decisões: o que o pacote não guarda | Você, à mão |

Por que o `agente.md`? No JSON, as instruções ficam numa linha só, com `\n` e acentos escapados. No `agente.md` elas aparecem quebradas em linhas, e a comparação entre versões mostra exatamente qual frase mudou.

Ao lado das três camadas, `testes/` guarda as perguntas de controle e a matriz de resultados por versão.

## Perguntas de controle

Cada agente tem uma bateria de regressão:

- **`PERGUNTAS-DE-CONTROLE.md`**: cenários com um caso fixo, um roteiro e um critério de aprovação sim/não para cada pergunta. Cada pergunta tem severidade: **Crítica** (bloqueia a versão), **Importante** ou **Desejável**.
- **`fixtures/`**: os arquivos usados nos cenários (decks, transcrições, prompts de exemplo), todos fictícios.
- **`RESULTADOS.md`**: uma coluna por versão, para ver regressões de relance.

Regras:
- Uma versão só vale com **nenhuma Crítica reprovada** e **nenhuma regressão** sem justificativa nas Decisões.
- **O que rodar depende do que mudou.** Cada bateria tem uma matriz "o que mudou → cenários a rodar": mudança de redação roda o cenário curto; mudança grande roda tudo.
- **Defeito do uso real vira pergunta antes da correção.** Assim dá para provar que a correção funcionou.
- IDs nunca são reaproveitados. Pergunta que deixa de valer vira "aposentada em vX".

Para rodar rápido: cada cenário numa conversa nova, várias em abas paralelas, com uma abertura pronta que já traz o caso. No fim, copie as conversas e peça a um assistente (o Claude, por exemplo) para preencher a coluna da versão em `RESULTADOS.md`.

Exemplo completo: [`produto/coach-apresentacao/testes/`](../produto/coach-apresentacao/testes/).

Modelos para começar: [`modelos/NOTAS.md`](modelos/NOTAS.md) e [`modelos/PERGUNTAS-DE-CONTROLE.md`](modelos/PERGUNTAS-DE-CONTROLE.md).

## Uma versão nova, passo a passo

1. No Copilot: edite o agente e exporte o pacote .zip.
2. Na pasta do repositório:
   ```
   python ferramentas/importar.py "caminho/para/Agente.zip"
   ```
   Agente novo: acrescente `--tema produto` ou `--tema gestao`. O script cria a pasta e o `NOTAS.md` a partir do modelo.
3. Revise a diferença entre as versões, principalmente no `agente.md`.
4. Rode as perguntas de controle conforme a matriz, preencha a coluna da versão em `RESULTADOS.md` e registre o motivo em **Decisões**, no `NOTAS.md`.
5. Faça um commit por versão, com o motivo na mensagem. Exemplo:
   `coach-apresentacao: v1.0.7: exige fonte rastreável em todo slide`

## Quando a mudança é escrita fora do Copilot

Quando a versão nova nasce numa conversa com o Claude, por exemplo:

1. Crie um branch `proposta/<agente>-v<versão>`. Só nele os arquivos de `pacote/` são editados à mão.
2. Abra um pull request para revisar a diferença.
3. Aplique no Copilot: instruções, skills, descrição e prompts iniciais.
4. Rode as perguntas de controle e registre o resultado.
5. Exporte o pacote e importe **no mesmo branch**. A diferença contra a proposta deve sair vazia, salvo metadados como a versão. Qualquer outra diferença indica algo colado errado.
6. Faça o merge se nenhuma pergunta Crítica foi reprovada e não houve regressão.

## Limites do Agent Builder

O Agent Builder aceita até **8.000 caracteres nas instruções** e até **20.000 por `SKILL.md`**, com até 8 skills por agente. Código longo não cabe no texto da skill: ele vai para `scripts/` dentro da skill, e o agente roda o script sem copiá-lo. Confira sempre:

```
python ferramentas/conferir_limites.py
```

Quando o código de uma skill vem de vários módulos (como no Redator de Atas), ele fica separado em `<agente>/codigo/` e é montado no script da skill:

```
python ferramentas/montar_skills.py             # monta os scripts das skills
python ferramentas/montar_skills.py --conferir  # só confere, por exemplo depois de importar um export
```

Não edite o script dentro da skill: edite `codigo/` e rode o montador.

## Regras do repositório

- Nada de dado real ou confidencial: nem nas instruções, nem nos exemplos, nem nos testes. Documentos usados como fonte de conhecimento não entram aqui.
- Não edite `pacote/` nem `agente.md` à mão: os dois são sobrescritos na próxima importação.
- Um commit por versão, com o motivo na mensagem. "update" não conta.

## Voltar a uma versão anterior

No GitHub: abra o `agente.md` do agente → **History** → o commit da versão desejada → copie as instruções de volta no Copilot.
