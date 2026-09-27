#!/bin/bash

set -e

PID_FILE=".frontend-port-forward.pid"

echo "=== Stopping AI Voice Transcriber ==="

echo "[1/2] Stopping frontend port-forward..."

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "Port-forward stopped (PID: $PID)"
    else
        echo "Port-forward is not running."
    fi

    rm -f "$PID_FILE"
else
    echo "No port-forward PID file found."
fi

echo "[2/2] Stopping Minikube..."
minikube stop

echo
echo "=== AI Voice Transcriber is stopped ==="
