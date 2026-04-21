#!/bin/bash

set -e

echo "========================================"
echo "Ollama Startup Script"
echo "========================================"

# ----------------------------------------
# Default values
# ----------------------------------------

DEFAULT_NUM_PARALLEL=2
DEFAULT_MAX_MODELS=1
DEFAULT_KEEP_ALIVE="5m"
DEFAULT_NUM_THREADS=4
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_START_TIMEOUT="${OLLAMA_START_TIMEOUT:-45}"

# ----------------------------------------
# Helper function
# ----------------------------------------

set_if_missing () {
    VAR_NAME=$1
    DEFAULT_VALUE=$2

    CURRENT_VALUE=$(printenv $VAR_NAME)

    if [ -z "$CURRENT_VALUE" ]; then
        export $VAR_NAME=$DEFAULT_VALUE
        echo "$VAR_NAME not set — using default: $DEFAULT_VALUE"
    else
        echo "$VAR_NAME already set to: $CURRENT_VALUE"
    fi
}

wait_for_ollama() {
    local retries="$1"

    for ((i=1; i<=retries; i++)); do
        if curl -s "$OLLAMA_HOST" > /dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done

    return 1
}

start_ollama_service() {
    if command -v brew >/dev/null 2>&1 && brew list --formula | grep -Eq '^ollama$'; then
        echo "Starting Ollama via Homebrew service..."
        brew services start ollama >/dev/null
        return 0
    fi

    if command -v ollama >/dev/null 2>&1; then
        echo "Starting Ollama via direct process..."
        nohup ollama serve >/tmp/ollama.log 2>&1 &
        return 0
    fi

    return 1
}

# ----------------------------------------
# Ensure environment variables exist
# ----------------------------------------

echo
echo "Checking Ollama environment variables..."
echo

set_if_missing "OLLAMA_NUM_PARALLEL" "$DEFAULT_NUM_PARALLEL"
set_if_missing "OLLAMA_MAX_LOADED_MODELS" "$DEFAULT_MAX_MODELS"
set_if_missing "OLLAMA_KEEP_ALIVE" "$DEFAULT_KEEP_ALIVE"
set_if_missing "OLLAMA_NUM_THREADS" "$DEFAULT_NUM_THREADS"

echo
echo "Active configuration:"
echo

env | grep OLLAMA | sort

# ----------------------------------------
# Check if Ollama is already running
# ----------------------------------------

echo
echo "Checking if Ollama is running..."

if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama is already running"
else
    if ! start_ollama_service; then
        echo "Unable to start Ollama automatically."
        echo "Install Ollama or start it manually, then rerun healthcheck."
        exit 1
    fi
fi

# ----------------------------------------
# Wait for API readiness
# ----------------------------------------

echo
echo "Waiting for Ollama API..."

if ! wait_for_ollama "$OLLAMA_START_TIMEOUT"; then
    echo "Ollama start command completed, but API is still not reachable at $OLLAMA_HOST"
    exit 1
fi

echo
echo "Ollama is ready"
echo "========================================"