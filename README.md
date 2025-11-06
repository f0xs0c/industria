# 🏭 Industria Dataflow  
**Containerized Data & AI Pipeline — Full Guide**

A complete mini data platform that simulates industrial sensor data, trains an AI model for yield prediction, exposes REST APIs, and provides a web dashboard — all containerized.

---

## 🧠 Overview

| Layer | Description |
|--------|--------------|
| **Data Collector** | Simulates temperature, pressure, flow, and yield data (CSV) |
| **Model Service** | Trains a predictive model (regression) and exposes `/predict` |
| **API Service** | REST endpoints for `/stats` and `/predict` |
| **Frontend** | Simple dashboard (HTML/JS + Nginx) |

Each service runs in its own container and communicates via a private network.

---

## 🧱 Project Structure

```
industria-dataflow/
├── data_collector/
│   ├── data_collector.py
│   └── Dockerfile
├── model_service/
│   ├── train_model.py
│   ├── app.py
│   └── Dockerfile
├── api_service/
│   ├── app.py
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── dashboard.js
│   └── Dockerfile
├── docker-compose.yml
├── k8s/
│   ├── pvc-data.yaml
│   ├── deployment-collector.yaml
│   ├── deployment-model.yaml
│   ├── deployment-api.yaml
│   ├── deployment-frontend.yaml
│   ├── frontend-config.yaml
│   └── services.yaml
└── README.md
```

---

# 🚀 Quick Start (Docker Compose)

### 1. Build and Start
```bash
docker compose up -d --build
```

### 2. Check Containers
```bash
docker ps
```

You should see `data_collector`, `model_service`, `api_service`, and `frontend`.

### 3. Access the Dashboard
Open **http://localhost:8080**

### 4. Test the API
```bash
curl http://localhost:8000/healthz
curl http://localhost:8000/stats
```

---

# ☸️ Kubernetes (Minikube) Deployment

### 1. Start Minikube
```bash
minikube start --driver=docker
kubectl get nodes
```

### 2. Create Namespace and Apply
```bash
kubectl create ns industria
kubectl -n industria apply -f k8s/
```

### 3. Check Pods
```bash
kubectl -n industria get pods -w
```

All pods (`collector`, `model`, `api`, `frontend`) should reach **Running (1/1)**.

### 4. Access the App
```bash
kubectl -n industria port-forward svc/frontend-svc 8080:80
```
Then open **http://localhost:8080**

### 5. Internal Tests
```bash
kubectl -n industria run curl --rm -it --image=curlimages/curl --restart=Never --   curl -sS http://api-svc:8000/healthz
```

### 6. Stop
```bash
minikube stop
```

---

# 🐧 Podman Deployment

Podman works like Docker but runs **rootless** and integrates well with SELinux and systemd.

### 1. Start Podman Services
```bash
podman machine init
podman machine start
```

### 2. Build the Images
```bash
podman build -t industria-collector ./data_collector
podman build -t industria-model ./model_service
podman build -t industria-api ./api_service
podman build -t industria-frontend ./frontend
```

### 3. Run with Compose (Podman Compose)
Install podman-compose if missing:
```bash
sudo apt install podman-compose
```

Then launch:
```bash
podman-compose up -d
```

Check:
```bash
podman ps
```

### 4. Access Web UI
Open **http://localhost:8080**

### 5. Stop and Clean
```bash
podman-compose down
podman system prune -f
```

---

# 🧩 Docker Hub Images

| Service | Image |
|----------|--------|
| Collector | `7mnm/industria-collector:latest` |
| Model | `7mnm/industria-model:latest` |
| API | `7mnm/industria-api:latest` |
| Frontend | `7mnm/industria-frontend:latest` |

---

# 🔒 Security Practices

- Non-root users in all containers  
- Read-only volumes for `/data` and `/model`  
- Healthchecks defined in Dockerfiles  
- Use `trivy` or `grype` to scan images:
  ```bash
  trivy image 7mnm/industria-api:latest
  ```

---

# 🧹 Cleanup

```bash
docker compose down -v
minikube delete
podman-compose down
```

---

# 🧠 Authors & Credits
f0xs0c & 7mnm & Adil-pro-simple
Cybersecurity & Data Engineering Student  
Docker Hub: [7mnm](https://hub.docker.com/u/7mnm)


