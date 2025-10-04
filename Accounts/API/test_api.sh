#!/bin/bash

# Start API in background
cargo run &
API_PID=$!

# Wait for API to start
sleep 3

echo "=== Testing API Endpoints ==="
echo ""

echo "1. Health Check:"
curl -s http://localhost:6600/health | jq .
echo ""

echo "2. List Products:"
curl -s http://localhost:6600/api/products | jq '.success, (.data | length)'
echo ""

echo "3. List Customers:"
curl -s http://localhost:6600/api/customers | jq '.success, (.data | length)'
echo ""

# Kill API
kill $API_PID
wait $API_PID 2>/dev/null

echo "=== Test Complete ==="
