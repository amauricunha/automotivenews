# scripts/processing/ai_processor.py
from transformers import pipeline

def summarize_news(news_list):
    summarizer = pipeline("summarization")
    for news in news_list:
        news['summary'] = summarizer(news['summary'], max_length=130, min_length=30, do_sample=False)
    return news_list

if __name__ == "__main__":
    news_list = [
        {'title': 'Exemplo de notícia', 'summary': 'Texto completo da notícia...'}
    ]
    summarized_news = summarize_news(news_list)
    print(summarized_news)