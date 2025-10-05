#!/usr/bin/env python3
"""
Monthly Interest Accrual Batch Processing Script

This script calculates and posts monthly interest on eligible accounts using the 30/360 day count convention.

Key Features:
- Uses 30/360 convention: Every month = 30 days, Every year = 360 days
- Formula: Monthly Interest = (Balance × Annual Rate × 30) / 360
- Processes all missing months from account opening to current month
- Posts interest on the last day of each month
- Creates proper ledger transactions
- Idempotent: Safe to run multiple times (skips already processed months)
- Handles catch-up for historical months

Usage:
    python3 batch_monthly_accruals.py [--month YYYY-MM] [--dry-run]

Options:
    --month YYYY-MM    Process specific month (default: current month)
    --dry-run          Show what would be processed without making changes
"""

import sqlite3
import sys
import argparse
from pathlib import Path
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP
import uuid
import calendar

DB_PATH = Path(__file__).parent.parent / "accounts.db"


def get_last_day_of_month(year: int, month: int) -> date:
    """Get the last day of a given month."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def calculate_monthly_interest_30_360(balance: Decimal, annual_rate: Decimal) -> Decimal:
    """
    Calculate monthly interest using 30/360 day count convention.

    Formula: (Balance × Annual Rate × 30) / 360

    This simplifies to: (Balance × Annual Rate) / 12

    Args:
        balance: Account balance at month-end
        annual_rate: Annual interest rate (e.g., 0.015 for 1.5%)

    Returns:
        Monthly interest amount, rounded to 2 decimal places
    """
    if balance <= Decimal('0') or annual_rate <= Decimal('0'):
        return Decimal('0')

    # 30/360 convention: (Balance × Rate × 30) / 360 = (Balance × Rate) / 12
    monthly_interest = (balance * annual_rate) / Decimal('12')
    return monthly_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_months_to_process(conn, account_id: str, opening_date: date, end_month: str) -> list:
    """
    Get list of months that need interest accrual for an account.

    Returns list of (year, month) tuples for months not yet processed.
    """
    cursor = conn.cursor()

    # Parse end month
    end_year, end_month_num = map(int, end_month.split('-'))

    # Get opening month
    opening_year = opening_date.year
    opening_month = opening_date.month

    # Get already processed months
    processed_months = set()
    rows = cursor.execute("""
        SELECT accrual_month
        FROM monthly_interest_accruals
        WHERE account_id = ? AND processing_status = 'Posted'
    """, (account_id,)).fetchall()

    for row in rows:
        processed_months.add(row[0])

    # Generate list of months from opening to end_month
    months_to_process = []
    current_date = date(opening_year, opening_month, 1)
    end_date = date(end_year, end_month_num, 1)

    while current_date <= end_date:
        month_str = current_date.strftime('%Y-%m')
        if month_str not in processed_months:
            months_to_process.append((current_date.year, current_date.month, month_str))
        current_date += relativedelta(months=1)

    return months_to_process


def get_balance_at_month_end(conn, account_id: str, month_end_date: date) -> Decimal:
    """
    Get account balance at the end of a specific month.

    Uses the running_balance from the last transaction on or before the month-end date.
    If no transactions exist, uses opening balance (0).
    """
    cursor = conn.cursor()

    # Get the most recent transaction on or before month_end_date
    row = cursor.execute("""
        SELECT running_balance
        FROM transactions
        WHERE account_id = ?
          AND date(value_date) <= ?
        ORDER BY value_date DESC, created_at DESC
        LIMIT 1
    """, (account_id, month_end_date.isoformat())).fetchone()

    if row:
        return Decimal(str(row[0]))

    # No transactions yet - check if account was open
    account_info = cursor.execute("""
        SELECT opening_date
        FROM accounts
        WHERE account_id = ?
    """, (account_id,)).fetchone()

    if account_info and date.fromisoformat(account_info[0]) <= month_end_date:
        return Decimal('0')  # Account was open but no transactions

    return None  # Account didn't exist yet


def process_monthly_accruals(conn, target_month: str = None, dry_run: bool = False):
    """
    Process monthly interest accruals for all eligible accounts.

    Args:
        target_month: Specific month to process (YYYY-MM), or None for current month
        dry_run: If True, show what would be processed without making changes
    """
    cursor = conn.cursor()

    # Determine which month to process
    if target_month:
        process_year, process_month = map(int, target_month.split('-'))
    else:
        today = date.today()
        process_year = today.year
        process_month = today.month

    month_str = f"{process_year:04d}-{process_month:02d}"
    month_end_date = get_last_day_of_month(process_year, process_month)

    print(f"\n{'='*80}")
    print(f"Monthly Interest Accrual Process - 30/360 Convention")
    print(f"Processing Month: {month_str}")
    print(f"Month-End Date: {month_end_date}")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE PROCESSING'}")
    print(f"{'='*80}\n")

    # Find all active accounts eligible for interest
    query = """
        SELECT
            a.account_id,
            a.account_number,
            a.opening_date,
            a.customer_id,
            p.interest_rate,
            p.minimum_balance_for_interest,
            p.currency,
            p.product_name
        FROM accounts a
        INNER JOIN products p ON a.product_id = p.product_id
        WHERE a.status = 'Active'
          AND p.interest_rate > 0
          AND date(a.opening_date) <= ?
    """

    eligible_accounts = cursor.execute(query, (month_end_date.isoformat(),)).fetchall()

    if not eligible_accounts:
        print("No accounts eligible for interest accrual.\n")
        return {"accounts_processed": 0, "total_interest": 0, "months_processed": 0}

    print(f"Found {len(eligible_accounts)} eligible accounts\n")

    total_interest_posted = Decimal('0')
    accounts_processed = 0
    months_processed_count = 0
    results = []

    for row in eligible_accounts:
        (account_id, account_number, opening_date_str, customer_id,
         interest_rate, min_balance, currency, product_name) = row

        opening_date = date.fromisoformat(opening_date_str)
        interest_rate = Decimal(str(interest_rate))
        min_balance = Decimal(str(min_balance))

        print(f"Processing Account: {account_number} ({product_name})")
        print(f"  Opened: {opening_date}, Rate: {interest_rate*100:.2f}%")

        # Get all months that need processing for this account
        months_to_process = get_months_to_process(conn, account_id, opening_date, month_str)

        if not months_to_process:
            print(f"  ℹ All months already processed\n")
            continue

        account_month_interest = Decimal('0')

        for year, month, month_key in months_to_process:
            month_end = get_last_day_of_month(year, month)

            # Get balance at month-end
            balance = get_balance_at_month_end(conn, account_id, month_end)

            if balance is None:
                print(f"  ⏭ {month_key}: Account not open yet")
                continue

            if balance < min_balance:
                print(f"  ⏭ {month_key}: Balance ${balance:,.2f} below minimum ${min_balance:,.2f}")
                continue

            # Calculate monthly interest using 30/360
            monthly_interest = calculate_monthly_interest_30_360(balance, interest_rate)

            if monthly_interest <= Decimal('0'):
                print(f"  ⏭ {month_key}: No interest (balance: ${balance:,.2f})")
                continue

            print(f"  ✓ {month_key}: Balance ${balance:>12,.2f} × {interest_rate*100:>5.2f}% ÷ 12 = ${monthly_interest:>8.2f}")

            if not dry_run:
                # Create interest transaction
                transaction_id = f"TXN-{uuid.uuid4()}"
                new_balance = balance + monthly_interest

                # Format dates properly for Rust parser: YYYY-MM-DD HH:MM:SS
                from datetime import datetime as dt
                transaction_datetime = dt.combine(month_end, dt.min.time()).strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute("""
                    INSERT INTO transactions (
                        transaction_id, account_id, transaction_date, value_date,
                        type, category, amount, currency, running_balance,
                        description, reference, channel, status, created_at
                    ) VALUES (?, ?, ?, ?, 'Credit', 'Interest', ?, ?, ?, ?, ?, 'Batch', 'Posted', datetime('now'))
                """, (
                    transaction_id,
                    account_id,
                    transaction_datetime,
                    month_end.isoformat(),
                    float(monthly_interest),
                    currency,
                    float(new_balance),
                    f"Monthly interest - {month_key} (30/360)",
                    month_key
                ))

                # Update account balance
                cursor.execute("""
                    UPDATE accounts
                    SET balance = ?,
                        updated_at = datetime('now')
                    WHERE account_id = ?
                """, (float(new_balance), account_id))

                # Record in monthly_interest_accruals table
                accrual_id = f"MACRL-{uuid.uuid4()}"
                cursor.execute("""
                    INSERT INTO monthly_interest_accruals (
                        monthly_accrual_id, account_id, accrual_month, posting_date,
                        month_end_balance, annual_interest_rate, monthly_interest,
                        transaction_id, processing_date, processing_status, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 'Posted', datetime('now'))
                """, (
                    accrual_id,
                    account_id,
                    month_key,
                    month_end.isoformat(),
                    float(balance),
                    float(interest_rate),
                    float(monthly_interest),
                    transaction_id
                ))

            account_month_interest += monthly_interest
            months_processed_count += 1

        if account_month_interest > Decimal('0'):
            total_interest_posted += account_month_interest
            accounts_processed += 1
            results.append({
                "account_number": account_number,
                "months": len(months_to_process),
                "total_interest": float(account_month_interest)
            })

        print()

    if not dry_run and months_processed_count > 0:
        conn.commit()

    print(f"{'='*80}")
    print(f"Summary:")
    print(f"  Accounts Processed: {accounts_processed}")
    print(f"  Months Processed: {months_processed_count}")
    print(f"  Total Interest Posted: ${total_interest_posted:,.2f}")
    print(f"{'='*80}\n")

    return {
        "accounts_processed": accounts_processed,
        "months_processed": months_processed_count,
        "total_interest": float(total_interest_posted),
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description='Monthly Interest Accrual Batch Processing')
    parser.add_argument('--month', help='Specific month to process (YYYY-MM)', default=None)
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (no changes)')

    args = parser.parse_args()

    try:
        conn = sqlite3.connect(DB_PATH)
        result = process_monthly_accruals(conn, args.month, args.dry_run)
        conn.close()

        print("✓ Processing complete")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
