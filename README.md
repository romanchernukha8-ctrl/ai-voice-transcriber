# AI Voice Transcriber

A local microservice-based platform for audio processing, speech-to-text transcription, and AI-powered text processing.

The project is designed as a **DevOps / Kubernetes portfolio project** and demonstrates containerization, microservice architecture, asynchronous processing, persistent storage, Kubernetes deployment, Helm, monitoring, and CI/CD.

---

## Overview

AI Voice Transcriber provides a pipeline for processing audio files:

```text
                    ┌──────────────┐
                    │   Frontend   │
                    │ React + Vite │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ API Service  │
                    │   FastAPI    │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      ┌──────────────┐           ┌──────────────┐
      │ File Service │           │   Database   │
      │   FastAPI    │           │ PostgreSQL   │
      └──────┬───────┘           └──────────────┘
             │
             ▼
      ┌──────────────┐
      │    MinIO     │
      │ Object Store │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │   RabbitMQ   │
      │ speech_queue │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │Speech Worker │
      │Faster-Whisper│
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │ Transcription│
      │   Database   │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │  AI Worker   │
      │   FastAPI    │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │    Ollama    │
      │ Local LLM    │
      └──────────────┘
```

---

## Main Features

- Audio file upload
- Object storage using MinIO
- PostgreSQL persistence
- Asynchronous processing with RabbitMQ
- Speech-to-text using Faster-Whisper
- AI text processing using Ollama
- React frontend
- FastAPI microservices
- Docker containerization
- Kubernetes deployment with Minikube
- Helm-based deployment
- Persistent volumes
- Health checks and Kubernetes probes
- Prometheus / Grafana / Loki monitoring stack
- GitHub Actions CI
- Docker image build validation
- Helm chart linting
- Frontend build validation

---

## Technology Stack

### Frontend

- React
- Vite
- Nginx

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- `uv`

### Speech Processing

- Faster-Whisper
- RabbitMQ

### AI

- Ollama
- Local LLM

### Storage

- PostgreSQL
- MinIO
- Redis

### Infrastructure

- Docker
- Docker Compose
- Kubernetes
- Minikube
- Helm

### Monitoring

- Prometheus
- Grafana
- Loki
- Promtail / Grafana Alloy

### CI/CD

- GitHub Actions
- Docker Buildx
- Helm lint

---

## Services

| Service | Purpose |
|---|---|
| `frontend` | React web interface |
| `api-service` | Main API / gateway |
| `auth-service` | Authentication service |
| `file-service` | File upload and storage management |
| `speech-worker` | Audio transcription using Faster-Whisper |
| `ai-worker` | AI text processing |
| `postgres` | Persistent relational database |
| `rabbitmq` | Asynchronous message broker |
| `redis` | In-memory data store |
| `minio` | S3-compatible object storage |
| `ollama` | Local LLM runtime |

---

## Project Structure

```text
ai-voice-transcriber/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── 01-architecture/
│   ├── 02-requirements/
│   ├── 03-api/
│   ├── 04-database/
│   ├── 05-deployment/
│   ├── 06-monitoring/
│   ├── 07-security/
│   ├── 08-testing/
│   ├── 09-aws/
│   ├── 10-adr/
│   └── diagrams/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── infrastructure/
│   ├── compose/
│   ├── docker/
│   ├── helm/
│   │   └── ai-voice-transcriber/
│   └── terraform/
│
├── monitoring/
│   ├── grafana/
│   ├── loki/
│   ├── prometheus/
│   └── promtail/
│
├── services/
│   ├── api-service/
│   ├── auth-service/
│   ├── file-service/
│   ├── speech-worker/
│   └── ai-worker/
│
├── shared/
│   └── shared/
│
├── tests/
│
├── docker-compose.yml
├── start.sh
├── stop.sh
├── Makefile
├── CHANGELOG.md
└── README.md
```

---

# Local Kubernetes Deployment

The primary local deployment uses:

- Minikube
- Kubernetes
- Helm

The Helm chart contains Kubernetes resources for the application and infrastructure components.

### Helm Chart

```text
infrastructure/helm/ai-voice-transcriber/
├── Chart.yaml
├── values.yaml
├── dashboards/
└── templates/
    ├── api-service.yaml
    ├── file-service.yaml
    ├── speech-worker.yaml
    ├── ai-worker.yaml
    ├── frontend.yaml
    ├── postgres.yaml
    ├── postgres-init.yaml
    ├── postgres-pvc.yaml
    ├── rabbitmq.yaml
    ├── redis.yaml
    ├── minio.yaml
    ├── minio-init.yaml
    ├── ollama.yaml
    ├── ollama-pvc.yaml
    ├── ollama-service.yaml
    ├── secret.yaml
    ├── configmap.yaml
    └── grafana-dashboard.yaml
```

---

# Quick Start

## Prerequisites

Install the following tools:

- Docker
- Minikube
- kubectl
- Helm
- Git

Start Minikube if it is not already running:

```bash
minikube start
```

---

## Start the Project

The project provides a unified startup script:

```bash
./start.sh
```

The script:

1. Starts Minikube.
2. Installs or upgrades the Helm release.
3. Waits for Kubernetes pods to become ready.
4. Creates a port-forward to the frontend.

After successful startup:

```text
http://127.0.0.1:8080
```

---

## Stop the Project

```bash
./stop.sh
```

The script stops the frontend port-forward and Minikube.

---

# Helm

The application is deployed using Helm:

```bash
helm upgrade --install ai-voice-transcriber \
  infrastructure/helm/ai-voice-transcriber
```

Validate the chart:

```bash
helm lint infrastructure/helm/ai-voice-transcriber
```

Check the deployment:

```bash
kubectl get pods
```

```bash
kubectl get services
```

```bash
kubectl get pvc
```

---

# Kubernetes Components

The Helm deployment includes:

### Application

- Frontend
- API Service
- File Service
- Speech Worker
- AI Worker

### Infrastructure

- PostgreSQL
- RabbitMQ
- Redis
- MinIO
- Ollama

### Persistence

Persistent volumes are used for stateful components such as:

- PostgreSQL
- MinIO
- Ollama
- RabbitMQ
- Redis

Ollama uses a persistent volume so that downloaded models can survive pod restarts.

---

# Ollama

Ollama runs inside the Kubernetes cluster as a dedicated service.

The deployment exposes:

```text
11434
```

The Ollama deployment includes:

- Persistent storage
- Startup probe
- Readiness probe
- Liveness probe
- CPU and memory resource limits

The AI worker communicates with Ollama through the internal Kubernetes service.

---

# Docker Compose

The repository also contains a Docker Compose environment for local service execution.

```bash
docker compose up -d
```

Stop the Compose environment:

```bash
docker compose down
```

The Compose stack includes:

- PostgreSQL
- RabbitMQ
- Redis
- MinIO
- File Service
- Speech Worker
- Ollama
- AI Worker
- API Service

The Kubernetes deployment is the primary integrated deployment workflow of the project.

---

# Application Ports

Important service ports include:

| Component | Port |
|---|---:|
| Frontend | `8080` via port-forward |
| API Service | `8000` |
| File Service | `8003` in Docker Compose |
| AI Worker | `8004` in Docker Compose |
| PostgreSQL | `5432` |
| RabbitMQ | `5672` |
| RabbitMQ Management | `15672` |
| Redis | `6379` |
| MinIO API | `9000` |
| MinIO Console | `9001` |
| Ollama | `11434` |

---

# CI

GitHub Actions is used for continuous integration.

The current CI workflow performs:

### Helm validation

```bash
helm lint infrastructure/helm/ai-voice-transcriber
```

### Frontend build

```bash
npm ci
npm run build
```

### Docker image builds

CI validates Docker builds for:

- API Service
- File Service
- Speech Worker
- AI Worker
- Auth Service
- Frontend

Docker images are built in CI for validation; the current workflow does not push them to a container registry.

---

# Monitoring

The project contains a monitoring stack based on:

- Prometheus
- Grafana
- Loki
- Promtail / Grafana Alloy

Monitoring configuration is located under:

```text
monitoring/
```

Grafana dashboards and Loki-related configuration are also integrated into the Helm deployment.

---

# Testing

The repository contains tests and service-level validation for the application components.

Examples include:

```text
services/api-service/tests/
services/auth-service/tests/
services/speech-worker/test_db.py
services/speech-worker/test_transcription.py
services/speech-worker/test_whisper.py
services/file-service/test_minio.py
```

CI additionally validates:

- Helm chart
- Frontend build
- Docker image builds

---

# Development

Backend services use Python and FastAPI.

Several Python services use `uv` for dependency management.

Example service structure:

```text
services/api-service/
├── app/
├── alembic/
├── tests/
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

The shared package provides reusable components for:

- clients
- models
- schemas
- security
- utilities

---

# Data Flow

The main transcription flow is:

```text
1. User uploads audio
        │
        ▼
2. API / File Service
        │
        ▼
3. MinIO stores the audio file
        │
        ▼
4. Message is published to RabbitMQ
        │
        ▼
5. Speech Worker consumes the message
        │
        ▼
6. Faster-Whisper processes the audio
        │
        ▼
7. Transcription is stored in PostgreSQL
        │
        ▼
8. AI Worker processes text
        │
        ▼
9. Ollama performs local LLM processing
```

---

# Configuration

Runtime configuration is provided through environment variables and Kubernetes configuration resources.

Sensitive credentials should not be committed to Git.

Use local configuration for:

- PostgreSQL credentials
- RabbitMQ credentials
- MinIO credentials
- database configuration
- service configuration

---

# Documentation

Project documentation is organized under:

```text
docs/
```

Main documentation areas include:

```text
01-architecture
02-requirements
03-api
04-database
05-deployment
06-monitoring
07-security
08-testing
09-aws
10-adr
diagrams
```

The `09-aws` section is retained as project/reference documentation and does **not** represent the current production deployment target.

---

# DevOps Focus

This project demonstrates practical DevOps concepts:

- Microservice architecture
- Containerization
- Docker image creation
- Docker Compose
- Kubernetes
- Minikube
- Helm
- Persistent Volumes
- Kubernetes health probes
- Service discovery
- Asynchronous messaging
- CI automation
- Docker build validation
- Infrastructure organization
- Monitoring and observability
- Local AI infrastructure
- Reproducible local deployment

---

# Current Scope

The project is intentionally focused on a **local Kubernetes environment**.

Current deployment target:

```text
Local machine
     │
     ├── Docker
     ├── Minikube
     └── Kubernetes
            │
            └── Helm
                 │
                 ├── Application services
                 ├── Databases
                 ├── Message broker
                 ├── Object storage
                 ├── Redis
                 ├── Ollama
                 └── Monitoring
```

Cloud infrastructure such as AWS EKS, ECR, RDS and S3 is **not part of the current implemented deployment scope**.

---

# Project Status

The project currently contains:

- Microservice backend
- React frontend
- File storage
- PostgreSQL persistence
- RabbitMQ messaging
- Faster-Whisper transcription
- Ollama integration
- Docker configuration
- Kubernetes deployment
- Helm chart
- Persistent storage
- Health probes
- Local unified startup / shutdown scripts
- Monitoring infrastructure
- GitHub Actions CI
- Docker build validation

The project is being finalized as a local DevOps / Kubernetes portfolio project.

---

# License

See [`LICENSE`](LICENSE).
