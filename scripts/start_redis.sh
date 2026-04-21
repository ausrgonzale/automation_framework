#!/bin/bash

set -e

CONTAINER_NAME="${REDIS_CONTAINER_NAME:-redis}"
PORT="${REDIS_PORT:-6379}"
IMAGE="${REDIS_IMAGE:-redis:7}"
START_TIMEOUT="${REDIS_START_TIMEOUT:-30}"

is_port_open() {
    if command -v nc >/dev/null 2>&1; then
        nc -z localhost "$PORT" >/dev/null 2>&1
        return $?
    fi

    (echo >"/dev/tcp/localhost/$PORT") >/dev/null 2>&1
}

wait_for_redis() {
    local retries="$1"

    for ((i=1; i<=retries; i++)); do
        if is_port_open; then
            return 0
        fi
        sleep 1
    done

    return 1
}

docker_available() {
    command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1
}

start_with_docker() {
    echo "Attempting Redis startup via Docker..."

    if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
        echo "Redis container exists."

        if docker ps --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
            echo "Redis container is already running."
            return 0
        fi

        echo "Starting existing Redis container..."
        docker start "$CONTAINER_NAME" >/dev/null
        return 0
    fi

    echo "Creating and starting Redis container..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$PORT:$PORT" \
        "$IMAGE" >/dev/null
}

start_with_brew() {
    if ! command -v brew >/dev/null 2>&1; then
        return 1
    fi

    if ! brew list --formula | grep -Eq '^redis$'; then
        return 1
    fi

    echo "Attempting Redis startup via Homebrew service..."
    brew services start redis >/dev/null
    return 0
}

start_with_redis_server() {
    if ! command -v redis-server >/dev/null 2>&1; then
        return 1
    fi

    echo "Attempting Redis startup via local redis-server..."
    redis-server --port "$PORT" --daemonize yes >/dev/null
    return 0
}

echo "Starting Redis dependency..."

if is_port_open; then
    echo "Redis is already reachable on localhost:$PORT"
    exit 0
fi

if docker_available; then
    start_with_docker
elif start_with_brew; then
    :
elif start_with_redis_server; then
    :
else
    echo "Unable to start Redis automatically."
    echo "Tried: Docker, Homebrew service, redis-server binary."
    echo "Please start Redis manually on localhost:$PORT."
    exit 1
fi

if wait_for_redis "$START_TIMEOUT"; then
    echo "Redis is ready on localhost:$PORT"
    exit 0
fi

echo "Redis startup command completed, but Redis is still not reachable."
exit 1
