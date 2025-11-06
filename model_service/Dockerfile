FROM python:3.11-slim

# Sécurité: user non-root
RUN useradd -m appuser
WORKDIR /app

# Déps système minimales
RUN apt-get update && apt-get install -y --no-install-recommends build-essential wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py train_model.py /app/

# Dossiers & permissions
RUN mkdir -p /data /model && chown -R appuser:appuser /data /model /app

USER appuser
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

VOLUME ["/data", "/model"]

EXPOSE 8001

# Entrée: serveur FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
