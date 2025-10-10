#!/bin/bash

# Stop RAG System
# Stops the RAG backend API and frontend UI

echo "========================================"
echo "Stopping RAG System"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Stop API
if [ -f "rag_api.pid" ]; then
    API_PID=$(cat rag_api.pid)
    echo "Stopping RAG API (PID: $API_PID)..."
    kill $API_PID 2>/dev/null || echo "  Process already stopped"
    rm rag_api.pid
    echo "  ✓ RAG API stopped"
else
    echo "  ⚠ No API PID file found"
fi

# Stop UI
if [ -f "rag_ui.pid" ]; then
    UI_PID=$(cat rag_ui.pid)
    echo "Stopping RAG UI (PID: $UI_PID)..."
    kill $UI_PID 2>/dev/null || echo "  Process already stopped"
    rm rag_ui.pid
    echo "  ✓ RAG UI stopped"
else
    echo "  ⚠ No UI PID file found"
fi

echo ""
echo "========================================"
echo "RAG System Stopped"
echo "========================================"
