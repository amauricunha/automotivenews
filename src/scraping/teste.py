from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_sae_news():
    options = Options()
    options.add_argument('--headless')  # Executa o Chrome em segundo plano
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicializa o driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    url = "https://www.sae.org/news"
    driver.get(url)

    time.sleep(5)  # Aguarda o carregamento da página

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
    return news_list

if __name__ == "__main__":
    news = scrape_sae_news()
    if not news:
        print("Nenhuma notícia foi coletada.")
    else:
        for article in news:
            print(f"Título: {article['title']}")
            print(f"Resumo: {article['summary']}")
            print(f"Link: {article['url']}")
            print(f"Data: {article['publication_date']}")
            print("-" * 40)
