#!/usr/bin/env python3
"""
Database Seed Data Script
Loads initial test data into the database
"""

import sqlite3
import sys
from pathlib import Path

# Get database directory
DB_DIR = Path(__file__).parent.parent
SEED_DIR = DB_DIR / "schema" / "seed"
DB_FILE = DB_DIR / "accounts.db"


def seed_database():
    """Load seed data into the database"""
    print("=" * 80)
    print("Account Processing System - Database Seeding")
    print("=" * 80)

    # Check if database exists
    if not DB_FILE.exists():
        print(f"ERROR: Database not found at {DB_FILE}")
        print("Please run 'python scripts/init_db.py' first")
        sys.exit(1)

    print(f"\nDatabase: {DB_FILE}")

    # Create database connection
    conn = sqlite3.connect(str(DB_FILE))
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Get all seed files
    seed_files = sorted(SEED_DIR.glob("*.sql"))

    if not seed_files:
        print(f"WARNING: No seed files found in {SEED_DIR}")
        sys.exit(0)

    print(f"\nFound {len(seed_files)} seed file(s):")
    for seed_file in seed_files:
        print(f"  - {seed_file.name}")

    # Ask for confirmation
    response = input("\nLoad seed data into database? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborting seed operation.")
        sys.exit(0)

    # Run each seed file
    print("\nLoading seed data...")
    for seed_file in seed_files:
        print(f"\nExecuting: {seed_file.name}")
        with open(seed_file, 'r') as f:
            seed_sql = f.read()

        try:
            cursor.executescript(seed_sql)
            conn.commit()
            print(f"  ✓ Success")
        except sqlite3.Error as e:
            print(f"  ✗ Error: {e}")
            conn.rollback()
            # Continue with other seed files even if one fails
            continue

    # Show summary
    print("\n" + "-" * 80)
    print("Data Summary:")
    print("-" * 80)

    tables = ['users', 'products', 'accounts', 'transactions', 'interest_accruals']
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"  {table:25} {count:5} rows")
        except sqlite3.Error:
            print(f"  {table:25} (table not found)")

    # Show account balances
    print("\n" + "-" * 80)
    print("Account Balances:")
    print("-" * 80)
    cursor.execute("""
        SELECT
            a.account_number,
            a.customer_id,
            p.product_name,
            a.balance,
            a.status
        FROM accounts a
        JOIN products p ON a.product_id = p.product_id
        ORDER BY a.account_number;
    """)

    accounts = cursor.fetchall()
    total_balance = 0
    for acc in accounts:
        print(f"  {acc[0]} | {acc[1]:10} | {acc[2]:20} | ${acc[3]:10.2f} | {acc[4]}")
        total_balance += acc[3]

    print("-" * 80)
    print(f"  Total Balance: ${total_balance:,.2f}")

    # Close connection
    conn.close()

    print("\n" + "=" * 80)
    print("Database seeding completed successfully!")
    print("=" * 80)
    print("\nTest Credentials:")
    print("  Admin:   admin / admin123")
    print("  Officer: officer / officer123")
    print("  Viewer:  viewer / viewer123")
    print("\nYou can now start the application!")
    print("=" * 80)


if __name__ == "__main__":
    seed_database()
