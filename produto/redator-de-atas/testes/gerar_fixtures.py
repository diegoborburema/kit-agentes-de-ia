"""Gera as fixtures do Redator de Atas: quatro reuniões fictícias, cada uma num formato de entrada.

Uso, na raiz do repositório:
    python produto/redator-de-atas/testes/gerar_fixtures.py

| Arquivo | Formato | Cenário |
|---|---|---|
| Refinamento Painel Jatoba 2026-11-10.docx | Transcrição do Teams em .docx (nome e hora numa linha, fala na seguinte) | A |
| Homologacao Taruma Modulo 4 2026-11-11.vtt | Transcrição do Teams em .vtt (<v Nome>, com id de deixa) | B |
| Notas Discovery Previsao de Ruptura 2026-11-05.txt | Notas coladas do Loop, com HTML, [Event] e referência truncada | C |
| Alinhamento Quimera-7 2026-11-09.docx | Transcrição do Teams em .docx | D |

As atas esperadas (`Ata esperada *.md`) são escritas à mão e não são geradas aqui. Todos os nomes, fatos e números
são fictícios (mundo do Tarumã, do Painel Jatobá, do Quimera-7 e da Previsão de Ruptura).
Precisa de python-docx só para gerar os .docx; o script da skill lê os .docx sem bibliotecas externas.
"""
import pathlib

from docx import Document

SAIDA = pathlib.Path(__file__).resolve().parent / "fixtures"

LUCAS = "Andrade,Lucas,BR-São Paulo"
ANA = "Souza,Ana,BR-São Paulo"
BRUNO = "Prado,Bruno,BR-São Paulo"
CAIO = "Teles,Caio,BR-Araras"
RENATA = "Okada,Renata,BR-São Paulo"
PAULA = "Paula Reis (Convidado)"
SALA = "Sala SP-12A"
GUSTAVO = "Lima,Gustavo,BR-São Paulo"
FABIO = "Rangel,Fabio,BR-São Paulo"

# ---------------------------------------------------------------- Cenário A: refinamento (Teams .docx)
REFINAMENTO = [
    (LUCAS, "0:05", "Bom, pessoal, boa tarde. Acho que dá pra começar. Hoje a ideia é refinar a história da "
                    "pós-avaliação de promoções da Onda 2 do Painel Jatobá. Como tem gente nova, rapidinho cada um se "
                    "apresenta, por favor."),
    (ANA, "0:21", "Oi, gente. Ana, do time de Dados, eu sou a PO do Jatobá."),
    (BRUNO, "0:28", "Bruno, engenharia de dados. Tô cuidando dos pipelines da Onda 2."),
    (CAIO, "0:34", "Caio, ciência de dados."),
    (RENATA, "0:39", "Renata, Trade Marketing. Eu sou a dona do processo de pós-avaliação hoje."),
    (PAULA, "0:46", "Paula, da Parceiro+. A gente apoia a implantação do painel junto com vocês."),
    (SALA, "0:52", "Oi, aqui é o Marcos, de Vendas. Tô aqui na sala, entrei pra acompanhar."),
    (LUCAS, "0:58", "Ótimo, obrigado. Renata, você pode contar como é a pós-avaliação hoje, pra todo mundo ficar na "
                    "mesma página?"),
    (RENATA, "1:05", "Posso. Hoje, depois que a promoção acaba, o analista de Trade monta uma planilha comparando o "
                     "investimento com o volume vendido. Ele puxa o sell-out da Base Cambuci, puxa o faturamento por "
                     "filial do Hub Logístico e cruza na mão. Leva uns três dias por mês, porque são muitas promoções."),
    (RENATA, "1:40", "E as exceções a gente trata caso a caso: promoção cancelada no meio, ação conjunta com outro "
                     "fornecedor, troca de preço. Isso fica no e-mail ou na cabeça do analista. Não tem histórico "
                     "nenhum, então quando o analista sai de férias ninguém sabe por que um número foi ajustado."),
    (LUCAS, "2:05", "E é aí que o painel entra, né. Ana, quais são os insumos que a gente já mapeou?"),
    (ANA, "2:12", "São três. O sell-out semanal da Base Cambuci, o faturamento por filial do Hub Logístico e uma "
                  "tabela de exceções que hoje não existe, que o Trade teria que manter. O output é a pós-avaliação "
                  "por promoção, que vai pro painel, com investimento, volume incremental e retorno."),
    (BRUNO, "2:40", "A Base Cambuci e o Hub a gente já tem na camada bruta, carregando todo dia. A tabela de exceções "
                    "é que é o problema: onde ela vai morar? Eu tinha pensado num arquivo no SharePoint que a gente lê "
                    "toda noite."),
    (RENATA, "3:02", "Planilha solta no SharePoint eu acho arriscado, alguém muda o nome de uma coluna e quebra tudo. "
                     "O Trade já cadastra toda promoção no Portal Araçá. Não dá pra subir a exceção lá, no mesmo "
                     "cadastro?"),
    (PAULA, "3:25", "Dá. O Portal Araçá tem campo customizado por cadastro. Num outro cliente a gente fez exatamente "
                    "isso, um upload de tabela de exceção vinculado à promoção."),
    (BRUNO, "3:41", "Se o Araçá expõe isso na API que a gente já consome, pra mim é até melhor, porque eu não preciso "
                    "de mais uma origem. Eu só preciso confirmar se o campo customizado vem na API."),
    (LUCAS, "3:55", "Então, fechado: a tabela de exceções entra pelo Portal Araçá, no próprio cadastro da promoção, e "
                    "não por planilha no SharePoint. Todo mundo de acordo?"),
    (RENATA, "4:05", "De acordo."),
    (ANA, "4:06", "De acordo."),
    (BRUNO, "4:08", "Fechado. Eu confirmo a parte da API."),
    (LUCAS, "4:15", "Beleza. Agora a regra de rateio, que eu sei que é a parte que mais gera dúvida. Renata?"),
    (RENATA, "4:22", "Então. Quando o cliente é de rede, que é o nível N3 da hierarquia de clientes, o investimento da "
                     "promoção é rateado entre as filiais que atendem a rede, proporcional ao volume que cada filial "
                     "faturou no período da promoção. Quando é cliente direto, sem rede, vai cem por cento pra filial "
                     "que faturou."),
    (CAIO, "5:01", "E se o cliente muda de rede no meio da promoção? Isso acontece?"),
    (RENATA, "5:09", "Acontece, mas é raro. Deve ser uns 2% dos casos. Nesses a gente usa a rede do início da "
                     "promoção."),
    (ANA, "5:20", "Isso é importante porque a hierarquia no Hub é a do mês corrente, então a gente vai ter que guardar "
                  "a foto da hierarquia no início de cada promoção."),
    (BRUNO, "5:34", "Dá pra fazer, a gente tira um snapshot da hierarquia na data de início da promoção."),
    (LUCAS, "5:45", "Ok. E a tolerância, Renata? Quando a gente considera que o resultado precisa de revisão?"),
    (RENATA, "5:52", "Quando a divergência entre o sell-out e o faturamento passa de 15%, vai pra revisão humana. O "
                     "analista olha antes de publicar."),
    (CAIO, "6:10", "Isso me lembra o problema que a gente teve no Tarumã com duplicidade de filial. Lá a divergência "
                   "vinha toda de cadastro duplicado."),
    (ANA, "6:22", "Verdade, foi um caos. Mas lá era outro cadastro."),
    (RENATA, "6:30", "Na verdade, me corrigindo: a tolerância é 12%, não 15. Os 15% eram a regra do ano passado, mudou "
                     "em julho."),
    (LUCAS, "6:42", "Então 12% é o corte pra revisão humana. Anotado."),
    (RENATA, "6:48", "Isso. E todo resultado, mesmo dentro da tolerância, o analista de Trade valida antes de publicar "
                     "no painel. Isso não pode sumir, é exigência da diretoria."),
    (LUCAS, "7:02", "Perfeito, a validação humana fica. Outra coisa: tem promoção pequena demais pra valer a pena "
                    "avaliar?"),
    (RENATA, "7:10", "Tem. Abaixo de 5 mil reais de investimento não vale o esforço. A gente sugere deixar fora da "
                     "pós-avaliação."),
    (LUCAS, "7:20", "Ok, fica o corte de 5 mil. Eu levo pro Gustavo validar, porque mexe com o que a gente reporta."),
    (BRUNO, "7:35", "Pessoal, só uma coisa de arquitetura: a gente poderia fazer esse cálculo em Databricks em vez do "
                    "pipeline atual no Synapse. Ficaria mais fácil de manter o snapshot."),
    (LUCAS, "7:50", "Bruno, acho que vale a conversa, mas vamos deixar fora deste refinamento. A gente faz com o que "
                    "tem e discute plataforma em outro fórum."),
    (BRUNO, "8:00", "Justo."),
    (CAIO, "8:05", "Sobre a frequência: provavelmente o cálculo vai rodar semanal, mas depende do Hub, que hoje fecha "
                   "o faturamento só mensal."),
    (BRUNO, "8:20", "É, o Hub hoje fecha mensal. Eu vou perguntar pro time do Hub se eles têm um fechamento semanal "
                    "parcial."),
    (LUCAS, "8:30", "Se não tiver semanal, a gente roda mensal na primeira versão?"),
    (RENATA, "8:36", "Pra mim mensal atende no começo. O que eu não quero é esperar dois meses pra ver resultado."),
    (ANA, "8:44", "E dá pra rodar a pós-avaliação dos últimos seis meses, pra ter histórico desde o começo?"),
    (RENATA, "8:50", "Seria ótimo, mas não é prioridade agora. Se der, depois."),
    (ANA, "8:55", "Então fica como possibilidade pra depois."),
    (PAULA, "9:02", "Uma dúvida: a tabela de exceções vai ter dado pessoal? Tipo nome ou CPF do promotor que fez a "
                    "ação?"),
    (RENATA, "9:12", "Não sei. Às vezes a gente anota o nome do promotor, pra saber com quem falar."),
    (LUCAS, "9:20", "Isso a gente precisa ver com o jurídico antes de fechar o layout da tabela, se pode ter nome de "
                    "promotor ali."),
    (ANA, "9:30", "Concordo. Eu já deixo o campo de fora no desenho até ter a resposta."),
    (SALA, "9:38", "Uma pergunta de Vendas: o resultado vai abrir por vendedor ou só por filial?"),
    (RENATA, "9:45", "Por filial. Vendedor não entra nesta onda."),
    (SALA, "9:50", "Ok, era isso. Obrigado."),
    (LUCAS, "9:55", "Gente, falando nisso, vai ter a confraternização de fim de ano no dia 12/12, quem não respondeu o "
                    "convite responde, tá?"),
    (ANA, "10:02", "Já respondi."),
    (LUCAS, "10:10", "Bom, vamos pro desenho da tabela de exceções. Ana, como você imagina?"),
    (ANA, "10:18", "Eu imagino uma linha por exceção: código da promoção, tipo de exceção, período afetado, valor a "
                   "desconsiderar e uma justificativa curta. E validação no upload: o código da promoção tem que "
                   "existir no Araçá e o período tem que estar dentro da vigência da promoção. Se não passar, o upload "
                   "é recusado com a linha do erro."),
    (RENATA, "10:50", "Os tipos que mais aparecem são cancelamento, ação conjunta e troca de preço. Se tiver uma opção "
                      "'outros', vira bagunça, todo mundo joga tudo lá."),
    (ANA, "11:02", "Então a gente começa só com esses três tipos e sem 'outros'."),
    (RENATA, "11:08", "Fechado, só os três."),
    (LUCAS, "11:14", "Ana, você consegue fechar esse desenho?"),
    (ANA, "11:18", "Consigo. Eu fico com o desenho da tabela, as colunas e as validações, e mando pra Renata até "
                   "quinta."),
    (RENATA, "11:30", "E eu levanto com o time de Trade as exceções dos últimos 3 meses pra gente usar de exemplo e "
                      "testar o upload. Até sexta te mando, Ana."),
    (PAULA, "11:45", "Eu posso mandar o modelo de tabela que a gente usou no outro cliente, ajuda a Ana a não começar "
                     "do zero."),
    (ANA, "11:52", "Ajuda muito, obrigada."),
    (BRUNO, "11:58", "Uma coisa sobre a carga: a carga de outubro do... (inaudível) ... fica pra depois do fechamento "
                     "do Hub."),
    (LUCAS, "12:10", "Não peguei, Bruno, mas a gente vê depois. Caio, o cálculo em si, a lógica do rateio, fica "
                     "contigo?"),
    (CAIO, "12:18", "Hum, eu posso ajudar, mas acho que quem desenha a lógica tem que ser junto com o Bruno, por causa "
                    "do snapshot."),
    (LUCAS, "12:30", "Antes de fechar então: Bruno e Caio, vocês conseguem estimar o esforço do cálculo, com o snapshot "
                     "e o rateio, até a daily de segunda?"),
    (BRUNO, "12:40", "Consigo, junto com o Caio."),
    (CAIO, "12:43", "Fechado, segunda a gente traz."),
    (LUCAS, "12:50", "Ótimo. Recapitulando rapidinho: tabela de exceções pelo Araçá, três tipos, tolerância de 12%, "
                     "corte de 5 mil, que eu valido com o Gustavo, e validação humana do Trade antes de publicar. A "
                     "questão do nome do promotor fica pendente com o jurídico."),
    (RENATA, "13:15", "Isso. E quem vê com o jurídico?"),
    (LUCAS, "13:20", "Boa pergunta, a gente define isso no grupo. Obrigado, pessoal."),
]

# ---------------------------------------------------------------- Cenário B: homologação (Teams .vtt)
V_LUCAS, V_ANA, V_BRUNO = "Lucas Andrade", "Souza,Ana,BR-São Paulo", "Prado, Bruno (BR-São Paulo)"
V_FERNANDA, V_OTAVIO = "Fernanda Alves", "Mendes,Otavio,BR-Campinas"
HOMOLOGACAO = [
    (V_LUCAS, 4, "Bom dia, pessoal. Hoje é a homologação do módulo 4 do Tarumã. A Ana vai apresentar as três "
                 "funcionalidades e a gente vai passando uma por uma."),
    (V_ANA, 15, "São três: o filtro por canal, a exportação para Excel e o alerta de ruptura por e-mail. Começo pelo "
                "filtro."),
    (V_ANA, 24, "Dá pra filtrar por canal, atacado, varejo e e-commerce, e combina com o filtro de filial que já "
                "existia."),
    (V_FERNANDA, 52, "Eu testei ontem com a minha carteira e bateu tudo com o que eu tenho no sistema. Esse pode "
                     "considerar aprovado."),
    (V_OTAVIO, 64, "Concordo, filtro ok."),
    (V_ANA, 70, "Agora a exportação: o botão exporta a tabela com os filtros aplicados."),
    (V_FERNANDA, 85, "Funciona, mas o arquivo vem com o código da filial, não com o nome. Ninguém sabe código de "
                     "filial de cabeça."),
    (V_BRUNO, 98, "Dá pra trocar, é simples, é um ajuste no layout do arquivo."),
    (V_FERNANDA, 106, "Então eu aprovo a exportação com a ressalva de vir o nome da filial em vez do código."),
    (V_ANA, 118, "Anotado. Agora o alerta de ruptura: quando o estoque projetado de um SKU numa loja fica abaixo de 3 "
                 "dias de cobertura, dispara um e-mail pro vendedor da loja."),
    (V_OTAVIO, 140, "Esse é o que mais me interessa. Mas eu não consegui testar, a minha base de teste não tinha nenhuma "
                    "ruptura."),
    (V_FERNANDA, 152, "Eu também não testei direito. Vou testar com a base de outubro e te falo."),
    (V_ANA, 165, "Uma coisa que eu vi ontem: no card de total deu 1.204 lojas, e na tabela deu 1.240. Não bate."),
    (V_BRUNO, 178, "É um bug simples, é a contagem de loja inativa que entra num e não no outro. Eu corrijo até "
                   "amanhã."),
    (V_OTAVIO, 190, "Pra mim isso é bloqueante pro go-live. Diretor olha o card, não olha a tabela."),
    (V_LUCAS, 202, "Então, dá pra dizer que o módulo 4 está homologado?"),
    (V_FERNANDA, 208, "Ainda não. Falta o alerta. Filtro aprovado, exportação aprovada com a ressalva, e o alerta eu te "
                      "falo depois de testar."),
    (V_LUCAS, 222, "Ok. E o go-live, que estava pra 04/12?"),
    (V_ANA, 228, "Se o alerta for aprovado até a semana que vem, a gente mantém 04/12. Senão, eu reavalio a data."),
    (V_LUCAS, 240, "Combinado. Ana, você me avisa se mudar a data."),
    (V_OTAVIO, 248, "Uma sugestão: seria legal ter o alerta também no Teams, não só no e-mail."),
    (V_ANA, 258, "Dá pra pensar, mas fica pra depois do go-live."),
    (V_LUCAS, 266, "Obrigado, pessoal. Bom trabalho."),
]

# ---------------------------------------------------------------- Cenário C: discovery (notas coladas do Loop)
NOTAS_DISCOVERY = """<div class="loop-note"><h2>Discovery Previsão de Ruptura – sessão 1</h2></div>
Data: 05/11/2026 · 10h–11h30
Convidados: Lucas Andrade, Ana Souza, Caio Teles, Renata Okada, Jorge Nunes, Gustavo Lima
Presentes: Lucas Andrade, Ana Souza (Dados), Caio Teles (Ciência de Dados), Renata Okada (Trade Marketing), Jorge Nunes (Supply)
[Event] Gravação não disponível
<span class="note-heading">Dor</span>
- Lojas ficam sem produto na gôndola e o Trade só descobre pelo promotor, dias depois.
- Renata: Trade estima perda de 3% da venda nas lojas com ruptura (número da área, ainda não validado).
- Jorge: no Supply, o problema aparece como pedido urgente; não há visão antecipada.
<span class="note-heading">Usuários</span>
- Promotores (reportam a ruptura) e analistas de Trade (consolidam).
- Jorge citou o planejador de demanda do Supply como possível usuário. Não discutido.
<span class="note-heading">Hoje</span>
- Promotor manda foto e mensagem no WhatsApp para o analista.
- Analista consolida numa planilha semanal e manda para o KAM.
- Não existe registro histórico das rupturas.
<span class="note-heading">Ideias (hipóteses)</span>
- Caio: modelo de previsão de ruptura por SKU e loja, com base no sell-out da Base Cambuci e no estoque informado.
- Ana: alerta no app do promotor, antes da ruptura acontecer. Hipótese; depende de o app aceitar notificação.
- Renata: o ideal seria prever com uma semana de antecedência.
<span class="note-heading">Critério</span>
- Renata citou acerto mínimo de 70% como referência para considerar útil. A validar com a diretoria de Trade.
<span class="note-heading">Premissas e restrições</span>
- Base Cambuci chega com 2 semanas de atraso para parte das redes [3]
- Estoque de loja só existe para as redes que mandam EDI.
<span class="note-heading">Dúvidas</span>
- Lojas pequenas, sem EDI, entram no escopo?
- Quem é o dono do processo depois da implantação: Trade ou Supply?
<span class="note-heading">Próximos passos</span>
- Caio: protótipo com 2 categorias até 20/11.
- Ana: levantar com o time da Base Cambuci se dá pra reduzir o atraso.
- Discutir com Supply o papel do planejador de demanda (sem responsável).
"""

# ---------------------------------------------------------------- Cenário D: alinhamento (Teams .docx)
ALINHAMENTO = [
    (GUSTAVO, "0:04", "Pessoal, o objetivo hoje é alinhar o cronograma do Quimera-7 antes do congelamento de fim de "
                      "ano."),
    (FABIO, "0:15", "Do lado de TI, o congelamento de mudanças começa em 15/12 e vai até 05/01. Nada sobe nesse "
                    "período."),
    (GUSTAVO, "0:28", "Isso está decidido pela TI corporativa, não tem negociação."),
    (ANA, "0:35", "Com esse congelamento, eu não consigo entregar o escopo completo antes de 15/12. Faltam a "
                  "integração com o Hub e os relatórios de filial. Minha proposta é adiar o go-live para a segunda "
                  "quinzena de janeiro, com o escopo completo."),
    (FABIO, "1:05", "Eu prefiro subir em dezembro, antes do congelamento, com escopo reduzido, só os relatórios de "
                    "filial. A integração com o Hub entra em fevereiro."),
    (ANA, "1:22", "Mas sem a integração os relatórios saem com dado manual. Eu tenho receio de o usuário perder a "
                  "confiança no painel logo de cara."),
    (FABIO, "1:40", "Entendo, mas se a gente adia, perde a janela do orçamento de 2026."),
    (LUCAS, "1:52", "Gustavo, isso tem impacto no budget, né? O valor de 2026 que não for usado não passa pro ano que "
                    "vem."),
    (GUSTAVO, "2:03", "Tem. São uns 180 mil que a gente perde se não executar até dezembro."),
    (LUCAS, "2:15", "Então são duas visões: a da Ana, de adiar com escopo completo, e a do Fábio, de subir reduzido em "
                    "dezembro."),
    (GUSTAVO, "2:28", "Eu não quero decidir isso agora sem ver o plano. Ana e Fábio, me tragam até sexta as duas opções "
                      "com prazo, custo e risco, numa página."),
    (ANA, "2:45", "Combinado."),
    (FABIO, "2:47", "Ok."),
    (GUSTAVO, "2:52", "Uma coisa já está decidida: o que estiver pronto em dezembro passa pelo comitê de mudança de "
                      "10/12. Quem perder o comitê, só em janeiro."),
    (LUCAS, "3:08", "Eu reservo o horário do comitê, então, pra garantir."),
    (GUSTAVO, "3:14", "Faz isso."),
    (ANA, "3:20", "Outra coisa: a Helena saiu do projeto, né? Quem fica com os testes?"),
    (GUSTAVO, "3:28", "Isso eu resolvo com o RH, não é tema daqui. Depois te falo."),
    (LUCAS, "3:40", "Fechou. Obrigado, gente."),
]


def docx_teams(caminho, titulo, data, duracao, quem_iniciou, falas):
    """Transcrição no formato do download do Teams: cabeçalho, evento e, por fala, 'Nome   m:ss' e o texto."""
    doc = Document()
    doc.add_paragraph(titulo)
    doc.add_paragraph(data)
    doc.add_paragraph(duracao)
    doc.add_paragraph(f"{quem_iniciou} iniciou a transcrição")
    for nome, hora, texto in falas:
        doc.add_paragraph(f"{nome}   {hora}")
        doc.add_paragraph(texto)
    doc.save(caminho)


def vtt_teams(caminho, falas):
    """Transcrição .vtt do Teams: id de deixa, intervalo e <v Nome>fala</v>; frases longas viram duas deixas."""
    def hms(s):
        return f"{int(s) // 3600:02d}:{int(s) % 3600 // 60:02d}:{int(s) % 60:02d}.{int(s * 1000) % 1000:03d}"
    linhas = ["WEBVTT", ""]
    for i, (nome, ini, texto) in enumerate(falas):
        fim = falas[i + 1][1] - 0.5 if i + 1 < len(falas) else ini + 6
        partes = [texto]
        if len(texto) > 90 and ". " in texto:
            k = texto.index(". ") + 1
            partes = [texto[:k], texto[k + 1:]]
        passo = (fim - ini) / len(partes)
        for j, p in enumerate(partes):
            a, b = ini + j * passo, ini + (j + 1) * passo
            linhas += [f"7c3e1f3a-9b2d-4c55-8e1a-0d9f6b2a{i:02d}{j}/{i * 2 + j}-0", f"{hms(a)} --> {hms(b)}",
                       f"<v {nome}>{p}</v>", ""]
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def main():
    SAIDA.mkdir(exist_ok=True)
    docx_teams(SAIDA / "Refinamento Painel Jatoba 2026-11-10.docx",
               "Refinamento Painel Jatobá – Onda 2-20261110_140112-Gravação de Reunião",
               "10 de novembro de 2026, 02:01PM", "13m 32s", LUCAS, REFINAMENTO)
    vtt_teams(SAIDA / "Homologacao Taruma Modulo 4 2026-11-11.vtt", HOMOLOGACAO)
    (SAIDA / "Notas Discovery Previsao de Ruptura 2026-11-05.txt").write_text(NOTAS_DISCOVERY, encoding="utf-8")
    docx_teams(SAIDA / "Alinhamento Quimera-7 2026-11-09.docx",
               "Alinhamento cronograma Quimera-7-20261109_160305-Gravação de Reunião",
               "9 de novembro de 2026, 04:03PM", "3m 46s", GUSTAVO, ALINHAMENTO)
    for f in sorted(SAIDA.iterdir()):
        print("gerado: " + f.name)


if __name__ == "__main__":
    main()
