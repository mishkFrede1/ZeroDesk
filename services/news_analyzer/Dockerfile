FROM python:3.11-slim

WORKDIR /app/services/news_analyzer

COPY . .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]