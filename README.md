# Account Processing System - MVP

A demonstration application showcasing a documentation-first architecture pattern for building applications with comprehensive RAG-based knowledge systems.

## 🚀 Quick Start

```bash
# Initialize database
cd Accounts/Database
python3 scripts/init_db.py
python3 scripts/seed_data.py

# Start the API (from Accounts directory)
cd ../
./start.sh

# Run tests
cd API
./test_curl.sh
```

The API will be available at `http://localhost:6600`

## ✅ Current Status

**MVP Phase 1 Complete** - All 18/18 tests passing ✅

### Implemented Features

- ✅ **Products Management**
  - Create, read, list products
  - Filter active products
  - Product configuration (interest rates, fees, etc.)

- ✅ **Customer Management**
  - Create, read, list customers
  - Support for Individual and Business customers
  - External customer ID integration

- ✅ **Account Processing**
  - Create accounts with opening balance
  - Account status management
  - Balance tracking

- ✅ **Transaction Processing**
  - Credit operations (deposits)
  - Debit operations (withdrawals)
  - Complete ledger with running balance
  - Transaction history retrieval

## 🏗️ Architecture

### Tech Stack

- **Database**: SQLite (Python for scripts)
- **Business Logic**: Rust
- **API**: Rust (Actix-web) - RESTful on port 6600
- **UI**: React (planned) - port 6601

### Project Structure

```
Accounts/
├── Database/          # SQLite database and Python scripts
│   ├── schema/        # Migrations and seed data
│   └── scripts/       # Database utilities
├── Application/       # Rust business logic layer
│   ├── domain/        # Domain models
│   ├── repositories/  # Data access layer
│   └── services/      # Business services
├── API/              # Rust REST API
│   ├── handlers/     # HTTP handlers
│   └── models/       # API DTOs
└── UI/               # React frontend (planned)
```

## 📊 Database

**6 Test Accounts** with **$22,500.50** total balance:
- Individual accounts (checking, savings)
- Business accounts
- Student account

### Entities

- **Products**: Account product configurations
- **Customers**: Individual and Business customers
- **Accounts**: Customer accounts with balances
- **Transactions**: Complete ledger with audit trail
- **Users**: System users (planned)

## 🔌 API Endpoints

### Products
- `GET /api/products` - List all products
- `GET /api/products/active` - List active products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create new product

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer

### Accounts
- `GET /api/accounts` - List all accounts
- `GET /api/accounts/{id}` - Get account by ID
- `POST /api/accounts` - Create new account
- `GET /api/accounts/{id}/transactions` - Get transaction history
- `POST /api/accounts/{id}/credit` - Credit account (deposit)
- `POST /api/accounts/{id}/debit` - Debit account (withdrawal)

### Health
- `GET /health` - API health check

## 🧪 Testing

Comprehensive test suite with 18 test cases:

```bash
cd Accounts/API
./test_curl.sh
```

**Test Coverage:**
- ✅ Product CRUD operations
- ✅ Customer CRUD operations
- ✅ Account CRUD operations
- ✅ Transaction processing (credit/debit)
- ✅ Ledger retrieval
- ✅ Validation and error handling
- ✅ Overdraft prevention

## 📝 Documentation

- [Functional Requirements](functional_requirements.md)
- [MVP Scope](MVP.md)
- [Implementation Tasks](MVP_implementation_tasks.md)
- [Technical Architecture](Accounts/claude.md)

## 🛣️ Roadmap

### Phase 2 (Next)
- React UI implementation
- Authentication & authorization
- Advanced transaction workflows (authorization/clearing)
- Internal transfers

### Phase 3
- Overdraft management
- Formula-based fees and interest
- Multi-currency support
- Reporting and analytics

### Phase 4
- Documentation artifacts (9 categories)
- API vocabulary and Swagger/OpenAPI specs
- RAG system with ChromaDB
- Interactive chatbot

## 🧑‍💻 Development

### Prerequisites

- Rust 1.70+ (`cargo --version`)
- Python 3.11+ (`python3 --version`)
- SQLite 3 (`sqlite3 --version`)

### Build

```bash
# Build API
cd Accounts/API
cargo build --release

# Build Application layer
cd ../Application
cargo build --release
```

### Run

```bash
# Start all services
cd Accounts
./start.sh

# Stop all services
./stop.sh
```

## 📄 License

This is a demonstration project for showcasing documentation-first architecture patterns.

## 🤖 Generated with Claude Code

This project was built with assistance from [Claude Code](https://claude.com/claude-code), Anthropic's official CLI for Claude.

---

**Status**: MVP Phase 1 Complete ✅
**Last Updated**: 2025-10-04
**Test Results**: 18/18 Passing ✅
