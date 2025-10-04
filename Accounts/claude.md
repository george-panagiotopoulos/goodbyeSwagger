# Accounts Application - Technical Documentation

## Overview

This folder contains the complete implementation of the Account Processing System MVP. The application is organized into four main components, each responsible for a specific layer of the architecture.

## Development Principles

### Quality Standards
**This is a small MVP that must be TOP QUALITY**. The following principles are non-negotiable:

1. **No Shortcuts**: Every feature must be properly implemented with no workarounds
2. **No Error Cover-ups**: All errors must be investigated and properly fixed at their root cause
3. **Production-Grade Code**: Despite being an MVP, all code must be production-ready
4. **Complete Testing**: Every endpoint and feature must be thoroughly tested and working
5. **Proper Error Handling**: All error cases must be handled gracefully with meaningful messages
6. **Data Integrity**: All database operations must maintain data integrity and consistency

### Documentation Requirements
**Prompt Log Maintenance is MANDATORY**. For every user instruction:

1. **Record the Instruction**: Log the exact user prompt in `/About/Prompts_log.txt`
2. **Document Actions Taken**: Record all files created/modified and key decisions made
3. **Record the Outcome**: Document what was accomplished and any issues encountered
4. **Update Immediately**: Prompt log must be updated before moving to the next task
5. **Include Context**: Capture enough detail for future reference and audit trail

**Failure to maintain the prompt log will result in rework and delays.**

---

## Technology Stack

### Database Layer
- **Technology**: SQLite 3
- **Language**: Python 3.11+
- **Port**: 6602 (if exposed)
- **Purpose**: Data persistence and storage
- **Key Libraries**:
  - `sqlite3` - Built-in Python SQLite interface
  - `pytest` - Testing framework

### Application/Business Logic Layer
- **Technology**: Rust 1.70+
- **Purpose**: Core business logic, domain models, and validation
- **Key Dependencies**:
  - `rusqlite` - SQLite client for Rust
  - `serde` / `serde_json` - Serialization/deserialization
  - `chrono` - Date and time handling
  - `rust_decimal` - Precise decimal arithmetic for financial calculations
  - `thiserror` - Error handling
  - `uuid` - Unique identifier generation
- **Build Tool**: Cargo

### API Layer
- **Technology**: Rust 1.70+
- **Framework**: Actix-web 4.x
- **Port**: 6600
- **Purpose**: RESTful API with HATEOAS, authentication, and request handling
- **Key Dependencies**:
  - `actix-web` - Web framework
  - `actix-cors` - CORS middleware
  - `jsonwebtoken` - JWT authentication
  - `bcrypt` / `argon2` - Password hashing
  - `env_logger` - Logging infrastructure
  - `utoipa` - OpenAPI/Swagger generation
  - `utoipa-swagger-ui` - Swagger UI integration
  - `validator` - Request validation
- **Build Tool**: Cargo

### User Interface Layer
- **Technology**: React 18+
- **Framework**: Vite 4.x
- **Port**: 6601
- **Purpose**: Modern web-based user interface
- **Key Dependencies**:
  - `react` / `react-dom` - React framework
  - `react-router-dom` - Client-side routing
  - `axios` - HTTP client
  - `@tanstack/react-query` - Data fetching and caching
  - `zustand` or `jotai` - Lightweight state management
  - `react-hook-form` - Form handling
  - `zod` - Schema validation
  - `tailwindcss` - Utility-first CSS framework
  - `lucide-react` - Icon library
- **Build Tool**: Vite
- **Package Manager**: npm

---

## Folder Structure

```
Accounts/
├── Database/                       # SQLite + Python layer
│   ├── schema/                     # Database schema files
│   │   ├── migrations/             # Migration scripts
│   │   │   ├── 001_initial_schema.sql
│   │   │   ├── 002_add_interest_accruals.sql
│   │   │   └── ...
│   │   └── seed/                   # Seed data scripts
│   │       ├── seed_products.sql
│   │       └── seed_test_accounts.sql
│   ├── scripts/                    # Python utility scripts
│   │   ├── init_db.py              # Database initialization
│   │   ├── migrate.py              # Migration runner
│   │   ├── backup.py               # Backup utility
│   │   └── seed_data.py            # Seed data loader
│   ├── tests/                      # Database tests
│   │   └── test_schema.py
│   ├── accounts.db                 # SQLite database file (generated)
│   ├── requirements.txt            # Python dependencies
│   └── README.md                   # Database documentation
│
├── Application/                    # Rust business logic
│   ├── src/
│   │   ├── domain/                 # Domain models
│   │   │   ├── mod.rs
│   │   │   ├── account.rs          # Account entity
│   │   │   ├── product.rs          # Product entity
│   │   │   ├── transaction.rs      # Transaction entity
│   │   │   ├── interest.rs         # Interest accrual entity
│   │   │   └── user.rs             # User entity
│   │   ├── repository/             # Data access layer
│   │   │   ├── mod.rs
│   │   │   ├── account_repository.rs
│   │   │   ├── product_repository.rs
│   │   │   ├── transaction_repository.rs
│   │   │   ├── interest_repository.rs
│   │   │   └── user_repository.rs
│   │   ├── services/               # Business logic services
│   │   │   ├── mod.rs
│   │   │   ├── account_service.rs  # Account operations
│   │   │   ├── product_service.rs  # Product management
│   │   │   ├── transaction_service.rs  # Transaction processing
│   │   │   ├── interest_service.rs # Interest calculation
│   │   │   ├── fee_service.rs      # Fee application
│   │   │   └── auth_service.rs     # Authentication
│   │   ├── utils/                  # Utility functions
│   │   │   ├── mod.rs
│   │   │   ├── decimal.rs          # Decimal helpers
│   │   │   ├── date.rs             # Date helpers
│   │   │   └── validation.rs       # Validation helpers
│   │   ├── error.rs                # Error types
│   │   ├── config.rs               # Configuration
│   │   └── lib.rs                  # Library entry point
│   ├── tests/                      # Integration tests
│   │   ├── account_tests.rs
│   │   ├── transaction_tests.rs
│   │   ├── interest_tests.rs
│   │   └── fee_tests.rs
│   ├── Cargo.toml                  # Rust dependencies
│   └── README.md                   # Application layer docs
│
├── API/                            # Rust REST API
│   ├── src/
│   │   ├── handlers/               # HTTP request handlers
│   │   │   ├── mod.rs
│   │   │   ├── account_handlers.rs # Account endpoints
│   │   │   ├── product_handlers.rs # Product endpoints
│   │   │   ├── transaction_handlers.rs # Transaction endpoints
│   │   │   ├── interest_handlers.rs    # Interest endpoints
│   │   │   ├── fee_handlers.rs         # Fee endpoints
│   │   │   ├── auth_handlers.rs        # Auth endpoints
│   │   │   └── health_handlers.rs      # Health check
│   │   ├── middleware/             # Middleware components
│   │   │   ├── mod.rs
│   │   │   ├── auth.rs             # JWT authentication
│   │   │   ├── logging.rs          # Request logging
│   │   │   ├── cors.rs             # CORS configuration
│   │   │   └── error.rs            # Error handling
│   │   ├── models/                 # API request/response models
│   │   │   ├── mod.rs
│   │   │   ├── account_models.rs   # Account DTOs
│   │   │   ├── product_models.rs   # Product DTOs
│   │   │   ├── transaction_models.rs # Transaction DTOs
│   │   │   ├── interest_models.rs  # Interest DTOs
│   │   │   ├── fee_models.rs       # Fee DTOs
│   │   │   ├── auth_models.rs      # Auth DTOs
│   │   │   └── common.rs           # Common models (pagination, errors)
│   │   ├── routes.rs               # Route definitions
│   │   ├── config.rs               # Server configuration
│   │   ├── openapi.rs              # OpenAPI/Swagger configuration
│   │   └── main.rs                 # Application entry point
│   ├── tests/                      # API integration tests
│   │   ├── api_tests.rs
│   │   └── auth_tests.rs
│   ├── Cargo.toml                  # Rust dependencies
│   ├── .env.example                # Environment variables template
│   └── README.md                   # API documentation
│
├── UI/                             # React user interface
│   ├── public/                     # Static assets
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   │   ├── common/             # Common UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── Spinner.tsx
│   │   │   ├── layout/             # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── products/           # Product components
│   │   │   │   ├── ProductList.tsx
│   │   │   │   ├── ProductDetail.tsx
│   │   │   │   ├── ProductForm.tsx
│   │   │   │   └── ProductCard.tsx
│   │   │   ├── accounts/           # Account components
│   │   │   │   ├── AccountList.tsx
│   │   │   │   ├── AccountDetail.tsx
│   │   │   │   ├── AccountForm.tsx
│   │   │   │   ├── AccountCard.tsx
│   │   │   │   └── BalanceDisplay.tsx
│   │   │   ├── transactions/       # Transaction components
│   │   │   │   ├── TransactionForm.tsx
│   │   │   │   ├── LedgerView.tsx
│   │   │   │   └── TransactionRow.tsx
│   │   │   ├── interest/           # Interest components
│   │   │   │   └── InterestDetails.tsx
│   │   │   └── fees/               # Fee components
│   │   │       └── FeesSummary.tsx
│   │   ├── pages/                  # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Products.tsx
│   │   │   ├── Accounts.tsx
│   │   │   ├── AccountDetail.tsx
│   │   │   ├── Transactions.tsx
│   │   │   └── NotFound.tsx
│   │   ├── services/               # API client services
│   │   │   ├── api.ts              # Axios instance configuration
│   │   │   ├── authService.ts      # Authentication API calls
│   │   │   ├── productService.ts   # Product API calls
│   │   │   ├── accountService.ts   # Account API calls
│   │   │   ├── transactionService.ts # Transaction API calls
│   │   │   ├── interestService.ts  # Interest API calls
│   │   │   └── feeService.ts       # Fee API calls
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useAuth.ts          # Authentication hook
│   │   │   ├── useProducts.ts      # Products data hook
│   │   │   ├── useAccounts.ts      # Accounts data hook
│   │   │   ├── useTransactions.ts  # Transactions data hook
│   │   │   └── useApi.ts           # Generic API hook
│   │   ├── stores/                 # State management
│   │   │   ├── authStore.ts        # Auth state (Zustand)
│   │   │   └── appStore.ts         # App-level state
│   │   ├── types/                  # TypeScript type definitions
│   │   │   ├── account.ts
│   │   │   ├── product.ts
│   │   │   ├── transaction.ts
│   │   │   ├── interest.ts
│   │   │   ├── fee.ts
│   │   │   ├── auth.ts
│   │   │   └── common.ts
│   │   ├── utils/                  # Utility functions
│   │   │   ├── formatters.ts       # Format currency, dates, etc.
│   │   │   ├── validators.ts       # Validation helpers
│   │   │   └── constants.ts        # App constants
│   │   ├── App.tsx                 # Root component
│   │   ├── main.tsx                # Application entry point
│   │   ├── router.tsx              # Router configuration
│   │   └── index.css               # Global styles
│   ├── package.json                # npm dependencies
│   ├── tsconfig.json               # TypeScript configuration
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   ├── .env.example                # Environment variables template
│   └── README.md                   # UI documentation
│
└── claude.md                       # This file
```

---

## Component Communication

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                      (React - Port 6601)                     │
│                                                              │
│  Components → Services → API Client (Axios)                 │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/JSON
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                         REST API                             │
│                   (Rust Actix-web - Port 6600)              │
│                                                              │
│  Routes → Handlers → Middleware → Response                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Logic                         │
│                        (Rust Library)                        │
│                                                              │
│  Services → Domain Models → Repository                       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                         Database                             │
│                  (SQLite - accounts.db)                      │
│                                                              │
│  Tables: products, accounts, transactions, etc.              │
└─────────────────────────────────────────────────────────────┘
```

---

## Development Workflow

### 1. Database First
When implementing a new feature:
1. Design the database schema (tables, columns, indexes)
2. Create migration script in `Database/schema/migrations/`
3. Run migration to update database

### 2. Domain Models
1. Define Rust struct in `Application/src/domain/`
2. Implement serialization/deserialization
3. Add validation logic

### 3. Repository Layer
1. Create repository trait in `Application/src/repository/`
2. Implement CRUD operations using `rusqlite`
3. Handle database errors and transactions

### 4. Business Logic
1. Create service in `Application/src/services/`
2. Implement business rules and validation
3. Write unit tests

### 5. API Layer
1. Define request/response models in `API/src/models/`
2. Create handler in `API/src/handlers/`
3. Register route in `API/src/routes.rs`
4. Add OpenAPI annotations
5. Test with Postman or curl

### 6. User Interface
1. Create TypeScript types in `UI/src/types/`
2. Create service function in `UI/src/services/`
3. Create custom hook if needed in `UI/src/hooks/`
4. Build React component in `UI/src/components/`
5. Integrate component into page
6. Test in browser

---

## Building and Running

### Database Setup
```bash
cd Database
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py
python scripts/seed_data.py
```

### Build Application Layer
```bash
cd Application
cargo build --release
cargo test
```

### Build and Run API
```bash
cd API
cp .env.example .env
# Edit .env with your configuration
cargo build --release
cargo run
# API will be available at http://localhost:6600
```

### Build and Run UI
```bash
cd UI
cp .env.example .env
# Edit .env with API URL
npm install
npm run dev
# UI will be available at http://localhost:6601
```

### Run All Components
From the project root:
```bash
./start.sh
```

Stop all components:
```bash
./stop.sh
```

---

## Testing Strategy

### Database Tests
- Schema validation
- Migration testing
- Seed data verification

**Run**: `cd Database && pytest`

### Unit Tests (Application Layer)
- Domain model validation
- Service business logic
- Repository operations

**Run**: `cd Application && cargo test`

### Integration Tests (API Layer)
- Endpoint testing
- Authentication flows
- Error handling

**Run**: `cd API && cargo test`

### UI Tests
- Component rendering
- User interactions
- API integration

**Run**: `cd UI && npm test`

### End-to-End Tests
- Complete workflows
- Multi-component interactions

**Tool**: Playwright or Cypress (to be set up)

---

## Configuration

### Database Configuration
- **File**: `Database/accounts.db`
- **Connection String**: Managed by Python scripts
- **Migrations**: `Database/schema/migrations/`

### Application Configuration
- **File**: `Application/src/config.rs`
- **Settings**: Database path, logging level

### API Configuration
- **File**: `API/.env`
- **Settings**:
  - `HOST` - Server host (default: 0.0.0.0)
  - `PORT` - Server port (default: 6600)
  - `DATABASE_URL` - SQLite database path
  - `JWT_SECRET` - Secret for JWT token signing
  - `JWT_EXPIRATION` - Token expiration time (e.g., 3600 for 1 hour)
  - `RUST_LOG` - Logging level (debug, info, warn, error)

### UI Configuration
- **File**: `UI/.env`
- **Settings**:
  - `VITE_API_URL` - API base URL (default: http://localhost:6600)
  - `VITE_APP_NAME` - Application name

---

## API Documentation

### Swagger UI
Once the API is running, OpenAPI/Swagger documentation is available at:
```
http://localhost:6600/swagger-ui/
```

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

#### Products
- `POST /api/products` - Create product
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product details
- `PUT /api/products/{id}` - Update product

#### Accounts
- `POST /api/accounts` - Create account
- `GET /api/accounts/{id}` - Get account details
- `PATCH /api/accounts/{id}/status` - Update account status

#### Transactions
- `POST /api/accounts/{id}/debit` - Process withdrawal
- `POST /api/accounts/{id}/credit` - Process deposit
- `GET /api/accounts/{id}/ledger` - Get transaction history

#### Interest & Fees
- `GET /api/accounts/{id}/interest` - Get interest details
- `GET /api/accounts/{id}/fees` - Get fee summary

---

## Security

### Authentication
- JWT-based authentication
- Tokens expire after configured time
- Refresh token mechanism for extended sessions

### Password Security
- Passwords hashed using bcrypt or argon2
- Minimum password requirements enforced
- No plain-text password storage

### API Security
- CORS configured for UI origin
- Request validation on all inputs
- SQL injection prevention (parameterized queries)
- XSS prevention (proper escaping in UI)

### Database Security
- File permissions on SQLite database
- No sensitive data in logs
- Audit trail for all operations

---

## Performance Considerations

### Database
- Indexes on frequently queried columns (account_id, transaction_date)
- Connection pooling (if needed for concurrent access)
- Batch operations for interest/fee processing

### API
- Response caching where appropriate
- Pagination for large result sets
- Rate limiting (to be implemented)

### UI
- React Query for data caching
- Lazy loading of components
- Debounced search inputs
- Optimistic updates for better UX

---

## Logging and Monitoring

### API Logging
- Request/response logging via `env_logger`
- Error logging with stack traces
- Audit logging for sensitive operations

### Application Logging
- Business logic events
- Error conditions
- Performance metrics

### UI Logging
- Error boundary for catching React errors
- API error logging
- User action tracking (optional)

---

## Error Handling

### Database Errors
- Connection failures
- Constraint violations
- Transaction rollbacks

### Application Errors
- Validation errors
- Business rule violations
- Concurrency conflicts

### API Errors
- Standard HTTP status codes
- Structured error responses:
  ```json
  {
    "error": {
      "code": "INSUFFICIENT_BALANCE",
      "message": "Account has insufficient balance for this transaction",
      "details": {
        "requested": 100.00,
        "available": 50.00
      }
    }
  }
  ```

### UI Errors
- User-friendly error messages
- Retry mechanisms for network errors
- Fallback UI for critical errors

---

## HATEOAS Implementation

Responses include hypermedia links for navigation:

```json
{
  "account_id": "ACC-001",
  "account_number": "1234567890",
  "balance": 1000.00,
  "_links": {
    "self": {
      "href": "/api/accounts/ACC-001"
    },
    "ledger": {
      "href": "/api/accounts/ACC-001/ledger"
    },
    "debit": {
      "href": "/api/accounts/ACC-001/debit",
      "method": "POST"
    },
    "credit": {
      "href": "/api/accounts/ACC-001/credit",
      "method": "POST"
    }
  }
}
```

---

## Future Enhancements

### Phase 2 (Roadmap)
- Authorization/clearing workflow
- Internal transfers
- Transaction reversals
- Additional account statuses

### Technical Debt
- Add rate limiting to API
- Implement request throttling
- Add API versioning
- Improve error messages
- Add telemetry/metrics collection
- Set up CI/CD pipeline

---

## Troubleshooting

### Database Issues
**Problem**: Database locked error
**Solution**: Ensure no other process is accessing the database, use WAL mode

**Problem**: Migration fails
**Solution**: Check migration script syntax, ensure database backup exists

### API Issues
**Problem**: Port 6600 already in use
**Solution**: Change port in `.env`, kill process using port, or use different port

**Problem**: CORS errors in browser
**Solution**: Verify CORS configuration in `API/src/middleware/cors.rs`

### UI Issues
**Problem**: API calls failing
**Solution**: Check `VITE_API_URL` in `.env`, ensure API is running

**Problem**: Build errors
**Solution**: Delete `node_modules` and `package-lock.json`, run `npm install` again

---

## Resources

### Documentation
- Rust: https://www.rust-lang.org/learn
- Actix-web: https://actix.rs/docs/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- SQLite: https://www.sqlite.org/docs.html

### Tools
- Rust Analyzer (VS Code extension)
- Postman (API testing)
- DB Browser for SQLite (database inspection)
- React Developer Tools (browser extension)

---

**Last Updated**: 2025-10-04
**Maintainer**: Development Team
