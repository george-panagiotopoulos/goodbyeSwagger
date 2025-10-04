# Database Layer - Account Processing System

## Overview

This directory contains the SQLite database implementation for the Account Processing System MVP. The database layer is implemented using Python scripts for management and SQLite for data storage.

## Technology

- **Database**: SQLite 3.x
- **Language**: Python 3.11+
- **Port**: 6602 (if database API is exposed)

## Directory Structure

```
Database/
├── schema/
│   ├── migrations/          # Database migration scripts
│   │   └── 001_initial_schema.sql
│   └── seed/                # Seed data scripts
│       ├── 001_seed_users.sql
│       ├── 002_seed_products.sql
│       └── 003_seed_test_accounts.sql
├── scripts/                 # Python utility scripts
│   ├── init_db.py           # Initialize database
│   ├── seed_data.py         # Load seed data
│   └── backup.py            # Backup database (to be created)
├── tests/                   # Database tests
│   └── test_schema.py       # Schema validation tests (to be created)
├── accounts.db              # SQLite database file (generated)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Database Schema

### Tables

#### 1. users
User authentication and authorization

| Column | Type | Description |
|--------|------|-------------|
| user_id | TEXT | Primary key |
| username | TEXT | Unique username |
| password_hash | TEXT | Bcrypt hashed password |
| full_name | TEXT | User's full name |
| email | TEXT | Unique email address |
| role | TEXT | User role (admin, officer, viewer) |
| status | TEXT | Account status (active, inactive) |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |

#### 2. products
Product configurations for checking accounts

| Column | Type | Description |
|--------|------|-------------|
| product_id | TEXT | Primary key |
| product_name | TEXT | Unique product name |
| product_code | TEXT | Unique product code |
| description | TEXT | Product description |
| status | TEXT | Active/Inactive |
| currency | TEXT | ISO 4217 currency code (3 chars) |
| interest_rate | REAL | Annual interest rate (0.0-1.0) |
| minimum_balance_for_interest | REAL | Minimum balance to earn interest |
| monthly_maintenance_fee | REAL | Fixed monthly fee |
| transaction_fee | REAL | Fee per withdrawal transaction |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |
| created_by | TEXT | User who created (FK to users) |

#### 3. accounts
Customer checking accounts

| Column | Type | Description |
|--------|------|-------------|
| account_id | TEXT | Primary key |
| account_number | TEXT | Unique account number |
| customer_id | TEXT | Customer identifier |
| product_id | TEXT | FK to products |
| currency | TEXT | ISO 4217 currency code |
| status | TEXT | Active/Closed |
| balance | REAL | Current balance (>= 0) |
| interest_accrued | REAL | Interest accrued to date |
| opening_date | TEXT | Account opening date |
| closing_date | TEXT | Account closing date (nullable) |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |
| created_by | TEXT | User who created (FK to users) |

#### 4. transactions
Transaction ledger with complete history

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | TEXT | Primary key |
| account_id | TEXT | FK to accounts |
| transaction_date | TEXT | Transaction timestamp |
| value_date | TEXT | Value date for balance calculation |
| type | TEXT | Debit/Credit |
| category | TEXT | Deposit/Withdrawal/Fee/Interest/Opening |
| amount | REAL | Transaction amount (> 0) |
| currency | TEXT | ISO 4217 currency code |
| running_balance | REAL | Balance after transaction |
| description | TEXT | Transaction description |
| reference | TEXT | External reference |
| channel | TEXT | API/UI/Batch |
| status | TEXT | Posted (MVP only has Posted status) |
| created_at | TEXT | Creation timestamp |
| created_by | TEXT | User who created (FK to users) |

#### 5. interest_accruals
Daily interest accrual tracking

| Column | Type | Description |
|--------|------|-------------|
| accrual_id | TEXT | Primary key |
| account_id | TEXT | FK to accounts |
| accrual_date | TEXT | Date of accrual |
| balance | REAL | Balance used for calculation |
| annual_rate | REAL | Interest rate applied |
| daily_interest | REAL | Interest accrued for this day |
| cumulative_accrued | REAL | Total accrued in period |
| created_at | TEXT | Creation timestamp |

**Unique constraint**: (account_id, accrual_date) - one accrual per account per day

#### 6. audit_log
Audit trail for all operations

| Column | Type | Description |
|--------|------|-------------|
| audit_id | TEXT | Primary key |
| event_type | TEXT | Type of event |
| entity_type | TEXT | Type of entity (Account, Transaction, etc.) |
| entity_id | TEXT | ID of affected entity |
| user_id | TEXT | User who performed action (FK to users) |
| timestamp | TEXT | Event timestamp |
| event_data | TEXT | JSON data (before/after values) |
| ip_address | TEXT | IP address of request |
| channel | TEXT | Channel (API, UI, Batch) |

### Views

#### v_account_summary
Combines account and product information for quick access

```sql
SELECT
    a.account_id,
    a.account_number,
    a.customer_id,
    a.status,
    a.balance,
    a.interest_accrued,
    p.product_name,
    p.interest_rate,
    p.monthly_maintenance_fee,
    -- ... and more
FROM accounts a
INNER JOIN products p ON a.product_id = p.product_id;
```

#### v_transaction_ledger
Combines transaction and account information

```sql
SELECT
    t.transaction_id,
    t.account_id,
    a.account_number,
    a.customer_id,
    t.transaction_date,
    t.type,
    t.amount,
    -- ... and more
FROM transactions t
INNER JOIN accounts a ON t.account_id = a.account_id;
```

### Indexes

- **users**: username, email, status
- **products**: status, currency, product_code
- **accounts**: account_number, customer_id, product_id, status, opening_date
- **transactions**: account_id, transaction_date, value_date, type, category, status
- **interest_accruals**: account_id, accrual_date

### Triggers

- **Auto-update timestamps**: `updated_at` fields are automatically updated on UPDATE
- Triggers for: users, products, accounts

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd Accounts/Database
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python scripts/init_db.py
```

This will:
- Create `accounts.db` file
- Run all migration scripts
- Create all tables, views, indexes, and triggers

### 4. Load Seed Data (Optional)

```bash
python scripts/seed_data.py
```

This will:
- Load test users (admin, officer, viewer)
- Load sample products (5 active, 1 inactive)
- Load sample accounts (6 test accounts)
- Load opening balance transactions

## Seed Data

### Test Users

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | admin | admin@accountsystem.com |
| officer | officer123 | officer | officer@accountsystem.com |
| viewer | viewer123 | viewer | viewer@accountsystem.com |

### Sample Products

1. **Basic Checking** (CHK-BASIC-001)
   - Interest: 1.5% annual
   - Min balance for interest: $100
   - Monthly fee: $5
   - Transaction fee: $1

2. **Premium Checking** (CHK-PREM-001)
   - Interest: 2.5% annual
   - Min balance for interest: $500
   - Monthly fee: $15
   - Transaction fee: $0

3. **Student Checking** (CHK-STUDENT-001)
   - Interest: 1.0% annual
   - Min balance for interest: $0
   - Monthly fee: $0
   - Transaction fee: $0

4. **High-Yield Savings** (SAV-HIGH-001)
   - Interest: 4.0% annual
   - Min balance for interest: $1000
   - Monthly fee: $0
   - Transaction fee: $3

5. **Business Checking** (CHK-BUS-001)
   - Interest: 2.0% annual
   - Min balance for interest: $1000
   - Monthly fee: $25
   - Transaction fee: $0.50

### Sample Accounts

6 test accounts across 5 customers with balances ranging from $50 to $12,500

## Database Operations

### Connect to Database

```bash
sqlite3 accounts.db
```

### View Schema

```sql
.schema
```

### View Tables

```sql
.tables
```

### Query Examples

```sql
-- List all products
SELECT * FROM products WHERE status = 'Active';

-- List all accounts
SELECT * FROM v_account_summary;

-- Get account transactions
SELECT * FROM v_transaction_ledger
WHERE account_id = 'ACC-2025100401'
ORDER BY transaction_date DESC;

-- Calculate total balances
SELECT SUM(balance) as total_balance FROM accounts WHERE status = 'Active';
```

### Backup Database

```bash
# Simple file copy
cp accounts.db accounts_backup_$(date +%Y%m%d).db

# Or use SQLite backup
sqlite3 accounts.db ".backup accounts_backup.db"
```

## Data Integrity

### Constraints

- **Foreign Keys**: Enabled and enforced
- **Check Constraints**:
  - Balance >= 0 (no overdraft in MVP)
  - Interest rate 0.0 - 1.0
  - Currency codes exactly 3 characters
  - Status values restricted to defined enums
- **Unique Constraints**:
  - account_number (accounts)
  - product_name, product_code (products)
  - username, email (users)
  - account_id + accrual_date (interest_accruals)

### Referential Integrity

- Accounts reference valid products
- Transactions reference valid accounts (cascade delete)
- Interest accruals reference valid accounts (cascade delete)
- Audit logs reference valid users

## Performance Considerations

### Indexes

All frequently queried columns have indexes:
- Primary keys (automatic)
- Foreign keys
- Status fields
- Date fields
- Composite indexes for common queries (account_id + date)

### Query Optimization

- Use views for common joins (v_account_summary, v_transaction_ledger)
- Pagination for large result sets
- Date range filters on indexed columns

## Migrations

### Creating a New Migration

1. Create new file: `schema/migrations/00X_description.sql`
2. Use sequential numbering (002, 003, etc.)
3. Include comments describing changes
4. Test migration on copy of database first

### Migration Best Practices

- Always use `IF NOT EXISTS` for CREATE statements
- Include rollback instructions in comments
- Test with existing data
- Backup database before running migrations

## Testing

### Run Tests

```bash
pytest tests/
```

### Test Coverage

```bash
pytest --cov=scripts --cov-report=html
```

## Troubleshooting

### Database Locked Error

**Cause**: Another process has the database open
**Solution**:
- Close all connections to the database
- Use WAL mode: `PRAGMA journal_mode=WAL;`

### Foreign Key Constraint Failed

**Cause**: Referenced entity doesn't exist
**Solution**:
- Verify foreign key references
- Check data integrity
- Ensure foreign keys are enabled: `PRAGMA foreign_keys = ON;`

### Migration Failed

**Cause**: SQL syntax error or constraint violation
**Solution**:
- Check migration script syntax
- Restore from backup
- Fix script and re-run

## Security

### Password Storage

- Passwords hashed with bcrypt (cost=12)
- No plaintext passwords in database
- Salt generated per password

### File Permissions

```bash
chmod 600 accounts.db  # Read/write for owner only
```

### Audit Trail

All operations logged in `audit_log` table with:
- Timestamp
- User ID
- Action type
- Before/after values (JSON)

## Future Enhancements

### Roadmap (Not in MVP)

- Overdraft management (new fields in accounts table)
- Authorization/clearing workflow (new authorizations table)
- Multi-currency support (currency conversion rates table)
- Product versioning (product_versions table)
- Transaction reversals (reversal_status field)

## Resources

- SQLite Documentation: https://www.sqlite.org/docs.html
- Python sqlite3: https://docs.python.org/3/library/sqlite3.html
- DB Browser for SQLite: https://sqlitebrowser.org/

## Support

For issues or questions:
- Check troubleshooting section above
- Review migration scripts in `schema/migrations/`
- Inspect database: `sqlite3 accounts.db`

---

**Last Updated**: 2025-10-04
**Schema Version**: 001
**Status**: MVP Implementation
