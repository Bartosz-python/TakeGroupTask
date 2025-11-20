FROM python:3.11-slim

# Instalacja zależności systemowych wymaganych przez Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium firefox webkit
COPY . .
RUN mkdir -p test-reports traces

CMD ["pytest", "--html=test-reports/test_report.html", "--self-contained-html"]