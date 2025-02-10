from crewai_tools import RagTool, SeleniumScrapingTool, BaseTool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from typing import List

from pydantic import BaseModel
from bs4.element import Comment
from pydantic.v1 import Field
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from crewai.tools import BaseTool
from bs4 import BeautifulSoup

import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class ScrapeTribunalTool(BaseTool):
    name: str = "Tribunal Scraper Tool"
    description: str = "Busca por palavras-chave em um website específico"

    def scrape_search(self, driver, url: str, keyword: str, find_element: str = 'pre', parser_type: str = 'html.parser'):
        ans = ""
        driver.get(self.compose_url(url, keywords=keyword))
        driver.implicitly_wait(5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, parser_type)
        pre = json.loads(soup.find(find_element).get_text(strip=True))

        for item in pre["items"]:
            new_url = url + str(item["slug"])

            tool = SeleniumScrapingTool(website_url=new_url, return_html=False)
            text = tool._run()

            ans += text + "\n --- fim do documento --- \n"

    def scrape_search2(self, url: str, keyword: str):
        ans = ""
        tool = SeleniumScrapingTool(website_url=self.compose_url(url, keywords=keyword), return_html=False)
        text = tool._run()

        ans += text + "\n --- fim do documento --- \n"

    def _run(self, url: List[str] = ["https://doe.sp.gov.br/busca-avancada"], keyword: List[str] = ["jurisprudencia"]) -> str: #TODO change in here
        ans = ""

        driver = webdriver.Chrome()
        if "doe.sp.gov" in url:
            driver.get(self.compose_url(url, keywords=keyword))
            driver.implicitly_wait(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            pre = json.loads(soup.find('pre').get_text(strip=True))

            for item in pre["items"]:
                new_url = url + str(item["slug"])

                tool = SeleniumScrapingTool(website_url=new_url, return_html=False)
                text = tool._run()

                ans += text + "\n --- fim da busca para o site doe.sp.gov --- \n"

        if "jusbrasil" in url:
            driver.get(self.compose_url(url, keywords=keyword))
            driver.implicitly_wait(10)
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site jusbrasil --- \n"
        driver.quit()

        if "imprensaoficial" in url:
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site imprensaoficial --- \n"
                
        if "dje.tjsp.jus" in url:
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site dje.tjsp.jus --- \n"
                
        if "jurisprudencia.stf.jus" in url:
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site jurisprudencia.stf.jus --- \n"
                
        if "portal.stf.jus" in url:
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site portal.stf.jus --- \n"

        if "stj.jus" in url:
            ans += self.scrape_search2(url = url, keyword=keyword)
            ans += "\n --- fim da busca para o site stj.jus --- \n"

        ans += "\n ------- fim da busca para todos os sites ------- \n"
        return ans
    
    def compose_url(self, url: List[str], keywords: List[str]):

        try:
            if "doe.sp.gov" in url:
                url = "https://do-api-web-search.doe.sp.gov.br/v2/advanced-search/publications?periodStartingDate=personalized&"
                pageno = "PageNumber=1&"
                terms = "Terms%5B0%5D=jurisprudencia&" 
                fromdate = "FromDate=1900-2-1&"
                todate = "ToDate=2024-12-31&"
                opts = "PageSize=10&SortField=Title"

                for kw in keywords: terms += "Terms%5B0%5D=" + str(kw) + "&"
                return url + pageno + terms + fromdate + todate + opts
            
            if "imprensaoficial" in url:
                url = "https://www.imprensaoficial.com.br/DO/BuscaDO2001Resultado_11_3.aspx?"
                pad01 = str("&f=xhitlist&xhitlist_vpc=first&xhitlist_x=Advanced&xhitlist_q=%5bfield+%27dc%3a")
                terms1 = "filtropalavraschave=jurisprudencia" 
                fromdate = "02.01.1900"
                todate = "12.31.2024"
                pad_data = "datapubl%27%3a%3e%3d" + fromdate + "%3c%3d" + todate + "%5d"
                terms2 = "(jurisprudencia"
                pad02 = "filtrogrupos=Todos%2c+Cidade+de+SP%2c+Editais+e+Leil%c3%b5es%2c+Empresarial%2c+Executivo%2c+Junta+Comercial%2c+DOU-Justi%c3%a7a%2c+Judici%c3%a1rio%2c+DJE%2c+Legislativo%2c+Municipios%2c+OAB%2c+Suplemento%2c+TRT+&xhitlist_mh=9999&"
                pageno = ""
                opts = ""

                for kw in keywords: 
                    terms1 += "+" + str(kw)
                    terms2 += str("a%2b") + str(kw)
                terms2 = terms2 + ")&"
                return url + terms1 + pad01 + pad_data + terms2 + pad02 
            
            if "dje.tjsp.jus" in url: ### TODO:  strange error
                # "https://dje.tjsp.jus.br/cdje/index.do;jsessionid=1B3770731DB94D80A57E22667EB0398D.cdje2"
                url = ""
                terms = "" 
                pad01 = str("")
                terms1 = "" 
                fromdate = ""
                todate = ""
                pad_data = "datapubl%27%3a%3e%3d" + fromdate + "%3c%3d" + todate + "%5d"
                terms2 = ""
                pad02 = ""
                pageno = ""
                opts = ""

                for kw in keywords: 
                    terms1 += "+" + str(kw)
                    terms2 += str("a%2b") + str(kw)
                terms2 = terms2 + ")&"
                return url + terms + pad01 + pad_data + terms2 + pad02 
            
            if "jusbrasil" in url:
                url = "https://www.jusbrasil.com.br/jurisprudencia/busca?"
                terms = "q=" + str(keywords[0])
                for kw in keywords[1:]: 
                    terms += "+" + str(kw) 
                return url + terms 
            
            if "jurisprudencia.stf.jus" in url:
                # https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString=saude%20%20ou%20planos&sort=_score&sortBy=desc
                url = "https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&"
                # publicacao_data=03051990-31122024&
                # page=1&
                # pageSize=10&
                # queryString=saude%20%20ou%20planos&sort=_score&sortBy=desc
                query_data = "publicacao_data="
                fromdate = "03051990" + "-"
                todate = "31122024" + "&"
                pageno = "page=1&"
                page_size = "pageSize=10&"
                terms = "queryString="
                pad = "sort=_score&sortBy=desc"
                for kw in keywords: 
                    terms += str(kw) + "%20%20ou%20"
                return url + query_data + fromdate + todate + pageno + page_size + terms + pad
            
            if "stj.jus" in url:
                # "https://portal.stf.jus.br/textos/verTexto.asp?servico=jurisprudenciaInternacional"
                #"https://www.stj.jus.br/sites/portalp/paginas/Sob-medida/Advogado/Jurisprudencia/Pesquisa-de-Jurisprudencia.aspx" 

                #https://scon.stj.jus.br/SCON/pesquisar.jsp?pesquisaAmigavel=+saude+planos+e++Publica%26ccedil%3B%26atilde%3Bo%3A+14%2F02%2F2024+a+31%2F12%2F2024&
                # acao=pesquisar&
                # novaConsulta=true&i=1&b=ACOR&
                # livre=saude+planos&
                # filtroPorOrgao=&filtroPorMinistro=&filtroPorNota=&
                # data=%40DTPB+%3E%3D+%2220240214%22+E+
                # %40DTPB+%3C%3D+%2220241231%22&
                # operador=e&thesaurus=JURIDICO&
                # p=true&tp=T&processo=&classe=&uf=&relator=&
                # dtpb=%40DTPB+%3E%3D+%22
                # 20240214
                # %22+E+%40DTPB+%3C%3D+%22
                # 20241231
                # %22&
                # dtpb1=
                # 14%2F02%2F2024
                # &dtpb2=
                # 31%2F12%2F2024&
                # dtde=&dtde1=&dtde2=&orgao=&ementa=&nota=&ref=

                url        = "https://scon.stj.jus.br/SCON/pesquisar.jsp?pesquisaAmigavel="
                terms      = ""
                for kw in keywords: 
                    terms += "+" + str(kw)
                opts       = "+e++Publica%26ccedil%3B%26atilde%3Bo%3A+"
                fromdate   = "14%2F02%2F2024"
                pad_fdate1 = "+a+"
                todate     = "31%2F12%2F2024" + "&"
                pad_1      = "acao=pesquisar&novaConsulta=true&i=1&b=ACOR&"
                terms2     = "livre=" + str(keywords[0])
                for kw in keywords[1:]: 
                    terms2 += "+" + str(kw)
                terms2     += "&"
                pad_2      = "filtroPorOrgao=&filtroPorMinistro=&filtroPorNota=&"
                fdate2     = "20240214"
                tdate2     = "20241231"
                fromdate2  = "data=%40DTPB+%3E%3D+%22" + fdate2 + "%22+E+"
                todate2    = "%40DTPB+%3C%3D+%22" + fdate2 + "%22&"
                pad_3      = "operador=e&thesaurus=JURIDICO&p=true&tp=T&processo=&classe=&uf=&relator=&"
                fromdate3  = "dtpb=%40DTPB+%3E%3D+%22" + fdate2
                todate3    = "%22+E+%40DTPB+%3C%3D+%22" + tdate2 + "%22&"
                fromdate4  = "dtpb1=" + fromdate
                todate4    = "&dtpb2=" + todate
                pad_4      = "dtde=&dtde1=&dtde2=&orgao=&ementa=&nota=&ref=&"
                return url + terms + opts + fromdate + pad_fdate1 + todate + pad_1 + terms2 + pad_2 + fromdate2 + todate2 + pad_3 + fromdate3 + todate3 + fromdate4 + todate4 + pad_4
        
        except:
            raise NotImplementedError


    

