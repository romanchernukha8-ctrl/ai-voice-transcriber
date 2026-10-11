# AI Voice Transcriber

A local microservice-based platform for audio processing, speech-to-text transcription, and AI-powered text processing.

**AI Voice Transcriber is a DevOps / Kubernetes portfolio project** demonstrating containerization, microservice architecture, asynchronous processing, persistent storage, Helm-based Kubernetes deployment, monitoring, automated testing, security scanning, and CI/CD.

The current deployment target is a local environment built around **Docker, Minikube, Kubernetes, and Helm**. AWS deployment is outside the current implemented scope.

## Table of Contents

- [Overview](#overview)
- [Main Features](#main-features)
- [Architecture and Data Flow](#architecture-and-data-flow)
- [Technology Stack](#technology-stack)
- [Services](#services)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Kubernetes Deployment with Helm](#kubernetes-deployment-with-helm)
- [Docker Compose](#docker-compose)
- [Configuration and Persistent Data](#configuration-and-persistent-data)
- [Monitoring](#monitoring)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Security](#security)
- [Documentation](#documentation)
- [Current Scope and Project Status](#current-scope-and-project-status)
- [License](#license)

## Overview

The application accepts audio files, stores them, processes transcription jobs asynchronously, and can send the resulting text to a local language model for AI-powered processing.

```text
                         ┌──────────────────┐
                         │     Frontend     │
                         │    React + Vite  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   API Service    │
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
            ┌─────────────────┐      ┌─────────────────┐
            │  File Service   │      │   PostgreSQL    │
            │     FastAPI     │      │ Application Data│
            └────────┬────────┘      └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │      MinIO      │
            │  Object Storage │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │     RabbitMQ    │
            │  Speech Queue   │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Speech Worker  │
            │  Faster-Whisper │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   PostgreSQL    │
            │ Transcriptions  │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │    AI Worker    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │     Ollama      │
            │    Local LLM    │
            └─────────────────┘
```

## Main Features

- Audio upload through the web interface.
- Object storage using MinIO.
- PostgreSQL persistence.
- Asynchronous task processing through RabbitMQ.
- Speech-to-text transcription using Faster-Whisper.
- AI text processing through Ollama running locally.
- React frontend and FastAPI-based services.
- Docker containerization and Docker Compose support.
- Kubernetes deployment with Minikube and Helm.
- Persistent volumes for stateful components.
- Kubernetes health probes.
- Monitoring configuration for Prometheus, Grafana, and Loki.
- Automated backend tests and frontend build validation.
- CI security checks, dependency scanning, Helm validation, Kubernetes manifest validation, and container image scanning.
- Automated deployment to a configured local Minikube environment through a self-hosted GitHub Actions runner.

## Architecture and Data Flow

The main transcription flow is:

1. A user uploads an audio file through the frontend.
2. The API and File Service handle the request.
3. MinIO stores the audio file.
4. A transcription job is placed on RabbitMQ.
5. The Speech Worker consumes the job and processes the audio with Faster-Whisper.
6. The transcription is stored in PostgreSQL.
7. The AI Worker can send text to Ollama for local language-model processing.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | React, Vite, Nginx |
| Backend | Python, FastAPI, SQLAlchemy, Alembic, `uv` |
| Speech processing | Faster-Whisper |
| Asynchronous messaging | RabbitMQ |
| AI processing | Ollama, local language model |
| Database | PostgreSQL |
| Object storage | MinIO |
| Cache / in-memory data | Redis |
| Containers | Docker, Docker Compose, Docker Buildx |
| Orchestration | Kubernetes, Minikube |
| Deployment | Helm |
| Monitoring | Prometheus, Grafana, Loki, Promtail / Grafana Alloy configuration |
| CI/CD | GitHub Actions |
| Security and validation | Gitleaks, OSV-Scanner, Trivy, Kubeconform, Helm lint |

## Services

| Service | Purpose |
|---|---|
| `frontend` | React web interface served through Nginx |
| `api-service` | Main API / gateway |
| `auth-service` | Authentication service |
| `file-service` | File upload and storage management |
| `speech-worker` | Asynchronous audio transcription using Faster-Whisper |
| `ai-worker` | AI text processing through Ollama |
| `postgres` | Persistent relational database |
| `rabbitmq` | Message broker for asynchronous jobs |
| `redis` | In-memory data store |
| `minio` | S3-compatible object storage |
| `ollama` | Local language-model runtime |

## Project Structure

```text
ai-voice-transcriber/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── 01-architecture/
│   │   └── Architecture-Design-Document.md
│   ├── 02-requirements/
│   │   └── System-Requirements-Specification.md
│   └── README.md
├── frontend/
├── infrastructure/
│   ├── compose/
│   ├── docker/
│   ├── helm/
│   │   └── ai-voice-transcriber/
│   └── terraform/
├── monitoring/
├── services/
│   ├── api-service/
│   ├── auth-service/
│   ├── file-service/
│   ├── speech-worker/
│   └── ai-worker/
├── shared/
├── tests/
├── docker-compose.yml
├── start.sh
├── stop.sh
├── Makefile
├── CHANGELOG.md
├── LICENSE
└── README.md
```

This is a high-level overview; individual directories contain additional source files and configuration. The active deployment target is local Kubernetes, not AWS.

## Quick Start

### Prerequisites

Install and configure:

- Docker
- Minikube
- `kubectl`
- Helm
- Git

### Start the application

From the repository root:

```bash
minikube start
./start.sh
```

The startup script is intended to start Minikube if needed, install or upgrade the Helm release, wait for workloads to become ready, and create a port-forward to the frontend.

When startup completes, open:

**http://127.0.0.1:8080**

### Stop the application

```bash
./stop.sh
```

The stop script stops the frontend port-forward and Minikube. Persistent data stored in Kubernetes persistent volumes may remain between runs.

## Kubernetes Deployment with Helm

The primary integrated deployment uses Minikube, Kubernetes, and the Helm chart at:

```text
infrastructure/helm/ai-voice-transcriber/
```

Install or upgrade the release:

```bash
helm upgrade --install ai-voice-transcriber \
  infrastructure/helm/ai-voice-transcriber
```

Validate the chart:

```bash
helm lint infrastructure/helm/ai-voice-transcriber
```

Inspect Kubernetes resources:

```bash
kubectl get pods
kubectl get services
kubectl get pvc
```

The chart configures application and infrastructure workloads, including persistent storage and health probes for supported components.

### Persistent components

Persistent volumes are configured for stateful components such as PostgreSQL, MinIO, Ollama, RabbitMQ, and Redis. Ollama's persistent storage allows downloaded models to survive pod restarts. Actual persistence depends on the Kubernetes storage configuration and whether the relevant volumes are retained.

## Docker Compose

A Docker Compose environment is also provided for local service execution.

Start:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

The Compose configuration includes the application's supporting services and workers. **Minikube + Helm is the primary integrated deployment path** documented for this project.

## Configuration and Persistent Data

Runtime configuration is supplied through environment variables and Kubernetes configuration resources.

Keep credentials and other secrets out of Git. Configure the required local values for items such as:

- PostgreSQL credentials and database connection settings
- RabbitMQ connection settings
- MinIO credentials
- Inter-service configuration
- Ollama endpoint and model settings

Use example configuration files where provided. Do not commit real `.env` files, access tokens, passwords, or private keys.

## Monitoring

The repository contains monitoring configuration based on:

- Prometheus
- Grafana
- Loki
- Promtail / Grafana Alloy

Monitoring-related configuration is stored under `monitoring/`. Grafana dashboards and Loki-related resources are also integrated with the Helm deployment.

This describes the monitoring configuration included in the project; it does not imply that an external hosted monitoring service is used.

## Testing

The repository contains automated tests for backend components, plus frontend tests and build validation in CI.

The CI workflow includes Python test jobs for the API, authentication, file, speech, and AI-worker components. A PostgreSQL service container is provided where required by tests. The frontend job runs its tests and production build.

Relevant source areas include:

```text
services/api-service/
services/auth-service/
services/file-service/
services/speech-worker/
services/ai-worker/
frontend/
```

The exact commands and test selection are defined in the service configuration and `.github/workflows/ci.yml`.

## CI/CD Pipeline

GitHub Actions automates code validation, security checks, container image builds, and deployment to a configured local Kubernetes environment.

Workflow definition: `.github/workflows/ci.yml`.

### Pipeline stages

1. **Secret scanning — Gitleaks**
   - Checks repository changes for accidentally committed secrets.

2. **Backend tests**
   - Runs Python tests for API, authentication, file, speech, and AI-worker components.
   - Uses a PostgreSQL service container for tests that require a database.

3. **Frontend validation**
   - Installs frontend dependencies.
   - Runs frontend tests.
   - Builds production frontend assets.

4. **Dependency vulnerability scanning — OSV-Scanner**
   - Scans project dependencies for known vulnerabilities.

5. **Helm validation**
   - Runs Helm chart linting and template rendering.

6. **Kubernetes manifest validation — Kubeconform**
   - Validates rendered Kubernetes manifests against Kubernetes schemas.

7. **Docker image build and security scan**
   - Builds six images: API Service, Auth Service, File Service, Speech Worker, AI Worker, and Frontend.
   - Scans the built images with Trivy.

8. **Publish images to GitHub Container Registry**
   - On pushes to `main`, the workflow publishes the images to GHCR when the image build and scan jobs succeed.

9. **Local Kubernetes deployment**
   - A deployment job runs on a configured **self-hosted GitHub Actions runner** with access to the local Minikube cluster.
   - Helm performs an install or upgrade and waits for the release resources to become ready.
   - The workflow checks deployment availability and runs smoke checks against the API and authentication health endpoints.
   - If deployment or smoke checks fail, the workflow attempts to roll back to the previous Helm revision. If the release was being installed for the first time, the failed release is removed.

### Pipeline flow

```text
Push / Pull Request
        │
        ▼
Secret scanning + tests + frontend validation
        │
        ▼
Dependency vulnerability scan
        │
        ▼
Helm lint / template + Kubeconform
        │
        ▼
Build six Docker images + Trivy scans
        │
        ├── On push to main: publish images to GHCR
        │
        ▼
Self-hosted runner with Minikube access
        │
        ▼
Helm install / upgrade and readiness checks
        │
        ▼
API and authentication health smoke checks
        │
        ├── Success: deployment job completes
        └── Failure: rollback / cleanup attempt
```

### Deployment runner requirements

The local deployment job depends on a self-hosted GitHub Actions runner configured with the necessary tools and access to the target Minikube cluster. A GitHub-hosted runner cannot automatically access a Minikube cluster running on the developer's local machine.

The deployment workflow therefore depends on the self-hosted runner being online and correctly configured. Other CI checks validate code, manifests, and images independently of the local cluster.

## Security

Security-related CI controls include:

- **Gitleaks** for secret detection.
- **OSV-Scanner** for dependency vulnerability scanning.
- **Trivy** for container image vulnerability scanning.
- **Kubeconform** for Kubernetes manifest validation.

These checks help identify common issues but do not guarantee that an application or its dependencies are free of vulnerabilities. Credentials must be managed outside version control.

## Documentation

The `docs/` directory contains:

- `01-architecture/Architecture-Design-Document.md` — architecture documentation.
- `02-requirements/System-Requirements-Specification.md` — system requirements specification.
- `README.md` — documentation index.

This root README is the main entry point for setup, deployment, CI/CD, and project scope. AWS is outside the current implemented deployment scope.

## Current Scope and Project Status

The project is being finalized as a local DevOps / Kubernetes portfolio project. It includes:

- React frontend and FastAPI-based services.
- Audio storage and asynchronous transcription.
- Faster-Whisper speech recognition.
- Local Ollama integration for AI text processing.
- PostgreSQL, RabbitMQ, Redis, and MinIO.
- Docker and Docker Compose configuration.
- Kubernetes deployment through Minikube and Helm.
- Persistent volumes and Kubernetes health probes.
- Monitoring configuration.
- Automated tests and CI security / validation checks.
- Docker image publishing to GHCR on pushes to `main`.
- Deployment automation to a configured local Minikube cluster through a self-hosted runner.

The current implemented deployment target is local Kubernetes. **AWS EKS, ECR, RDS, and S3 are outside the current deployment scope.**

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
