# Known Issues and Limitations
## Account Processing System

**Version**: 1.0 (MVP)
**Last Updated**: October 2025
**Status**: Active Development

---

## Overview

This document tracks known issues, limitations, and technical debt in the Account Processing System MVP. Issues are categorized by severity and component.

---

## Issue Categories

- 🔴 **Critical**: System breaking, data loss risk, security vulnerability
- 🟠 **High**: Major functionality impacted, workaround exists
- 🟡 **Medium**: Minor functionality impacted, cosmetic issues
- 🟢 **Low**: Nice-to-have, future enhancement

---

## Current Known Issues

### API Layer

#### 🟠 ISSUE-001: Nested Data Response Structure
**Component**: API Response Handler
**Severity**: High
**Status**: Known, Workaround Applied

**Description**:
The API returns responses wrapped in a nested `data` structure, requiring clients to access values via `response.data.data` instead of `response.data`.

**Example**:
```json
{
  "data": {
    "data": [
      { "account_id": "ACCT-001", ... }
    ]
  }
}
```

**Impact**:
- Inconsistent with REST best practices
- Requires extra unwrapping in UI code
- API documentation shows flatter structure

**Workaround**:
UI components unwrap the nested data structure as documented in AccountDetail.tsx:116, Customers.tsx:58, Products.tsx:62

**Resolution Plan**:
Refactor API response handler in Rust to return single-level data structure (Planned: Q1 2026)

**References**:
- `/Accounts/UI/src/pages/AccountDetail.tsx:116`
- `/Accounts/UI/src/pages/Customers.tsx:58`
- `/Accounts/UI/src/pages/Products.tsx:62`

---

#### 🟡 ISSUE-002: Missing Request Validation
**Component**: API Endpoints
**Severity**: Medium
**Status**: Known

**Description**:
Some API endpoints lack comprehensive input validation, relying on database constraints to catch errors.

**Affected Endpoints**:
- `POST /api/accounts` - No validation for negative opening balance
- `POST /api/products` - Limited validation on fee amounts
- `PUT /api/products/:id` - No validation preventing interest rate > 100%

**Impact**:
- Poor error messages for invalid input
- Database errors exposed to clients
- Security risk for injection attacks (partially mitigated)

**Workaround**:
Frontend performs validation before submission

**Resolution Plan**:
Add request validation layer with Validator crate (Planned: Q1 2026)

---

#### 🟢 ISSUE-003: No Rate Limiting
**Component**: API Gateway
**Severity**: Low
**Status**: Known, Not Implemented

**Description**:
API does not implement rate limiting, making it vulnerable to abuse and DDoS attacks.

**Impact**:
- Potential for API abuse
- No protection against brute force attacks
- Scalability concerns under load

**Workaround**:
Deploy behind reverse proxy (nginx) with rate limiting in production

**Resolution Plan**:
Implement token bucket rate limiting (Planned: Q2 2026)

---

### Database Layer

#### 🟡 ISSUE-004: SQLite Concurrency Limitations
**Component**: Database
**Severity**: Medium
**Status**: Known, By Design (MVP)

**Description**:
SQLite has limited write concurrency, causing "database is locked" errors under high concurrent write load.

**Impact**:
- Failed transactions during peak load
- Poor performance with > 100 concurrent writers
- Not suitable for production at scale

**Workaround**:
- Connection pooling with retry logic
- Batch processing for bulk operations

**Resolution Plan**:
Migrate to PostgreSQL for production deployment (Planned: Q1 2026)

---

#### 🟠 ISSUE-005: Missing Indexes on Transaction Date
**Component**: Database Schema
**Severity**: High
**Status**: Known

**Description**:
Large ledger queries perform full table scans when filtering by date range.

**Impact**:
- Slow query performance for date-based queries
- Degraded performance as transaction volume grows

**Workaround**:
Limit date ranges in queries

**Resolution Plan**:
Add composite index on (account_id, transaction_date) (Planned: Q4 2025)

**SQL Fix**:
```sql
CREATE INDEX idx_transaction_account_date
ON transaction(account_id, transaction_date DESC);
```

---

#### 🔴 ISSUE-006: No Transaction Rollback on Batch Failure
**Component**: Batch Processing
**Severity**: Critical
**Status**: Under Investigation

**Description**:
If interest calculation batch fails mid-process, partial results are committed without rollback.

**Impact**:
- Data integrity risk
- Duplicate interest accruals possible
- Manual reconciliation required

**Workaround**:
- Run batch processing during maintenance window
- Verify results before committing
- Keep detailed logs for reconciliation

**Resolution Plan**:
Implement proper transaction boundaries for batch operations (Urgent: Q4 2025)

---

### Business Logic

#### 🟡 ISSUE-007: Interest Calculation Rounding Errors
**Component**: Interest Service
**Severity**: Medium
**Status**: Known, By Design

**Description**:
30/360 day count convention with decimal rounding can cause minor balance discrepancies (< $0.01) over time.

**Impact**:
- Cumulative rounding errors
- Balance reconciliation challenges
- Potential regulatory compliance issues

**Workaround**:
Monthly reconciliation process

**Resolution Plan**:
Implement banker's rounding and periodic balance correction (Planned: Q1 2026)

---

#### 🟢 ISSUE-008: No Support for Overdraft Protection
**Component**: Transaction Processing
**Severity**: Low
**Status**: Not Implemented

**Description**:
System rejects all debit transactions that would result in negative balance. No overdraft facility.

**Impact**:
- Limited product offering
- No grace period for customers

**Workaround**:
None - by design for MVP

**Resolution Plan**:
Add overdraft product feature (Planned: Q2 2026)

---

### UI Layer

#### 🟡 ISSUE-009: No Form Validation Feedback
**Component**: React Forms
**Severity**: Medium
**Status**: Known

**Description**:
Form components don't provide real-time validation feedback. Errors only shown after submission.

**Impact**:
- Poor user experience
- Increased error rate
- Multiple failed submissions

**Workaround**:
Users must carefully review before submitting

**Resolution Plan**:
Add real-time validation with React Hook Form (Planned: Q4 2025)

---

#### 🟢 ISSUE-010: Limited Mobile Responsiveness
**Component**: UI Layout
**Severity**: Low
**Status**: Known

**Description**:
UI is functional on mobile but not optimized for small screens. Tables don't scroll well.

**Impact**:
- Suboptimal mobile experience
- Horizontal scrolling required
- Small touch targets

**Workaround**:
Use desktop browser

**Resolution Plan**:
Responsive design overhaul (Planned: Q2 2026)

---

#### 🟡 ISSUE-011: No Loading Indicators
**Component**: UI Components
**Severity**: Medium
**Status**: Partially Implemented

**Description**:
Many components lack loading states, causing UI to appear frozen during API calls.

**Impact**:
- Users unsure if action is processing
- Multiple clicks/submissions
- Poor UX perception

**Workaround**:
Be patient, avoid clicking multiple times

**Resolution Plan**:
Add loading spinners and skeleton screens (Planned: Q4 2025)

---

### Authentication & Security

#### 🔴 ISSUE-012: JWT Tokens Don't Expire
**Component**: Authentication Service
**Severity**: Critical
**Status**: Known, Security Risk

**Description**:
JWT tokens are issued without expiration (`exp` claim), remaining valid indefinitely.

**Impact**:
- Security vulnerability
- Stolen tokens remain valid forever
- No session timeout

**Workaround**:
Manual logout required, clear localStorage

**Resolution Plan**:
Implement token expiration (24hr) and refresh mechanism (Urgent: Q4 2025)

---

#### 🟠 ISSUE-013: Passwords Stored with Weak Hashing
**Component**: User Authentication
**Severity**: High
**Status**: Known

**Description**:
bcrypt used with default cost factor (10), which is below current security recommendations (12-14).

**Impact**:
- Vulnerable to brute force attacks
- Below industry security standards

**Workaround**:
Strong password policy enforcement

**Resolution Plan**:
Increase bcrypt cost to 12 and implement password rotation (Planned: Q1 2026)

---

#### 🟡 ISSUE-014: No HTTPS Enforcement
**Component**: API Server
**Severity**: Medium
**Status**: Known, Deployment Issue

**Description**:
API runs on HTTP in development. HTTPS not enforced.

**Impact**:
- Credentials transmitted in cleartext
- MITM attack vulnerability
- Not production-ready

**Workaround**:
Deploy behind HTTPS reverse proxy (nginx/Cloudflare)

**Resolution Plan**:
Add HTTPS support in Actix-web config (Planned: Q4 2025)

---

### Performance

#### 🟡 ISSUE-015: No Database Connection Pooling
**Component**: Database Layer
**Severity**: Medium
**Status**: Known

**Description**:
Each API request creates a new database connection, causing performance overhead.

**Impact**:
- Slower response times
- Resource exhaustion under load
- Connection limit reached quickly

**Workaround**:
Limit concurrent requests

**Resolution Plan**:
Implement connection pooling with r2d2 (Planned: Q4 2025)

---

#### 🟢 ISSUE-016: Large Ledger Queries Not Paginated
**Component**: Transaction API
**Severity**: Low
**Status**: Known

**Description**:
`GET /api/transactions/ledger/:id` returns all transactions without pagination.

**Impact**:
- Slow response for accounts with many transactions
- High memory usage
- Timeout risk

**Workaround**:
Manually limit query in SQL

**Resolution Plan**:
Add pagination with limit/offset parameters (Planned: Q1 2026)

---

## Limitations (By Design for MVP)

### Feature Limitations

1. **No Multi-Currency Support**
   - Only USD supported
   - No FX rate handling
   - Planned: Q2 2026

2. **No Inter-Account Transfers**
   - Can only credit/debit individual accounts
   - No internal transfer workflow
   - Planned: Q1 2026

3. **Limited Account Status**
   - Only ACTIVE and CLOSED supported
   - No FROZEN, DORMANT, or other statuses
   - Planned: Q2 2026

4. **No Audit Trail**
   - Changes not logged
   - No change history
   - Planned: Q1 2026

5. **No Scheduled Transactions**
   - No recurring payments
   - No future-dated transactions
   - Planned: Q2 2026

### Technical Limitations

1. **Single Database**
   - No read replicas
   - No sharding
   - Scalability limited

2. **No Caching Layer**
   - All queries hit database
   - No Redis/Memcached
   - Performance impact

3. **Synchronous Processing Only**
   - No async job queue
   - Batch operations block
   - No background jobs

4. **Limited Error Handling**
   - Generic error messages
   - No error codes
   - Limited debugging info

---

## Testing Gaps

### Areas Requiring More Test Coverage

1. **Concurrent Transaction Testing**
   - Race conditions not fully tested
   - Simultaneous updates to same account
   - Priority: High

2. **Edge Cases**
   - Very large balances (> $1B)
   - Accounts with millions of transactions
   - Boundary value testing
   - Priority: Medium

3. **Security Testing**
   - Penetration testing not performed
   - SQL injection testing incomplete
   - Auth bypass scenarios
   - Priority: High

4. **Performance Testing**
   - No load testing performed
   - Stress testing incomplete
   - Scalability limits unknown
   - Priority: Medium

---

## Technical Debt

### High Priority Debt

1. **Inconsistent Error Handling**
   - Mix of Result<T,E> and unwrap()
   - Error types not standardized
   - Effort: 2-3 weeks

2. **Code Duplication**
   - Similar logic in handlers
   - Repeated validation code
   - Effort: 1-2 weeks

3. **Missing Documentation**
   - Some functions lack doc comments
   - Complex logic not explained
   - Effort: 1 week

### Medium Priority Debt

1. **Hard-coded Configuration**
   - Port numbers in code
   - Database paths not configurable
   - Effort: 3-5 days

2. **Limited Logging**
   - Insufficient debug logs
   - No structured logging
   - Effort: 1 week

---

## Workarounds & Mitigations

### For Developers

1. **Nested API Response**: Use `.data.data` to access response payload
2. **SQLite Locking**: Add retry logic with exponential backoff
3. **No Pagination**: Limit queries with SQL WHERE clauses
4. **Connection Pooling**: Reuse connections where possible

### For Users

1. **Form Errors**: Review all fields carefully before submit
2. **Mobile Experience**: Use desktop browser when possible
3. **Loading States**: Wait for page to update before clicking again
4. **Security**: Always log out when finished

---

## Issue Reporting

### How to Report New Issues

1. **Check Existing Issues**: Review this document first
2. **Gather Information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs
   - Environment details
3. **Submit via GitHub**: Create issue with template
4. **Severity Assessment**: Team will triage within 48 hours

### Issue Template

```markdown
**Title**: [Component] Brief description

**Severity**: Critical/High/Medium/Low

**Description**:
Detailed description of the issue

**Steps to Reproduce**:
1. Step one
2. Step two
3. ...

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Environment**:
- API Version:
- Database:
- Browser (if UI issue):

**Logs/Screenshots**:
Attach relevant information
```

---

## Resolution Timeline

### Q4 2025 (Current Quarter)
- ✅ ISSUE-012: JWT expiration (Critical)
- ✅ ISSUE-006: Batch transaction rollback (Critical)
- ✅ ISSUE-005: Transaction date index (High)
- ⏳ ISSUE-009: Form validation (Medium)
- ⏳ ISSUE-011: Loading indicators (Medium)
- ⏳ ISSUE-015: Connection pooling (Medium)

### Q1 2026
- ISSUE-001: API response structure (High)
- ISSUE-002: Request validation (Medium)
- ISSUE-004: PostgreSQL migration (Medium)
- ISSUE-007: Interest rounding (Medium)
- ISSUE-013: Password hashing (High)
- ISSUE-016: Ledger pagination (Low)

### Q2 2026
- ISSUE-003: Rate limiting (Low)
- ISSUE-008: Overdraft support (Low)
- ISSUE-010: Mobile responsiveness (Low)

---

## Document Maintenance

This document is reviewed and updated:
- **Weekly**: During sprint planning
- **Monthly**: For major releases
- **Quarterly**: For strategic planning

**Document Owner**: Kevin O'Brien, Senior QA Engineer
**Contributors**: Engineering Team
**Last Review**: October 2025
**Next Review**: November 2025

---

## Appendix: Fixed Issues

### Recently Resolved (October 2025)

#### ✅ FIXED-001: API Response Unwrapping in UI
**Resolution**: Updated UI components to handle nested data structure
**Fixed in**: UI v1.0
**Date**: October 2025

#### ✅ FIXED-002: CORS Configuration
**Resolution**: Added proper CORS middleware to API
**Fixed in**: API v1.0
**Date**: October 2025

#### ✅ FIXED-003: Database Schema Foreign Keys
**Resolution**: Added missing FK constraints
**Fixed in**: Database migration v1.0
**Date**: October 2025

---

© 2025 Account Processing System | Internal Documentation
