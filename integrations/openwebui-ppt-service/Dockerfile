FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    nodejs \
    npm \
    gcc \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY integrations/openwebui-ppt-service/requirements.txt /tmp/service-requirements.txt
COPY requirements.txt /tmp/ppt-master-requirements.txt

RUN pip install --no-cache-dir -r /tmp/service-requirements.txt && \
    pip install --no-cache-dir -r /tmp/ppt-master-requirements.txt

COPY integrations/openwebui-ppt-service /app
COPY . /opt/ppt-master

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8099"]
