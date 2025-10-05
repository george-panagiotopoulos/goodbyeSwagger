-- Migration 003: Add Monthly Interest Accruals Table
-- Description: Tracks month-end interest postings using 30/360 convention
-- Created: 2025-10-05

CREATE TABLE IF NOT EXISTS monthly_interest_accruals (
    monthly_accrual_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,

    -- Month being processed (YYYY-MM format, e.g., '2025-09')
    accrual_month TEXT NOT NULL,

    -- Month-end date when interest was posted
    posting_date TEXT NOT NULL,

    -- Account state at month-end
    month_end_balance REAL NOT NULL CHECK(month_end_balance >= 0),
    annual_interest_rate REAL NOT NULL CHECK(annual_interest_rate >= 0 AND annual_interest_rate <= 1),

    -- Interest calculation (30/360 convention)
    -- Formula: (Balance × Annual Rate × 30) / 360
    monthly_interest REAL NOT NULL CHECK(monthly_interest >= 0),

    -- Transaction reference
    transaction_id TEXT,  -- Reference to the Interest transaction in ledger

    -- Processing details
    processing_date TEXT NOT NULL DEFAULT (datetime('now')),
    processing_status TEXT NOT NULL DEFAULT 'Posted' CHECK(processing_status IN ('Posted', 'Reversed')),

    -- Audit
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),

    -- Ensure one accrual per account per month
    UNIQUE(account_id, accrual_month)
);

CREATE INDEX idx_monthly_accruals_account ON monthly_interest_accruals(account_id);
CREATE INDEX idx_monthly_accruals_month ON monthly_interest_accruals(accrual_month);
CREATE INDEX idx_monthly_accruals_posting_date ON monthly_interest_accruals(posting_date);
CREATE INDEX idx_monthly_accruals_status ON monthly_interest_accruals(processing_status);
