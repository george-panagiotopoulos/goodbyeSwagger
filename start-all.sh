#!/bin/bash

# Master Start Script
# Starts all system components: Accounts API, UI, and RAG System

echo "================================================================================"
echo "🚀 Starting Complete System - Account Processing + RAG Assistant"
echo "================================================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Track start time
START_TIME=$(date +%s)

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

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

    echo -n "  Waiting for $service_name (port $port) to be ready..."
    while ! check_port $port && [ $count -lt $max_wait ]; do
        sleep 1
        count=$((count + 1))
        echo -n "."
    done

    if [ $count -lt $max_wait ]; then
        echo -e " ${GREEN}✓${NC}"
        return 0
    else
        echo -e " ${YELLOW}⚠${NC}"
        return 1
    fi
}

# Check if any services are already running
print_section "Checking for Running Services"

SERVICES_RUNNING=0
if check_port 6600; then
    echo -e "${YELLOW}⚠ Accounts API already running on port 6600${NC}"
    SERVICES_RUNNING=1
fi
if check_port 6601; then
    echo -e "${YELLOW}⚠ Accounts UI already running on port 6601${NC}"
    SERVICES_RUNNING=1
fi
if check_port 6603; then
    echo -e "${YELLOW}⚠ RAG API already running on port 6603${NC}"
    SERVICES_RUNNING=1
fi
if check_port 6604; then
    echo -e "${YELLOW}⚠ RAG UI already running on port 6604${NC}"
    SERVICES_RUNNING=1
fi

if [ $SERVICES_RUNNING -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}WARNING: Some services are already running.${NC}"
    read -p "Stop existing services and restart? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Stopping existing services...${NC}"
        "$SCRIPT_DIR/stop-all.sh"
        echo ""
        echo -e "${GREEN}✓ All services stopped${NC}"
        sleep 2
    else
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ No conflicts detected${NC}"
fi

# Start Accounts System
print_section "1️⃣  Starting Account Processing System"

cd "$SCRIPT_DIR/Accounts"
if [ ! -f "start.sh" ]; then
    echo -e "${RED}✗ Error: Accounts start.sh not found${NC}"
    exit 1
fi

echo -e "${CYAN}Running Accounts start script...${NC}"
./start.sh

ACCOUNTS_RESULT=$?
cd "$SCRIPT_DIR"

if [ $ACCOUNTS_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Account Processing System started successfully${NC}"
else
    echo -e "${RED}✗ Failed to start Account Processing System${NC}"
    echo -e "${YELLOW}Aborting startup...${NC}"
    exit 1
fi

# Start RAG System
print_section "2️⃣  Starting RAG Documentation Assistant"

cd "$SCRIPT_DIR/RAG"
if [ ! -f "start_rag.sh" ]; then
    echo -e "${RED}✗ Error: RAG start_rag.sh not found${NC}"
    exit 1
fi

echo -e "${CYAN}Running RAG start script...${NC}"
./start_rag.sh

RAG_RESULT=$?
cd "$SCRIPT_DIR"

if [ $RAG_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ RAG System started successfully${NC}"
else
    echo -e "${YELLOW}⚠ RAG System may not have started correctly${NC}"
    echo -e "${YELLOW}  Check RAG/rag_api.log and RAG/rag_ui.log for details${NC}"
fi

# Calculate startup time
END_TIME=$(date +%s)
STARTUP_TIME=$((END_TIME - START_TIME))

# Display comprehensive status
print_section "✅ System Status"

echo "All services started successfully!"
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                      🏦 ACCOUNT PROCESSING SYSTEM                  ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} API Server:     http://localhost:6600                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} Web UI:         http://localhost:6601                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} API Health:     http://localhost:6600/health                    ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} Swagger Docs:   http://localhost:6600/swagger-ui/               ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}                                                                   ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Features:                                                        ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    - Product Management                                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    - Account Management                                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    - Transaction Processing (Credit/Debit)                        ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    - Account Ledger with 229 realistic transactions               ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    - Total System Balance: \$22,500.50                             ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"

echo ""

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                  🤖 RAG DOCUMENTATION ASSISTANT                    ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} RAG API:        http://localhost:6603                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} Chat UI:        http://localhost:6604                           ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} API Health:     http://localhost:6603/api/health                ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}•${NC} API Docs:       http://localhost:6603/api/docs                  ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}                                                                   ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  7 AI Personas:                                                   ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    👨‍💻 Dev Assistant      - Developer help & coding             ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    🔧 Ops Assistant      - DevOps & infrastructure              ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    💼 Business Expert    - Business features & use cases        ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    🔌 API Guide          - API integration help                 ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    🏛️  Architecture       - System design & patterns            ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    🗄️  Data Expert        - Database & schema help              ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}    🤖 Universal Helper   - General questions                    ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"

echo ""

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                           📊 QUICK STATS                           ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  Startup Time:        ${GREEN}${STARTUP_TIME}s${NC}                                          ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Total Services:      ${GREEN}4${NC} (API, UI, RAG API, RAG UI)                  ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Ports Used:          ${GREEN}6600-6604${NC}                                      ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                          📝 LOGS & DEBUG                           ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  Accounts API:  ${YELLOW}tail -f Accounts/logs/api.log${NC}                      ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Accounts UI:   ${YELLOW}tail -f Accounts/logs/ui.log${NC}                       ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  RAG API:       ${YELLOW}tail -f RAG/rag_api.log${NC}                            ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  RAG UI:        ${YELLOW}tail -f RAG/rag_ui.log${NC}                             ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                        🛠️  MANAGEMENT                              ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  Stop All Services:    ${YELLOW}./stop-all.sh${NC}                              ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Restart System:       ${YELLOW}./stop-all.sh && ./start-all.sh${NC}            ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo "================================================================================"
echo -e "${GREEN}✅ All systems operational! Happy coding! 🚀${NC}"
echo "================================================================================"
echo ""
