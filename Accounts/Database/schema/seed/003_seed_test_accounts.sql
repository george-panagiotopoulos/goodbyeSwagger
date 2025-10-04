-- Seed Data: Test Accounts
-- Description: Sample accounts for testing and demonstration

-- Customer CUST-001 accounts
INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100401',
    '1000000001',
    'CUST-001',
    'PROD-CHK-BASIC-001',
    'USD',
    'Active',
    1500.00,
    0.00,
    '2025-01-15',
    'USR-OFFICER-001'
);

INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100402',
    '1000000002',
    'CUST-001',
    'PROD-SAV-HIGH-001',
    'USD',
    'Active',
    5000.00,
    0.00,
    '2025-01-15',
    'USR-OFFICER-001'
);

-- Customer CUST-002 accounts
INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100403',
    '1000000003',
    'CUST-002',
    'PROD-CHK-PREM-001',
    'USD',
    'Active',
    3200.50,
    0.00,
    '2025-03-10',
    'USR-OFFICER-001'
);

-- Customer CUST-003 - Student account
INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100404',
    '1000000004',
    'CUST-003',
    'PROD-CHK-STUDENT-001',
    'USD',
    'Active',
    250.00,
    0.00,
    '2025-08-20',
    'USR-OFFICER-001'
);

-- Customer CUST-004 - Business account
INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100405',
    '1000000005',
    'CUST-004',
    'PROD-CHK-BUS-001',
    'USD',
    'Active',
    12500.00,
    0.00,
    '2025-02-01',
    'USR-OFFICER-001'
);

-- Customer CUST-005 - Low balance account
INSERT INTO accounts (
    account_id,
    account_number,
    customer_id,
    product_id,
    currency,
    status,
    balance,
    interest_accrued,
    opening_date,
    created_by
) VALUES (
    'ACC-2025100406',
    '1000000006',
    'CUST-005',
    'PROD-CHK-BASIC-001',
    'USD',
    'Active',
    50.00,
    0.00,
    '2025-09-15',
    'USR-OFFICER-001'
);

-- ============================================================================
-- OPENING BALANCE TRANSACTIONS
-- ============================================================================

-- Opening transaction for ACC-2025100401
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100401-OPEN',
    'ACC-2025100401',
    '2025-01-15 09:00:00',
    '2025-01-15',
    'Credit',
    'Opening',
    1500.00,
    'USD',
    1500.00,
    'Opening balance',
    'OPEN-ACC-2025100401',
    'UI',
    'USR-OFFICER-001'
);

-- Opening transaction for ACC-2025100402
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100402-OPEN',
    'ACC-2025100402',
    '2025-01-15 09:05:00',
    '2025-01-15',
    'Credit',
    'Opening',
    5000.00,
    'USD',
    5000.00,
    'Opening balance',
    'OPEN-ACC-2025100402',
    'UI',
    'USR-OFFICER-001'
);

-- Opening transaction for ACC-2025100403
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100403-OPEN',
    'ACC-2025100403',
    '2025-03-10 10:30:00',
    '2025-03-10',
    'Credit',
    'Opening',
    3200.50,
    'USD',
    3200.50,
    'Opening balance',
    'OPEN-ACC-2025100403',
    'UI',
    'USR-OFFICER-001'
);

-- Opening transaction for ACC-2025100404
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100404-OPEN',
    'ACC-2025100404',
    '2025-08-20 14:15:00',
    '2025-08-20',
    'Credit',
    'Opening',
    250.00,
    'USD',
    250.00,
    'Opening balance',
    'OPEN-ACC-2025100404',
    'UI',
    'USR-OFFICER-001'
);

-- Opening transaction for ACC-2025100405
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100405-OPEN',
    'ACC-2025100405',
    '2025-02-01 11:00:00',
    '2025-02-01',
    'Credit',
    'Opening',
    12500.00,
    'USD',
    12500.00,
    'Opening balance',
    'OPEN-ACC-2025100405',
    'UI',
    'USR-OFFICER-001'
);

-- Opening transaction for ACC-2025100406
INSERT INTO transactions (
    transaction_id,
    account_id,
    transaction_date,
    value_date,
    type,
    category,
    amount,
    currency,
    running_balance,
    description,
    reference,
    channel,
    created_by
) VALUES (
    'TXN-2025100406-OPEN',
    'ACC-2025100406',
    '2025-09-15 16:45:00',
    '2025-09-15',
    'Credit',
    'Opening',
    50.00,
    'USD',
    50.00,
    'Opening balance',
    'OPEN-ACC-2025100406',
    'UI',
    'USR-OFFICER-001'
);

-- ============================================================================
-- TEST ACCOUNTS SUMMARY
-- ============================================================================
-- Total Accounts: 6
-- Total Balances: $22,500.50
--
-- By Customer:
--   CUST-001: 2 accounts ($6,500.00)
--   CUST-002: 1 account ($3,200.50)
--   CUST-003: 1 account ($250.00)
--   CUST-004: 1 account ($12,500.00)
--   CUST-005: 1 account ($50.00)
--
-- By Product:
--   Basic Checking: 2 accounts
--   Premium Checking: 1 account
--   Student Checking: 1 account
--   Business Checking: 1 account
--   High-Yield Savings: 1 account
--
-- Test Scenarios Covered:
--   - Multiple accounts per customer
--   - Different product types
--   - High balance vs low balance
--   - Below minimum for interest (ACC-2025100406)
--   - Above minimum for interest (all others)
