# Minimum Viable Product (MVP) Specification

## Account Processing System - Phase 1

**Document Version**: 1.0
**Last Updated**: 2025-10-04
**Status**: MVP Definition
**Target Scope**: ~30% of Full Feature Set

---

## Table of Contents

1. [MVP Overview](#mvp-overview)
2. [MVP Scope](#mvp-scope)
3. [Included Features](#included-features)
4. [Excluded Features (Roadmap)](#excluded-features-roadmap)
5. [MVP User Stories](#mvp-user-stories)
6. [Success Criteria](#success-criteria)

---

## MVP Overview

### Purpose

The MVP focuses on establishing a **solid foundation** for account processing with core functionality that demonstrates the documentation-first architecture pattern. The MVP includes:

- Basic account lifecycle management
- Simple transaction processing with ledger
- Credit interest calculation with basic formulas
- Static fee configuration and application
- Product configuration with essential parameters

### MVP Philosophy

The MVP is designed to be:
- **Functional**: Users can create accounts, process transactions, and see interest/fees applied
- **Complete**: All included features are fully implemented (not partial)
- **Demonstrable**: Showcases the RAG documentation architecture effectively
- **Extensible**: Architecture supports adding roadmap features without major refactoring

### Estimated Scope

- **Features Included**: ~30% of total functionality
- **Complexity Coverage**: ~40% (includes core complex features like interest and ledger)
- **Time to Implement**: 3-4 weeks
- **Documentation Artifacts**: All 9 categories (but with MVP feature scope)

---

## MVP Scope

### Module 1: Account Processing (MVP)

#### ✅ Included in MVP

1. **Basic Account Management** (FR-AP-001, FR-AP-002, FR-AP-003)
   - Create accounts
   - Inquiry account details and balances
   - Basic status management (Active, Closed only)

2. **Simple Transaction Processing** (FR-AP-019, FR-AP-020)
   - Direct debit (withdrawal)
   - Direct credit (deposit)
   - No authorization/clearing workflow (roadmap)

3. **Transaction Ledger** (FR-AP-013, FR-AP-014, FR-AP-015)
   - Complete ledger entry creation
   - Ledger inquiry with basic filtering
   - Running balance calculation
   - Balance reconciliation

4. **Credit Interest Calculation** (FR-AP-004, FR-AP-005, FR-AP-006)
   - Daily balance method
   - Simple interest calculation
   - Basic formula support (fixed rate or simple formula)
   - Monthly interest posting
   - Interest accrual tracking

5. **Static Fees and Charges** (FR-AP-010)
   - Fixed amount fees only (no formulas in MVP)
   - Monthly maintenance fee
   - Transaction fee (per withdrawal)
   - Fee application and tracking

6. **Basic Balance Management** (FR-AP-023, FR-AP-024)
   - Ledger balance only (no available balance complexity)
   - Real-time balance updates
   - Sufficient funds checking

#### ❌ Excluded from MVP (Roadmap)

1. **Advanced Account Status** (FR-AP-003 partial)
   - Inactive and Suspended status
   - Complex status transitions

2. **Overdraft Management** (FR-AP-007, FR-AP-008, FR-AP-009)
   - Overdraft limits
   - Overdraft utilization
   - Overdraft interest
   - *Reason*: Adds significant complexity, not core to MVP demo

3. **Funds Authorization/Clearing** (FR-AP-016, FR-AP-017, FR-AP-018, FR-AP-019 partial, FR-AP-020 partial)
   - Authorization holds
   - Authorization clearing
   - Two-phase commit for transactions
   - *Reason*: Advanced feature, can be added later

4. **Internal Transfers** (FR-AP-021, FR-AP-022)
   - Transfer between accounts
   - Transfer reversals
   - *Reason*: Can be implemented as two transactions in MVP, full feature in Phase 2

5. **Advanced Interest Features** (FR-AP-004 partial)
   - Tiered interest rates
   - Compound interest
   - Complex formulas
   - Multiple day count conventions (MVP: Actual/365 only)
   - *Reason*: Simple interest sufficient for MVP

6. **Advanced Fee Features** (FR-AP-011, FR-AP-012)
   - Formula-based fees
   - Tiered fees
   - Fee waivers and reversals
   - Conditional fees
   - *Reason*: Static fees sufficient for MVP demo

7. **Account Reporting** (FR-AP-025, FR-AP-026)
   - Formatted account statements
   - Export functionality
   - *Reason*: Ledger inquiry is sufficient for MVP

### Module 2: Product Configuration (MVP)

#### ✅ Included in MVP

1. **Basic Product Management** (FR-PC-001, FR-PC-002, FR-PC-003)
   - Create products
   - Inquiry product details
   - Product status (Active, Inactive only)

2. **Simple Interest Configuration** (FR-PC-004 partial)
   - Fixed interest rate (percentage)
   - Simple interest method only
   - Actual/365 day count convention only
   - Monthly posting frequency only
   - Minimum balance for interest (simple threshold)

3. **Static Fee Configuration** (FR-PC-009 partial)
   - Monthly maintenance fee (fixed amount)
   - Transaction fee (fixed amount per withdrawal)
   - Enable/disable fees

4. **Single Currency Configuration** (FR-PC-013 partial)
   - Primary currency only
   - USD as default
   - No multi-currency support in MVP

5. **Basic Product Versioning** (FR-PC-015 partial)
   - Track configuration changes
   - Simple audit trail (who, when, what changed)
   - No automated version management

#### ❌ Excluded from MVP (Roadmap)

1. **Advanced Interest Configuration** (FR-PC-004 partial, FR-PC-005, FR-PC-006)
   - Compound interest
   - Tiered interest rates
   - Complex interest formulas
   - Multiple day count conventions
   - Overdraft interest configuration
   - Variable posting frequencies
   - *Reason*: Simple fixed rate sufficient for MVP

2. **Overdraft Configuration** (FR-PC-007, FR-PC-008)
   - Overdraft limits
   - Overdraft fees
   - *Reason*: No overdraft in MVP

3. **Advanced Fee Configuration** (FR-PC-010, FR-PC-011, FR-PC-012)
   - Formula-based fees
   - Tiered fee structures
   - Automatic fee waivers
   - Event-based fees
   - *Reason*: Static fees sufficient for MVP

4. **Multi-Currency Support** (FR-PC-014)
   - Multiple currencies per product
   - Currency conversion
   - *Reason*: Single currency sufficient for MVP

5. **Advanced Versioning** (FR-PC-015 partial, FR-PC-016)
   - Automatic version management
   - Impact analysis
   - Version effective dates
   - *Reason*: Basic audit trail sufficient for MVP

6. **Product Templates** (FR-PC-017, FR-PC-018)
   - Template creation
   - Product cloning
   - *Reason*: Nice-to-have, not essential for MVP

7. **Product Reporting** (FR-PC-019, FR-PC-020)
   - Performance reports
   - Product comparison
   - *Reason*: Basic inquiry sufficient for MVP

---

## Included Features

### 1. Account Management (MVP)

**Functional Requirements**: FR-AP-001, FR-AP-002, FR-AP-003 (partial)

#### 1.1 Create Account
**API Endpoint**: `POST /api/accounts`

**Request**:
```json
{
  "customer_id": "CUST-12345",
  "product_id": "PROD-001",
  "currency": "USD",
  "opening_balance": 1000.00,
  "account_nickname": "My Checking Account"
}
```

**Response**:
```json
{
  "account_id": "ACC-67890",
  "account_number": "1234567890",
  "customer_id": "CUST-12345",
  "product_id": "PROD-001",
  "currency": "USD",
  "status": "Active",
  "opening_date": "2025-10-04T10:30:00Z",
  "balance": 1000.00
}
```

**Business Rules**:
- Account MUST be linked to a valid product
- Opening balance MUST be >= 0
- Account number is system-generated (sequential or pattern-based)
- Default status is "Active"

#### 1.2 Get Account Details
**API Endpoint**: `GET /api/accounts/{account_id}`

**Response**:
```json
{
  "account_id": "ACC-67890",
  "account_number": "1234567890",
  "customer_id": "CUST-12345",
  "product_id": "PROD-001",
  "product_name": "Basic Checking",
  "currency": "USD",
  "status": "Active",
  "opening_date": "2025-10-04T10:30:00Z",
  "balance": 1000.00,
  "interest_accrued_to_date": 2.50,
  "last_transaction_date": "2025-10-04T15:30:00Z"
}
```

#### 1.3 Update Account Status
**API Endpoint**: `PATCH /api/accounts/{account_id}/status`

**Request**:
```json
{
  "status": "Closed",
  "reason": "Customer request"
}
```

**Supported Status Transitions (MVP)**:
- Active → Closed (only if balance = 0)

**Roadmap**: Inactive, Suspended statuses and complex transitions

---

### 2. Transaction Processing (MVP)

**Functional Requirements**: FR-AP-019 (partial), FR-AP-020 (partial)

#### 2.1 Debit Transaction (Withdrawal)
**API Endpoint**: `POST /api/accounts/{account_id}/debit`

**Request**:
```json
{
  "amount": 100.00,
  "description": "ATM Withdrawal",
  "reference": "ATM-REF-12345",
  "value_date": "2025-10-04"
}
```

**Response**:
```json
{
  "transaction_id": "TXN-001",
  "account_id": "ACC-67890",
  "type": "Debit",
  "category": "Withdrawal",
  "amount": 100.00,
  "transaction_date": "2025-10-04T15:30:00Z",
  "value_date": "2025-10-04",
  "balance_after": 900.00,
  "status": "Posted",
  "description": "ATM Withdrawal",
  "reference": "ATM-REF-12345"
}
```

**Business Rules**:
- Account MUST be in "Active" status
- Sufficient balance check: amount <= current balance
- No overdraft support in MVP
- Transaction fee applied if configured (e.g., $2.00 withdrawal fee)
- Fee is separate transaction following the main transaction

#### 2.2 Credit Transaction (Deposit)
**API Endpoint**: `POST /api/accounts/{account_id}/credit`

**Request**:
```json
{
  "amount": 500.00,
  "description": "Salary Deposit",
  "reference": "PAYROLL-2025-10",
  "value_date": "2025-10-04"
}
```

**Response**:
```json
{
  "transaction_id": "TXN-002",
  "account_id": "ACC-67890",
  "type": "Credit",
  "category": "Deposit",
  "amount": 500.00,
  "transaction_date": "2025-10-04T16:00:00Z",
  "value_date": "2025-10-04",
  "balance_after": 1400.00,
  "status": "Posted",
  "description": "Salary Deposit",
  "reference": "PAYROLL-2025-10"
}
```

**Business Rules**:
- Credits allowed even if account is not Active (but not Closed)
- No fees on credit transactions (MVP)
- Balance increases immediately

**Roadmap**:
- Authorization/clearing workflow
- Reversal transactions
- Bulk transaction processing

---

### 3. Transaction Ledger (MVP)

**Functional Requirements**: FR-AP-013, FR-AP-014, FR-AP-015

#### 3.1 Ledger Entry Structure

Every transaction creates a ledger entry with:

```json
{
  "transaction_id": "TXN-001",
  "account_id": "ACC-67890",
  "transaction_date": "2025-10-04T15:30:00.123Z",
  "value_date": "2025-10-04",
  "type": "Debit",
  "category": "Withdrawal",
  "amount": 100.00,
  "currency": "USD",
  "running_balance": 900.00,
  "description": "ATM Withdrawal",
  "reference": "ATM-REF-12345",
  "channel": "API",
  "status": "Posted"
}
```

#### 3.2 Get Account Ledger
**API Endpoint**: `GET /api/accounts/{account_id}/ledger`

**Query Parameters**:
- `from_date`: Start date (ISO 8601)
- `to_date`: End date (ISO 8601)
- `type`: Filter by Debit/Credit
- `category`: Filter by category
- `page`: Page number (default: 1)
- `page_size`: Records per page (default: 50, max: 200)

**Response**:
```json
{
  "account_id": "ACC-67890",
  "from_date": "2025-10-01",
  "to_date": "2025-10-04",
  "opening_balance": 1000.00,
  "closing_balance": 1400.00,
  "total_credits": 500.00,
  "total_debits": 100.00,
  "transactions": [
    {
      "transaction_id": "TXN-001",
      "transaction_date": "2025-10-04T15:30:00Z",
      "value_date": "2025-10-04",
      "type": "Debit",
      "category": "Withdrawal",
      "amount": 100.00,
      "running_balance": 900.00,
      "description": "ATM Withdrawal",
      "reference": "ATM-REF-12345"
    },
    {
      "transaction_id": "TXN-002",
      "transaction_date": "2025-10-04T16:00:00Z",
      "value_date": "2025-10-04",
      "type": "Credit",
      "category": "Deposit",
      "amount": 500.00,
      "running_balance": 1400.00,
      "description": "Salary Deposit",
      "reference": "PAYROLL-2025-10"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_records": 2,
    "total_pages": 1
  }
}
```

#### 3.3 Balance Reconciliation
**API Endpoint**: `GET /api/accounts/{account_id}/reconcile`

**Response**:
```json
{
  "account_id": "ACC-67890",
  "opening_balance": 1000.00,
  "total_credits": 500.00,
  "total_debits": 100.00,
  "calculated_balance": 1400.00,
  "current_balance": 1400.00,
  "is_balanced": true,
  "discrepancy": 0.00
}
```

**Business Rules**:
- Ledger entries are immutable (no updates or deletes)
- Running balance recalculated on each transaction
- Chronological order maintained (by transaction_date)
- All transactions tracked (debits, credits, fees, interest)

**Roadmap**:
- Transaction reversals (new transactions, not deletions)
- Advanced ledger analytics
- Export to PDF/CSV

---

### 4. Interest Calculation (MVP)

**Functional Requirements**: FR-AP-004, FR-AP-005, FR-AP-006

#### 4.1 Interest Accrual Process

**Daily Process** (automated batch job):
1. For each account with balance > 0:
2. Retrieve interest rate from product configuration
3. Calculate daily interest: `(Balance × Annual Rate × 1) / 365`
4. Add to interest accrual accumulator
5. Store accrual record

**Interest Accrual Record**:
```json
{
  "account_id": "ACC-67890",
  "accrual_date": "2025-10-04",
  "balance": 1400.00,
  "annual_rate": 0.025,
  "daily_interest": 0.096,
  "cumulative_accrued": 2.50
}
```

#### 4.2 Interest Posting

**Monthly Process** (automated batch job on last day of month):
1. For each account with accrued interest > 0:
2. Sum all accrued interest for the month
3. Create credit transaction for interest amount
4. Category: "Interest"
5. Update account balance
6. Reset accrual accumulator

**Interest Posting Transaction**:
```json
{
  "transaction_id": "TXN-INT-001",
  "account_id": "ACC-67890",
  "type": "Credit",
  "category": "Interest",
  "amount": 2.50,
  "transaction_date": "2025-10-31T23:59:59Z",
  "value_date": "2025-10-31",
  "balance_after": 1402.50,
  "description": "Interest for October 2025",
  "status": "Posted"
}
```

#### 4.3 Get Interest Details
**API Endpoint**: `GET /api/accounts/{account_id}/interest`

**Response**:
```json
{
  "account_id": "ACC-67890",
  "annual_rate": 0.025,
  "day_count_convention": "Actual/365",
  "current_balance": 1400.00,
  "accrued_to_date": 2.50,
  "last_accrual_date": "2025-10-04",
  "last_posting_date": "2025-09-30",
  "next_posting_date": "2025-10-31",
  "estimated_monthly_interest": 2.92
}
```

**MVP Simplifications**:
- Simple interest only (no compounding)
- Fixed interest rate from product (no formulas in MVP)
- Actual/365 day count convention only
- Monthly posting on last day of month only
- Interest calculated on positive balances only (no overdraft interest)

**Roadmap**:
- Tiered interest rates
- Formula-based interest calculation
- Multiple day count conventions
- Flexible posting frequencies
- Compound interest
- Overdraft interest

---

### 5. Fees and Charges (MVP)

**Functional Requirements**: FR-AP-010 (partial)

#### 5.1 Static Fee Types (MVP)

**Monthly Maintenance Fee**:
- Fixed amount (e.g., $10.00)
- Applied on first day of month
- Configured at product level

**Transaction Fee**:
- Fixed amount per withdrawal (e.g., $2.00)
- Applied immediately after debit transaction
- Configured at product level

#### 5.2 Fee Application Process

**Monthly Maintenance Fee** (automated batch job):
1. On first day of month, for each active account:
2. Retrieve monthly fee from product configuration
3. If fee > 0, create debit transaction
4. Category: "Fee - Maintenance"
5. Update account balance

**Transaction Fee** (real-time):
1. After successful debit transaction:
2. Retrieve transaction fee from product configuration
3. If fee > 0, create separate debit transaction
4. Category: "Fee - Transaction"
5. Update account balance

**Fee Transaction Example**:
```json
{
  "transaction_id": "TXN-FEE-001",
  "account_id": "ACC-67890",
  "type": "Debit",
  "category": "Fee - Transaction",
  "amount": 2.00,
  "transaction_date": "2025-10-04T15:30:01Z",
  "value_date": "2025-10-04",
  "balance_after": 898.00,
  "description": "Withdrawal fee",
  "reference": "TXN-001",
  "status": "Posted"
}
```

#### 5.3 Get Fee Summary
**API Endpoint**: `GET /api/accounts/{account_id}/fees`

**Query Parameters**:
- `from_date`: Start date
- `to_date`: End date

**Response**:
```json
{
  "account_id": "ACC-67890",
  "from_date": "2025-10-01",
  "to_date": "2025-10-04",
  "fees": [
    {
      "fee_type": "Monthly Maintenance",
      "count": 1,
      "total_amount": 10.00
    },
    {
      "fee_type": "Transaction Fee",
      "count": 5,
      "total_amount": 10.00
    }
  ],
  "total_fees": 20.00
}
```

**MVP Simplifications**:
- Fixed amount fees only (no percentages or formulas)
- Two fee types only (maintenance and transaction)
- No fee waivers or reversals
- No tiered fees
- Fees always applied (no conditional logic)

**Roadmap**:
- Formula-based fees
- Fee waivers (balance-based, relationship-based)
- Fee reversals
- Tiered fee structures
- Event-based fees (overdraft, statement, etc.)
- Fee caps and minimums

---

### 6. Product Configuration (MVP)

**Functional Requirements**: FR-PC-001, FR-PC-002, FR-PC-003, FR-PC-004 (partial), FR-PC-009 (partial), FR-PC-013 (partial)

#### 6.1 Create Product
**API Endpoint**: `POST /api/products`

**Request**:
```json
{
  "product_name": "Basic Checking",
  "product_code": "CHK-BASIC-001",
  "description": "Basic checking account with simple interest",
  "status": "Active",
  "currency": "USD",
  "interest_rate": 0.025,
  "interest_posting_frequency": "Monthly",
  "minimum_balance_for_interest": 100.00,
  "monthly_maintenance_fee": 10.00,
  "transaction_fee": 2.00
}
```

**Response**:
```json
{
  "product_id": "PROD-001",
  "product_name": "Basic Checking",
  "product_code": "CHK-BASIC-001",
  "description": "Basic checking account with simple interest",
  "status": "Active",
  "effective_date": "2025-10-04T10:00:00Z",
  "currency": "USD",
  "interest_config": {
    "annual_rate": 0.025,
    "calculation_method": "Simple",
    "day_count_convention": "Actual/365",
    "posting_frequency": "Monthly",
    "minimum_balance": 100.00
  },
  "fee_config": {
    "monthly_maintenance_fee": 10.00,
    "transaction_fee": 2.00
  }
}
```

#### 6.2 Get Product Details
**API Endpoint**: `GET /api/products/{product_id}`

**Response**: Same as create response

#### 6.3 Update Product
**API Endpoint**: `PUT /api/products/{product_id}`

**Request**: Same structure as create (partial updates supported)

**Response**: Updated product details

**Business Rules**:
- Product updates create audit trail entry
- Changes apply to new accounts immediately
- Existing accounts retain old configuration (MVP - no automatic migration)
- Product name and code MUST be unique

#### 6.4 List Products
**API Endpoint**: `GET /api/products`

**Query Parameters**:
- `status`: Filter by status (Active, Inactive)
- `currency`: Filter by currency

**Response**:
```json
{
  "products": [
    {
      "product_id": "PROD-001",
      "product_name": "Basic Checking",
      "product_code": "CHK-BASIC-001",
      "status": "Active",
      "currency": "USD",
      "account_count": 150
    },
    {
      "product_id": "PROD-002",
      "product_name": "Premium Checking",
      "product_code": "CHK-PREM-001",
      "status": "Active",
      "currency": "USD",
      "account_count": 45
    }
  ],
  "total_products": 2
}
```

**MVP Simplifications**:
- Simple product structure (flat, not nested)
- No product versioning (updates overwrite)
- No product templates or cloning
- Single currency per product
- No impact analysis for changes

**Roadmap**:
- Product versioning with effective dates
- Impact analysis before changes
- Product templates and cloning
- Multi-currency support
- Product performance analytics

---

### 7. Balance Management (MVP)

**Functional Requirements**: FR-AP-023 (partial), FR-AP-024

#### 7.1 Balance Calculation

**MVP Balance Types**:
- **Ledger Balance**: Current balance including all posted transactions
  ```
  Ledger Balance = Opening Balance + Sum(Credits) - Sum(Debits)
  ```

**Balance Update Process**:
1. Lock account record (pessimistic locking)
2. Validate sufficient funds for debits
3. Create transaction
4. Update balance
5. Create ledger entry with running balance
6. Release lock
7. Commit transaction (database transaction)

**Concurrency Handling**:
- Database-level locking prevents race conditions
- Transactions are serialized per account
- ACID compliance ensures consistency

**Roadmap Balance Types**:
- **Available Balance**: Ledger balance minus holds/authorizations
- **Cleared Balance**: Only value-dated transactions
- **Overdraft Utilized**: Amount of overdraft in use
- **Overdraft Available**: Remaining overdraft

---

## Excluded Features (Roadmap)

### Phase 2: Advanced Transaction Processing
**Estimated Time**: 2 weeks

- **Funds Authorization & Clearing** (FR-AP-016, FR-AP-017, FR-AP-018)
  - Hold funds without debiting
  - Clear authorizations
  - Authorization expiry and release

- **Internal Transfers** (FR-AP-021, FR-AP-022)
  - Atomic transfer between accounts
  - Transfer reversals
  - Transfer fees

- **Transaction Reversals**
  - Reverse posted transactions
  - Reversal audit trail

- **Additional Account Statuses** (FR-AP-003 partial)
  - Inactive (no debits allowed)
  - Suspended (no transactions)
  - Status transition workflows

### Phase 3: Overdraft Management
**Estimated Time**: 1.5 weeks

- **Overdraft Configuration** (FR-PC-007, FR-PC-008)
  - Overdraft limits at product and account level
  - Overdraft fees

- **Overdraft Processing** (FR-AP-007, FR-AP-008, FR-AP-009)
  - Overdraft utilization
  - Overdraft interest calculation
  - Overdraft interest posting

- **Available Balance Calculation**
  - Balance including overdraft
  - Overdraft utilized tracking

### Phase 4: Advanced Interest & Fees
**Estimated Time**: 2 weeks

- **Advanced Interest** (FR-AP-004 partial, FR-PC-004 partial, FR-PC-005, FR-PC-006)
  - Tiered interest rates
  - Compound interest
  - Formula-based interest calculation
  - Multiple day count conventions
  - Flexible posting frequencies
  - Interest rate formulas with conditions

- **Advanced Fees** (FR-AP-011, FR-AP-012, FR-PC-010, FR-PC-011, FR-PC-012)
  - Formula-based fees
  - Tiered fee structures
  - Fee waivers (automatic and manual)
  - Fee reversals
  - Percentage-based fees
  - Conditional fees
  - Fee caps and minimums

### Phase 5: Multi-Currency & Product Features
**Estimated Time**: 1.5 weeks

- **Multi-Currency** (FR-PC-013, FR-PC-014)
  - Multiple currencies per product
  - Currency-specific rates and fees
  - Currency conversion for transfers

- **Product Versioning** (FR-PC-015, FR-PC-016)
  - Automatic version management
  - Effective dates for versions
  - Impact analysis
  - Account migration to new versions

- **Product Templates** (FR-PC-017, FR-PC-018)
  - Create product templates
  - Clone products
  - Template library

### Phase 6: Reporting & Analytics
**Estimated Time**: 1 week

- **Account Statements** (FR-AP-025, FR-AP-026)
  - Generate formatted statements
  - PDF and CSV export
  - Statement scheduling

- **Product Analytics** (FR-PC-019, FR-PC-020)
  - Product performance reports
  - Product comparison
  - Profitability analysis

- **Advanced Ledger Features**
  - Advanced filtering and search
  - Bulk export
  - Ledger analytics

---

## MVP User Stories

### As a Bank Administrator

**Story 1: Create Account Product**
```
As a bank administrator,
I want to create a new checking account product with interest rate and fees,
So that customers can open accounts with predefined terms.

Acceptance Criteria:
- I can set product name, code, and description
- I can configure a fixed annual interest rate (e.g., 2.5%)
- I can set monthly maintenance fee and transaction fee
- I can set minimum balance required to earn interest
- Product is available immediately for account creation
```

**Story 2: Modify Product Configuration**
```
As a bank administrator,
I want to update product interest rates and fees,
So that I can adapt to market conditions.

Acceptance Criteria:
- I can update interest rate
- I can update fee amounts
- Changes are audited (who, when, what changed)
- Existing accounts are not automatically affected
```

### As an Account Officer

**Story 3: Open New Account**
```
As an account officer,
I want to open a new checking account for a customer,
So that they can start using banking services.

Acceptance Criteria:
- I can select a product from available products
- I can set an opening balance (optional)
- Account number is automatically generated
- Account is immediately active
- Opening balance creates initial ledger entry
```

**Story 4: Process Deposit**
```
As an account officer,
I want to process a deposit to a customer's account,
So that their balance increases.

Acceptance Criteria:
- I can enter deposit amount and description
- Balance updates immediately
- Ledger entry is created with running balance
- Transaction confirmation is provided
```

**Story 5: Process Withdrawal**
```
As an account officer,
I want to process a withdrawal from a customer's account,
So that customers can access their funds.

Acceptance Criteria:
- System checks sufficient balance before allowing withdrawal
- Transaction fee is automatically applied (if configured)
- Balance updates immediately
- Ledger entries created for withdrawal and fee
- Transaction is rejected if insufficient funds
```

### As a Customer (via UI)

**Story 6: View Account Balance**
```
As a customer,
I want to view my current account balance,
So that I know how much money I have.

Acceptance Criteria:
- I can see my current balance
- I can see interest accrued to date
- I can see last transaction date
- Information is real-time
```

**Story 7: View Transaction History**
```
As a customer,
I want to view my transaction history,
So that I can track my account activity.

Acceptance Criteria:
- I can see all transactions in chronological order
- Each transaction shows date, type, amount, description, and balance after
- I can filter by date range
- I can see running balance for each transaction
- Results are paginated for large histories
```

**Story 8: View Interest Earnings**
```
As a customer,
I want to see my interest earnings,
So that I understand how my money is growing.

Acceptance Criteria:
- I can see my interest rate
- I can see interest accrued this month
- I can see last interest posting date and amount
- I can see estimated monthly interest
```

### As a System (Batch Jobs)

**Story 9: Daily Interest Accrual**
```
As the system,
I want to calculate and accrue interest daily,
So that interest is accurately tracked.

Acceptance Criteria:
- Process runs automatically each day
- Interest calculated for all accounts with balance > minimum
- Daily interest = (Balance × Annual Rate) / 365
- Accrual records are created and tracked
- Process completes successfully with audit log
```

**Story 10: Monthly Interest Posting**
```
As the system,
I want to post accrued interest monthly,
So that customers receive their interest earnings.

Acceptance Criteria:
- Process runs on last day of each month
- All accrued interest is summed
- Credit transaction created for interest amount
- Account balance updated
- Accrual counter reset for next month
```

**Story 11: Monthly Fee Application**
```
As the system,
I want to apply monthly maintenance fees,
So that account costs are charged.

Acceptance Criteria:
- Process runs on first day of each month
- Fee amount from product configuration
- Debit transaction created for fee
- Account balance updated
- Process handles insufficient balance gracefully
```

---

## Success Criteria

### Functional Success Criteria

✅ **Account Operations**:
- [ ] Can create accounts linked to products
- [ ] Can process deposits (credits)
- [ ] Can process withdrawals (debits) with balance checking
- [ ] Can view account details and balance
- [ ] Can close accounts (when balance = 0)

✅ **Ledger & Transactions**:
- [ ] All transactions create ledger entries
- [ ] Running balance calculated correctly
- [ ] Ledger inquiry works with date range filtering
- [ ] Balance reconciliation matches ledger
- [ ] Transactions are immutable

✅ **Interest Calculation**:
- [ ] Daily interest accrual works correctly
- [ ] Interest calculated on balances above minimum
- [ ] Monthly interest posting creates transactions
- [ ] Interest accrual tracking is accurate
- [ ] Interest rate from product configuration is applied

✅ **Fees**:
- [ ] Monthly maintenance fee applied automatically
- [ ] Transaction fee applied on withdrawals
- [ ] Fees create ledger entries
- [ ] Fee configuration at product level works

✅ **Product Configuration**:
- [ ] Can create products with interest and fee settings
- [ ] Can update product configurations
- [ ] Can view product details
- [ ] Products can be activated/deactivated
- [ ] Accounts inherit product configuration

### Technical Success Criteria

✅ **API Layer**:
- [ ] All REST endpoints return correct responses
- [ ] Authentication works (JWT tokens)
- [ ] Error handling returns meaningful messages
- [ ] API follows HATEOAS principles (basic links)
- [ ] OpenAPI/Swagger spec is complete

✅ **Database**:
- [ ] SQLite database with proper schema
- [ ] ACID transactions ensure data consistency
- [ ] Concurrent transactions handled safely
- [ ] Database can be backed up and restored

✅ **Business Logic**:
- [ ] Rust business logic layer functions correctly
- [ ] Validation rules enforced
- [ ] Calculations are accurate (interest, fees, balances)
- [ ] Unit tests pass with >80% coverage

✅ **User Interface**:
- [ ] React UI can perform all account operations
- [ ] UI displays real-time balance updates
- [ ] Ledger view shows transaction history
- [ ] Form validation works correctly
- [ ] Responsive design works on mobile

✅ **System Scripts**:
- [ ] `start.sh` starts all components successfully
- [ ] `stop.sh` stops all components gracefully
- [ ] Health checks verify all services running
- [ ] Batch jobs can be run manually for testing

### Documentation Success Criteria

✅ **Documentation Artifacts** (All 9 Categories):
- [ ] **Category 1**: Sample workflow scripts for account creation, transactions
- [ ] **Category 2**: ADRs, technical design docs, developer guide
- [ ] **Category 3**: Business value proposition, user personas, use cases
- [ ] **Category 4**: Deployment guide, start/stop scripts documented
- [ ] **Category 5**: Component diagram, sequence diagrams, ERD
- [ ] **Category 6**: Domain vocabulary, bounded context
- [ ] **Category 7**: Complete OpenAPI/Swagger spec for MVP APIs
- [ ] **Category 8**: Postman collection with all MVP endpoints
- [ ] **Category 9**: API vocabulary, database schema docs, data model

✅ **RAG System**:
- [ ] Vector database contains all MVP documentation
- [ ] Chatbot can answer questions about MVP features
- [ ] RAG API returns accurate context
- [ ] Response time < 5 seconds
- [ ] Citations reference correct documents

✅ **Claude Code Integration**:
- [ ] Project structure allows Claude Code to understand codebase
- [ ] Can generate new endpoints using existing patterns
- [ ] Can create sample data using documentation
- [ ] Documentation artifacts provide sufficient context

### Performance Success Criteria

✅ **Response Times**:
- [ ] Account creation: < 500ms
- [ ] Transaction processing: < 500ms
- [ ] Balance inquiry: < 200ms
- [ ] Ledger query (100 records): < 1 second
- [ ] Product configuration: < 500ms

✅ **Batch Processing**:
- [ ] Daily interest accrual for 1000 accounts: < 5 minutes
- [ ] Monthly interest posting for 1000 accounts: < 5 minutes
- [ ] Monthly fee application for 1000 accounts: < 5 minutes

### Quality Success Criteria

✅ **Testing**:
- [ ] Unit test coverage > 80%
- [ ] Integration tests for all API endpoints
- [ ] End-to-end tests for key workflows
- [ ] All tests pass in CI/CD pipeline

✅ **Code Quality**:
- [ ] Code follows Rust, Python, and React best practices
- [ ] No critical security vulnerabilities
- [ ] Code is properly formatted (rustfmt, black, prettier)
- [ ] Code is documented with inline comments

---

## MVP Timeline

### Week 1: Foundation
- Project structure setup
- Database schema design and implementation
- Basic API framework (authentication, middleware)
- Start documentation (Categories 2, 4, 5)

### Week 2: Core Features
- Account management (create, inquiry, status)
- Transaction processing (debit, credit)
- Ledger implementation
- Product configuration (create, update, inquiry)
- Continue documentation (Categories 1, 6, 7, 9)

### Week 3: Interest & Fees
- Interest calculation logic
- Daily accrual batch job
- Monthly posting batch job
- Fee application (maintenance, transaction)
- UI implementation (account views, transaction forms)
- Complete documentation (Categories 3, 8)

### Week 4: Integration & Testing
- React UI completion
- End-to-end testing
- RAG system implementation
- Chatbot interface
- start/stop scripts
- Final documentation review
- Demo preparation

**Total MVP Timeline**: 4 weeks

---

## MVP Risks & Mitigations

### Risk 1: Interest Calculation Complexity
**Risk**: Interest calculation may be more complex than anticipated
**Mitigation**: MVP uses simplest method (simple interest, Actual/365, fixed rate)
**Fallback**: Defer interest to Phase 2 if needed

### Risk 2: Concurrent Transaction Handling
**Risk**: Race conditions in balance updates
**Mitigation**: Use database-level pessimistic locking
**Fallback**: Serialize all transactions for an account (performance trade-off)

### Risk 3: RAG System Quality
**Risk**: RAG retrieval quality may be poor with limited data
**Mitigation**: Focus on quality of documentation, not quantity
**Fallback**: Use simpler keyword search initially

### Risk 4: Timeline Slippage
**Risk**: 4-week timeline may be optimistic
**Mitigation**: Prioritize core features, reduce UI complexity if needed
**Fallback**: Extend to 5 weeks, defer UI polish to post-MVP

---

## Post-MVP Roadmap Summary

**Phase 2**: Advanced Transaction Processing (2 weeks)
**Phase 3**: Overdraft Management (1.5 weeks)
**Phase 4**: Advanced Interest & Fees (2 weeks)
**Phase 5**: Multi-Currency & Product Features (1.5 weeks)
**Phase 6**: Reporting & Analytics (1 week)

**Total Roadmap**: 8 weeks after MVP
**Complete Project**: 12 weeks total

---

## Appendix: MVP API Endpoints Summary

### Account Management
- `POST /api/accounts` - Create account
- `GET /api/accounts/{account_id}` - Get account details
- `PATCH /api/accounts/{account_id}/status` - Update status
- `GET /api/accounts/{account_id}/ledger` - Get ledger
- `GET /api/accounts/{account_id}/reconcile` - Reconcile balance
- `GET /api/accounts/{account_id}/interest` - Get interest details
- `GET /api/accounts/{account_id}/fees` - Get fee summary

### Transactions
- `POST /api/accounts/{account_id}/debit` - Process withdrawal
- `POST /api/accounts/{account_id}/credit` - Process deposit

### Product Configuration
- `POST /api/products` - Create product
- `GET /api/products` - List products
- `GET /api/products/{product_id}` - Get product details
- `PUT /api/products/{product_id}` - Update product

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token

**Total MVP Endpoints**: 15

---

**Document Control**:
- **Version**: 1.0
- **Status**: MVP Definition
- **Approval**: Pending
- **Next Review**: After MVP completion

