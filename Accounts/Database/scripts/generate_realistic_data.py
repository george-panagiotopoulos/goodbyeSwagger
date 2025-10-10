#!/usr/bin/env python3
"""
Generate Realistic Account Data
Creates realistic transaction history for test accounts with balances tracing to 0
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Get database directory
DB_DIR = Path(__file__).parent.parent
DB_FILE = DB_DIR / "accounts.db"


def generate_realistic_data():
    """Generate realistic account data with transactions"""
    print("=" * 80)
    print("Generating Realistic Account Data")
    print("=" * 80)

    # Check if database exists
    if not DB_FILE.exists():
        print(f"ERROR: Database not found at {DB_FILE}")
        print("Please run 'python scripts/init_db.py' first")
        sys.exit(1)

    # Create database connection
    conn = sqlite3.connect(str(DB_FILE))
    cursor = conn.cursor()

    try:
        # Clear existing transactions and accounts (disable FK temporarily)
        print("\nClearing existing data...")
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("DELETE FROM transactions;")
        cursor.execute("DELETE FROM interest_accruals;")
        cursor.execute("DELETE FROM accounts;")
        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        print("  ✓ Existing data cleared")

        # Define realistic account scenarios
        accounts = [
            {
                'account_id': 'ACC-2025100401',
                'account_number': '1000000001',
                'customer_id': 'CUST-001',
                'product_id': 'PROD-CHK-BASIC-001',
                'opening_date': '2025-01-15',
                'target_balance': 1500.00,
                'transaction_pattern': 'salary_worker'  # Regular salary deposits, modest spending
            },
            {
                'account_id': 'ACC-2025100402',
                'account_number': '1000000002',
                'customer_id': 'CUST-001',
                'product_id': 'PROD-SAV-HIGH-001',
                'opening_date': '2025-01-15',
                'target_balance': 5000.00,
                'transaction_pattern': 'savings'  # Mostly deposits, rare withdrawals
            },
            {
                'account_id': 'ACC-2025100403',
                'account_number': '1000000003',
                'customer_id': 'CUST-002',
                'product_id': 'PROD-CHK-PREM-001',
                'opening_date': '2025-03-10',
                'target_balance': 3200.50,
                'transaction_pattern': 'professional'  # Higher salary, moderate spending
            },
            {
                'account_id': 'ACC-2025100404',
                'account_number': '1000000004',
                'customer_id': 'CUST-003',
                'product_id': 'PROD-CHK-STUDENT-001',
                'opening_date': '2025-08-20',
                'target_balance': 250.00,
                'transaction_pattern': 'student'  # Small deposits, frequent small purchases
            },
            {
                'account_id': 'ACC-2025100405',
                'account_number': '1000000005',
                'customer_id': 'CUST-004',
                'product_id': 'PROD-CHK-BUS-001',
                'opening_date': '2025-02-01',
                'target_balance': 12500.00,
                'transaction_pattern': 'business'  # Large deposits and withdrawals
            },
            {
                'account_id': 'ACC-2025100406',
                'account_number': '1000000006',
                'customer_id': 'CUST-005',
                'product_id': 'PROD-CHK-BASIC-001',
                'opening_date': '2025-09-15',
                'target_balance': 50.00,
                'transaction_pattern': 'low_balance'  # Minimal activity
            },
        ]

        print("\nCreating accounts and transactions...")

        for acc in accounts:
            create_account_with_history(cursor, acc)
            conn.commit()

        # Show summary
        print("\n" + "-" * 80)
        print("Account Summary:")
        print("-" * 80)

        cursor.execute("""
            SELECT
                a.account_number,
                a.customer_id,
                p.product_name,
                a.balance,
                (SELECT COUNT(*) FROM transactions WHERE account_id = a.account_id) as txn_count
            FROM accounts a
            JOIN products p ON a.product_id = p.product_id
            ORDER BY a.account_number;
        """)

        accounts_summary = cursor.fetchall()
        total_balance = 0
        total_transactions = 0

        for acc_summary in accounts_summary:
            print(f"  {acc_summary[0]} | {acc_summary[1]:10} | {acc_summary[2]:25} | ${acc_summary[3]:10.2f} | {acc_summary[4]} txns")
            total_balance += acc_summary[3]
            total_transactions += acc_summary[4]

        print("-" * 80)
        print(f"  Total Balance: ${total_balance:,.2f}")
        print(f"  Total Transactions: {total_transactions}")

        # Verify all balances trace to 0
        print("\n" + "-" * 80)
        print("Balance Verification (tracing to 0):")
        print("-" * 80)

        cursor.execute("SELECT account_id, account_number, balance FROM accounts;")
        for acc_id, acc_num, balance in cursor.fetchall():
            cursor.execute("""
                SELECT transaction_date, type, amount, running_balance
                FROM transactions
                WHERE account_id = ?
                ORDER BY transaction_date ASC, created_at ASC
                LIMIT 1;
            """, (acc_id,))
            first_txn = cursor.fetchone()

            if first_txn and first_txn[3] == first_txn[2]:  # running_balance == amount
                print(f"  ✓ {acc_num}: Balance ${balance:.2f} traces to $0.00")
            else:
                print(f"  ✗ {acc_num}: ERROR - first transaction doesn't start at 0!")

        # Close connection
        conn.close()

        print("\n" + "=" * 80)
        print("Realistic data generation completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\nERROR: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)


def create_account_with_history(cursor, account_info):
    """Create an account with realistic transaction history"""

    # Insert account with 0 balance initially
    cursor.execute("""
        INSERT INTO accounts (
            account_id, account_number, customer_id, product_id,
            currency, status, balance, interest_accrued, opening_date, created_by
        ) VALUES (?, ?, ?, ?, 'USD', 'Active', 0.00, 0.00, ?, 'USR-OFFICER-001');
    """, (
        account_info['account_id'],
        account_info['account_number'],
        account_info['customer_id'],
        account_info['product_id'],
        account_info['opening_date']
    ))

    # Get product details for interest/fees
    cursor.execute("""
        SELECT interest_rate, monthly_maintenance_fee, transaction_fee
        FROM products WHERE product_id = ?;
    """, (account_info['product_id'],))
    product = cursor.fetchone()
    interest_rate, monthly_fee, txn_fee = product

    # Generate transaction history
    opening_date = datetime.strptime(account_info['opening_date'], '%Y-%m-%d')
    current_date = datetime.now()

    transactions = generate_transactions(
        account_info['account_id'],
        account_info['account_number'],
        opening_date,
        current_date,
        account_info['target_balance'],
        account_info['transaction_pattern'],
        interest_rate,
        monthly_fee,
        txn_fee
    )

    # Insert transactions in chronological order, but we'll query them in reverse later
    running_balance = 0.00
    for txn in transactions:
        if txn['type'] == 'Credit':
            running_balance += txn['amount']
        else:  # Debit
            running_balance -= txn['amount']

        txn['running_balance'] = round(running_balance, 2)

        cursor.execute("""
            INSERT INTO transactions (
                transaction_id, account_id, transaction_date, value_date,
                type, category, amount, currency, running_balance,
                description, reference, channel, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            txn['transaction_id'],
            txn['account_id'],
            txn['transaction_date'],
            txn['value_date'],
            txn['type'],
            txn['category'],
            txn['amount'],
            'USD',
            txn['running_balance'],
            txn['description'],
            txn['reference'],
            txn['channel'],
            'USR-OFFICER-001'
        ))

    # Update account balance to final running balance
    cursor.execute("""
        UPDATE accounts SET balance = ? WHERE account_id = ?;
    """, (running_balance, account_info['account_id']))

    print(f"  ✓ Created {account_info['account_number']} with {len(transactions)} transactions (Balance: ${running_balance:.2f})")


def generate_transactions(account_id, account_number, start_date, end_date, target_balance,
                         pattern, interest_rate, monthly_fee, txn_fee):
    """Generate realistic transactions based on account pattern"""

    transactions = []
    txn_counter = 1
    current_date = start_date

    # Helper function to calculate running balance from transactions
    def calc_balance(txns):
        bal = 0.00
        for t in txns:
            if t['type'] == 'Credit':
                bal += t['amount']
            else:
                bal -= t['amount']
        return round(bal, 2)

    # Transaction patterns
    if pattern == 'salary_worker':
        # Monthly salary deposits, weekly/bi-weekly spending
        while current_date <= end_date:
            # Monthly salary (1st of month)
            if current_date.day == 1 or (current_date == start_date):
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(2000, 2500), 2),
                    'description': 'Salary deposit',
                    'reference': f'SAL-{current_date.strftime("%Y%m")}',
                    'channel': 'Batch'
                })
                txn_counter += 1

            # Random spending 2-4 times per month
            if random.random() < 0.15:  # ~15% chance per day
                amount = round(random.uniform(50, 300), 2)
                total_debit = amount + (txn_fee if txn_fee > 0 else 0)

                # Only add if we have sufficient balance
                if calc_balance(transactions) >= total_debit:
                    transactions.append({
                        'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                        'account_id': account_id,
                        'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'value_date': current_date.strftime('%Y-%m-%d'),
                        'type': 'Debit',
                        'category': 'Withdrawal',
                        'amount': amount,
                        'description': random.choice(['ATM withdrawal', 'POS purchase', 'Online payment']),
                        'reference': f'WD-{txn_counter:06d}',
                        'channel': 'API'
                    })
                    txn_counter += 1

                    # Transaction fee if applicable
                    if txn_fee > 0:
                        transactions.append({
                            'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                            'account_id': account_id,
                            'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'value_date': current_date.strftime('%Y-%m-%d'),
                            'type': 'Debit',
                            'category': 'Fee',
                            'amount': txn_fee,
                            'description': 'Transaction fee',
                            'reference': f'FEE-{txn_counter:06d}',
                            'channel': 'Batch'
                        })
                        txn_counter += 1

            current_date += timedelta(days=1)

    elif pattern == 'savings':
        # Quarterly deposits, very rare withdrawals
        while current_date <= end_date:
            # Quarterly deposits
            if current_date.month in [1, 4, 7, 10] and current_date.day == 15:
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(1000, 1500), 2),
                    'description': 'Savings deposit',
                    'reference': f'SAV-{current_date.strftime("%Y%m")}',
                    'channel': 'UI'
                })
                txn_counter += 1

            current_date += timedelta(days=7)

    elif pattern == 'professional':
        # Higher salary, moderate spending
        while current_date <= end_date:
            if current_date.day == 1 or (current_date == start_date):
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(4000, 5000), 2),
                    'description': 'Salary deposit',
                    'reference': f'SAL-{current_date.strftime("%Y%m")}',
                    'channel': 'Batch'
                })
                txn_counter += 1

            if random.random() < 0.1:
                amount = round(random.uniform(100, 500), 2)
                if calc_balance(transactions) >= amount:
                    transactions.append({
                        'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                        'account_id': account_id,
                        'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'value_date': current_date.strftime('%Y-%m-%d'),
                        'type': 'Debit',
                        'category': 'Withdrawal',
                        'amount': amount,
                        'description': random.choice(['ATM withdrawal', 'Online transfer']),
                        'reference': f'WD-{txn_counter:06d}',
                        'channel': 'API'
                    })
                    txn_counter += 1

            current_date += timedelta(days=1)

    elif pattern == 'student':
        # Small irregular deposits, frequent small purchases
        while current_date <= end_date:
            if random.random() < 0.1:  # Occasional deposit
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(100, 300), 2),
                    'description': random.choice(['Part-time job', 'Allowance', 'Gift']),
                    'reference': f'DEP-{txn_counter:06d}',
                    'channel': 'UI'
                })
                txn_counter += 1

            if random.random() < 0.2:  # Frequent small purchases
                amount = round(random.uniform(5, 50), 2)
                if calc_balance(transactions) >= amount:
                    transactions.append({
                        'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                        'account_id': account_id,
                        'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'value_date': current_date.strftime('%Y-%m-%d'),
                        'type': 'Debit',
                        'category': 'Withdrawal',
                        'amount': amount,
                        'description': random.choice(['Coffee shop', 'Grocery', 'Online purchase']),
                        'reference': f'WD-{txn_counter:06d}',
                        'channel': 'API'
                    })
                    txn_counter += 1

            current_date += timedelta(days=1)

    elif pattern == 'business':
        # Large irregular deposits and withdrawals
        while current_date <= end_date:
            if random.random() < 0.15:
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(2000, 8000), 2),
                    'description': 'Business revenue',
                    'reference': f'REV-{current_date.strftime("%Y%m%d")}',
                    'channel': 'API'
                })
                txn_counter += 1

            if random.random() < 0.12:
                amount = round(random.uniform(1000, 5000), 2)
                # Only add withdrawal if we have sufficient balance
                if calc_balance(transactions) >= amount:
                    transactions.append({
                        'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                        'account_id': account_id,
                        'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'value_date': current_date.strftime('%Y-%m-%d'),
                        'type': 'Debit',
                        'category': 'Withdrawal',
                        'amount': amount,
                        'description': random.choice(['Supplier payment', 'Payroll', 'Rent']),
                        'reference': f'EXP-{current_date.strftime("%Y%m%d")}',
                        'channel': 'API'
                    })
                    txn_counter += 1

            current_date += timedelta(days=1)

    elif pattern == 'low_balance':
        # Minimal activity
        while current_date <= end_date:
            if random.random() < 0.05:
                transactions.append({
                    'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
                    'account_id': account_id,
                    'transaction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'value_date': current_date.strftime('%Y-%m-%d'),
                    'type': 'Credit',
                    'category': 'Deposit',
                    'amount': round(random.uniform(20, 100), 2),
                    'description': 'Cash deposit',
                    'reference': f'DEP-{txn_counter:06d}',
                    'channel': 'UI'
                })
                txn_counter += 1

            current_date += timedelta(days=3)

    # Sort transactions chronologically
    transactions.sort(key=lambda x: x['transaction_date'])

    # Add monthly interest accrual (last day of each month)
    if interest_rate > 0:
        transactions = add_monthly_interest(transactions, account_id, account_number,
                                           start_date, end_date, interest_rate, txn_counter)

    # Adjust to reach target balance
    transactions = adjust_to_target_balance(transactions, account_id, account_number,
                                            target_balance, end_date, len(transactions) + 1)

    return transactions


def add_monthly_interest(transactions, account_id, account_number, start_date, end_date,
                        interest_rate, txn_counter):
    """Add monthly interest accrual transactions"""

    current_month = start_date.replace(day=1)

    while current_month <= end_date:
        # Last day of month
        next_month = current_month.replace(day=28) + timedelta(days=4)
        last_day = (next_month.replace(day=1) - timedelta(days=1))

        if last_day <= end_date and last_day >= start_date:
            # Calculate balance at end of month
            month_balance = 0.00
            for txn in transactions:
                txn_date = datetime.strptime(txn['transaction_date'], '%Y-%m-%d %H:%M:%S')
                if txn_date <= last_day:
                    if txn['type'] == 'Credit':
                        month_balance += txn['amount']
                    else:
                        month_balance -= txn['amount']

            # Calculate monthly interest (simple interest)
            if month_balance > 0:
                daily_rate = interest_rate / 365
                days_in_month = (last_day - current_month).days + 1
                interest = round(month_balance * daily_rate * days_in_month, 2)

                if interest > 0:
                    transactions.append({
                        'transaction_id': f'TXN-{account_number}-INT-{current_month.strftime("%Y%m")}',
                        'account_id': account_id,
                        'transaction_date': last_day.strftime('%Y-%m-%d 23:59:59'),
                        'value_date': last_day.strftime('%Y-%m-%d'),
                        'type': 'Credit',
                        'category': 'Interest',
                        'amount': interest,
                        'description': f'Interest for {current_month.strftime("%B %Y")}',
                        'reference': f'INT-{current_month.strftime("%Y%m")}',
                        'channel': 'Batch'
                    })

        current_month = current_month.replace(day=1) + timedelta(days=32)
        current_month = current_month.replace(day=1)

    transactions.sort(key=lambda x: x['transaction_date'])
    return transactions


def adjust_to_target_balance(transactions, account_id, account_number, target_balance,
                             end_date, txn_counter):
    """Add final adjustment transaction to reach exact target balance"""

    # Calculate current balance from all transactions
    current_balance = 0.00
    for txn in transactions:
        if txn['type'] == 'Credit':
            current_balance += txn['amount']
        else:
            current_balance -= txn['amount']

    current_balance = round(current_balance, 2)
    difference = round(target_balance - current_balance, 2)

    if abs(difference) >= 0.01:  # Only adjust if difference is significant
        # Add final adjustment transaction
        adjustment_date = end_date - timedelta(days=random.randint(0, 5))

        transactions.append({
            'transaction_id': f'TXN-{account_number}-{txn_counter:04d}',
            'account_id': account_id,
            'transaction_date': adjustment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'value_date': adjustment_date.strftime('%Y-%m-%d'),
            'type': 'Credit' if difference > 0 else 'Debit',
            'category': 'Deposit' if difference > 0 else 'Withdrawal',
            'amount': abs(difference),
            'description': 'Balance adjustment',
            'reference': f'ADJ-{account_number}',
            'channel': 'UI'
        })

        transactions.sort(key=lambda x: x['transaction_date'])

    return transactions


if __name__ == "__main__":
    generate_realistic_data()
