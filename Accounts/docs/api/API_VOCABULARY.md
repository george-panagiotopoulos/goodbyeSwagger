# API Vocabulary

This document defines all data entities, fields, and relationships exposed through the Account Processing System API.

## Table of Contents
- [Core Entities](#core-entities)
- [Enumerations](#enumerations)
- [Field Definitions](#field-definitions)
- [Relationships](#relationships)
- [Conventions](#conventions)

---

## Core Entities

### Product
Defines account product types with associated rates, fees, and features.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `product_id` | String | Auto | Primary Key | Unique product identifier (PROD-xxx) |
| `product_code` | String | Yes | Unique, uppercase | Short code for product (e.g., STD_CHECKING) |
| `product_name` | String | Yes | Max 200 chars | Display name for product |
| `description` | String | No | Max 1000 chars | Detailed product description |
| `currency` | String | Yes | ISO 4217 (3 chars) | Currency code (e.g., USD, EUR) |
| `interest_rate` | Decimal | Yes | >= 0, <= 1 | Annual interest rate (0.025 = 2.5%) |
| `minimum_balance_for_interest` | Decimal | Yes | >= 0 | Minimum balance to earn interest |
| `monthly_maintenance_fee` | Decimal | Yes | >= 0 | Fixed monthly fee |
| `transaction_fee` | Decimal | Yes | >= 0 | Fee per debit transaction |
| `status` | Enum | Yes | Active/Inactive | Product availability status |
| `created_at` | DateTime | Auto | ISO 8601 | Record creation timestamp |
| `updated_at` | DateTime | Auto | ISO 8601 | Record last update timestamp |

**Business Rules:**
- Product code must be unique across all products
- Interest rate is expressed as decimal (e.g., 0.025 = 2.5% per annum)
- Inactive products cannot be assigned to new accounts
- Currency cannot be changed after product creation

---

### Customer
Represents a customer who can hold one or more accounts.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customer_id` | String | Auto | Primary Key | Unique customer identifier (CUST-xxx) |
| `external_customer_id` | String | No | Max 100 chars | External system customer reference |
| `customer_name` | String | Yes | Max 200 chars | Full name (individual) or legal name (corporate) |
| `customer_type` | Enum | Yes | Individual/Corporate | Type of customer entity |
| `email` | String | No | Valid email format | Contact email address |
| `phone` | String | No | Max 50 chars | Contact phone number |
| `status` | Enum | Yes | Active/Inactive/Suspended | Customer account status |
| `created_at` | DateTime | Auto | ISO 8601 | Record creation timestamp |
| `updated_at` | DateTime | Auto | ISO 8601 | Record last update timestamp |

**Business Rules:**
- External customer ID is optional but should be unique if provided
- Email must be valid email format if provided
- Suspended customers cannot perform transactions

---

### Account
Represents a checking/current account held by a customer.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `account_id` | String | Auto | Primary Key | Unique account identifier (ACC-{UUID}) |
| `account_number` | String | Auto | Unique, 10 digits | Customer-facing account number |
| `customer_id` | String | Yes | Foreign Key → Customer | Owner of the account |
| `product_id` | String | Yes | Foreign Key → Product | Account product type |
| `currency` | String | Auto | ISO 4217 | Account currency (inherited from product) |
| `status` | Enum | Yes | Active/Closed | Account operational status |
| `balance` | Decimal | Auto | >= 0 (MVP) | Current account balance |
| `interest_accrued` | Decimal | Auto | >= 0 | Cumulative interest accrued |
| `opening_date` | Date | Auto | ISO 8601 | Account opening date |
| `closing_date` | Date | No | ISO 8601 | Account closing date (null if active) |
| `created_at` | DateTime | Auto | ISO 8601 | Record creation timestamp |
| `updated_at` | DateTime | Auto | ISO 8601 | Record last update timestamp |

**Business Rules:**
- Account number auto-generated in format: YYYY000NNN (year + sequential)
- Currency inherited from product and cannot be changed
- Balance cannot be negative (no overdraft in MVP)
- Closed accounts cannot accept new transactions
- Opening date defaults to account creation date

**Derived Fields:**
- `available_balance` = `balance` (no holds/authorization in MVP)
- `total_balance` = `balance` + `interest_accrued`

---

### Transaction
Represents a financial movement (credit or debit) on an account.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transaction_id` | String | Auto | Primary Key | Unique transaction identifier (TXN-{UUID}) |
| `account_id` | String | Yes | Foreign Key → Account | Account affected by transaction |
| `transaction_date` | DateTime | Auto | ISO 8601 | Transaction timestamp |
| `value_date` | Date | Auto | ISO 8601 | Effective date for balance impact |
| `transaction_type` | Enum | Yes | Credit/Debit | Direction of funds movement |
| `category` | Enum | Yes | See categories | Transaction classification |
| `amount` | Decimal | Yes | > 0 | Transaction amount (always positive) |
| `currency` | String | Yes | ISO 4217 | Transaction currency |
| `running_balance` | Decimal | Auto | >= 0 | Account balance after transaction |
| `description` | String | Yes | Max 500 chars | Transaction description |
| `reference` | String | No | Max 100 chars | External reference number |
| `channel` | String | Auto | Max 50 chars | Transaction channel (API/Batch/UI) |
| `status` | String | Auto | Posted | Transaction status (MVP: always Posted) |
| `created_at` | DateTime | Auto | ISO 8601 | Record creation timestamp |
| `created_by` | String | No | User ID | User who created transaction |

**Transaction Categories:**
- **Deposit**: Customer-initiated credit (incoming funds)
- **Withdrawal**: Customer-initiated debit (outgoing funds)
- **Fee**: System-generated debit (transaction/maintenance fees)
- **Interest**: System-generated credit (interest posting)
- **Opening**: Initial account funding transaction

**Business Rules:**
- Amount is always positive; direction indicated by transaction_type
- Running balance calculated as: previous balance ± amount
- Value date defaults to transaction date
- Status is always "Posted" in MVP (no pending/authorized states)

---

### MonthlyInterestAccrual
Tracks month-end interest accrual postings using 30/360 convention.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `monthly_accrual_id` | String | Auto | Primary Key | Unique accrual record identifier (MACRL-{UUID}) |
| `account_id` | String | Yes | Foreign Key → Account | Account receiving interest |
| `accrual_month` | String | Yes | YYYY-MM format | Month of accrual (e.g., "2025-10") |
| `posting_date` | Date | Yes | ISO 8601 | Date interest was posted (month-end) |
| `month_end_balance` | Decimal | Yes | >= 0 | Account balance on last day of month |
| `annual_interest_rate` | Decimal | Yes | >= 0 | Rate used for calculation |
| `monthly_interest` | Decimal | Yes | >= 0 | Calculated monthly interest amount |
| `transaction_id` | String | No | Foreign Key → Transaction | Associated interest transaction |
| `processing_date` | DateTime | Auto | ISO 8601 | When batch process ran |
| `processing_status` | String | Auto | Posted/Failed | Processing result |
| `created_at` | DateTime | Auto | ISO 8601 | Record creation timestamp |

**Interest Calculation (30/360 Convention):**
```
Monthly Interest = (Balance × Annual Rate × 30) / 360
Simplified:       = (Balance × Annual Rate) / 12
```

**Business Rules:**
- Unique constraint on (account_id, accrual_month)
- Month-end date is last day of the accrual month
- Interest only accrued if balance >= minimum_balance_for_interest
- Creates corresponding Transaction record with category=Interest

---

## Enumerations

### ProductStatus
- **Active**: Product available for new accounts
- **Inactive**: Product unavailable, existing accounts continue

### CustomerType
- **Individual**: Personal customer account
- **Corporate**: Business/company account

### CustomerStatus
- **Active**: Customer can perform all operations
- **Inactive**: Customer archived, no operations allowed
- **Suspended**: Temporary restriction on operations

### AccountStatus
- **Active**: Account operational, can accept transactions
- **Closed**: Account permanently closed, no transactions allowed

### TransactionType
- **Credit**: Adds funds to account (increases balance)
- **Debit**: Removes funds from account (decreases balance)

### TransactionCategory
- **Deposit**: Customer-initiated credit
- **Withdrawal**: Customer-initiated debit
- **Fee**: System-generated fee debit
- **Interest**: System-generated interest credit
- **Opening**: Initial account funding

### TransactionChannel
- **API**: Transaction via REST API
- **Batch**: Transaction via batch processing
- **UI**: Transaction via web interface
- **Branch**: Transaction at physical branch (future)
- **ATM**: Transaction at ATM (future)
- **Mobile**: Transaction via mobile app (future)

---

## Relationships

### Entity Relationship Diagram

```
Customer (1) ──────< (M) Account
                            │
                            │ (1)
                            │
Product (1) ────────< (M)   │
                            │
                            V (M)
                        Transaction
                            │
                            │ (0..1)
                            V
                    MonthlyInterestAccrual
```

**Relationship Details:**

1. **Customer → Account**: One-to-Many
   - One customer can have multiple accounts
   - Each account belongs to exactly one customer
   - Foreign Key: `account.customer_id` → `customer.customer_id`

2. **Product → Account**: One-to-Many
   - One product can be assigned to multiple accounts
   - Each account has exactly one product
   - Foreign Key: `account.product_id` → `product.product_id`

3. **Account → Transaction**: One-to-Many
   - One account can have multiple transactions
   - Each transaction belongs to exactly one account
   - Foreign Key: `transaction.account_id` → `account.account_id`

4. **Transaction → MonthlyInterestAccrual**: One-to-One (optional)
   - Interest accrual records link to transaction that posted the interest
   - Optional: not all transactions have accrual records
   - Foreign Key: `monthly_interest_accrual.transaction_id` → `transaction.transaction_id`

---

## Conventions

### Identifier Formats

| Entity | Prefix | Format | Example |
|--------|--------|--------|---------|
| Product | `PROD-` | PROD-NNN | PROD-001 |
| Customer | `CUST-` | CUST-NNN | CUST-005 |
| Account | `ACC-` | ACC-{UUID} | ACC-ca347c63-9969-4920-851c-05ca574edab4 |
| Transaction | `TXN-` | TXN-{UUID} | TXN-79da9f3d-590b-4c80-ba6c-1326c315bec6 |
| Monthly Accrual | `MACRL-` | MACRL-{UUID} | MACRL-abc12345-6789-def0-1234-567890abcdef |
| Account Number | N/A | YYYYNNNNN | 2025000001 |

### Numeric Precision

| Field Type | Precision | Rounding | Example |
|------------|-----------|----------|---------|
| Currency amounts | 2 decimals | Half-up | 100.50 |
| Interest rates | 4 decimals | Half-up | 0.0250 |
| Balances | 2 decimals | Half-up | 12345.67 |

### Date/Time Formats

| Field Type | Format | Timezone | Example |
|------------|--------|----------|---------|
| DateTime | ISO 8601 | UTC | 2025-10-05T12:30:00Z |
| Date | ISO 8601 | N/A | 2025-10-05 |
| Month | YYYY-MM | N/A | 2025-10 |

### Currency Codes
- ISO 4217 standard (3-letter codes)
- Examples: USD, EUR, GBP, JPY
- MVP supports USD only

### String Constraints

| Field Pattern | Max Length | Case | Notes |
|---------------|-----------|------|-------|
| Email | 254 | Mixed | RFC 5322 compliant |
| Phone | 50 | Mixed | International format accepted |
| Product Code | 50 | Upper | Alphanumeric + underscore |
| Description | 1000 | Mixed | Free text |

---

## API Response Format

All API responses follow this structure:

### Success Response
```json
{
  "success": true,
  "data": <response_payload>
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "additional context"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INSUFFICIENT_BALANCE` | 400 | Insufficient funds for transaction |
| `ACCOUNT_NOT_FOUND` | 404 | Account does not exist |
| `PRODUCT_NOT_FOUND` | 404 | Product does not exist |
| `CUSTOMER_NOT_FOUND` | 404 | Customer does not exist |
| `ACCOUNT_CLOSED` | 400 | Account is closed |
| `AUTHENTICATION_REQUIRED` | 401 | Valid JWT token required |
| `INTERNAL_ERROR` | 500 | Server error occurred |

---

## Pagination (Future)

Currently not implemented. All list endpoints return all records.

**Planned Format:**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total_pages": 10,
    "total_records": 485
  }
}
```

---

## Versioning

Current API version: **v1.0.0**

- Version included in base path: `/api/v1/...` (future)
- Current endpoints: `/api/...` (v1 implicit)
- Breaking changes will increment major version
- See [API Changelog](./CHANGELOG.md) for version history

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: Current
