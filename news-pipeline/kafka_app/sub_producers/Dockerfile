FROM python:3.10-slim

WORKDIR /app

# Safe to copy everything now, because .dockerignore excludes sensitive/unwanted files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bbc_producer_script.py"]
