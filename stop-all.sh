#!/bin/bash

# Master Stop Script
# Stops all system components: Accounts API, UI, and RAG System

echo "================================================================================"
echo "🛑 Stopping Complete System - Account Processing + RAG Assistant"
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

# Check what's running
print_section "Checking Running Services"

RUNNING_COUNT=0
if check_port 6600; then
    echo -e "${YELLOW}• Accounts API running on port 6600${NC}"
    RUNNING_COUNT=$((RUNNING_COUNT + 1))
fi
if check_port 6601; then
    echo -e "${YELLOW}• Accounts UI running on port 6601${NC}"
    RUNNING_COUNT=$((RUNNING_COUNT + 1))
fi
if check_port 6603; then
    echo -e "${YELLOW}• RAG API running on port 6603${NC}"
    RUNNING_COUNT=$((RUNNING_COUNT + 1))
fi
if check_port 6604; then
    echo -e "${YELLOW}• RAG UI running on port 6604${NC}"
    RUNNING_COUNT=$((RUNNING_COUNT + 1))
fi

if [ $RUNNING_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ No services currently running${NC}"
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}All systems already stopped${NC}"
    echo "================================================================================"
    echo ""
    exit 0
fi

echo ""
echo -e "${CYAN}Found $RUNNING_COUNT running service(s)${NC}"

# Stop RAG System first
print_section "1️⃣  Stopping RAG Documentation Assistant"

cd "$SCRIPT_DIR/RAG"
if [ -f "stop_rag.sh" ]; then
    echo -e "${CYAN}Running RAG stop script...${NC}"
    ./stop_rag.sh
    echo -e "${GREEN}✓ RAG System stop script completed${NC}"
else
    echo -e "${YELLOW}⚠ RAG stop_rag.sh not found, checking ports...${NC}"
fi

# Force kill RAG processes if still running
if check_port 6603; then
    echo -n "  Force stopping RAG API (port 6603)..."
    lsof -ti:6603 | xargs kill -9 2>/dev/null
    echo -e " ${GREEN}✓${NC}"
fi
if check_port 6604; then
    echo -n "  Force stopping RAG UI (port 6604)..."
    lsof -ti:6604 | xargs kill -9 2>/dev/null
    echo -e " ${GREEN}✓${NC}"
fi

cd "$SCRIPT_DIR"

# Stop Accounts System
print_section "2️⃣  Stopping Account Processing System"

cd "$SCRIPT_DIR/Accounts"
if [ -f "stop.sh" ]; then
    echo -e "${CYAN}Running Accounts stop script...${NC}"
    # Provide "n" to skip the log clearing prompt
    echo "n" | ./stop.sh
    echo -e "${GREEN}✓ Accounts System stop script completed${NC}"
else
    echo -e "${YELLOW}⚠ Accounts stop.sh not found, checking ports...${NC}"
fi

# Force kill Accounts processes if still running
if check_port 6600; then
    echo -n "  Force stopping Accounts API (port 6600)..."
    lsof -ti:6600 | xargs kill -9 2>/dev/null
    echo -e " ${GREEN}✓${NC}"
fi
if check_port 6601; then
    echo -n "  Force stopping Accounts UI (port 6601)..."
    lsof -ti:6601 | xargs kill -9 2>/dev/null
    echo -e " ${GREEN}✓${NC}"
fi

cd "$SCRIPT_DIR"

# Final verification
print_section "Verification"

echo "Checking if all services stopped..."
echo ""

ALL_STOPPED=1
if check_port 6600; then
    echo -e "${RED}✗ Port 6600 still in use${NC}"
    ALL_STOPPED=0
else
    echo -e "${GREEN}✓ Port 6600 free (Accounts API)${NC}"
fi

if check_port 6601; then
    echo -e "${RED}✗ Port 6601 still in use${NC}"
    ALL_STOPPED=0
else
    echo -e "${GREEN}✓ Port 6601 free (Accounts UI)${NC}"
fi

if check_port 6603; then
    echo -e "${RED}✗ Port 6603 still in use${NC}"
    ALL_STOPPED=0
else
    echo -e "${GREEN}✓ Port 6603 free (RAG API)${NC}"
fi

if check_port 6604; then
    echo -e "${RED}✗ Port 6604 still in use${NC}"
    ALL_STOPPED=0
else
    echo -e "${GREEN}✓ Port 6604 free (RAG UI)${NC}"
fi

echo ""

if [ $ALL_STOPPED -eq 1 ]; then
    echo "================================================================================"
    echo -e "${GREEN}✅ All systems stopped successfully!${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}To restart the system, run:${NC}"
    echo -e "  ${YELLOW}./start-all.sh${NC}"
    echo ""
else
    echo "================================================================================"
    echo -e "${YELLOW}⚠ Some services may still be running${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}Try manually killing processes:${NC}"
    echo -e "  ${YELLOW}lsof -ti:6600,6601,6603,6604 | xargs kill -9${NC}"
    echo ""
    exit 1
fi
