FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    whois \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies 
# (Playwright 1.42 has pre-built wheels for Python 3.12)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Playwright browsers and OS dependencies
RUN apt-get update && \
    python -m playwright install chromium && \
    python -m playwright install-deps chromium && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "app.py"]