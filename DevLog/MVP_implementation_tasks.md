# MVP Implementation Tasks

## Account Processing System - MVP Phase 1

**Document Version**: 1.0
**Last Updated**: 2025-10-04
**Status**: Implementation Plan
**Timeline**: 4 Weeks

---

## Table of Contents

1. [Implementation Strategy](#implementation-strategy)
2. [Week 1: Foundation](#week-1-foundation)
3. [Week 2: Core Features](#week-2-core-features)
4. [Week 3: Interest & Fees](#week-3-interest--fees)
5. [Week 4: Integration & Testing](#week-4-integration--testing)
6. [Task Checklist](#task-checklist)

---

## Implementation Strategy

### Layer-by-Layer Approach

For each feature, implement in this order:
1. **Database Schema** - Design and create tables
2. **Application Logic** (Rust) - Business rules and validation
3. **REST API** (Rust) - Endpoints with HATEOAS
4. **User Interface** (React) - UI components and forms

### Technology Stack

- **Database**: SQLite + Python (port 6602)
- **Application Logic**: Rust
- **API**: Rust with Actix-web/Axum (port 6600)
- **UI**: React with Vite (port 6601)

### Development Workflow

1. Start with database schema for the feature
2. Implement Rust business logic with unit tests
3. Create API endpoints with OpenAPI annotations
4. Build React UI components
5. Integration testing
6. Document as you build

---

## Week 1: Foundation

### Day 1-2: Project Setup

#### Task 1.1: Project Structure
- [x] Create `/Accounts` folder structure
  - [x] `/Accounts/Database` - SQLite + Python
  - [x] `/Accounts/Application` - Rust business logic
  - [x] `/Accounts/API` - Rust REST API
  - [x] `/Accounts/UI` - React application
- [x] Create `/Accounts/claude.md` with tech stack details
- [ ] Set up `.gitignore` files
- [ ] Initialize version control

#### Task 1.2: Database Setup
- [ ] Install SQLite
- [ ] Set up Python virtual environment
- [ ] Install Python dependencies:
  - [ ] `sqlite3` (built-in)
  - [ ] `pytest` for testing
- [ ] Create database initialization script
- [ ] Design core database schema:
  - [ ] Products table
  - [ ] Accounts table
  - [ ] Transactions/Ledger table
  - [ ] Interest accruals table
  - [ ] Audit log table
- [ ] Create migration scripts
- [ ] Create seed data scripts

#### Task 1.3: Rust Application Setup
- [ ] Initialize Rust workspace in `/Accounts/Application`
- [ ] Set up Cargo.toml with dependencies:
  - [ ] `rusqlite` - SQLite client
  - [ ] `serde` - Serialization
  - [ ] `chrono` - Date/time handling
  - [ ] `rust_decimal` - Precise decimal calculations
  - [ ] `thiserror` - Error handling
  - [ ] `uuid` - ID generation
- [ ] Create module structure:
  - [ ] `domain/` - Domain models
  - [ ] `repository/` - Database access
  - [ ] `services/` - Business logic
  - [ ] `utils/` - Utilities
- [ ] Set up unit testing framework

#### Task 1.4: Rust API Setup
- [ ] Initialize Rust API project in `/Accounts/API`
- [ ] Choose web framework (Actix-web recommended)
- [ ] Set up Cargo.toml with dependencies:
  - [ ] `actix-web` - Web framework
  - [ ] `actix-cors` - CORS middleware
  - [ ] `jsonwebtoken` - JWT authentication
  - [ ] `env_logger` - Logging
  - [ ] `serde_json` - JSON serialization
  - [ ] `utoipa` - OpenAPI generation
  - [ ] `utoipa-swagger-ui` - Swagger UI
- [ ] Configure server to run on port 6600
- [ ] Set up middleware:
  - [ ] Logging
  - [ ] CORS
  - [ ] Error handling
  - [ ] Request validation
- [ ] Create basic health check endpoint

#### Task 1.5: React UI Setup
- [ ] Create React app with Vite
- [ ] Configure to run on port 6601
- [ ] Install dependencies:
  - [ ] `react-router-dom` - Routing
  - [ ] `axios` - HTTP client
  - [ ] `@tanstack/react-query` - Data fetching
  - [ ] `zustand` or `jotai` - State management
  - [ ] `react-hook-form` - Form handling
  - [ ] `zod` - Validation
  - [ ] `tailwindcss` - Styling
  - [ ] `shadcn/ui` - UI components (optional)
- [ ] Set up project structure:
  - [ ] `/src/components` - React components
  - [ ] `/src/pages` - Page components
  - [ ] `/src/services` - API client
  - [ ] `/src/hooks` - Custom hooks
  - [ ] `/src/stores` - State management
  - [ ] `/src/types` - TypeScript types
- [ ] Configure API client for port 6600
- [ ] Create basic layout and routing

#### Task 1.6: Authentication Setup
- [ ] Database: Create users table
- [ ] Application: Implement JWT token generation
- [ ] Application: Implement password hashing (bcrypt/argon2)
- [ ] API: Create `/api/auth/login` endpoint
- [ ] API: Create `/api/auth/refresh` endpoint
- [ ] API: Create authentication middleware
- [ ] UI: Create login page
- [ ] UI: Implement token storage (localStorage)
- [ ] UI: Create protected route wrapper

#### Task 1.7: DevOps Scripts
- [ ] Create `start.sh` script:
  - [ ] Start database (if needed)
  - [ ] Start Rust API (cargo run)
  - [ ] Start React UI (npm run dev)
  - [ ] Health check all services
- [ ] Create `stop.sh` script
- [ ] Create `health_check.sh` script
- [ ] Test scripts on clean environment

### Day 3-5: Product Configuration

#### Task 1.8: Product Database Schema
- [ ] Design `products` table:
  - [ ] product_id (PK)
  - [ ] product_name
  - [ ] product_code (unique)
  - [ ] description
  - [ ] status (Active/Inactive)
  - [ ] currency
  - [ ] interest_rate (decimal)
  - [ ] minimum_balance_for_interest (decimal)
  - [ ] monthly_maintenance_fee (decimal)
  - [ ] transaction_fee (decimal)
  - [ ] created_at
  - [ ] updated_at
  - [ ] created_by
- [ ] Create table migration script
- [ ] Create seed data for 2-3 sample products

#### Task 1.9: Product Application Logic
- [ ] Create `Product` domain model (Rust struct)
- [ ] Create `ProductRepository` trait and implementation
- [ ] Implement `ProductService` with methods:
  - [ ] `create_product()` - Validation and creation
  - [ ] `get_product()` - Retrieve by ID
  - [ ] `list_products()` - List all products
  - [ ] `update_product()` - Update configuration
  - [ ] `update_status()` - Activate/deactivate
- [ ] Implement validation rules:
  - [ ] Unique product name and code
  - [ ] Valid interest rate (0-100%)
  - [ ] Valid fee amounts (>= 0)
  - [ ] Valid minimum balance (>= 0)
- [ ] Write unit tests for ProductService

#### Task 1.10: Product REST API
- [ ] Create `POST /api/products` endpoint
- [ ] Create `GET /api/products` endpoint (list with filters)
- [ ] Create `GET /api/products/{id}` endpoint
- [ ] Create `PUT /api/products/{id}` endpoint
- [ ] Create `PATCH /api/products/{id}/status` endpoint
- [ ] Add OpenAPI/Swagger annotations
- [ ] Implement request validation
- [ ] Implement error responses
- [ ] Add HATEOAS links to responses
- [ ] Test all endpoints with Postman

#### Task 1.11: Product UI Components
- [ ] Create `ProductList` component (view all products)
- [ ] Create `ProductDetail` component (view single product)
- [ ] Create `ProductForm` component (create/edit product)
- [ ] Create product management page
- [ ] Implement form validation with Zod
- [ ] Implement API integration
- [ ] Add loading states and error handling
- [ ] Test UI flows

---

## Week 2: Core Features

### Day 6-8: Account Management

#### Task 2.1: Account Database Schema
- [ ] Design `accounts` table:
  - [ ] account_id (PK)
  - [ ] account_number (unique, auto-generated)
  - [ ] customer_id
  - [ ] product_id (FK to products)
  - [ ] currency
  - [ ] status (Active/Closed)
  - [ ] balance (decimal)
  - [ ] interest_accrued (decimal)
  - [ ] opening_date
  - [ ] closing_date (nullable)
  - [ ] created_at
  - [ ] updated_at
- [ ] Create table migration script
- [ ] Create account number generation function
- [ ] Add foreign key constraints

#### Task 2.2: Account Application Logic
- [ ] Create `Account` domain model
- [ ] Create `AccountRepository` trait and implementation
- [ ] Implement `AccountService` with methods:
  - [ ] `create_account()` - Create with product link
  - [ ] `get_account()` - Retrieve by ID
  - [ ] `get_account_by_number()` - Retrieve by account number
  - [ ] `update_status()` - Change status
  - [ ] `get_balance()` - Get current balance
- [ ] Implement validation rules:
  - [ ] Valid product ID
  - [ ] Opening balance >= 0
  - [ ] Can only close if balance = 0
- [ ] Implement account number generation logic
- [ ] Write unit tests

#### Task 2.3: Account REST API
- [ ] Create `POST /api/accounts` endpoint
- [ ] Create `GET /api/accounts/{id}` endpoint
- [ ] Create `PATCH /api/accounts/{id}/status` endpoint
- [ ] Add OpenAPI annotations
- [ ] Add HATEOAS links (links to transactions, ledger, etc.)
- [ ] Test endpoints

#### Task 2.4: Account UI Components
- [ ] Create `AccountList` component
- [ ] Create `AccountDetail` component
- [ ] Create `AccountForm` component (create account)
- [ ] Create account management page
- [ ] Integrate with Product API (dropdown for product selection)
- [ ] Test UI flows

### Day 9-10: Transaction Processing & Ledger

#### Task 2.5: Transaction Database Schema
- [ ] Design `transactions` table (ledger):
  - [ ] transaction_id (PK)
  - [ ] account_id (FK to accounts)
  - [ ] transaction_date (timestamp)
  - [ ] value_date (date)
  - [ ] type (Debit/Credit enum)
  - [ ] category (Deposit/Withdrawal/Fee/Interest enum)
  - [ ] amount (decimal)
  - [ ] currency
  - [ ] running_balance (decimal)
  - [ ] description
  - [ ] reference
  - [ ] channel (API/UI/Batch)
  - [ ] status (Posted)
  - [ ] created_at
  - [ ] created_by
- [ ] Create table migration script
- [ ] Add indexes on account_id, transaction_date

#### Task 2.6: Transaction Application Logic
- [ ] Create `Transaction` domain model
- [ ] Create `TransactionRepository` trait and implementation
- [ ] Implement `TransactionService` with methods:
  - [ ] `process_debit()` - Process withdrawal
  - [ ] `process_credit()` - Process deposit
  - [ ] `get_ledger()` - Get transaction history
  - [ ] `calculate_running_balance()` - Calculate balance
  - [ ] `reconcile_balance()` - Verify balance correctness
- [ ] Implement validation rules:
  - [ ] Account must be Active for debits
  - [ ] Sufficient balance for debits
  - [ ] Amount > 0
- [ ] Implement balance locking (prevent concurrent updates)
- [ ] Implement ledger entry creation with running balance
- [ ] Write unit tests (including concurrency tests)

#### Task 2.7: Transaction REST API
- [ ] Create `POST /api/accounts/{id}/debit` endpoint
- [ ] Create `POST /api/accounts/{id}/credit` endpoint
- [ ] Create `GET /api/accounts/{id}/ledger` endpoint (with pagination)
- [ ] Create `GET /api/accounts/{id}/reconcile` endpoint
- [ ] Add query parameters for ledger (date range, type, category)
- [ ] Implement pagination for ledger queries
- [ ] Add OpenAPI annotations
- [ ] Test endpoints

#### Task 2.8: Transaction UI Components
- [ ] Create `TransactionForm` component (debit/credit)
- [ ] Create `LedgerView` component (transaction history)
- [ ] Create `BalanceDisplay` component
- [ ] Create transaction processing page
- [ ] Add date range filter for ledger
- [ ] Add pagination for ledger
- [ ] Test UI flows

---

## Week 3: Interest & Fees

### Day 11-13: Interest Calculation

#### Task 3.1: Interest Accrual Database Schema
- [ ] Design `interest_accruals` table:
  - [ ] accrual_id (PK)
  - [ ] account_id (FK to accounts)
  - [ ] accrual_date (date)
  - [ ] balance (decimal)
  - [ ] annual_rate (decimal)
  - [ ] daily_interest (decimal)
  - [ ] cumulative_accrued (decimal)
  - [ ] created_at
- [ ] Create table migration script
- [ ] Add indexes on account_id, accrual_date

#### Task 3.2: Interest Application Logic
- [ ] Create `InterestAccrual` domain model
- [ ] Create `InterestService` with methods:
  - [ ] `calculate_daily_interest()` - Calculate for one account/day
  - [ ] `accrue_interest_for_account()` - Accrue for one account
  - [ ] `accrue_interest_for_all_accounts()` - Daily batch job
  - [ ] `post_interest_for_account()` - Post accrued interest
  - [ ] `post_interest_for_all_accounts()` - Monthly batch job
  - [ ] `get_interest_details()` - Get accrual summary
- [ ] Implement interest calculation formula:
  - [ ] Daily Interest = (Balance × Annual Rate × 1) / 365
- [ ] Implement minimum balance check
- [ ] Integrate with TransactionService for posting
- [ ] Write unit tests (test various scenarios)

#### Task 3.3: Interest REST API
- [ ] Create `GET /api/accounts/{id}/interest` endpoint
- [ ] Create `POST /api/batch/interest/accrue` endpoint (manual trigger)
- [ ] Create `POST /api/batch/interest/post` endpoint (manual trigger)
- [ ] Add OpenAPI annotations
- [ ] Test endpoints

#### Task 3.4: Interest UI Components
- [ ] Create `InterestDetails` component
- [ ] Add interest info to AccountDetail page
- [ ] Create admin page for batch job triggers (testing)
- [ ] Test UI

#### Task 3.5: Interest Batch Jobs
- [ ] Create Python script for daily interest accrual
- [ ] Create Python script for monthly interest posting
- [ ] Add scheduling capability (cron-like)
- [ ] Create manual trigger scripts for testing
- [ ] Test batch jobs thoroughly

### Day 14-15: Fees and Charges

#### Task 3.6: Fee Application Logic
- [ ] Create `FeeService` with methods:
  - [ ] `apply_transaction_fee()` - Apply fee after withdrawal
  - [ ] `apply_monthly_maintenance_fee()` - Apply to one account
  - [ ] `apply_monthly_fees_for_all_accounts()` - Monthly batch job
  - [ ] `get_fee_summary()` - Get fees for date range
- [ ] Integrate with TransactionService for fee transactions
- [ ] Implement fee application rules:
  - [ ] Transaction fee after each debit
  - [ ] Monthly fee on first of month
- [ ] Write unit tests

#### Task 3.7: Fee REST API
- [ ] Create `GET /api/accounts/{id}/fees` endpoint
- [ ] Create `POST /api/batch/fees/monthly` endpoint (manual trigger)
- [ ] Modify debit endpoint to include fee application
- [ ] Add OpenAPI annotations
- [ ] Test endpoints

#### Task 3.8: Fee UI Components
- [ ] Create `FeesSummary` component
- [ ] Add fee info to AccountDetail page
- [ ] Show fees in ledger view (distinct category)
- [ ] Create admin page for batch job triggers
- [ ] Test UI

#### Task 3.9: Fee Batch Jobs
- [ ] Create Python script for monthly fee application
- [ ] Add to scheduling system
- [ ] Create manual trigger script
- [ ] Test batch job

---

## Week 4: Integration & Testing

### Day 16-17: Complete Integration

#### Task 4.1: End-to-End Workflows
- [ ] Test complete workflow: Create Product → Create Account → Deposit → Withdraw → View Ledger
- [ ] Test interest workflow: Create account → Daily accrual → Monthly posting
- [ ] Test fee workflow: Withdrawal with fee → Monthly maintenance fee
- [ ] Test edge cases:
  - [ ] Insufficient balance for withdrawal
  - [ ] Close account with non-zero balance
  - [ ] Account with zero balance earning no interest
  - [ ] Multiple concurrent transactions

#### Task 4.2: API Integration Testing
- [ ] Create integration test suite for all endpoints
- [ ] Test authentication flows
- [ ] Test error responses
- [ ] Test validation errors
- [ ] Test HATEOAS links
- [ ] Generate Postman collection for all endpoints

#### Task 4.3: UI Integration Testing
- [ ] Test all UI flows end-to-end
- [ ] Test form validations
- [ ] Test error handling
- [ ] Test loading states
- [ ] Test responsive design
- [ ] Browser compatibility testing

#### Task 4.4: Performance Testing
- [ ] Load test API endpoints (concurrent requests)
- [ ] Test batch job performance (1000 accounts)
- [ ] Optimize slow queries
- [ ] Add database indexes where needed
- [ ] Profile and optimize Rust code

### Day 18: Documentation (Categories 1-9)

#### Task 4.5: Category 1 - Code & Execution
- [ ] Create sample workflow scripts:
  - [ ] `create_account_workflow.py` - Complete account creation example
  - [ ] `process_transactions_workflow.py` - Transaction examples
  - [ ] `interest_calculation_demo.py` - Interest demo
- [ ] Generate execution outputs
- [ ] Save to `/docs/execution/`

#### Task 4.6: Category 2 - Strategic Documentation
- [ ] Write ADRs:
  - [ ] Why SQLite for database
  - [ ] Why Rust for API and business logic
  - [ ] Why React for UI
  - [ ] Interest calculation approach
  - [ ] Transaction locking strategy
- [ ] Create system overview document
- [ ] Write developer onboarding guide
- [ ] Save to `/docs/guides/`

#### Task 4.7: Category 3 - Business Documents
- [ ] Create marketing brochure (MVP features)
- [ ] Write business value proposition
- [ ] Define user personas
- [ ] Create use cases
- [ ] Save to `/docs/business/`

#### Task 4.8: Category 4 - DevOps & Infrastructure
- [ ] Document deployment process
- [ ] Create environment setup guide
- [ ] Document start/stop scripts
- [ ] Create troubleshooting guide
- [ ] Save to `/docs/devops/`

#### Task 4.9: Category 5 - System Architecture Diagrams
- [ ] Create component architecture diagram (Mermaid)
- [ ] Create class diagrams (PlantUML):
  - [ ] Account domain model
  - [ ] Product domain model
  - [ ] Transaction domain model
- [ ] Create sequence diagrams:
  - [ ] Account creation flow
  - [ ] Transaction processing flow
  - [ ] Interest calculation flow
- [ ] Create ERD for database
- [ ] Save to `/docs/architecture/`

#### Task 4.10: Category 6 - Domain Mapping
- [ ] Create domain vocabulary
- [ ] Define bounded contexts
- [ ] Document domain model
- [ ] Create glossary
- [ ] Save to `/docs/domain/`

#### Task 4.11: Category 7 - API Specifications
- [ ] Generate complete OpenAPI/Swagger spec from code
- [ ] Review and enhance descriptions
- [ ] Add request/response examples
- [ ] Document error codes
- [ ] Save to `/docs/api/swagger.yaml`
- [ ] Create API documentation guide
- [ ] Save to `/docs/api/README.md`

#### Task 4.12: Category 8 - Live API Examples
- [ ] Export Postman collection
- [ ] Create cURL examples for all endpoints
- [ ] Create integration examples
- [ ] Document sample payloads
- [ ] Save to `/docs/examples/`

#### Task 4.13: Category 9 - Data Models
- [ ] Create comprehensive API vocabulary (JSON):
  - [ ] All entities and fields
  - [ ] Field types and constraints
  - [ ] Relationships
- [ ] Create database schema documentation
- [ ] Create logical data model doc
- [ ] Create ERD
- [ ] Save to `/docs/data_models/`

### Day 19: RAG System Implementation

#### Task 4.14: Vector Database Setup
- [ ] Install ChromaDB
- [ ] Set up OpenAI API integration
- [ ] Create embedding generation script
- [ ] Configure collection structure
- [ ] Save to `/rag/embeddings/`

#### Task 4.15: Knowledge Base Ingestion
- [ ] Create ingestion script for all 9 categories
- [ ] Generate embeddings for all documentation
- [ ] Store in ChromaDB
- [ ] Test retrieval quality
- [ ] Create refresh script

#### Task 4.16: RAG API Service
- [ ] Create Python FastAPI app (port 6603)
- [ ] Implement query endpoint
- [ ] Integrate with OpenAI for LLM
- [ ] Implement response formatting
- [ ] Test RAG API
- [ ] Save to `/rag/api/`

#### Task 4.17: Chatbot Interface
- [ ] Create React chatbot UI (port 6604)
- [ ] Implement chat components
- [ ] Connect to RAG API
- [ ] Add example questions
- [ ] Test chatbot
- [ ] Save to `/rag/chatbot/`

### Day 20: Finalization & Demo

#### Task 4.18: Final Testing
- [ ] Complete regression testing
- [ ] Security audit (SQL injection, XSS, etc.)
- [ ] Code review
- [ ] Fix any critical bugs

#### Task 4.19: Documentation Review
- [ ] Review all 9 documentation categories
- [ ] Ensure consistency
- [ ] Check for completeness
- [ ] Update any outdated information

#### Task 4.20: Demo Preparation
- [ ] Create demo script
- [ ] Prepare sample data
- [ ] Create presentation slides
- [ ] Record demo video (optional)
- [ ] Prepare Q&A for common questions

#### Task 4.21: Deployment
- [ ] Test start/stop scripts
- [ ] Verify all services start correctly
- [ ] Run health checks
- [ ] Create deployment checklist

#### Task 4.22: Project Cleanup
- [ ] Remove temporary files
- [ ] Update README files
- [ ] Tag MVP release in git
- [ ] Archive MVP documentation

---

## Task Checklist

### Week 1: Foundation ⬜
- [ ] Project structure created
- [ ] Database schema designed
- [ ] Rust application framework set up
- [ ] Rust API framework set up
- [ ] React UI framework set up
- [ ] Authentication implemented
- [ ] DevOps scripts created
- [ ] Product configuration complete (DB + App + API + UI)

### Week 2: Core Features ⬜
- [ ] Account management complete (DB + App + API + UI)
- [ ] Transaction processing complete (DB + App + API + UI)
- [ ] Ledger implementation complete
- [ ] All core APIs tested

### Week 3: Interest & Fees ⬜
- [ ] Interest calculation complete (DB + App + API + UI)
- [ ] Interest batch jobs working
- [ ] Fee application complete (DB + App + API + UI)
- [ ] Fee batch jobs working

### Week 4: Integration & Testing ⬜
- [ ] End-to-end testing complete
- [ ] All 9 documentation categories complete
- [ ] RAG system implemented
- [ ] Chatbot working
- [ ] Demo prepared
- [ ] MVP ready for presentation

---

## Definition of Done

A task is considered "done" when:
- [ ] Code is written and follows best practices
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Deployed and tested in local environment

---

## Dependencies

### Critical Path
1. Database schema must be complete before application logic
2. Application logic must be complete before API implementation
3. API must be complete before UI implementation
4. Authentication must be complete before secured endpoints
5. Product configuration must be complete before account creation
6. Account management must be complete before transactions
7. Transaction processing must be complete before interest/fees

### Parallel Work Opportunities
- Documentation can be written alongside implementation
- UI components can be built with mock data while API is being developed
- RAG system can be started once initial documentation exists
- Batch jobs can be developed after core services are complete

---

**Document Control**:
- **Version**: 1.0
- **Status**: Implementation Plan
- **Owner**: Development Team
- **Start Date**: TBD
- **Target Completion**: TBD + 4 weeks
