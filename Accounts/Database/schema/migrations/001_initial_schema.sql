-- Migration 001: Initial Schema
-- Description: Creates core tables for MVP: users, products, accounts, transactions
-- Created: 2025-10-04

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('admin', 'officer', 'viewer')),
    status TEXT NOT NULL CHECK(status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- ============================================================================
-- PRODUCTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL UNIQUE,
    product_code TEXT NOT NULL UNIQUE,
    description TEXT,
    status TEXT NOT NULL CHECK(status IN ('Active', 'Inactive')) DEFAULT 'Active',
    currency TEXT NOT NULL DEFAULT 'USD' CHECK(length(currency) = 3),

    -- Interest configuration (simple interest, Actual/365)
    interest_rate REAL NOT NULL DEFAULT 0.0 CHECK(interest_rate >= 0 AND interest_rate <= 1),
    minimum_balance_for_interest REAL NOT NULL DEFAULT 0.0 CHECK(minimum_balance_for_interest >= 0),

    -- Fee configuration (fixed amounts only for MVP)
    monthly_maintenance_fee REAL NOT NULL DEFAULT 0.0 CHECK(monthly_maintenance_fee >= 0),
    transaction_fee REAL NOT NULL DEFAULT 0.0 CHECK(transaction_fee >= 0),

    -- Audit fields
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,

    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_currency ON products(currency);
CREATE INDEX idx_products_code ON products(product_code);

-- ============================================================================
-- ACCOUNTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    account_number TEXT NOT NULL UNIQUE,
    customer_id TEXT NOT NULL,  -- Reference to customer (external system for MVP)
    product_id TEXT NOT NULL,
    currency TEXT NOT NULL CHECK(length(currency) = 3),
    status TEXT NOT NULL CHECK(status IN ('Active', 'Closed')) DEFAULT 'Active',

    -- Balance fields
    balance REAL NOT NULL DEFAULT 0.0,
    interest_accrued REAL NOT NULL DEFAULT 0.0,

    -- Dates
    opening_date TEXT NOT NULL DEFAULT (date('now')),
    closing_date TEXT,

    -- Audit fields
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,

    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),

    CHECK (
        (status = 'Closed' AND closing_date IS NOT NULL) OR
        (status = 'Active' AND closing_date IS NULL)
    ),
    CHECK (balance >= 0)  -- No overdraft in MVP
);

CREATE INDEX idx_accounts_number ON accounts(account_number);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_product ON accounts(product_id);
CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_accounts_opening_date ON accounts(opening_date);

-- ============================================================================
-- TRANSACTIONS TABLE (Ledger)
-- ============================================================================
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,

    -- Transaction details
    transaction_date TEXT NOT NULL DEFAULT (datetime('now')),
    value_date TEXT NOT NULL DEFAULT (date('now')),
    type TEXT NOT NULL CHECK(type IN ('Debit', 'Credit')),
    category TEXT NOT NULL CHECK(category IN ('Deposit', 'Withdrawal', 'Fee', 'Interest', 'Opening')),

    -- Amounts
    amount REAL NOT NULL CHECK(amount > 0),
    currency TEXT NOT NULL CHECK(length(currency) = 3),
    running_balance REAL NOT NULL CHECK(running_balance >= 0),

    -- Description and reference
    description TEXT NOT NULL,
    reference TEXT,

    -- Channel and status
    channel TEXT NOT NULL DEFAULT 'API' CHECK(channel IN ('API', 'UI', 'Batch')),
    status TEXT NOT NULL DEFAULT 'Posted' CHECK(status IN ('Posted')),

    -- Audit fields
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_value_date ON transactions(value_date);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_category ON transactions(category);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_account_date ON transactions(account_id, transaction_date);

-- ============================================================================
-- INTEREST ACCRUALS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS interest_accruals (
    accrual_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,

    -- Accrual details
    accrual_date TEXT NOT NULL DEFAULT (date('now')),
    balance REAL NOT NULL CHECK(balance >= 0),
    annual_rate REAL NOT NULL CHECK(annual_rate >= 0 AND annual_rate <= 1),

    -- Calculated interest
    daily_interest REAL NOT NULL CHECK(daily_interest >= 0),
    cumulative_accrued REAL NOT NULL CHECK(cumulative_accrued >= 0),

    -- Audit fields
    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,

    -- Ensure one accrual per account per day
    UNIQUE(account_id, accrual_date)
);

CREATE INDEX idx_interest_account ON interest_accruals(account_id);
CREATE INDEX idx_interest_date ON interest_accruals(accrual_date);
CREATE INDEX idx_interest_account_date ON interest_accruals(account_id, accrual_date);

-- ============================================================================
-- AUDIT LOG TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id TEXT PRIMARY KEY,

    -- Event details
    event_type TEXT NOT NULL,  -- e.g., 'ACCOUNT_CREATED', 'TRANSACTION_POSTED', 'PRODUCT_UPDATED'
    entity_type TEXT NOT NULL,  -- e.g., 'Account', 'Transaction', 'Product'
    entity_id TEXT NOT NULL,

    -- User and timestamp
    user_id TEXT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),

    -- Event data (JSON)
    event_data TEXT,  -- JSON string containing before/after values

    -- IP and channel
    ip_address TEXT,
    channel TEXT,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_type ON audit_log(event_type);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_user ON audit_log(user_id);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Account Summary
CREATE VIEW IF NOT EXISTS v_account_summary AS
SELECT
    a.account_id,
    a.account_number,
    a.customer_id,
    a.status,
    a.balance,
    a.interest_accrued,
    a.opening_date,
    a.closing_date,
    p.product_id,
    p.product_name,
    p.product_code,
    p.currency,
    p.interest_rate,
    p.monthly_maintenance_fee,
    p.transaction_fee,
    (SELECT MAX(transaction_date) FROM transactions WHERE account_id = a.account_id) as last_transaction_date,
    (SELECT COUNT(*) FROM transactions WHERE account_id = a.account_id) as transaction_count
FROM accounts a
INNER JOIN products p ON a.product_id = p.product_id;

-- View: Transaction Ledger (with product info)
CREATE VIEW IF NOT EXISTS v_transaction_ledger AS
SELECT
    t.transaction_id,
    t.account_id,
    a.account_number,
    a.customer_id,
    t.transaction_date,
    t.value_date,
    t.type,
    t.category,
    t.amount,
    t.currency,
    t.running_balance,
    t.description,
    t.reference,
    t.channel,
    t.status,
    t.created_at,
    t.created_by
FROM transactions t
INNER JOIN accounts a ON t.account_id = a.account_id;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger: Update updated_at on products
CREATE TRIGGER IF NOT EXISTS trg_products_updated_at
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    UPDATE products SET updated_at = datetime('now') WHERE product_id = NEW.product_id;
END;

-- Trigger: Update updated_at on accounts
CREATE TRIGGER IF NOT EXISTS trg_accounts_updated_at
AFTER UPDATE ON accounts
FOR EACH ROW
BEGIN
    UPDATE accounts SET updated_at = datetime('now') WHERE account_id = NEW.account_id;
END;

-- Trigger: Update updated_at on users
CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = datetime('now') WHERE user_id = NEW.user_id;
END;

-- ============================================================================
-- FUNCTIONS (Implemented in application layer, documented here)
-- ============================================================================

-- Account Number Generation: Pattern ACC-{YYYYMMDD}-{SEQUENCE}
-- Implemented in Rust application layer

-- Interest Calculation: (Balance × Annual Rate × 1) / 365
-- Implemented in Rust InterestService

-- Running Balance Calculation: Previous Balance + Credits - Debits
-- Implemented in Rust TransactionService

-- ============================================================================
-- COMMENTS
-- ============================================================================

-- Schema Version: 001
-- MVP Features:
--   - Basic account management (Active/Closed status only)
--   - Simple transaction processing (no authorization/clearing)
--   - Credit interest calculation (simple interest, Actual/365)
--   - Static fees (fixed amounts only)
--   - Single currency per account
--   - Real-time balance updates
--
-- Future Enhancements (Roadmap):
--   - Overdraft management (overdraft_limit, overdraft_utilized fields)
--   - Authorization/clearing workflow (authorizations table)
--   - Additional account statuses (Inactive, Suspended)
--   - Multi-currency support
--   - Formula-based interest and fees
--   - Tiered interest rates
