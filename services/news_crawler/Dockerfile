FROM python:3.11-slim

WORKDIR /app/services/news_crawler

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]