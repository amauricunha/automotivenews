import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Importar o webdriver manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Função para scraping usando requests e BeautifulSoup
def fetch_news_from_site(url, site_name, article_tag, article_class=None, limit=30):
    """Realiza scraping genérico em um site com base nas tags HTML fornecidas."""
    print(f"Fazendo scraping de: {site_name} ({url})")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta exceção para erros HTTP
        
        soup = BeautifulSoup(response.content, 'html.parser')

        news_list = []
        seen_urls = set()  # Conjunto para rastrear URLs já vistos
        articles = []  # Inicializando a lista de artigos
        
        # Seletores refinados manualmente para cada site
        if site_name == "IEEE Automotive":
            driver = setup_selenium()
            driver.get(url)
            time.sleep(5)
            
            # Simula rolagem da página
            last_height = driver.execute_script("return document.body.scrollHeight")
            while len(news_list) < limit:
                # Encontra os artigos na página carregada
                articles = driver.find_elements(By.CLASS_NAME, 'widget__body')
                
                for article in articles:
                    title_tag = article.find_element(By.CLASS_NAME, 'widget__headline')
                    title = title_tag.text.strip() if title_tag else "Título não encontrado"
                    
                    link_tag = title_tag.find_element(By.TAG_NAME, 'a') if title_tag else None
                    link = link_tag.get_attribute('href') if link_tag else "Link não encontrado"
                    
                    summary_tag = article.find_element(By.CLASS_NAME, 'widget__subheadline')
                    summary = summary_tag.text.strip() if summary_tag else "Sem resumo"
                    
                    publication_date_tag = article.find_element(By.CLASS_NAME, 'social-date__text')
                    publication_date = publication_date_tag.text.strip() if publication_date_tag else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if link not in seen_urls:  # Verifica se o link já foi adicionado
                        seen_urls.add(link)  # Adiciona o link ao conjunto
                        news_list.append({
                            "title": title,
                            "summary": summary,
                            "url": link,
                            "publication_date": publication_date,
                            "source": site_name
                        })
                
                # Tenta rolar para o final da página para carregar mais artigos
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Sai do loop se não houver mais conteúdo a ser carregado
                last_height = new_height
            driver.quit()
        elif site_name == "TechCrunch Transportation":
            articles = soup.select('.wp-block-tc23-post-picker')
            for article in articles:
                # Verifica diferentes possíveis tags para o título
                title_tag = article.select_one('h2 a') or article.select_one('h3 a') or article.select_one('a')
                link_tag = article.select_one('h2 a') or article.find('a')

                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                
                # Verifica se há resumo disponível
                summary_tag = article.select_one('.wp-block-post-excerpt__excerpt')
                summary = summary_tag.text.strip() if summary_tag else "Sem resumo"
                
                # Verifica se há data de publicação
                publication_date_tag = article.select_one('time')
                publication_date = publication_date_tag['datetime'] if publication_date_tag else "Data não encontrada"
                
                # Adiciona os dados ao dicionário da lista de notícias
                if link not in seen_urls:  # Verifica se o link já foi adicionado
                        seen_urls.add(link)  # Adiciona o link ao conjunto
                        news_list.append({
                            "title": title,
                            "summary": summary,
                            "url": link,
                            "publication_date": publication_date,
                            "source": site_name
                        })
            # Captura artigos com a classe featured (destaque)
            featured_articles = soup.select('.is-featured.wp-block-tc23-post-picker')
            for article in featured_articles:
                # Captura o título e link do artigo destacado
                title_tag = article.select_one('h2 a') or article.select_one('a')
                link_tag = title_tag
                
                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                
                # Captura o resumo do artigo destacado
                summary_tag = article.select_one('.wp-block-post-excerpt__excerpt')
                summary = summary_tag.text.strip() if summary_tag else "Sem resumo"

                # Captura a data de publicação
                publication_date_tag = article.select_one('time')
                publication_date = publication_date_tag['datetime'] if publication_date_tag else "Data não encontrada"

                # Adiciona os dados do artigo destacado na lista
                if link not in seen_urls:  # Verifica se o link já foi adicionado
                        seen_urls.add(link)  # Adiciona o link ao conjunto
                        news_list.append({
                            "title": title,
                            "summary": summary,
                            "url": link,
                            "publication_date": publication_date,
                            "source": site_name
                        })
        elif site_name == "SAE Automotive Engineering":
            options = Options()
            options.add_argument('--headless')  # Executa o Chrome em segundo plano
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            # Inicializa o driver
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            url = "https://www.sae.org/news"
            driver.get(url)

            time.sleep(0)  # Aguarda o carregamento da página

            news_list = []

            # Encontrar todos os artigos na página
            articles = driver.find_elements(By.CLASS_NAME, 'nx-card-body')

            if not articles:
                print("Nenhum artigo encontrado. Verifique se a classe 'nx-card-body' está correta.")
                driver.quit()
                return []

            for article in articles:
                try:
                    title_tag = article.find_element(By.CLASS_NAME, 'nx-card-name')
                    title = title_tag.text.strip() if title_tag else "Título não encontrado"

                    link_tag = article.find_element(By.CLASS_NAME, 'nx-card-view-link')
                    link = link_tag.get_attribute('href') if link_tag else "Link não encontrado"

                    summary_tag = article.find_element(By.CLASS_NAME, 'nx-card-description')
                    summary = summary_tag.text.strip() if summary_tag else "Sem resumo"

                    publication_date_tag = summary_tag.find_element(By.CLASS_NAME, 'nx-date')
                    publication_date = publication_date_tag.text.strip() if publication_date_tag else "Data não encontrada"

                    news_list.append({
                        "title": title,
                        "summary": summary,
                        "url": link,
                        "publication_date": publication_date
                    })
                except Exception as e:
                    print(f"Erro ao processar artigo: {e}")

            driver.quit()

        elif site_name == "IJAE":
            articles = soup.find_all('div', class_='entry-content', limit=limit)
            for article in articles:
                title_tag = article.find('h3') or article.find('h2') or article.find('a')
                link_tag = article.find('a')

                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                summary = article.find('p').text.strip() if article.find('p') else "Sem resumo"
                news_list.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "publication_date": publication_date,
                    "source": site_name
                })
        elif site_name == "MotorTrend":
            articles = soup.find_all('div', class_='article-preview', limit=limit)
            for article in articles:
                title_tag = article.find('h3') or article.find('h2') or article.find('a')
                link_tag = article.find('a')

                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                summary = article.find('p').text.strip() if article.find('p') else "Sem resumo"
                news_list.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "publication_date": publication_date,
                    "source": site_name
                })
        elif site_name == "Just Auto":
            articles = soup.find_all('div', class_='news-item', limit=limit)
            for article in articles:
                title_tag = article.find('h3') or article.find('h2') or article.find('a')
                link_tag = article.find('a')

                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                summary = article.find('p').text.strip() if article.find('p') else "Sem resumo"
                news_list.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "publication_date": publication_date,
                    "source": site_name
                })
        else:
            articles = soup.find_all(article_tag, class_=article_class, limit=limit)
            for article in articles:
                title_tag = article.find('h3') or article.find('h2') or article.find('a')
                link_tag = article.find('a')

                title = title_tag.text.strip() if title_tag else "Título não encontrado"
                link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"{url}{link_tag['href']}"
                summary = article.find('p').text.strip() if article.find('p') else "Sem resumo"
                news_list.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "publication_date": publication_date,
                    "source": site_name
                })

        if not articles:
            print(f"⚠️ Nenhum artigo encontrado no site: {site_name}. Verifique o seletor.")
            return []

        print(f"✔️ {len(news_list)} notícias coletadas de {site_name}")
        return news_list

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erro HTTP ao acessar {site_name}: {http_err}")
    except Exception as err:
        print(f"❌ Erro ao fazer scraping de {site_name}: {err}")
    
    return []

# Configurando o Selenium com Chrome headless para contornar bloqueios
def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Adiciona um User-Agent para simular um navegador real
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # Configura o ChromeDriver automaticamente com a versão correta
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def fetch_news_selenium(url, site_name):
    print(f"Fazendo scraping de: {site_name} ({url}) com Selenium")
    
    driver = setup_selenium()
    news_list = []
    
    try:
        driver.get(url)
        time.sleep(5)  # Aguarda o carregamento da página
        
        # Exemplo de scraping em Car and Driver
        if site_name == "Car and Driver":
            articles = driver.find_elements(By.CLASS_NAME, 'full-item')
            for article in articles:
                title = article.find_element(By.TAG_NAME, 'h2').text
                link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                news_list.append({
                    "title": title,
                    "summary": "Sem resumo",
                    "url": link,
                    "publication_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "source": site_name
                })
        # Exemplo para Auto News
        elif site_name == "Auto News":
            articles = driver.find_elements(By.CLASS_NAME, 'article__content')
            for article in articles:
                title = article.find_element(By.TAG_NAME, 'h2').text
                link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                news_list.append({
                    "title": title,
                    "summary": "Sem resumo",
                    "url": link,
                    "publication_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "source": site_name
                })
    
        print(f"✔️ {len(news_list)} notícias coletadas de {site_name}")
    
    finally:
        driver.quit()
    
    return news_list

# Função para salvar os dados em um arquivo CSV
def save_to_csv(news_list, filename='news_data.csv'):
    # Lê os URLs existentes no arquivo
    existing_urls = set()
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                existing_urls.add(row['url'])
    except FileNotFoundError:
        print(f"⚠️ O arquivo {filename} não existe. Um novo será criado.")

    # Filtra apenas as notícias novas
    new_news_list = [news for news in news_list if news['url'] not in existing_urls]

    if new_news_list:
        keys = new_news_list[0].keys()
        with open(filename, 'a', newline='', encoding='utf-8') as output_file:  # Modo append
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            if output_file.tell() == 0:  # Verifica se o arquivo está vazio
                dict_writer.writeheader()  # Escreve o cabeçalho se o arquivo foi criado agora
            dict_writer.writerows(new_news_list)
        print(f"✔️ {len(new_news_list)} novas notícias salvas em {filename}")
    else:
        print("⚠️ Nenhuma nova notícia para salvar.")

# Sites a serem raspados
news_sites = [
    ("IEEE Automotive", "https://spectrum.ieee.org/tag/automotive", 'a', 'https://spectrum.ieee.org/te-automotive'),
    ("TechCrunch Transportation", "https://techcrunch.com/category/transportation/", 'article', 'post-block'),
    ("SAE Automotive Engineering", "https://www.sae.org/news", 'div', 'nx-card-content'),
    #("IJAE", "https://ijae.jp/", 'div', 'entry-content'),
    #("Just Auto", "https://www.just-auto.com/", 'div', 'news-item')
]

selenium_sites = [
    #("Car and Driver", "https://www.caranddriver.com/"),
    #("Auto News", "https://www.autonews.com/")
]

# Executa o scraping
all_news = []

# Scraping com BeautifulSoup e com Selenium para sites que têm rolagem infinita
for site_name, url, tag, tag_class in news_sites:
    news = fetch_news_from_site(url, site_name, tag, tag_class)
    all_news.extend(news)

# Scraping com Selenium para sites que retornam 403
for site_name, url in selenium_sites:
    news = fetch_news_selenium(url, site_name)
    all_news.extend(news)
    
# Salvando as notícias no arquivo CSV
save_to_csv(all_news)
