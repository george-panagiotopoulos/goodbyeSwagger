#!/usr/bin/env python3
"""
Database Initialization Script
Creates the SQLite database and runs all migrations
"""

import sqlite3
import os
import sys
from pathlib import Path

# Get database directory
DB_DIR = Path(__file__).parent.parent
SCHEMA_DIR = DB_DIR / "schema" / "migrations"
DB_FILE = DB_DIR / "accounts.db"


def create_database():
    """Create the database file and run migrations"""
    print("=" * 80)
    print("Account Processing System - Database Initialization")
    print("=" * 80)

    # Check if database already exists
    if DB_FILE.exists():
        response = input(f"\nDatabase already exists at {DB_FILE}\nDo you want to recreate it? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborting initialization.")
            sys.exit(0)
        else:
            print(f"Removing existing database: {DB_FILE}")
            os.remove(DB_FILE)

    print(f"\nCreating database: {DB_FILE}")

    # Create database connection
    conn = sqlite3.connect(str(DB_FILE))
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Get all migration files
    migration_files = sorted(SCHEMA_DIR.glob("*.sql"))

    if not migration_files:
        print(f"ERROR: No migration files found in {SCHEMA_DIR}")
        sys.exit(1)

    print(f"\nFound {len(migration_files)} migration(s):")
    for migration_file in migration_files:
        print(f"  - {migration_file.name}")

    # Run each migration
    print("\nRunning migrations...")
    for migration_file in migration_files:
        print(f"\nExecuting: {migration_file.name}")
        with open(migration_file, 'r') as f:
            migration_sql = f.read()

        try:
            cursor.executescript(migration_sql)
            conn.commit()
            print(f"  ✓ Success")
        except sqlite3.Error as e:
            print(f"  ✗ Error: {e}")
            conn.rollback()
            sys.exit(1)

    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()

    print(f"\nCreated {len(tables)} table(s):")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]} ({count} rows)")

    # Close connection
    conn.close()

    print("\n" + "=" * 80)
    print("Database initialization completed successfully!")
    print("=" * 80)
    print(f"\nDatabase location: {DB_FILE}")
    print(f"Database size: {DB_FILE.stat().st_size / 1024:.2f} KB")
    print("\nNext steps:")
    print("  1. Run seed data: python scripts/seed_data.py")
    print("  2. Verify database: sqlite3 accounts.db \".schema\"")
    print("=" * 80)


if __name__ == "__main__":
    create_database()
