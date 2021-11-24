# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
FROM tensorflow/tensorflow:2.7.0-gpu

LABEL org.opencontainers.image.authors='info@argodis.de'
LABEL org.opencontainers.image.url='https://argodis.de'
LABEL org.opencontainers.image.vendor='Argodis GmbH'

ENV PYTHONWARNINGS=default
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY entrypoint.sh /

WORKDIR /app/

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY app .

ENTRYPOINT ["/entrypoint.sh"]
