#!/usr/bin/env python3
"""
End-of-Day Batch Processing Script

This script performs critical end-of-day operations for the banking system:
1. Interest accrual on eligible accounts
2. Monthly maintenance fee application
3. Balance verification and reconciliation

This ensures all financial calculations are accurate and consistent.
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
import uuid

DB_PATH = Path(__file__).parent.parent / "accounts.db"


def calculate_daily_interest(balance: Decimal, annual_rate: Decimal) -> Decimal:
    """
    Calculate daily interest using Actual/365 convention.

    Formula: (Balance × Annual Rate × 1) / 365

    Args:
        balance: Account balance
        annual_rate: Annual interest rate (e.g., 0.015 for 1.5%)

    Returns:
        Daily interest amount, rounded to 2 decimal places
    """
    if balance <= Decimal('0'):
        return Decimal('0')

    daily_interest = (balance * annual_rate) / Decimal('365')
    return daily_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def accrue_interest(conn, processing_date: date):
    """
    Accrue interest on all eligible accounts.

    An account is eligible for interest if:
    - Status is 'Active'
    - Balance >= minimum_balance_for_interest (from product)
    - Product interest_rate > 0
    """
    cursor = conn.cursor()

    print(f"\n{'='*70}")
    print(f"Interest Accrual Process - {processing_date}")
    print(f"{'='*70}\n")

    # Find all active accounts eligible for interest
    query = """
        SELECT
            a.account_id,
            a.account_number,
            a.balance,
            a.interest_accrued,
            p.interest_rate,
            p.minimum_balance_for_interest,
            p.currency
        FROM accounts a
        INNER JOIN products p ON a.product_id = p.product_id
        WHERE a.status = 'Active'
          AND p.interest_rate > 0
          AND a.balance >= p.minimum_balance_for_interest
    """

    eligible_accounts = cursor.execute(query).fetchall()

    if not eligible_accounts:
        print("No accounts eligible for interest accrual.")
        return

    print(f"Found {len(eligible_accounts)} eligible accounts:\n")

    total_interest_accrued = Decimal('0')

    for row in eligible_accounts:
        account_id, account_number, balance, current_accrued, interest_rate, min_balance, currency = row

        balance = Decimal(str(balance))
        current_accrued = Decimal(str(current_accrued))
        interest_rate = Decimal(str(interest_rate))

        # Calculate daily interest
        daily_interest = calculate_daily_interest(balance, interest_rate)

        if daily_interest <= Decimal('0'):
            continue

        # Update interest_accrued on account
        new_accrued = current_accrued + daily_interest

        cursor.execute("""
            UPDATE accounts
            SET interest_accrued = ?,
                updated_at = datetime('now')
            WHERE account_id = ?
        """, (float(new_accrued), account_id))

        # Record accrual in interest_accruals table
        accrual_id = f"ACRL-{uuid.uuid4()}"
        cursor.execute("""
            INSERT INTO interest_accruals (
                accrual_id, account_id, accrual_date, balance,
                annual_rate, daily_interest, cumulative_accrued, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            accrual_id,
            account_id,
            processing_date.isoformat(),
            float(balance),
            float(interest_rate),
            float(daily_interest),
            float(new_accrued)
        ))

        total_interest_accrued += daily_interest

        print(f"  {account_number}: Balance ${balance:>12,.2f} × {interest_rate*100:>5.2f}% = ${daily_interest:>8.2f} (Accrued: ${new_accrued:>10.2f})")

    conn.commit()

    print(f"\n{'='*70}")
    print(f"✓ Interest accrued on {len(eligible_accounts)} accounts: ${total_interest_accrued:,.2f}")
    print(f"{'='*70}\n")


def apply_monthly_fees(conn, processing_date: date):
    """
    Apply monthly maintenance fees if today is the last day of the month.

    Fees are applied as:
    - Debit transaction with category 'Fee'
    - Description: 'Monthly maintenance fee'
    - Amount from product.monthly_maintenance_fee
    """
    # Check if today is last day of month
    next_day = date(processing_date.year, processing_date.month, processing_date.day) + \
               __import__('datetime').timedelta(days=1)

    if next_day.month == processing_date.month:
        print("Not end of month - skipping monthly fee application.\n")
        return

    cursor = conn.cursor()

    print(f"\n{'='*70}")
    print(f"Monthly Fee Application - {processing_date}")
    print(f"{'='*70}\n")

    # Find all active accounts with monthly fees
    query = """
        SELECT
            a.account_id,
            a.account_number,
            a.balance,
            p.monthly_maintenance_fee,
            p.currency
        FROM accounts a
        INNER JOIN products p ON a.product_id = p.product_id
        WHERE a.status = 'Active'
          AND p.monthly_maintenance_fee > 0
    """

    accounts_with_fees = cursor.execute(query).fetchall()

    if not accounts_with_fees:
        print("No accounts with monthly fees.")
        return

    print(f"Found {len(accounts_with_fees)} accounts with monthly fees:\n")

    total_fees_applied = Decimal('0')
    insufficient_balance_count = 0

    for row in accounts_with_fees:
        account_id, account_number, balance, monthly_fee, currency = row

        balance = Decimal(str(balance))
        monthly_fee = Decimal(str(monthly_fee))

        # Check sufficient balance
        if balance < monthly_fee:
            print(f"  {account_number}: SKIPPED - Insufficient balance (${balance:,.2f} < ${monthly_fee:,.2f})")
            insufficient_balance_count += 1
            continue

        # Deduct fee from balance
        new_balance = balance - monthly_fee

        # Update account balance
        cursor.execute("""
            UPDATE accounts
            SET balance = ?,
                updated_at = datetime('now')
            WHERE account_id = ?
        """, (float(new_balance), account_id))

        # Create transaction record
        transaction_id = f"TXN-FEE-{uuid.uuid4()}"
        cursor.execute("""
            INSERT INTO transactions (
                transaction_id, account_id, transaction_date, value_date,
                type, category, amount, currency, running_balance,
                description, reference, channel, status, created_at, created_by
            ) VALUES (?, ?, datetime('now'), ?, 'Debit', 'Fee', ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_id,
            account_id,
            processing_date.isoformat(),
            float(monthly_fee),
            currency,
            float(new_balance),
            'Monthly maintenance fee',
            f'FEE-{processing_date.strftime("%Y%m")}',
            'Batch',
            'Posted',
            datetime.now().isoformat(),
            'SYSTEM'
        ))

        total_fees_applied += monthly_fee

        print(f"  {account_number}: ${monthly_fee:>8.2f} applied (New balance: ${new_balance:>12,.2f})")

    conn.commit()

    print(f"\n{'='*70}")
    print(f"✓ Fees applied to {len(accounts_with_fees) - insufficient_balance_count} accounts: ${total_fees_applied:,.2f}")
    if insufficient_balance_count > 0:
        print(f"  ⚠ {insufficient_balance_count} accounts skipped due to insufficient balance")
    print(f"{'='*70}\n")


def verify_data_integrity(conn):
    """
    Verify that all account balances match their transaction history.
    """
    print(f"\n{'='*70}")
    print(f"Data Integrity Verification")
    print(f"{'='*70}\n")

    query = """
        SELECT
            a.account_id,
            a.account_number,
            a.balance as stored_balance,
            COALESCE((
                SELECT SUM(CASE WHEN type = 'Credit' THEN amount ELSE -amount END)
                FROM transactions
                WHERE account_id = a.account_id
            ), 0) as calculated_balance
        FROM accounts a
        WHERE a.status = 'Active'
    """

    cursor = conn.cursor()
    all_good = True

    for row in cursor.execute(query):
        account_id, account_number, stored_balance, calculated_balance = row

        stored = Decimal(str(stored_balance))
        calculated = Decimal(str(calculated_balance))

        diff = abs(stored - calculated)

        if diff > Decimal('0.01'):  # Allow 1 cent rounding difference
            print(f"  ✗ MISMATCH: {account_number}")
            print(f"     Stored: ${stored:,.2f}")
            print(f"     Calculated: ${calculated:,.2f}")
            print(f"     Difference: ${diff:,.2f}\n")
            all_good = False
        else:
            print(f"  ✓ {account_number}: ${stored:>12,.2f} (matches transaction history)")

    print(f"\n{'='*70}")
    if all_good:
        print("✓ All account balances are consistent!")
    else:
        print("✗ Data integrity issues found!")
        sys.exit(1)
    print(f"{'='*70}\n")


def main():
    print("\n")
    print("="*70)
    print(" BANKING SYSTEM - END-OF-DAY BATCH PROCESSING")
    print("="*70)

    processing_date = date.today()
    print(f"\nProcessing Date: {processing_date.strftime('%Y-%m-%d')}\n")

    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    try:
        # Step 1: Accrue Interest
        accrue_interest(conn, processing_date)

        # Step 2: Apply Monthly Fees (if end of month)
        apply_monthly_fees(conn, processing_date)

        # Step 3: Verify Data Integrity
        verify_data_integrity(conn)

        print("\n")
        print("="*70)
        print(" END-OF-DAY PROCESSING COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\n")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
