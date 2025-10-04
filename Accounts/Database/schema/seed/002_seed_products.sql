-- Seed Data: Products
-- Description: Sample product configurations for testing

-- Basic Checking Account
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-CHK-BASIC-001',
    'Basic Checking',
    'CHK-BASIC-001',
    'Basic checking account with low fees and modest interest',
    'Active',
    'USD',
    0.015,  -- 1.5% annual interest
    100.00,  -- Minimum $100 balance to earn interest
    5.00,   -- $5 monthly maintenance fee
    1.00,   -- $1 per withdrawal transaction fee
    'USR-ADMIN-001'
);

-- Premium Checking Account
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-CHK-PREM-001',
    'Premium Checking',
    'CHK-PREM-001',
    'Premium checking account with higher interest and no transaction fees',
    'Active',
    'USD',
    0.025,  -- 2.5% annual interest
    500.00,  -- Minimum $500 balance to earn interest
    15.00,  -- $15 monthly maintenance fee
    0.00,   -- No transaction fees
    'USR-ADMIN-001'
);

-- Student Checking Account
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-CHK-STUDENT-001',
    'Student Checking',
    'CHK-STUDENT-001',
    'Fee-free checking account for students with basic interest',
    'Active',
    'USD',
    0.010,  -- 1.0% annual interest
    0.00,   -- No minimum balance requirement
    0.00,   -- No monthly fee
    0.00,   -- No transaction fees
    'USR-ADMIN-001'
);

-- High-Yield Savings Account
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-SAV-HIGH-001',
    'High-Yield Savings',
    'SAV-HIGH-001',
    'High-yield savings account with premium interest rates',
    'Active',
    'USD',
    0.040,  -- 4.0% annual interest
    1000.00,  -- Minimum $1000 balance to earn interest
    0.00,   -- No monthly fee
    3.00,   -- $3 per withdrawal (encourage saving)
    'USR-ADMIN-001'
);

-- Business Checking Account
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-CHK-BUS-001',
    'Business Checking',
    'CHK-BUS-001',
    'Checking account for small businesses',
    'Active',
    'USD',
    0.020,  -- 2.0% annual interest
    1000.00,  -- Minimum $1000 balance to earn interest
    25.00,  -- $25 monthly maintenance fee
    0.50,   -- $0.50 per transaction
    'USR-ADMIN-001'
);

-- Inactive Product (for testing)
INSERT INTO products (
    product_id,
    product_name,
    product_code,
    description,
    status,
    currency,
    interest_rate,
    minimum_balance_for_interest,
    monthly_maintenance_fee,
    transaction_fee,
    created_by
) VALUES (
    'PROD-CHK-OLD-001',
    'Legacy Checking',
    'CHK-OLD-001',
    'Discontinued checking account product',
    'Inactive',
    'USD',
    0.005,  -- 0.5% annual interest
    0.00,
    10.00,
    2.00,
    'USR-ADMIN-001'
);

-- ============================================================================
-- PRODUCT SUMMARY
-- ============================================================================
-- Active Products: 5
-- Inactive Products: 1
--
-- Interest Rates Range: 1.0% - 4.0%
-- Monthly Fees Range: $0 - $25
-- Transaction Fees Range: $0 - $3
--
-- Products by Type:
--   - Basic Checking: Low fees, modest interest
--   - Premium Checking: No transaction fees, higher interest
--   - Student Checking: Fee-free for students
--   - High-Yield Savings: Maximum interest for savers
--   - Business Checking: For business customers
