#!/bin/bash

echo "========================================"
echo "Ollama Status"
echo "========================================"

echo
echo "Service status:"
brew services list | grep ollama

echo
echo "Process tree:"
ps -o pid,ppid,user,command -ax | grep '[o]llama'

echo
echo "Environment variables:"
env | grep OLLAMA | sort

echo
echo "API check:"

if curl -s http://localhost:11434 > /dev/null; then
    echo "Ollama API is responding"
else
    echo "Ollama API is NOT responding"
fi

echo "========================================"