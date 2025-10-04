#!/bin/bash

# API Manual Testing Script
# Tests all implemented endpoints with curl

API_URL="http://localhost:6600"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local expected_status=$5

    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}TEST:${NC} $description"
    echo -e "${BLUE}→${NC} $method $endpoint"

    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$ d')

    if [ "$http_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Status: $http_code)"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (Expected: $expected_status, Got: $http_code)"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo "========================================="
echo "Account Processing API - Manual Testing"
echo "========================================="
echo ""
echo "Testing API at: $API_URL"
echo ""

# Test 1: Health Check
test_endpoint "GET" "/health" "Health check endpoint" "" "200"

# Test 2: List all products
test_endpoint "GET" "/api/products" "List all products" "" "200"

# Test 3: List active products
test_endpoint "GET" "/api/products/active" "List active products only" "" "200"

# Test 4: Get specific product
test_endpoint "GET" "/api/products/PROD-f158cbba-db1d-4a05-af58-b7718193d368" "Get product by ID" "" "200"

# Test 5: Get non-existent product
test_endpoint "GET" "/api/products/NONEXISTENT" "Get non-existent product" "" "404"

# Test 6: Create new product (use timestamp for unique name and code)
TIMESTAMP=$(date +%s)
NEW_PRODUCT=$(cat <<EOF
{
  "product_name": "Test Product ${TIMESTAMP}",
  "product_code": "TST-SAV-${TIMESTAMP}",
  "description": "Test product created via API",
  "currency": "USD",
  "interest_rate": "0.035",
  "minimum_balance_for_interest": "500.00",
  "monthly_maintenance_fee": "2.50",
  "transaction_fee": "1.00"
}
EOF
)
test_endpoint "POST" "/api/products" "Create new product" "$NEW_PRODUCT" "201"

# Save product ID for later use
CREATED_PRODUCT_ID=$(echo "$body" | jq -r '.data.product_id')

# Test 7: List all customers
test_endpoint "GET" "/api/customers" "List all customers" "" "200"

# Test 8: Get specific customer
test_endpoint "GET" "/api/customers/CUST-003" "Get customer by ID" "" "200"

# Test 9: Create new customer (use timestamp for unique external ID)
NEW_CUSTOMER=$(cat <<EOF
{
  "customer_name": "Test Customer",
  "customer_type": "Individual",
  "external_customer_id": "EXT-TEST-${TIMESTAMP}",
  "email": "test${TIMESTAMP}@example.com",
  "phone": "+1-555-0100"
}
EOF
)
test_endpoint "POST" "/api/customers" "Create new customer" "$NEW_CUSTOMER" "201"

# Save customer ID for later use
CREATED_CUSTOMER_ID=$(echo "$body" | jq -r '.data.customer_id')

# Test 10: List all accounts
test_endpoint "GET" "/api/accounts" "List all accounts" "" "200"

# Test 11: Get specific account
test_endpoint "GET" "/api/accounts/ACC-2025100406" "Get account by ID" "" "200"

# Test 12: Create new account (use timestamp for unique account number)
NEW_ACCOUNT=$(cat <<EOF
{
  "account_number": "TEST-ACC-${TIMESTAMP}",
  "customer_id": "${CREATED_CUSTOMER_ID}",
  "product_id": "${CREATED_PRODUCT_ID}",
  "currency": "USD",
  "opening_balance": "1000.00"
}
EOF
)
test_endpoint "POST" "/api/accounts" "Create new account" "$NEW_ACCOUNT" "201"

# Save account ID for later use
CREATED_ACCOUNT_ID=$(echo "$body" | jq -r '.data.account_id')

# Test 13: Get account transactions (should have opening transaction)
test_endpoint "GET" "/api/accounts/$CREATED_ACCOUNT_ID/transactions" "Get account transactions" "" "200"

# Test 14: Credit account (deposit)
CREDIT_REQUEST='{
  "amount": "500.00",
  "description": "Test deposit",
  "reference": "TEST-DEP-001"
}'
test_endpoint "POST" "/api/accounts/$CREATED_ACCOUNT_ID/credit" "Credit account (deposit)" "$CREDIT_REQUEST" "200"

# Test 15: Debit account (withdrawal)
DEBIT_REQUEST='{
  "amount": "250.00",
  "description": "Test withdrawal",
  "reference": "TEST-WD-001"
}'
test_endpoint "POST" "/api/accounts/$CREATED_ACCOUNT_ID/debit" "Debit account (withdrawal)" "$DEBIT_REQUEST" "200"

# Test 16: Get transactions again (should have 3 transactions now)
test_endpoint "GET" "/api/accounts/$CREATED_ACCOUNT_ID/transactions" "Get updated transactions" "" "200"

# Test 17: Attempt overdraft (should fail)
OVERDRAFT_REQUEST='{
  "amount": "10000.00",
  "description": "Test overdraft attempt",
  "reference": "TEST-OD-001"
}'
test_endpoint "POST" "/api/accounts/$CREATED_ACCOUNT_ID/debit" "Attempt overdraft (should fail)" "$OVERDRAFT_REQUEST" "400"

# Test 18: Create account with invalid product (FK constraint fails - expecting 500)
INVALID_ACCOUNT=$(cat <<EOF
{
  "account_number": "INVALID-ACC-${TIMESTAMP}",
  "customer_id": "${CREATED_CUSTOMER_ID}",
  "product_id": "NONEXISTENT",
  "currency": "USD",
  "opening_balance": "100.00"
}
EOF
)
test_endpoint "POST" "/api/accounts" "Create account with invalid product" "$INVALID_ACCOUNT" "500"

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed:${NC} $TESTS_PASSED"
echo -e "${RED}Failed:${NC} $TESTS_FAILED"
echo "Total:  $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
