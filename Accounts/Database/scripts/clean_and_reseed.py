#!/usr/bin/env python3
"""
Clean existing test data and create fresh seed data with:
- 1 default product (Standard Checking Account)
- 5 customers with realistic data
- 1 account per customer
- 2-5 random transactions per account
"""

import sqlite3
import random
from datetime import datetime, timedelta
import uuid
import os

# Get the Database directory path (parent of scripts directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(DB_DIR, 'accounts.db')

def clean_data(conn):
    """Delete all existing data from tables"""
    cursor = conn.cursor()

    print("Cleaning existing data...")
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM accounts")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")

    conn.commit()
    print("✓ All existing data deleted")

def create_default_product(conn):
    """Create the default product for all accounts"""
    cursor = conn.cursor()

    product_id = f"PROD-{uuid.uuid4()}"
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO products (
            product_id, product_code, product_name, description, status,
            currency, interest_rate, minimum_balance_for_interest,
            monthly_maintenance_fee, transaction_fee, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        'CHK-STD-001',
        'Standard Checking Account',
        'Standard checking account with competitive interest rates and low fees',
        'Active',
        'USD',
        0.015,  # 1.5% interest
        1000.00,  # Minimum balance for interest
        5.00,  # Monthly maintenance fee
        0.50,  # Transaction fee
        now,
        now
    ))

    conn.commit()
    print(f"✓ Created default product: {product_id}")
    return product_id

def create_customers(conn):
    """Create 5 customers with realistic data"""
    cursor = conn.cursor()

    customers_data = [
        {
            'name': 'John Smith',
            'type': 'Individual',
            'email': 'john.smith@email.com',
            'phone': '+1-555-0101'
        },
        {
            'name': 'Sarah Johnson',
            'type': 'Individual',
            'email': 'sarah.johnson@email.com',
            'phone': '+1-555-0102'
        },
        {
            'name': 'Tech Solutions Inc',
            'type': 'Business',
            'email': 'accounting@techsolutions.com',
            'phone': '+1-555-0201'
        },
        {
            'name': 'Michael Chen',
            'type': 'Individual',
            'email': 'michael.chen@email.com',
            'phone': '+1-555-0103'
        },
        {
            'name': 'Global Retail LLC',
            'type': 'Business',
            'email': 'finance@globalretail.com',
            'phone': '+1-555-0202'
        }
    ]

    customer_ids = []
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    for i, data in enumerate(customers_data, 1):
        customer_id = f"CUST-{str(i).zfill(3)}"
        external_id = f"EXT-{str(i).zfill(6)}"

        cursor.execute("""
            INSERT INTO customers (
                customer_id, external_customer_id, customer_name, customer_type,
                email, phone, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            external_id,
            data['name'],
            data['type'],
            data['email'],
            data['phone'],
            'Active',
            now,
            now
        ))

        customer_ids.append(customer_id)
        print(f"✓ Created customer: {customer_id} - {data['name']}")

    conn.commit()
    return customer_ids

def create_accounts(conn, product_id, customer_ids):
    """Create 1 account per customer"""
    cursor = conn.cursor()

    account_ids = []
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    opening_date = datetime.utcnow().date().strftime('%Y-%m-%d')

    # Random opening balances
    opening_balances = [5000.00, 12500.50, 25000.00, 3500.75, 50000.00]

    for i, customer_id in enumerate(customer_ids):
        account_id = f"ACC-{uuid.uuid4()}"
        account_number = f"{datetime.now().year}{str(i+1).zfill(6)}"

        cursor.execute("""
            INSERT INTO accounts (
                account_id, account_number, product_id, customer_id, currency,
                balance, interest_accrued, status, opening_date,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            account_id,
            account_number,
            product_id,
            customer_id,
            'USD',
            opening_balances[i],
            0.00,
            'Active',
            opening_date,
            now,
            now
        ))

        account_ids.append({
            'account_id': account_id,
            'customer_id': customer_id,
            'balance': opening_balances[i]
        })
        print(f"✓ Created account: {account_number} for {customer_id} (${opening_balances[i]:,.2f})")

    conn.commit()
    return account_ids

def create_transactions(conn, accounts):
    """Create transactions with proper balance tracking"""
    cursor = conn.cursor()

    transaction_descriptions = {
        'Credit': [
            'Salary Deposit',
            'Wire Transfer In',
            'Direct Deposit',
            'Customer Payment',
            'Interest Credit',
            'Refund',
            'Transfer In'
        ],
        'Debit': [
            'ATM Withdrawal',
            'Online Purchase',
            'Bill Payment',
            'Wire Transfer Out',
            'Check Payment',
            'Monthly Fee',
            'Transfer Out'
        ]
    }

    total_transactions = 0
    base_date = datetime.utcnow() - timedelta(days=30)

    for account in accounts:
        account_id = account['account_id']
        opening_balance = account['balance']

        # First transaction is ALWAYS the opening balance
        opening_txn_id = f"TXN-OPEN-{account_id}"
        opening_date = base_date.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO transactions (
                transaction_id, account_id, type, category, amount, currency,
                running_balance, description, reference, channel,
                transaction_date, value_date, created_at, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opening_txn_id,
            account_id,
            'Credit',
            'Opening',
            opening_balance,
            'USD',
            opening_balance,  # First transaction, so running balance = amount
            'Opening balance',
            'OPENING',
            'API',
            opening_date,
            opening_date[:10],
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'SYSTEM'
        ))

        print(f"\n  Creating transactions for {account_id} (Opening: ${opening_balance:,.2f}):")
        print(f"    Credit ${opening_balance:8,.2f} - Opening balance      (Balance: ${opening_balance:,.2f})")

        # Now create subsequent transactions
        running_balance = opening_balance
        num_additional_txns = random.randint(2, 5)

        for i in range(num_additional_txns):
            # Mix of credits and debits
            txn_type = random.choice(['Credit', 'Credit', 'Debit'])  # 2:1 ratio favoring credits

            # Map transaction type to category
            if txn_type == 'Credit':
                category = random.choice(['Deposit', 'Interest'])
                amount = round(random.uniform(100, 5000), 2)
                running_balance += amount
            else:
                category = random.choice(['Withdrawal', 'Fee'])
                # Ensure we don't go negative
                max_debit = min(running_balance * 0.3, 2000)  # Max 30% of balance or $2000
                amount = round(random.uniform(50, max(max_debit, 100)), 2)
                running_balance -= amount

            # Transaction date (spread over last 29 days after opening)
            days_offset = random.randint(1, 29)
            txn_date = (base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d %H:%M:%S')

            transaction_id = f"TXN-{uuid.uuid4()}"
            description = random.choice(transaction_descriptions[txn_type])
            reference = f"REF-{random.randint(100000, 999999)}"
            channel = random.choice(['API', 'UI', 'Batch'])

            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id, account_id, type, category, amount, currency,
                    running_balance, description, reference, channel,
                    transaction_date, value_date, created_at, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction_id,
                account_id,
                txn_type,
                category,
                amount,
                'USD',
                running_balance,
                description,
                reference,
                channel,
                txn_date,
                txn_date[:10],  # Just the date part
                datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'SYSTEM'
            ))

            total_transactions += 1
            print(f"    {txn_type:6s} ${amount:8,.2f} - {description:20s} (Balance: ${running_balance:,.2f})")

        # Update final account balance to match final running balance
        cursor.execute("""
            UPDATE accounts SET balance = ? WHERE account_id = ?
        """, (running_balance, account_id))

    conn.commit()
    print(f"\n✓ Created {total_transactions + len(accounts)} total transactions (including {len(accounts)} opening transactions)")

def main():
    print("=" * 60)
    print("Account Processing System - Data Cleanup & Reseeding")
    print("=" * 60)
    print()

    conn = sqlite3.connect(DB_PATH)

    try:
        # Step 1: Clean existing data
        clean_data(conn)
        print()

        # Step 2: Create default product
        product_id = create_default_product(conn)
        print()

        # Step 3: Create 5 customers
        print("Creating customers...")
        customer_ids = create_customers(conn)
        print()

        # Step 4: Create 1 account per customer
        print("Creating accounts...")
        accounts = create_accounts(conn, product_id, customer_ids)
        print()

        # Step 5: Create 2-5 transactions per account
        print("Creating transactions...")
        create_transactions(conn, accounts)
        print()

        print("=" * 60)
        print("✓ Database successfully cleaned and reseeded!")
        print("=" * 60)
        print()
        print("Summary:")
        print("  • 1 Product (Standard Checking Account)")
        print("  • 5 Customers (3 Individual, 2 Business)")
        print("  • 5 Accounts (1 per customer)")
        print("  • Multiple transactions per account")
        print()

    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
