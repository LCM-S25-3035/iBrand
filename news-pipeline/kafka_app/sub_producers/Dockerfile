FROM python:3.10-slim

WORKDIR /app

# Safe to copy everything now, because .dockerignore excludes sensitive/unwanted files
COPY requirements.txt .
COPY bbc_producer_script.py .

# Only copy config if needed for the script
COPY config.py .



RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bbc_producer_script.py"]
