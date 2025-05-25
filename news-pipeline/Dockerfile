FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libasound2 libxss1 libxtst6 libgbm1 libxshmfence1 libglu1-mesa && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN pip install playwright && playwright install --with-deps

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "kafka_app.producer_service"]
