# Redator de Atas

Transforma a transcrição de uma reunião numa ata objetiva e **fiel à fonte**, pronta para mandar no Teams, no Loop ou por e-mail. Antes de mostrar a ata, um script confere o texto contra a transcrição e aponta o que só você pode confirmar.

## O que ele faz

1. **Lê a transcrição inteira**, em blocos, com um script. Assim ele não escreve a partir de uma leitura parcial e não esquece quem falou pouco nem as ações do fim da reunião.
2. **Escreve na estrutura do tipo de reunião:** homologação, discovery, refinamento, alinhamento ou outro.
3. **Separa cada coisa no seu nome:** decisão, alinhamento, hipótese, dúvida e próximo passo. Um "acho que" não vira decisão.
4. **Só registra responsável e prazo quando foram ditos.** Quem só comentou não vira dono de ação.
5. **Confere a ata contra a fonte** e mostra, abaixo dela, no máximo 6 pontos para você resolver, cada um com uma sugestão:
   - convidado que não falou (convite não é presença);
   - ação sem responsável;
   - número ou prazo que não está na fonte, ou que foi corrigido durante a reunião;
   - dia da semana convertido em data.
6. **Deixa de fora** saúde, vida pessoal, avaliação de pessoas e recados sociais, mesmo que tenham sido ditos.

Ele redige; quem envia é você. O agente não manda mensagem nem publica nada.

## Como é uma conversa (ilustrativo)

> **Você:** Quero a ata de uma reunião de refinamento. *(anexa a transcrição .docx baixada do Teams)*
>
> **Redator:** `Etapa 2/4 Rascunho · Refinamento · Painel Jatobá · ter 10/11/2026 · Fonte: transcrição .docx, 7 participantes · Leitura 2/2 blocos`
> *(a ata, e depois de uma linha a Conferência)*
> 1. Gustavo e Helena foram convidados, mas não falaram. Ficaram fora de Participantes. Confirma?
> 2. "Quinta" virou 12/11 e "sexta" virou 13/11, pela data da reunião. Estão certos?
>
> **Você:** confirmo os dois
>
> **Redator:** mostra só as seções que mudaram. Quando você disser **"aprovado"**, ele entrega a ata limpa, pronta para copiar.

## Como usar

### Primeiro, baixe a transcrição

Na reunião do Teams: **Recap → Transcrição → Baixar**, em .docx ou .vtt. Notas coladas (.txt ou .md) também servem.

### No Microsoft 365 Copilot

Você precisa do Microsoft 365 Copilot com o **Agent Builder** e a área de **Skills** na aba Configurar. Os nomes dos botões podem variar um pouco entre versões.

1. **Baixe as 4 skills** da pasta [`skills-zip/`](skills-zip/): `ata-fidelidade.zip`, `ata-tipos.zip`, `ata-formato.zip` e `ata-transcricao.zip`. Clique em cada arquivo e depois no botão de download.
2. No Copilot, crie um agente novo e vá para a aba **Configurar**.
3. **Nome:** `Redator de Atas`.
4. **Descrição:** copie de [`agente.md`](agente.md), seção *Descrição*.
5. **Instruções:** em [`agente.md`](agente.md), copie o bloco da seção *Instruções* (ícone de copiar no canto do bloco) e cole.
6. **Conhecimento:** ligue os chats e reuniões do Teams (inclui calendário e transcrições) e as pessoas da organização. Não ligue e-mail nem arquivos: outra fonte só aumenta o risco de trazer fato de outra reunião.
7. **Capacidades:** ligue o **interpretador de código**. É ele que roda o script de leitura e conferência.
8. **Skills:** suba os 4 .zip.
9. Se aparecer a opção de usar só as fontes configuradas, ligue. Se aparecer a de modo de resposta, escolha a que pensa mais antes de responder (*Think deeper*).
10. **Prompts iniciais** (opcional): copie da tabela no fim do [`agente.md`](agente.md).
11. Salve e teste com uma transcrição anexada.

Sem a licença do Microsoft 365 Copilot, o Teams não aparece como conhecimento. Nesse caso, o agente funciona só com a transcrição anexada.

### No Claude

1. Baixe os 4 .zip de [`skills-zip/`](skills-zip/) e suba cada um como skill, na área de Skills das configurações do Claude.
2. Crie um projeto e cole nas instruções do projeto o bloco *Instruções* do [`agente.md`](agente.md).
3. Anexe a transcrição e diga o tipo da reunião. A busca no Teams não existe aqui: a ata sai só do que você anexar.

### Em outros assistentes

Dá para colar as instruções e anexar os `SKILL.md` como arquivos, mas a leitura completa e a conferência dependem do script da skill `ata-transcricao`. Sem ele, o agente perde justamente o que o diferencia.

## Comandos durante a conversa

- **"evidência <item>"**: as falas que sustentam um item da ata, com hora e falante.
- **"conferência"**: roda a conferência de novo.
- **"omitidos"**: os temas que ficaram de fora; **"incluir <tema>"** traz um de volta.
- **"tipo <tipo>"**: refaz a ata na estrutura de outro tipo.
- **"markdown"**: a ata em Markdown cru.

## Limites conhecidos

- A conferência por código confere nomes, números, datas, seções e formato. Se algo foi mesmo uma decisão, ou se alguém assumiu a ação, quem julga são as regras do agente e você.
- Número dito por extenso ("duas semanas") não é conferido.
- Um número da fonte usado no lugar errado passa pela conferência.
- Sem a transcrição anexada, pela busca do Teams, a conferência é só de formato.

## Status

| Versão | Situação |
|---|---|
| 1.0.0 | Em uso pelo autor. O código da skill passa na conferência automática ([`testes/conferir_codigo.py`](testes/conferir_codigo.py)) com 4 reuniões fictícias. A rodada de perguntas de controle em conversa ainda não foi registrada |

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| [`agente.md`](agente.md) | Instruções, descrição e prompts iniciais, prontos para copiar |
| [`skills-zip/`](skills-zip/) | As 4 skills empacotadas, prontas para subir |
| [`pacote/`](pacote/) | O agente como o Copilot exporta |
| [`codigo/`](codigo/) | O código do script de leitura e conferência, separado por módulo. O script da skill é montado a partir daqui |
| [`NOTAS.md`](NOTAS.md) | Objetivo, desenho, decisões e o que mudou desde a primeira versão |
| [`testes/`](testes/) | Perguntas de controle, 4 reuniões fictícias (.docx, .vtt e notas) com as atas esperadas, e a conferência automática |

Para rodar a conferência automática, com Python 3 instalado, na pasta principal do repositório:

```
python produto/redator-de-atas/testes/conferir_codigo.py
```
