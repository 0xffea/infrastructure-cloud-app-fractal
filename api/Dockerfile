FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

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

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
