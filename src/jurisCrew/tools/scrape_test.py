#Generated from ChatGPT


#https://do-api-web-search.doe.sp.gov.br/v2/advanced-search/publications?periodStartingDate=2025-1-6&PageNumber=1&FromDate=2025-1-4&ToDate=2025-1-6&PageSize=20&SortField=

#https://do-api-web-search.doe.sp.gov.br/v2/advanced-search/publications?periodStartingDate=personalized&PageNumber=1&Terms%5B0%5D=direito%20administrativo&Terms%5B1%5D=reajustes&Terms%5B2%5D=sa%C3%BAde&FromDate=2020-2-14&ToDate=2025-1-4&JournalId=ca96256b-6ca1-407f-866e-567ef9430123&SectionId=257b103f-1eb2-4f24-a170-4e553c7e4aac&PageSize=20&SortField=Title


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from urllib.request import Request 
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from crewai_tools import SeleniumScrapingTool

import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

#from lxml import html, etree

# Configurar o navegador Selenium (Chromedriver necessário)
driver = webdriver.Chrome()

def compose_url(url, keywords):
    #https://do-api-web-search.doe.sp.gov.br/v2/advanced-search/publications?periodStartingDate=personalized&PageNumber=1&Terms%5B0%5D=direito%20administrativo&Terms%5B1%5D=reajustes&Terms%5B2%5D=sa%C3%BAde&FromDate=2020-2-14&ToDate=2025-1-4&JournalId=ca96256b-6ca1-407f-866e-567ef9430123&SectionId=257b103f-1eb2-4f24-a170-4e553c7e4aac&PageSize=20&SortField=Title
    #PageNumber=1&Terms%5B0%5D=direito%20administrativo&Terms%5B1%5D=reajustes&Terms%5B2%5D=sa%C3%BAde&
    #FromDate=2020-2-14&ToDate=2025-1-4&
    #JournalId=ca96256b-6ca1-407f-866e-567ef9430123&SectionId=257b103f-1eb2-4f24-a170-4e553c7e4aac&
    #PageSize=20&SortField=Title

    if "doe.sp.gov.br" in url:
        url = "https://do-api-web-search.doe.sp.gov.br/v2/advanced-search/publications?periodStartingDate=personalized&"
        pageno = "PageNumber=1&"
        terms = "" 
        fromdate = "FromDate=1900-1-1&"
        todate = "ToDate=2024-12-31&"
        opts = "PageSize=3&SortField=Title"
        for kw in keywords: terms += "Terms%5B0%5D=" + str(kw) + "&"

        return url + pageno + terms + fromdate + todate + opts

# Função genérica para pesquisar palavras-chave
def search_keyword(url, keyword):

    driver.get(compose_url(url, keywords=keyword))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    pre = json.loads(soup.find('pre').get_text(strip=True))
    #print(pre["items"][0]["slug"])
    #new_url = url + str(pre["items"][0]["slug"])
    #driver.get(new_url)

    meal = []
    for item in pre["items"]:
        new_url = url + str(item["slug"])

        tool = SeleniumScrapingTool(website_url=new_url, return_html=False)
        text = tool._run()

        meal.append((text,new_url))

    print("")
    print("RESULTADO: ")
    print(meal)
    print(len(meal))


   





 

# Lista de URLs para pesquisa
urls = [
    "https://doe.sp.gov.br/"
    #"https://www.imprensaoficial.com.br/#13/12/2024",
    #"https://dje.tjsp.jus.br/cdje/index.do;jsessionid=1B3770731DB94D80A57E22667EB0398D.cdje2",
    #"https://www.jusbrasil.com.br",
    #"https://jurisprudencia.stf.jus.br/pages/search",
    #"https://portal.stf.jus.br/jurisprudencia/",
    #"https://www.stj.jus.br/sites/portalp/paginas/Sob-medida/Advogado/Jurisprudencia/Pesquisa-de-Jurisprudencia.aspx"
]

# Palavra-chave para busca
keyword = "direito administrativo"

# Realizar a pesquisa em cada site
for url in urls:
    print(f"Pesquisando em: {url}")
    search_keyword(url, keyword)

# Encerrar o navegador
driver.quit()


#   https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString=planos%20de%20sa%C3%BAde&sort=_score&sortBy=desc