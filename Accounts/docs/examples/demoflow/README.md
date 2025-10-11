# API Flow Demonstration

This directory contains a comprehensive demonstration of the Accounts API workflow, showcasing a complete end-to-end integration example.

## Overview

The `demo_api_flow.py` script demonstrates a complete API workflow including:

1. **Authentication** - Login to obtain JWT token
2. **Customer Creation** - Create a new customer record
3. **Account Opening** - Open a savings account for the customer
4. **Transaction Processing** - Process 5 transactions (credits and debits)
5. **Data Retrieval** - Fetch customer details and transaction history

## Files

### demo_api_flow.py

A Python script that executes the complete API flow. Features:
- Automated API calls to localhost:6600
- JWT authentication handling
- Comprehensive logging of all requests and responses
- Error handling and status reporting
- Detailed step-by-step execution

**Usage:**
```bash
cd /Accounts/docs/examples/demoflow
python3 demo_api_flow.py
```

### flowoutput.txt

Complete log of all HTTP requests and responses from the demonstration flow. This file contains:

- **Request Details**: Method, URL, headers, and request body (JSON formatted)
- **Response Details**: Status code, response body (JSON formatted), and descriptions
- **Flow Summary**: Customer ID, Account ID, transaction count, and completion time

## API Endpoints Demonstrated

### 1. Authentication
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "demo_user",
  "password": "demo_pass123"
}
```

**Response:** JWT token and user information

### 2. Create Customer
```
POST /api/customers
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_name": "John Demo Customer",
  "customer_type": "Individual",
  "external_customer_id": "EXT-20251011091300",
  "email": "john.demo@example.com",
  "phone": "+1-555-0123"
}
```

**Response:** Customer object with generated customer_id

### 3. Get Products (to select one for account)
```
GET /api/products
Authorization: Bearer <token>
```

**Response:** List of available banking products

### 4. Create Account
```
POST /api/accounts
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_id": "CUST-xxxxx",
  "product_id": "PROD-SAV-HIGH-001",
  "opening_balance": "1000.00"
}
```

**Response:** Account object with generated account_id and account_number

### 5. Process Credit Transaction
```
POST /api/accounts/{account_id}/credit
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": "500.00",
  "description": "Salary deposit",
  "reference": "SAL-001"
}
```

**Response:** Updated account object with new balance

### 6. Process Debit Transaction
```
POST /api/accounts/{account_id}/debit
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": "150.00",
  "description": "Utility payment",
  "reference": "UTIL-001"
}
```

**Response:** Updated account object with new balance (includes transaction fees)

### 7. Get Customer Details
```
GET /api/customers/{customer_id}
Authorization: Bearer <token>
```

**Response:** Complete customer information

### 8. Get Transaction History
```
GET /api/accounts/{account_id}/transactions
Authorization: Bearer <token>
```

**Response:** Array of all transactions including:
- Opening balance credit
- Deposits (credits)
- Withdrawals (debits)
- Transaction fees
- Running balance for each transaction

## cURL Examples

You can use these cURL commands to test the API manually on localhost:

### Login
```bash
curl -X POST http://localhost:6600/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "password": "demo_pass123"
  }'
```

### Create Customer (requires token from login)
```bash
curl -X POST http://localhost:6600/api/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "customer_name": "Test Customer",
    "customer_type": "Individual",
    "email": "test@example.com",
    "phone": "+1-555-9999"
  }'
```

### Open Account (requires token and customer_id)
```bash
curl -X POST http://localhost:6600/api/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "customer_id": "CUST-xxxxx",
    "product_id": "PROD-SAV-HIGH-001",
    "opening_balance": "1000.00"
  }'
```

### Credit Transaction (requires token and account_id)
```bash
curl -X POST http://localhost:6600/api/accounts/ACC-xxxxx/credit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "amount": "500.00",
    "description": "Deposit",
    "reference": "DEP-001"
  }'
```

### Debit Transaction (requires token and account_id)
```bash
curl -X POST http://localhost:6600/api/accounts/ACC-xxxxx/debit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "amount": "100.00",
    "description": "Withdrawal",
    "reference": "WD-001"
  }'
```

### Get Transaction History (requires token and account_id)
```bash
curl -X GET http://localhost:6600/api/accounts/ACC-xxxxx/transactions \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Postman Collection

To use with Postman:

1. Import the requests from `flowoutput.txt` or manually create requests
2. Set up environment variables:
   - `base_url`: http://localhost:6600
   - `token`: (obtained from login response)
   - `customer_id`: (obtained from create customer response)
   - `account_id`: (obtained from create account response)

3. Use the following request sequence:
   - Login (saves token to environment)
   - Create Customer (saves customer_id)
   - Get Products
   - Create Account (saves account_id)
   - Credit Transaction
   - Debit Transaction
   - Get Customer
   - Get Transactions

## Response Format

All successful responses follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Error responses:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

## Authentication

All endpoints except `/api/auth/login` and `/api/auth/register` require a Bearer token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

Tokens expire after the configured time (default: 24 hours). Use the refresh endpoint to obtain a new token.

## Notes

- The demo user (`demo_user` / `demo_pass123`) must be created first by running the registration endpoint or via the demo script
- All amounts are in USD
- The system automatically applies transaction fees based on the product configuration
- Running balances are calculated and returned with each transaction
- Transaction history includes all debits, credits, fees, and the opening balance

## Related Documentation

- `/Accounts/docs/api/` - Complete API specifications
- `/Accounts/docs/examples/` - Other API examples
- `/Accounts/docs/data_models/` - Entity and field definitions
- `/Accounts/API/src/handlers/` - API implementation source code

## Last Updated

2025-10-11
