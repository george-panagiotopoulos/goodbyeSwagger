# Getting Started with Account Processing System

Welcome to the Account Processing System! This guide will help you get up and running quickly.

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [First Login](#first-login)
- [Basic Operations](#basic-operations)
- [Next Steps](#next-steps)

---

## Overview

The Account Processing System is a comprehensive platform for managing checking/current accounts with features including:

- **Account Management**: Open and manage customer accounts
- **Transaction Processing**: Process deposits and withdrawals
- **Interest Calculation**: Automated monthly interest accrual
- **Fee Management**: Transaction and maintenance fees
- **Batch Processing**: End-of-month operations

### System Architecture

The system consists of three main components:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Web UI    │────▶│   REST API   │────▶│   Database   │
│ Port 6601   │     │  Port 6600   │     │   SQLite     │
└─────────────┘     └──────────────┘     └──────────────┘
```

---

## Quick Start

### For End Users (Web Interface)

1. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:6601`

2. **Login**
   - Username: `testuser`
   - Password: `password123`

3. **Explore**
   - View dashboard
   - Browse products, customers, and accounts
   - Process transactions

### For Developers (API)

1. **Obtain Access Token**
   ```bash
   curl -X POST http://localhost:6600/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"password123"}'
   ```

2. **Make API Calls**
   ```bash
   # Save token
   export TOKEN="your_jwt_token_here"

   # List all accounts
   curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:6600/api/accounts
   ```

3. **Import Postman Collection**
   - Import `docs/examples/postman_collection.json`
   - Run requests from collection

---

## System Requirements

### Server Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Linux, macOS, Windows |
| Rust | 1.70 or higher |
| Python | 3.8 or higher |
| Node.js | 16.x or higher |
| npm | 8.x or higher |
| SQLite | 3.x |
| Available Ports | 6600, 6601 |
| Disk Space | 500 MB minimum |
| RAM | 2 GB minimum |

### Client Requirements (Web UI)

| Browser | Minimum Version |
|---------|----------------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

---

## Installation

### Option 1: Using Start Script (Recommended)

1. **Navigate to Application Directory**
   ```bash
   cd /path/to/Accounts
   ```

2. **Run Start Script**
   ```bash
   ./start.sh
   ```

   This will:
   - Check for port availability
   - Start the API server (port 6600)
   - Start the UI server (port 6601)
   - Perform health checks
   - Display server URLs

3. **Verify Installation**
   ```bash
   curl http://localhost:6600/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-10-05T12:00:00Z"
   }
   ```

### Option 2: Manual Setup

#### 1. Database Setup

```bash
cd Database
python3 scripts/init_db.py
python3 scripts/seed_data.py
```

#### 2. API Server

```bash
cd API
cargo build --release
cargo run
```

Server starts on: `http://localhost:6600`

#### 3. UI Server

```bash
cd UI
npm install
npm run dev
```

Server starts on: `http://localhost:6601`

---

## First Login

### Web Interface

1. **Navigate to Login Page**
   - URL: `http://localhost:6601`
   - You'll be redirected to login if not authenticated

2. **Enter Credentials**
   - **Username**: `testuser`
   - **Password**: `password123`
   - **Role**: User (read-only demonstration)

3. **Successful Login**
   - You'll be redirected to the dashboard
   - Navigation menu appears with:
     - Dashboard
     - Products
     - Customers
     - Accounts
     - Batch Processes

### API Authentication

1. **Request Token**
   ```bash
   POST /api/auth/login
   Content-Type: application/json

   {
     "username": "testuser",
     "password": "password123"
   }
   ```

2. **Response**
   ```json
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "user_id": "USR-001",
       "username": "testuser",
       "full_name": "Test User",
       "email": "test@example.com",
       "role": "User"
     }
   }
   ```

3. **Use Token in Requests**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:6600/api/accounts
   ```

---

## Basic Operations

### View Dashboard

**Web UI**: Click "Dashboard" in navigation menu

**API**: `GET /api/accounts` (returns account list)

**What you see**:
- Quick statistics
- Recent activity
- Navigation cards to key sections

### Manage Products

Products define account types with interest rates, fees, and features.

**View Products**
- Web UI: Navigate to "Products"
- API: `GET /api/products`

**Create Product**
- Web UI: Click "Create New Product" button
- API: `POST /api/products`

Example:
```json
{
  "product_name": "Premium Savings",
  "product_code": "PREM_SAV",
  "currency": "USD",
  "interest_rate": "0.035",
  "minimum_balance_for_interest": "5000.00",
  "monthly_maintenance_fee": "10.00",
  "transaction_fee": "1.00"
}
```

### Manage Customers

**View Customers**
- Web UI: Navigate to "Customers"
- API: `GET /api/customers`

**View Customer Details**
- Web UI: Click "View Details" on customer row
- API: `GET /api/customers/{id}`

**Create Customer**
- Web UI: Click "Create New Customer" button
- API: `POST /api/customers`

Example:
```json
{
  "customer_name": "John Doe",
  "customer_type": "Individual",
  "email": "john.doe@example.com",
  "phone": "+1-555-0100"
}
```

### Open Account

**Prerequisites**:
- Customer must exist
- Product must be active

**Steps (Web UI)**:
1. Navigate to Customers
2. Find customer row
3. Click "Open Account"
4. Select product
5. Enter opening balance
6. Click "Create Account"

**API Call**:
```bash
POST /api/accounts
{
  "customer_id": "CUST-001",
  "product_id": "PROD-001",
  "opening_balance": "1000.00"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "account_id": "ACC-...",
    "account_number": "2025000001",
    "balance": 1000.00,
    "status": "Active",
    ...
  }
}
```

### Process Transactions

#### Deposit (Credit)

**Web UI**:
1. Navigate to account detail page
2. Click "New Transaction"
3. Select "Credit"
4. Enter amount and description
5. Click "Submit"

**API**:
```bash
POST /api/accounts/{id}/credit
{
  "amount": 500.00,
  "description": "Salary deposit",
  "reference": "PAYROLL-2025-10"
}
```

#### Withdrawal (Debit)

**Web UI**:
1. Navigate to account detail page
2. Click "New Transaction"
3. Select "Debit"
4. Enter amount and description
5. Click "Submit"

**Note**: Transaction fee ($0.50) automatically applied

**API**:
```bash
POST /api/accounts/{id}/debit
{
  "amount": 100.00,
  "description": "ATM withdrawal",
  "reference": "ATM-001"
}
```

**Important**: Total debit = amount + transaction fee

#### View Transaction History

**Web UI**: Account detail page shows transaction list

**API**: `GET /api/accounts/{id}/transactions`

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "transaction_id": "TXN-...",
      "transaction_type": "Credit",
      "category": "Deposit",
      "amount": 500.00,
      "running_balance": 1500.00,
      "description": "Salary deposit",
      "transaction_date": "2025-10-05T10:30:00Z"
    },
    ...
  ]
}
```

### Run Batch Processes

Monthly interest accrual using 30/360 day count convention.

**Web UI**:
1. Navigate to "Batch Processes"
2. Click "Run Monthly Accruals"
3. View processing results
4. Check accrual history

**API**:
```bash
POST /api/batch/monthly-accruals
{
  "dry_run": false
}
```

**What Happens**:
1. System scans all active accounts
2. Identifies months requiring processing
3. Calculates interest: `(Balance × Annual Rate) / 12`
4. Posts interest transactions on month-end date
5. Updates account balances

---

## Next Steps

### For End Users

1. **Explore Features**
   - Browse existing accounts
   - Process sample transactions
   - View transaction history
   - Run batch processes

2. **Learn More**
   - Read [User Manual](./USER_MANUAL.md)
   - Review [Transaction Guide](./TRANSACTION_GUIDE.md)
   - Understand [Interest Calculation](./INTEREST_CALCULATION.md)

3. **Get Help**
   - Check [FAQ](./FAQ.md)
   - Review [Troubleshooting Guide](./TROUBLESHOOTING.md)

### For Developers

1. **API Integration**
   - Review [API Documentation](../api/openapi.yaml)
   - Import [Postman Collection](../examples/postman_collection.json)
   - Read [API Vocabulary](../api/API_VOCABULARY.md)

2. **Development**
   - Read [Developer Guidelines](../../internal_docs/dev_guidelines/)
   - Review [Architecture Documentation](../architecture/)
   - Understand [Data Models](../data_models/)

3. **Contributing**
   - Fork repository
   - Create feature branch
   - Submit pull request

---

## Common Issues

### Port Already in Use

**Problem**: Error "Port 6600 already in use"

**Solution**:
```bash
# Find process using port
lsof -i :6600

# Kill process
kill -9 <PID>

# Or use stop script
./stop.sh
```

### Database Locked

**Problem**: "Database is locked" error

**Solution**:
```bash
# Stop all services
./stop.sh

# Wait 5 seconds

# Restart
./start.sh
```

### Authentication Failed

**Problem**: 401 Unauthorized error

**Solution**:
1. Verify credentials
2. Request new token (tokens expire after 1 hour)
3. Check token in Authorization header: `Bearer YOUR_TOKEN`

---

## Support

For additional help:

- **Documentation**: Browse `/docs` folder
- **API Reference**: See [OpenAPI Specification](../api/openapi.yaml)
- **Examples**: Check `/docs/examples` folder
- **Issues**: Report bugs via issue tracker

---

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: Current
