# Dockerfile para scraping e processamento
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ai_processor.py"]  # Para o processamento com IA
