# Coach de Estrutura

Ajuda a decidir **como o time se organiza para entregar o plano**: quem é dono de quê, com que autonomia, em quantas frentes e quem apoia quem.

> **Dados de pessoas.** O agente trabalha com o mapa do seu time e com a carga de cada pessoa. Ele não busca informação sobre ninguém: usa só o que você contar. O arquivo que ele gera sai marcado como confidencial. Use num ambiente aprovado pela sua empresa. Veja o [aviso do módulo](../README.md).

## O que ele faz

1. **Lê o plano 30-60-90** do [Coach de Gestão](../coach-de-gestao/) e monta o mapa do time com o que você disser: pessoa, frente, % do tempo, autonomia, dono ou apoio.
2. **Soma a carga** de cada pessoa e aponta quem passou de 100%, frente sem dono e dono sem apoio.
3. **Diagnostica antes de mexer:** a prioridade em risco é por capacidade, autonomia, clareza, coordenação ou foco?
4. **Propõe opções**, de "manter" ao movimento mais pesado, cada uma com custo, risco, um teste de 4 semanas e o critério de sucesso.
5. **Entrega três coisas:** um arquivo .pptx confidencial com o mapa, o diagnóstico e a decisão; um bloco para o plano; e os pontos para os 1:1, em termos neutros.

Mudanças formais (cargo, reporte, contratação) ele só sinaliza: não decide. Interesses de desenvolvimento que você contar entram na análise, mas nunca saem no arquivo nem nos blocos.

## Como usar

### No Microsoft 365 Copilot

1. **Baixe as 3 skills** da pasta [`skills-zip/`](skills-zip/): `estrutura-diagnostico`, `estrutura-movimentos` e `estrutura-pptx`.
2. Crie um agente novo e, na aba **Configurar**, preencha:
   - **Nome:** `Coach de Estrutura`.
   - **Descrição, instruções e prompts iniciais:** copie do [`agente.md`](agente.md).
   - **Conhecimento:** nenhum. O agente não busca sobre pessoas de propósito.
   - **Capacidades:** ligue o **interpretador de código**.
   - **Skills:** suba os 3 .zip.
3. **Primeiro uso:** anexe o plano 30-60-90 mais recente e escreva *"Quero reorganizar o time para o plano."*

### No Claude

Suba os 3 .zip como skills e cole as instruções num projeto. Como ele não depende de busca, funciona do mesmo jeito.

## Status

| Versão | Situação |
|---|---|
| 1.0.1 | O código passa na conferência automática ([`testes/conferir_codigo.py`](testes/conferir_codigo.py)). Ainda sem uso real nem rodada de perguntas de controle registrados |

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| [`agente.md`](agente.md) | Instruções, descrição e prompts iniciais, prontos para copiar |
| [`skills-zip/`](skills-zip/) | As 3 skills empacotadas, prontas para subir |
| [`pacote/`](pacote/) | O agente como o Copilot exporta |
| [`NOTAS.md`](NOTAS.md) | Desenho, decisões e limitações |
| [`testes/`](testes/) | Perguntas de controle, planos e análise fictícios e a conferência automática |
