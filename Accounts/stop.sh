#!/bin/bash

# Account Processing System - Stop Script
# Stops all application components

echo "========================================="
echo "Stopping Account Processing System"
echo "========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to stop a service gracefully
stop_service() {
    local pid_file=$1
    local service_name=$2

    if [ -f $pid_file ]; then
        local pid=$(cat $pid_file)
        echo -n "Stopping $service_name (PID: $pid)..."

        # Check if process is running
        if ps -p $pid > /dev/null 2>&1; then
            # Try graceful shutdown first
            kill $pid 2>/dev/null

            # Wait up to 10 seconds for graceful shutdown
            local count=0
            while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                count=$((count + 1))
            done

            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                echo -n " (force killing)..."
                kill -9 $pid 2>/dev/null
                sleep 1
            fi

            if ! ps -p $pid > /dev/null 2>&1; then
                echo -e " ${GREEN}✓${NC}"
                rm $pid_file
                return 0
            else
                echo -e " ${RED}✗${NC}"
                return 1
            fi
        else
            echo -e " ${YELLOW}not running${NC}"
            rm $pid_file
            return 0
        fi
    else
        echo -e "${YELLOW}$service_name:${NC} PID file not found (not started or already stopped)"
        return 0
    fi
}

# Function to kill processes on a specific port
kill_port() {
    local port=$1
    local service_name=$2

    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -n "Killing processes on port $port ($service_name)..."
        echo $pids | xargs kill -9 2>/dev/null
        echo -e " ${GREEN}✓${NC}"
        return 0
    fi
    return 1
}

# Stop services
echo "Stopping services..."
echo ""

# Stop API Server
stop_service ".api.pid" "API Server"

# Stop React UI
stop_service ".ui.pid" "React UI"

# Stop start script tracker
if [ -f ".start.pid" ]; then
    rm .start.pid
fi

# Fallback: kill by port if PID files didn't work
echo ""
echo "Checking ports for any remaining processes..."
kill_port 6600 "API Server" || echo "  Port 6600: already free"
kill_port 6601 "React UI" || echo "  Port 6601: already free"

# Clean up log files if requested
echo ""
read -p "Clear log files? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "logs" ]; then
        rm -f logs/*.log
        echo -e "${GREEN}Log files cleared${NC}"
    fi
fi

echo ""
echo "========================================="
echo "Account Processing System Stopped"
echo "========================================="
echo ""
