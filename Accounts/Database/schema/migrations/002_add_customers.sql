-- Migration 002: Add Customers Table
-- Purpose: Add customer entity for future integration with customer management systems

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    external_customer_id TEXT UNIQUE,  -- ID from external customer management system
    customer_name TEXT NOT NULL,
    customer_type TEXT NOT NULL,  -- 'Individual' or 'Business'
    status TEXT NOT NULL DEFAULT 'Active',  -- 'Active', 'Inactive', 'Suspended'
    email TEXT,
    phone TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Create index on external customer ID for quick lookups
CREATE INDEX IF NOT EXISTS idx_customers_external_id ON customers(external_customer_id);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);

-- Note: accounts table already has customer_id field
-- We just need to add the customers table for proper customer management

-- Update the account summary view
DROP VIEW IF EXISTS v_account_summary;

CREATE VIEW v_account_summary AS
SELECT
    a.account_id,
    a.account_number,
    c.customer_id,
    c.customer_name,
    p.product_name,
    a.balance,
    a.interest_accrued,
    a.status,
    a.opened_date,
    a.closed_date
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
JOIN products p ON a.product_id = p.product_id;
