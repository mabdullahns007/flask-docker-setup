FROM python:3.11-slim

WORKDIR /backendFlask

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    netcat-openbsd \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x scripts/*.sh

CMD ["python3", "-m", "flask", "--app", "app:create_app", "run", "--host=0.0.0.0"]

