#!/bin/bash

set -u

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Ensure PYTHONPATH includes project root for scripts and agents.
if [ -z "${PYTHONPATH:-}" ]; then
    export PYTHONPATH="$PROJECT_ROOT"
    echo "[healthcheck] PYTHONPATH set to $PYTHONPATH"
else
    echo "[healthcheck] PYTHONPATH already set: $PYTHONPATH"
fi

# -----------------------------------------------------------------------------
# Runtime settings (non-secret)
# -----------------------------------------------------------------------------

ENVIRONMENT="${ENVIRONMENT:-development}"
DOCKER_START_TIMEOUT="${DOCKER_START_TIMEOUT:-60}"

REDIS_CONTAINER_NAME="${REDIS_CONTAINER_NAME:-redis}"
REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_START_TIMEOUT="${REDIS_START_TIMEOUT:-30}"
REDIS_REQUIRED="${REDIS_REQUIRED:-false}"

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_START_TIMEOUT="${OLLAMA_START_TIMEOUT:-45}"

AUTO_START_SERVICES="${AUTO_START_SERVICES:-true}"
FAIL_FAST="${FAIL_FAST:-true}"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

log() {
    echo "[healthcheck] $1"
}

warn() {
    echo "[healthcheck][warn] $1"
}

err() {
    echo "[healthcheck][error] $1"
}

is_true() {
    [ "$(echo "$1" | tr '[:upper:]' '[:lower:]')" = "true" ]
}

is_port_open() {
    if command -v nc >/dev/null 2>&1; then
        nc -z "$REDIS_HOST" "$REDIS_PORT" >/dev/null 2>&1
        return $?
    fi

    (echo >"/dev/tcp/$REDIS_HOST/$REDIS_PORT") >/dev/null 2>&1
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

wait_for_ollama() {
    local retries="$1"

    for ((i=1; i<=retries; i++)); do
        if curl -s "$OLLAMA_HOST" >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done

    return 1
}

ensure_redis() {
    log "Checking Redis on $REDIS_HOST:$REDIS_PORT"

    if wait_for_redis 1; then
        log "Redis is available"
        return 0
    fi

    warn "Redis is not reachable"

    if is_true "$AUTO_START_SERVICES"; then
        log "Attempting to start Redis via scripts/start_redis.sh"
        if bash "$PROJECT_ROOT/scripts/start_redis.sh"; then
            if wait_for_redis "$REDIS_START_TIMEOUT"; then
                log "Redis started successfully"
                return 0
            fi
            err "Redis start command ran, but Redis is still not reachable"
            return 1
        fi

        err "Failed to run scripts/start_redis.sh"
        return 1
    fi

    err "AUTO_START_SERVICES=false and Redis is down"
    return 1
}

ensure_ollama() {
    log "Checking Ollama API at $OLLAMA_HOST"

    if wait_for_ollama 1; then
        log "Ollama is available"
        return 0
    fi

    warn "Ollama is not reachable"

    if is_true "$AUTO_START_SERVICES"; then
        log "Attempting to start Ollama via scripts/start_ollama.sh"
        if bash "$PROJECT_ROOT/scripts/start_ollama.sh"; then
            if wait_for_ollama "$OLLAMA_START_TIMEOUT"; then
                log "Ollama started successfully"
                return 0
            fi
            err "Ollama start command ran, but API is still not reachable"
            return 1
        fi

        err "Failed to run scripts/start_ollama.sh"
        return 1
    fi

    err "AUTO_START_SERVICES=false and Ollama is down"
    return 1
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

log "Environment: $ENVIRONMENT"

redis_ok=true
ollama_ok=true

if ! ensure_redis; then
    if is_true "$REDIS_REQUIRED"; then
        redis_ok=false
    else
        warn "Redis unavailable, continuing because REDIS_REQUIRED=false"
    fi
fi

if ! ensure_ollama; then
    ollama_ok=false
fi

if [ "$redis_ok" = true ] && [ "$ollama_ok" = true ]; then
    log "Environment health check passed"
    exit 0
fi

err "Environment health check failed (redis_ok=$redis_ok, ollama_ok=$ollama_ok)"

if is_true "$FAIL_FAST"; then
    exit 1
fi

exit 0
