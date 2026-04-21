#!/bin/bash

echo "Stopping Ollama..."

if pgrep -f "ollama serve" > /dev/null; then
    brew services stop ollama
    echo "Ollama stopped"
else
    echo "Ollama is not running"
fi