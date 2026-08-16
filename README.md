# Trip Planner — 3-Tier DevOps Project

A 3-tier web app (frontend + backend + database) containerized with Docker,
orchestrated with Kubernetes, and deployed via a Jenkins CI/CD pipeline.

## Architecture

```
Browser ──> Frontend (nginx + HTML/CSS/JS)
                 │  /api proxied to
                 ▼
            Backend (Python / Flask, REST API)
                 │
                 ▼
            Database (MySQL 8, persistent volume)
```

## Project structure

```
trip-planner/
├── frontend/      index.html, style.css, app.js, nginx.conf, Dockerfile
├── backend/       app.py, requirements.txt, Dockerfile
├── database/      init.sql, Dockerfile
├── k8s/           00-namespace, 01-config-secret, 02-mysql, 03-backend, 04-frontend
├── Jenkinsfile    CI/CD pipeline (build → push → deploy)
├── docker-compose.yml   local testing of all tiers
└── README.md
```

## Quick local test (Docker Compose)

```bash
docker compose up --build
# open http://localhost:8080
```

## Deploy to Kubernetes

```bash
kubectl apply -f k8s/
kubectl -n trip-planner get pods
# frontend reachable at http://<node-ip>:30080
```

See the chat instructions for the full step-by-step (Git, Docker, Jenkins, K8s).

