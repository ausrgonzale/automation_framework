#!/bin/bash

CONTAINER_NAME="${REDIS_CONTAINER_NAME:-redis}"
PORT="${REDIS_PORT:-6379}"

echo "Checking Redis status..."

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    echo
    echo "Docker container status:"
    docker ps --filter "name=${CONTAINER_NAME}"
else
    echo "Docker daemon unavailable; skipping Docker container status."
fi

echo
echo "Endpoint status (localhost:${PORT}):"

if command -v nc >/dev/null 2>&1; then
    if nc -z localhost "$PORT" >/dev/null 2>&1; then
        echo "Redis endpoint is reachable"
    else
        echo "Redis endpoint is NOT reachable"
    fi
else
    if (echo >"/dev/tcp/localhost/$PORT") >/dev/null 2>&1; then
        echo "Redis endpoint is reachable"
    else
        echo "Redis endpoint is NOT reachable"
    fi
fi
