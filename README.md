# Kit de agentes de IA 🤖

Agentes de IA para o dia a dia de quem trabalha com produto e gestão. Grátis, em português, prontos para copiar e adaptar.

Eles nasceram no **Microsoft 365 Copilot**, e a maior parte também funciona no **Claude**. Cada agente vem com as instruções, as skills já empacotadas e um passo a passo para criar o seu.

## O que tem aqui

| Agente | O que faz | Tema |
|---|---|---|
| [Coach de Apresentação](produto/coach-apresentacao/) | Conduz você por um canvas de storytelling e entrega um prompt pronto para o Claude montar o roteiro e o PowerPoint | Produto |
| [Redator de Atas](produto/redator-de-atas/) | Transforma a transcrição de uma reunião numa ata fiel à fonte e aponta o que só você pode confirmar | Produto |
| Gestão | Organizador de 1:1 e coaches de gestão | Chegando |

Também tem:
- [**O método**](metodo/): como versionar e testar um agente como se fosse um produto.
- [**Ferramentas**](ferramentas/): scripts que conferem limites, empacotam skills e diagnosticam o ambiente do Copilot.

## Nunca usou GitHub? Comece aqui

Você não precisa de conta, de git nem de programar.

1. **Escolha um agente** na tabela acima e clique no nome. A pasta dele tem um passo a passo próprio, logo abaixo da lista de arquivos.
2. **Para baixar um arquivo:** clique nele e depois no botão de download (a seta para baixo, no canto direito, acima do conteúdo).
3. **Para baixar tudo de uma vez:** volte para esta página, clique no botão verde **<> Code** e em **Download ZIP**.
4. **Para copiar um texto** (as instruções de um agente, por exemplo): passe o mouse sobre o bloco e clique no ícone de copiar, no canto direito do bloco.

## Onde funciona

| Onde | Como |
|---|---|
| **Microsoft 365 Copilot** (Agent Builder) | Onde os agentes foram criados. Você cola as instruções e sobe as skills em .zip |
| **Claude** | Aceita os mesmos .zip como skills. Você cria um projeto com as instruções |
| **Outros assistentes** (ChatGPT, Gemini) | Dá para usar as instruções e anexar as skills como arquivos. O que depende de script pode não rodar |

## Como as pastas estão organizadas

```
produto/        agentes para o trabalho de produto
gestao/         agentes para gestão de pessoas e times (chegando)
metodo/         o método e os modelos para criar e testar seus agentes
ferramentas/    scripts de apoio
```

Dentro de cada agente:

| Arquivo ou pasta | Para quê | Precisa para usar? |
|---|---|---|
| `README.md` | O passo a passo | Sim, comece por ele |
| `agente.md` | Instruções, descrição e prompts iniciais, prontos para copiar | Sim |
| `skills-zip/` | As skills empacotadas, prontas para subir | Sim |
| `pacote/` | O agente como o Copilot exporta | Não |
| `NOTAS.md` | Por que cada decisão foi tomada | Não |
| `testes/` | Perguntas de controle e casos de teste | Não, a menos que você vá mudar o agente |

## Sobre os dados

Todo nome de pessoa, projeto, sistema ou empresa nos exemplos e testes é **fictício**. Se algum coincidir com algo real, é coincidência.

## Achou um problema ou tem uma ideia?

Abra uma [issue](https://github.com/diegoborburema/kit-agentes-de-ia/issues): conte o que você fez, o que esperava e o que aconteceu. Precisa de uma conta gratuita no GitHub. Sem conta, me chame no [LinkedIn](https://www.linkedin.com/in/diego-borburema-8721389b).

## Licença

[MIT](LICENSE): pode usar, copiar, adaptar e usar no trabalho. Só mantenha o aviso de licença.

<sub>Projeto pessoal. Não representa a visão do meu empregador.</sub>
