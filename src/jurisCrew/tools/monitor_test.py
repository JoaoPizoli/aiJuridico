#Generated from ChatGPT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import hashlib

# Configurar o Selenium WebDriver
driver = webdriver.Chrome()

# Função para buscar jurisprudências
def fetch_jurisprudence(url, keyword, reference_date):
    driver.get(url)
    time.sleep(3)  # Aguarda o carregamento inicial

    if "doe.sp.gov.br" in url:
        search_box = driver.find_element(By.NAME, "palavrasChave")
    elif "imprensaoficial" in url:
        search_box = driver.find_element(By.ID, "search_input")
    elif "dje.tjsp.jus.br" in url:
        search_box = driver.find_element(By.NAME, "pesquisaPrincipal")
    elif "jusbrasil.com.br" in url:
        search_box = driver.find_element(By.ID, "q")
    elif "jurisprudencia.stf.jus.br" in url or "portal.stf.jus.br" in url:
        search_box = driver.find_element(By.NAME, "txtPesquisaLivre")
    elif "stj.jus.br" in url:
        search_box = driver.find_element(By.ID, "txtPesquisaLivre")
    else:
        print(f"Site não suportado: {url}")
        return []

    # Inserir palavra-chave e executar a busca
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Aguarda os resultados carregarem

    # Extrair resultados da página
    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.find_all("a")  # Ajuste o seletor para capturar links de resultados
    jurisprudences = []

    for result in results:
        text = result.text.strip()
        link = result.get("href")
        # Armazena apenas os resultados publicados após a data de referência
        if reference_date in text:  # Adapte para verificar datas
            jurisprudences.append({"text": text, "link": link})

    return jurisprudences

# Função para calcular hash do conteúdo
def calculate_hash(content):
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

# Monitoramento
def monitor_sites(keywords, reference_date, sites, previous_hashes):
    new_hashes = {}
    for url in sites:
        print(f"Monitorando: {url}")
        for keyword in keywords:
            results = fetch_jurisprudence(url, keyword, reference_date)
            content_hash = calculate_hash(results)
            # Verifica se o conteúdo é novo
            if previous_hashes.get(url + keyword) != content_hash:
                print(f"Novas jurisprudências encontradas para '{keyword}' em {url}!")
                print(results)
            new_hashes[url + keyword] = content_hash
    return new_hashes

# Configurações iniciais
keywords = ["direito administrativo", "contratos públicos"]
reference_date = "13/12/2024"
sites = [
    "https://doe.sp.gov.br/busca-avancada",
    "https://www.imprensaoficial.com.br/#13/12/2024",
    "https://dje.tjsp.jus.br/cdje/index.do;jsessionid=1B3770731DB94D80A57E22667EB0398D.cdje2",
    "https://www.jusbrasil.com.br",
    "https://jurisprudencia.stf.jus.br/pages/search",
    "https://portal.stf.jus.br/jurisprudencia/",
    "https://www.stj.jus.br/sites/portalp/paginas/Sob-medida/Advogado/Jurisprudencia/Pesquisa-de-Jurisprudencia.aspx"
]

# Carrega hashes anteriores
try:
    with open("previous_hashes.json", "r") as f:
        previous_hashes = json.load(f)
except FileNotFoundError:
    previous_hashes = {}

# Executa o monitoramento
new_hashes = monitor_sites(keywords, reference_date, sites, previous_hashes)

# Salva os novos hashes
with open("previous_hashes.json", "w") as f:
    json.dump(new_hashes, f)

# Fecha o navegador
driver.quit()
