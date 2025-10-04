#!/usr/bin/env python3
"""
Seed customer data for testing
"""

import sqlite3
from datetime import datetime, UTC
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "accounts.db"

def seed_customers():
    """Create sample customers"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Use SQLite datetime format: YYYY-MM-DD HH:MM:SS
    now = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')

    customers = [
        ('CUST-001', 'EXT-CUST-12345', 'John Doe', 'Individual', 'Active', 'john.doe@email.com', '+1-555-0100', now, now),
        ('CUST-002', 'EXT-CUST-12346', 'Jane Smith', 'Individual', 'Active', 'jane.smith@email.com', '+1-555-0101', now, now),
        ('CUST-003', 'EXT-CUST-12347', 'Acme Corporation', 'Business', 'Active', 'contact@acme.com', '+1-555-0200', now, now),
        ('CUST-004', 'EXT-CUST-12348', 'Tech Startup Inc', 'Business', 'Active', 'admin@techstartup.com', '+1-555-0201', now, now),
        ('CUST-005', None, 'Bob Johnson', 'Individual', 'Active', 'bob.j@email.com', '+1-555-0102', now, now),
        ('CUST-006', None, 'Alice Williams', 'Individual', 'Active', 'alice.w@email.com', '+1-555-0103', now, now),
    ]

    cursor.executemany(
        '''INSERT OR IGNORE INTO customers
           (customer_id, external_customer_id, customer_name, customer_type, status, email, phone, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        customers
    )

    conn.commit()
    print(f"✓ Seeded {cursor.rowcount} customers")

    # Show created customers
    cursor.execute("SELECT customer_id, customer_name, customer_type FROM customers ORDER BY customer_id")
    print("\nCustomers:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]})")

    conn.close()

if __name__ == "__main__":
    seed_customers()
