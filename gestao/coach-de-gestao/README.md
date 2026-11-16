# Coach de Gestão

Transforma os desafios e o alinhamento estratégico da sua área num **plano 30-60-90** que dá para executar e medir, e mantém o plano vivo: revisão toda sexta e virada a cada 4 semanas.

Ele é coach, não secretário: propõe rascunhos, força escolhas, cobra o critério de "feito" e aponta o trabalho que está fora do plano. Quem decide é você.

> **Dados de pessoas.** O plano cita quem é dono de cada entrega. Use num ambiente aprovado pela sua empresa e não leve esses dados para ferramentas não autorizadas. Veja o [aviso do módulo](../README.md).

## O que ele faz

1. **Lê o alinhamento** da área (um .pptx) e as pautas anotadas mais recentes. No Copilot, também busca no seu e-mail, no Teams, nas reuniões e nos arquivos, sempre com a fonte em cada linha.
2. **Monta o plano:**
   - até 3 resultados de 90 dias, cada um com KPI;
   - marcos de 60 dias;
   - até 3 prioridades de 30 dias, com uma entrega por semana;
   - a próxima semana em duas camadas: a da área e a sua agenda (atividades, delegações, pedidos ao gestor e o que parar de fazer).
3. **Cobra o essencial:** o critério de "feito", a escolha do que fica de fora e se a capacidade do time comporta o plano.
4. **Revisa toda sexta** por exceção, com uma nota de execução e a confiança em cada resultado.
5. **Vira o ciclo a cada 4 semanas**, com uma revisão do que funcionou.
6. **Entrega um .pptx** com os dados gravados dentro dele. Esse arquivo é o ponto de partida da revisão seguinte: guarde-o.

## Como usar

### No Microsoft 365 Copilot

Você precisa do Microsoft 365 Copilot com o **Agent Builder** e a área de **Skills** na aba Configurar. Os nomes dos botões podem variar um pouco entre versões.

1. **Baixe as 5 skills** da pasta [`skills-zip/`](skills-zip/): `coach-metodo`, `coach-fontes`, `coach-kpis`, `coach-rituais` e `coach-pptx`.
2. Crie um agente novo e, na aba **Configurar**, preencha:
   - **Nome:** `Coach de Gestão`.
   - **Descrição, instruções e prompts iniciais:** copie do [`agente.md`](agente.md). Para as instruções, use o ícone de copiar no canto do bloco.
   - **Conhecimento:** seus e-mails, chats e reuniões do Teams, as pessoas da organização, e seu OneDrive e SharePoint.
   - **Capacidades:** ligue o **interpretador de código**, que roda o script do plano.
   - **Skills:** suba os 5 .zip.
3. Se aparecerem, ligue a opção de usar só as fontes configuradas e escolha o modo de resposta que pensa mais antes de responder (*Think deeper*).
4. **Primeiro uso:** numa sexta, anexe o alinhamento e as pautas mais recentes e escreva *"Quero montar meu plano 30-60-90."*

### No Claude

Suba os 5 .zip como skills, na área de Skills das configurações, e cole as instruções num projeto. A busca no e-mail e no Teams não existe aqui: o plano sai só do que você anexar e contar.

## O que ele não faz

- Não envia mensagens, não cria tarefas e não edita roadmap.
- Não reorganiza o time: isso é com o [Coach de Estrutura](../coach-de-estrutura/).
- Não inventa fonte: o que não tem fonte fica marcado para você confirmar.

## Status

| Versão | Situação |
|---|---|
| 1.1.1 | Em uso pelo autor. O código passa na conferência automática ([`testes/conferir_codigo.py`](testes/conferir_codigo.py)); um uso real está registrado em [`testes/RESULTADOS.md`](testes/RESULTADOS.md). A rodada de perguntas de controle em conversa ainda não foi registrada |

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| [`agente.md`](agente.md) | Instruções, descrição e prompts iniciais, prontos para copiar |
| [`skills-zip/`](skills-zip/) | As 5 skills empacotadas, prontas para subir |
| [`pacote/`](pacote/) | O agente como o Copilot exporta |
| [`NOTAS.md`](NOTAS.md) | Desenho, decisões e limitações |
| [`testes/`](testes/) | Perguntas de controle, arquivos fictícios (alinhamento, planos e pautas) e a conferência automática |
