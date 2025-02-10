# JusAI

 poetry env use C:\...\AppData\Local\Programs\Python\Python310\python.exe

poetry show --tree >> poetry.tree

 poetry lock

 poetry install

 git add. 
 git commit -am "."
 git push


>>> to test
crewai test

    Pesquisar jurisprudências sobre as palavras-chave estraídas na task extreact_keys na fonte passada à ferramenta.
    Para o caso de https://jurisprudencia.stf.jus.br/pages/search a busca é feita compondo a url da seguinte maneira: https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString=planos%20de%20sa%C3%BAde&sort=_score&sortBy=desc
    Utilize as palavras-chave para inserir no espaço de queryString=

    https://doe.sp.gov.br
    https://www.imprensaoficial.com.br
    https://dje.tjsp.jus.br
    https://www.jusbrasil.com.br
    https://jurisprudencia.stf.jus.br
    https://portal.stf.jus.br
    https://www.stj.jus.br


 Pesquise jurisprudências apenas nas seguintes fontes: 
    Diário Oficial Eletrônico, Emprensa Oficial, JusBrasil, Tribunais de Justiça, STF, STJ.

  Response Template: >
    "Código: <código da jurisprudência aqui>
    Embedding: <embedding do texto da jurisprudência aqui>
    Texto: <Texto completo da jurisprudência aqui>
    Frequência de utilização: <ex: 150 vezes nos tribunais superiores>
    Ranking: <ex: 1ª posição em casos ambientais>
    Taxa de sucesso: <ex: 85% de êxito em demandas que citam essa jurisprudência>
    Data de criação: <data de criação aqui>"


after_kickoff for monitoring




#TODO:
> integrar back - 1 OK
> provisionar front e deploy na Azure - 1
> scrape mais sites - 1
> monitor mais sites - 1
> jurimetria básica --> nível de interseção das jurisprudencias -- jurimetria baseada na interpretação ;;  outras - 1, 3
> criar sistema de login e gerenciamento de acessos - 1

#FINAL do PROJETO
> cache for tools and multi-agents for search
> implement a manager
> readMe
> contas profissionais e validadas
> comparar saídas do ChatGPT com a do projeto
> fazer uma implementação Bayesiana do Crew com um que faça tudo

#EXTRAS:
> implementar banco de dados
> implementar outros tipos de saída, como interpreta=tivos de docs, como mapa mental e linha do tempo
> implementar custom crew composition com airflow e interface para usuário

#FUTURO
> implementação de estimação de honorários
> implementação de rascunho de laudo pericial
> implementação de contas básicas necessárias
> avaliar preços com diferentes nuvens
> avaliar o uso profissional do CrewAI
