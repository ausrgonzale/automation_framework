#!/bin/bash

CONTAINER_NAME="redis"

echo "Stopping Redis..."

docker stop ${CONTAINER_NAME} 2>/dev/null || true

echo "Redis stopped."