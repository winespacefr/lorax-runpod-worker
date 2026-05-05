FROM ghcr.io/predibase/lorax:latest

RUN pip install --no-cache-dir runpod httpx

COPY handler.py /app/handler.py
COPY start.sh /app/start.sh

WORKDIR /app

RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]