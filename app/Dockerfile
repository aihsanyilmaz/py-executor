FROM python:3.11-slim

RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends git
apt-get install -y build-essential
rm -rf /var/lib/apt/lists/*
EOF

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
