# INDUSTRIA DATAFLOW – Plateforme Data & IA conteneurisée

## Lancer en local (Docker Compose)
```bash
docker compose build
docker compose up -d
# Dashboard
http://localhost:8080
```

## Tester les endpoints
```bash
curl http://localhost:8080/api/healthz
curl http://localhost:8080/api/stats
curl http://localhost:8080/api/predict
```

## Variables du simulateur
- `INTERVAL_SEC` (défaut 1s)
- `BATCH_STARTUP_ROWS` (défaut 200)
- `SEED` (reproductibilité)
