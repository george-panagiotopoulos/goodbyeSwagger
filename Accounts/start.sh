#!/bin/bash

# Account Processing System - Start Script
# Starts all application components

echo "========================================="
echo "Starting Account Processing System"
echo "========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    lsof -ti:$1 >/dev/null 2>&1
}

# Function to wait for a service to be ready
wait_for_service() {
    local port=$1
    local service_name=$2
    local max_wait=30
    local count=0

    echo -n "Waiting for $service_name to be ready..."
    while ! check_port $port && [ $count -lt $max_wait ]; do
        sleep 1
        count=$((count + 1))
        echo -n "."
    done

    if [ $count -lt $max_wait ]; then
        echo -e " ${GREEN}✓${NC}"
        return 0
    else
        echo -e " ${RED}✗${NC}"
        return 1
    fi
}

# Check if services are already running
echo "Checking for running services..."
if check_port 6600; then
    echo -e "${YELLOW}WARNING:${NC} API server already running on port 6600"
    read -p "Stop existing services and restart? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./stop.sh
        sleep 2
    else
        echo "Aborted."
        exit 1
    fi
fi

# Store PIDs for cleanup
echo $$ > .start.pid

# Step 1: Start API Server (Port 6600)
echo ""
echo "1. Starting API Server (Port 6600)..."
cd API
if [ ! -f .env ]; then
    echo -e "${YELLOW}WARNING:${NC} .env file not found, copying from .env.example"
    cp .env.example .env
fi

# Start API in background
cargo run --release > ../logs/api.log 2>&1 &
API_PID=$!
echo $API_PID > ../.api.pid
echo -e "   API PID: ${GREEN}$API_PID${NC}"

# Wait for API to be ready
cd ..
if wait_for_service 6600 "API Server"; then
    echo -e "   ${GREEN}API Server started successfully${NC}"
    echo "   URL: http://localhost:6600"
    echo "   Health: http://localhost:6600/health"
    echo "   Logs: logs/api.log"
else
    echo -e "   ${RED}Failed to start API Server${NC}"
    echo "   Check logs/api.log for details"
    exit 1
fi

# Step 2: Start React UI (Port 6601)
echo ""
echo "2. Starting React UI (Port 6601)..."
if [ -d "UI" ]; then
    cd UI
    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install > ../logs/ui-install.log 2>&1
    fi

    if [ ! -f .env ]; then
        echo -e "${YELLOW}WARNING:${NC} .env file not found, copying from .env.example"
        cp .env.example .env
    fi

    # Start UI in background
    npm run dev > ../logs/ui.log 2>&1 &
    UI_PID=$!
    echo $UI_PID > ../.ui.pid
    echo -e "   UI PID: ${GREEN}$UI_PID${NC}"

    cd ..
    if wait_for_service 6601 "React UI"; then
        echo -e "   ${GREEN}React UI started successfully${NC}"
        echo "   URL: http://localhost:6601"
        echo "   Logs: logs/ui.log"
    else
        echo -e "   ${YELLOW}React UI not yet ready (still starting...)${NC}"
        echo "   Logs: logs/ui.log"
    fi
else
    echo -e "   ${YELLOW}UI folder not found - skipping${NC}"
fi

# Summary
echo ""
echo "========================================="
echo "Account Processing System Started"
echo "========================================="
echo ""
echo "Running Services:"
echo "  • API Server:  http://localhost:6600 (PID: $API_PID)"
if [ -f .ui.pid ]; then
    echo "  • React UI:    http://localhost:6601 (PID: $(cat .ui.pid))"
fi
echo ""
echo "Logs:"
echo "  • API:  tail -f logs/api.log"
if [ -f .ui.pid ]; then
    echo "  • UI:   tail -f logs/ui.log"
fi
echo ""
echo "To stop all services: ./stop.sh"
echo ""
