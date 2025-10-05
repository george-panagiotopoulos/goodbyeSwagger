# Developer Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Audience**: Development Team

---

## Important: Source Code Ownership

**This codebase is delivered with full source code access to customers.** Unlike proprietary banking platforms, clients receive:

- Complete access to all source code (UI, API, Business Logic, Database)
- Rights to modify, extend, and customize without restrictions
- No vendor lock-in or licensing limitations on development
- Freedom to maintain and evolve the platform independently

**Development Implications**:
- Write **production-quality code** knowing customers will read and modify it
- **Document thoroughly** - your comments help client development teams
- Follow **industry best practices** - this code represents our technical expertise
- **Think long-term** - customers may build on this foundation for years

---

## Table of Contents
1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Development Workflow](#development-workflow)
5. [Testing Guidelines](#testing-guidelines)
6. [Git Workflow](#git-workflow)
7. [Debugging](#debugging)
8. [Performance](#performance)
9. [Security](#security)

---

## Development Setup

### Prerequisites

Install the following before starting development:

1. **Rust Toolchain** (1.70+)
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   rustup update
   ```

2. **Python** (3.8+)
   ```bash
   python3 --version
   ```

3. **Node.js** (16+) and npm (8+)
   ```bash
   node --version
   npm --version
   ```

4. **SQLite** (3.x)
   ```bash
   sqlite3 --version
   ```

5. **Development Tools**
   ```bash
   # Rust tools
   cargo install cargo-watch     # Auto-rebuild on file changes
   cargo install cargo-edit       # Manage dependencies

   # Optional
   cargo install cargo-expand     # View macro expansions
   cargo install cargo-audit      # Security vulnerability scanning
   ```

### IDE Setup

**Recommended**: Visual Studio Code

**Required Extensions**:
- rust-analyzer - Rust language support
- CodeLLDB - Rust debugging
- Even Better TOML - TOML syntax
- ES7+ React/Redux/React-Native snippets - React development
- TypeScript + JavaScript - Type checking
- Prettier - Code formatter
- SQLite Viewer - Database inspection

**VSCode Settings** (`.vscode/settings.json`):
```json
{
  "rust-analyzer.checkOnSave.command": "clippy",
  "editor.formatOnSave": true,
  "[rust]": {
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Local Environment

1. **Clone Repository**
   ```bash
   git clone <repository_url>
   cd Accounts
   ```

2. **Database Setup**
   ```bash
   cd Database
   python3 scripts/init_db.py
   python3 scripts/clean_and_reseed.py
   ```

3. **API Setup**
   ```bash
   cd ../API
   cargo build
   cargo test
   ```

4. **UI Setup**
   ```bash
   cd ../UI
   npm install
   npm run dev
   ```

5. **Verify Setup**
   ```bash
   cd ..
   ./start.sh
   curl http://localhost:6600/health
   curl http://localhost:6601
   ```

---

## Project Structure

### Repository Layout

```
Accounts/
├── Database/              # SQLite + Python
│   ├── schema/
│   │   └── migrations/    # SQL migration files
│   ├── scripts/           # Python utilities
│   ├── accounts.db        # SQLite database (generated)
│   └── requirements.txt
│
├── Application/           # Rust business logic library
│   ├── src/
│   │   ├── domain/        # Domain models
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Business logic services (future)
│   │   ├── utils/         # Utility functions (future)
│   │   ├── error.rs       # Error types
│   │   └── lib.rs         # Library root
│   ├── tests/             # Integration tests
│   └── Cargo.toml
│
├── API/                   # Rust REST API (Actix-web)
│   ├── src/
│   │   ├── handlers/      # HTTP request handlers
│   │   ├── middleware/    # Authentication, logging, etc.
│   │   ├── models/        # API request/response DTOs
│   │   ├── app_state.rs   # Application state
│   │   └── main.rs        # Server entry point
│   ├── tests/             # API tests
│   ├── test_curl.sh       # Manual API testing
│   └── Cargo.toml
│
├── UI/                    # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── pages/         # Page components (routes)
│   │   ├── services/      # API client functions
│   │   ├── types/         # TypeScript type definitions
│   │   ├── App.tsx        # Main app component
│   │   ├── App.css        # Global styles
│   │   └── main.tsx       # Entry point
│   ├── public/            # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docs/                  # External documentation
│   ├── api/               # API specifications
│   ├── user_guides/       # User documentation
│   ├── examples/          # Code examples
│   └── README.md
│
├── internal_docs/         # Internal documentation
│   ├── project_state/     # Current state docs
│   ├── roadmap/           # Product roadmap
│   ├── dev_guidelines/    # This file
│   └── technical_specs/   # Technical specifications
│
├── start.sh               # Start all services
├── stop.sh                # Stop all services
├── claude.md              # Project overview
└── README.md              # Repository readme
```

### Module Organization

#### Rust Application Layer

**Domain Models** (`Application/src/domain/`):
- Each entity in its own file (e.g., `account.rs`, `product.rs`)
- Self-contained with validation logic
- No external dependencies except `serde`, `chrono`, `rust_decimal`

**Repositories** (`Application/src/repositories/`):
- One repository per domain entity
- Implements CRUD operations
- Direct SQLite access via `rusqlite`
- Returns `Result<T, AppError>`

**Services** (Future - `Application/src/services/`):
- Business logic orchestration
- Multi-entity operations
- Transaction coordination

#### Rust API Layer

**Handlers** (`API/src/handlers/`):
- One file per resource (e.g., `account_handlers.rs`)
- Thin layer - delegate to domain/repositories
- Return `Result<HttpResponse>`
- Use `web::Json` for request bodies

**Models** (`API/src/models/`):
- Request/Response DTOs
- Separate from domain models
- Implement `Serialize`/`Deserialize`

**Middleware** (`API/src/middleware/`):
- Authentication (`auth.rs`)
- Logging (Actix-web built-in)
- CORS (Actix-web built-in)

#### React UI

**Components** (`UI/src/components/`):
- Reusable, composable components
- Props-based API
- Minimal state (lift state up)

**Pages** (`UI/src/pages/`):
- Route-level components
- Manage page state
- Call API services

**Services** (`UI/src/services/`):
- API client functions
- Axios-based
- Type-safe (TypeScript)

---

## Coding Standards

### Rust

#### Style

Follow standard Rust formatting:
```bash
cargo fmt
cargo clippy
```

#### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Types | PascalCase | `Product`, `Transaction` |
| Functions | snake_case | `create_account`, `get_balance` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_CURRENCY`, `MAX_BALANCE` |
| Modules | snake_case | `account_handlers`, `product_repository` |

#### Error Handling

**Always use `Result<T, E>`**:
```rust
// Good
pub fn create_account(...) -> Result<Account, AppError> {
    // ...
}

// Bad - don't panic in library code
pub fn create_account(...) -> Account {
    // ... .unwrap()  ❌
}
```

**Custom error types**:
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    DatabaseError(#[from] rusqlite::Error),

    #[error("Validation error: {0}")]
    ValidationError(String),

    // ...
}
```

#### Documentation

Document public APIs:
```rust
/// Creates a new account for a customer.
///
/// # Arguments
/// * `customer_id` - The customer's unique identifier
/// * `product_id` - The product to use for the account
/// * `opening_balance` - Initial account balance
///
/// # Returns
/// * `Ok(Account)` - Successfully created account
/// * `Err(AppError)` - If customer/product not found or validation fails
///
/// # Example
/// ```
/// let account = Account::new("CUST-001", "PROD-001", dec!(1000.00))?;
/// ```
pub fn new(customer_id: String, product_id: String, opening_balance: Decimal) -> Result<Self, AppError> {
    // ...
}
```

#### Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_account_creation() {
        let account = Account::new(
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            dec!(1000.00),
        ).unwrap();

        assert_eq!(account.balance, dec!(1000.00));
        assert_eq!(account.status, AccountStatus::Active);
    }

    #[test]
    fn test_insufficient_balance() {
        let mut account = create_test_account();
        let result = account.debit(dec!(2000.00));

        assert!(result.is_err());
        assert_eq!(account.balance, dec!(1000.00)); // Unchanged
    }
}
```

---

### TypeScript/React

#### Style

Use Prettier for formatting:
```bash
npm run format
```

#### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `AccountForm`, `ProductList` |
| Functions | camelCase | `fetchAccounts`, `handleSubmit` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL`, `MAX_RETRIES` |
| Interfaces/Types | PascalCase | `Account`, `ApiResponse<T>` |
| Files | camelCase or PascalCase | `accountService.ts`, `AccountDetail.tsx` |

#### Type Safety

**Always define types**:
```typescript
// Good
interface Account {
  account_id: string;
  balance: number;
  currency: string;
}

function fetchAccount(id: string): Promise<Account> {
  // ...
}

// Bad - avoid 'any'
function fetchAccount(id: any): Promise<any> {  ❌
  // ...
}
```

**Use generics for API responses**:
```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: ApiError;
}

const response = await api.get<ApiResponse<Account[]>>('/api/accounts');
const accounts = response.data.data; // Type-safe
```

#### React Best Practices

**Functional components with hooks**:
```typescript
interface Props {
  accountId: string;
}

export default function AccountDetail({ accountId }: Props) {
  const [account, setAccount] = useState<Account | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAccount();
  }, [accountId]);

  const loadAccount = async () => {
    try {
      const data = await accountService.getById(accountId);
      setAccount(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!account) return <div>Not found</div>;

  return (
    <div>
      <h1>{account.account_number}</h1>
      {/* ... */}
    </div>
  );
}
```

---

### SQL

#### Naming

- Tables: lowercase, plural (`accounts`, `transactions`)
- Columns: lowercase, snake_case (`account_id`, `created_at`)
- Indexes: `idx_{table}_{column}` (`idx_accounts_customer_id`)
- Foreign keys: `fk_{table}_{ref_table}` (`fk_accounts_customers`)

#### Migrations

**Filename format**: `NNN_description.sql`
- Example: `001_initial_schema.sql`, `002_add_customers.sql`

**Content**:
```sql
-- Migration 003: Add monthly interest accruals
-- Date: 2025-10-05
-- Author: Dev Team

CREATE TABLE IF NOT EXISTS monthly_interest_accruals (
    monthly_accrual_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    -- ...
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX idx_monthly_accruals_account ON monthly_interest_accruals(account_id);
CREATE INDEX idx_monthly_accruals_month ON monthly_interest_accruals(accrual_month);
```

---

## Development Workflow

### Adding a New Feature

1. **Update Documentation First**
   - Add to roadmap if not present
   - Create technical spec (if complex)
   - Update API documentation

2. **Database Changes**
   - Create migration script (`NNN_description.sql`)
   - Test migration on clean database
   - Update seed data if needed

3. **Domain Model**
   - Add/update domain entity (`Application/src/domain/`)
   - Add validation logic
   - Write unit tests

4. **Repository**
   - Add/update repository (`Application/src/repositories/`)
   - Implement CRUD operations
   - Handle new database fields

5. **API Handler**
   - Add request/response models (`API/src/models/`)
   - Implement handler (`API/src/handlers/`)
   - Register route (`API/src/main.rs`)
   - Test with curl

6. **UI Integration**
   - Add TypeScript types (`UI/src/types/`)
   - Create service function (`UI/src/services/`)
   - Build component (`UI/src/components/` or `pages/`)
   - Integrate into navigation

7. **Testing**
   - Run all tests: `cargo test` (Application + API)
   - Test UI manually
   - Run `test_curl.sh`
   - Add integration tests

8. **Documentation**
   - Update API spec (OpenAPI)
   - Update API vocabulary
   - Add usage examples
   - Update changelog

### Example: Adding "Account Freeze" Feature

```bash
# 1. Create migration
echo "ALTER TABLE accounts ADD COLUMN frozen BOOLEAN DEFAULT 0;" > Database/schema/migrations/004_add_frozen_status.sql

# 2. Update domain model
# Edit Application/src/domain/account.rs
# Add frozen: bool field
# Add freeze() and unfreeze() methods

# 3. Update repository
# Edit Application/src/repositories/account_repository.rs
# Update SQL queries to include frozen field

# 4. Add API endpoint
# Create API/src/handlers/account_handlers.rs::freeze_account()
# Add route: .route("/accounts/{id}/freeze", web::post().to(freeze_account))

# 5. Test
cargo test
./test_curl.sh

# 6. Add UI
# Edit UI/src/pages/AccountDetail.tsx
# Add "Freeze Account" button
# Call new API endpoint
```

---

## Testing Guidelines

### Unit Tests (Rust)

**Location**: Same file as code, in `#[cfg(test)]` module

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    fn create_test_account() -> Account {
        Account {
            account_id: "ACC-TEST".to_string(),
            balance: dec!(1000.00),
            // ...
        }
    }

    #[test]
    fn test_credit_increases_balance() {
        let mut account = create_test_account();
        account.credit(dec!(500.00)).unwrap();
        assert_eq!(account.balance, dec!(1500.00));
    }
}
```

### Integration Tests (Rust)

**Location**: `tests/` directory

```rust
// tests/account_tests.rs
use accounts_application::domain::Account;
use accounts_application::repositories::AccountRepository;

#[test]
fn test_create_and_retrieve_account() {
    let repo = AccountRepository::new("test.db").unwrap();
    let account = Account::new(/* ... */).unwrap();

    repo.create(&account).unwrap();
    let retrieved = repo.find_by_id(&account.account_id).unwrap();

    assert_eq!(retrieved.unwrap().account_id, account.account_id);
}
```

### API Testing

**Manual** (`test_curl.sh`):
```bash
#!/bin/bash
# Test account creation
echo "Testing: Create Account"
RESPONSE=$(curl -s -X POST http://localhost:6600/api/accounts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST-001","product_id":"PROD-001","opening_balance":"1000.00"}')

if echo "$RESPONSE" | grep -q "account_id"; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi
```

### UI Testing

Currently manual. Future: Add Jest + React Testing Library.

---

## Git Workflow

### Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/description` | `feature/add-account-freeze` |
| Bug Fix | `fix/description` | `fix/balance-calculation` |
| Hotfix | `hotfix/description` | `hotfix/security-patch` |
| Docs | `docs/description` | `docs/api-spec-update` |

### Commit Messages

Format: `<type>: <description>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat: add account freeze endpoint
fix: correct balance calculation for fees
docs: update API vocabulary with new fields
refactor: extract validation logic to util
test: add unit tests for interest calculation
```

### Pull Request Process

1. Create feature branch
2. Make changes
3. Run all tests
4. Update documentation
5. Create PR with description
6. Request review
7. Address feedback
8. Merge after approval

---

## Debugging

### Rust Debugging

**Print debugging**:
```rust
dbg!(&account);  // Prints debug representation
println!("Balance: {:?}", account.balance);
```

**Logging**:
```rust
use log::{info, warn, error, debug};

info!("Creating account for customer {}", customer_id);
warn!("Low balance: {}", balance);
error!("Failed to create account: {}", e);
```

**VSCode debugging**:
Launch configuration (`.vscode/launch.json`):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug API",
      "cargo": {
        "args": ["build", "--bin=accounts_api"],
        "filter": {
          "name": "accounts_api",
          "kind": "bin"
        }
      }
    }
  ]
}
```

### Database Debugging

**Inspect database**:
```bash
sqlite3 accounts.db
sqlite> .tables
sqlite> .schema accounts
sqlite> SELECT * FROM accounts WHERE account_id = 'ACC-001';
```

**Transaction log**:
```sql
SELECT * FROM transactions
WHERE account_id = 'ACC-001'
ORDER BY created_at DESC
LIMIT 10;
```

### API Debugging

**Check logs**:
```bash
tail -f logs/api.log
```

**Test endpoint**:
```bash
curl -v http://localhost:6600/api/accounts \
  -H "Authorization: Bearer $TOKEN"
```

---

## Performance

### Rust Performance

- Use `Decimal` for financial calculations (not `f64`)
- Avoid unnecessary cloning - use references
- Use iterators instead of loops where possible
- Profile with `cargo flamegraph`

### Database Performance

- Add indexes on frequently queried columns
- Use `EXPLAIN QUERY PLAN` to analyze queries
- Batch inserts when possible
- Consider connection pooling for production

### API Performance

- Keep handlers thin
- Delegate to domain layer
- Use caching for static data
- Implement pagination for large result sets

---

## Security

### Authentication

- All endpoints protected except `/health` and `/api/auth/*`
- JWT tokens expire after 1 hour
- Passwords hashed with bcrypt
- Never log tokens or passwords

### Input Validation

- Validate all user input
- Use type system for validation
- Sanitize SQL inputs (use parameterized queries)
- Validate decimal precision

### SQL Injection Prevention

**Always use parameterized queries**:
```rust
// Good
conn.execute(
    "INSERT INTO accounts (account_id, balance) VALUES (?1, ?2)",
    params![account_id, balance]
)?;

// Bad
let sql = format!("INSERT INTO accounts VALUES ('{}', {})", account_id, balance);  ❌
conn.execute(&sql, [])?;
```

---

## Common Issues

### Issue: Port Already in Use

**Error**: `Address already in use (os error 48)`

**Solution**:
```bash
./stop.sh
# Wait 5 seconds
./start.sh
```

### Issue: Database Locked

**Error**: `database is locked`

**Solution**:
```bash
# Stop all services
./stop.sh

# Check for processes
lsof accounts.db

# Kill if necessary
kill -9 <PID>
```

### Issue: Compilation Errors

**Error**: Borrow checker errors

**Solution**:
- Read error message carefully
- Understand ownership rules
- Use references instead of moving values
- Clone when necessary (but sparingly)

---

## Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [Actix-web Documentation](https://actix.rs/docs/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**Document Version**: 1.0.0
**Maintained By**: Development Team
**Last Review**: 2025-10-05
**Next Review**: 2025-10-12
