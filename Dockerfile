# Base image
FROM python:3.11-slim

# İş qovluğu
WORKDIR /app

# Sistem paketləri (Postgres client, build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip quraşdır və güncəllə
RUN pip install --upgrade pip

# Layihə fayllarını kopyala.
COPY . .

# Dependencies quraşdır (virtualenv olmadan)
RUN pip install --no-cache-dir -r requirements.txt

# Ətraf mühit dəyişənləri
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV ENV=DEPLOY

# Port expose
EXPOSE ${PORT}

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
