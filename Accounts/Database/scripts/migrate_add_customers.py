#!/usr/bin/env python3
"""
Migration script to add customers table and update accounts
"""

import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "accounts.db"
MIGRATION_FILE = Path(__file__).parent.parent / "schema/migrations/002_add_customers.sql"

def run_migration():
    """Apply the customer migration"""
    try:
        # Read migration SQL
        with open(MIGRATION_FILE, 'r') as f:
            migration_sql = f.read()

        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Applying migration: 002_add_customers.sql")

        # Execute migration (split by semicolon for multiple statements)
        statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
        for statement in statements:
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("✓ Migration completed successfully")

        # Verify tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print("\nCurrent tables:")
        for table in tables:
            print(f"  - {table[0]}")

        conn.close()

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
