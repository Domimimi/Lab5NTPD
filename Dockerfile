#obraz bazowy z Pythonem
FROM python:3.9-slim

#ustawienie folderu roboczego w kontenerze
WORKDIR /app

#kopiowanie listy bibliotek
COPY requirements.txt .

#instalacja bibliotek
RUN pip install --no-cache-dir -r requirements.txt

#kopiowanie reszty plików
COPY . .

#port, na którym działa FastAPI
EXPOSE 8000

#start serwera
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]