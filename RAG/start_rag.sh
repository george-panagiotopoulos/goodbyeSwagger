#!/bin/bash

# Start RAG System
# Starts the RAG backend API and frontend UI

set -e

echo "========================================"
echo "Starting RAG System"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "ERROR: backend/.env file not found!"
    echo "Please copy backend/.env.example to backend/.env and configure it"
    exit 1
fi

# Setup Python environment if needed
if [ ! -d "backend/.venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
fi

# Start backend
echo ""
echo "Starting RAG API (port 6603)..."
cd backend
source .venv/bin/activate

# Start in background
nohup python3 -m src.main > ../rag_api.log 2>&1 &
API_PID=$!
echo $API_PID > ../rag_api.pid
echo "  ✓ RAG API started (PID: $API_PID)"
echo "  Log: $SCRIPT_DIR/rag_api.log"

cd ..

# Start frontend (simple HTTP server)
echo ""
echo "Starting RAG UI (port 6604)..."
if [ -f "frontend/index.html" ]; then
    cd frontend
    nohup python3 -m http.server 6604 > ../rag_ui.log 2>&1 &
    UI_PID=$!
    echo $UI_PID > ../rag_ui.pid
    echo "  ✓ RAG UI started (PID: $UI_PID)"
    echo "  Log: $SCRIPT_DIR/rag_ui.log"
    cd ..
else
    echo "  ⚠ Frontend not found, skipping UI server"
fi

echo ""
echo "========================================"
echo "RAG System Started Successfully!"
echo "========================================"
echo ""
echo "RAG API: http://localhost:6603"
echo "API Docs: http://localhost:6603/api/docs"
echo "RAG UI: http://localhost:6604"
echo ""
echo "To stop: ./stop_rag.sh"
echo "========================================"
