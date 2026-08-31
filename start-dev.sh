#!/bin/bash

set -e

echo "Starting Minikube..."
minikube start

echo "Applying Helm chart..."
helm upgrade --install ai-voice-transcriber \
  infrastructure/helm/ai-voice-transcriber \

echo "Waiting for File Service..."
kubectl wait --for=condition=available \
  deployment/file-service \
  --timeout=120s

echo "Stopping old port-forward..."

pkill -f "kubectl port-forward svc/file-service 8081:8000" 2>/dev/null || true
pkill -f "kubectl port-forward svc/api-service 8081:8000" 2>/dev/null || true

echo "Starting port-forward..."

kubectl port-forward svc/file-service 8081:8000 \
  >/tmp/ai-voice-transcriber-port-forward.log 2>&1 &

PORT_FORWARD_PID=$!

sleep 2

echo
echo "AI Voice Transcriber is running:"
echo "http://127.0.0.1:8081/docs"
echo
echo "Port-forward PID: $PORT_FORWARD_PID"
