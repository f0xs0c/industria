FROM python:3.11-slim

# Sécurité: user non-root
RUN useradd -m appuser

# Répertoires
WORKDIR /app
RUN mkdir -p /data && chown -R appuser:appuser /data

# Copie code
COPY data_collector.py /app/

USER appuser
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

VOLUME ["/data"]

CMD ["python", "data_collector.py"]
