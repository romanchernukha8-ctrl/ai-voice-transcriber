#!/bin/bash

set -e

PID_FILE=".frontend-port-forward.pid"
LOG_FILE=".frontend-port-forward.log"

echo "=== Starting AI Voice Transcriber ==="

echo "[1/4] Starting Minikube..."
minikube start

echo "[2/4] Applying Helm chart..."
helm upgrade --install ai-voice-transcriber \
  infrastructure/helm/ai-voice-transcriber

echo "[3/4] Waiting for pods..."
kubectl wait --for=condition=Ready pod \
  --all \
  --timeout=180s

echo "[4/4] Starting frontend access..."

kubectl port-forward service/frontend 8080:80 \
  > "$LOG_FILE" 2>&1 &

echo $! > "$PID_FILE"

sleep 2

echo
echo "Frontend:"
echo "http://127.0.0.1:8080"

echo
echo "Port-forward PID: $(cat "$PID_FILE")"

echo
echo "=== AI Voice Transcriber is running ==="
