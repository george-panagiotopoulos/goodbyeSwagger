# Functional Requirements

## Account Processing System - Current/Checking Accounts

**Document Version**: 1.0
**Last Updated**: 2025-10-04
**Status**: Draft

---

## Table of Contents

1. [Overview](#overview)
2. [Module 1: Account Processing](#module-1-account-processing)
3. [Module 2: Product Configuration](#module-2-product-configuration)
4. [Cross-Module Requirements](#cross-module-requirements)
5. [Data Model Overview](#data-model-overview)

---

## Overview

This document defines the functional requirements for a Current/Checking Account Processing System. The system consists of two core modules:

1. **Account Processing Module**: Handles account lifecycle, transaction processing, interest calculation, fees, and ledger management
2. **Product Configuration Module**: Enables configuration of account products with flexible parameters including interest rates, fees, overdrafts, and charges

### System Objectives

- Process current/checking account transactions in real-time
- Support flexible product configuration with formula-based calculations
- Maintain accurate ledger and balance tracking
- Handle multi-currency accounts
- Provide funds authorization and clearing capabilities
- Support internal transfers between accounts

---

## Module 1: Account Processing

### 1.1 Account Management

#### 1.1.1 Account Creation
**FR-AP-001**: The system SHALL allow creation of new current/checking accounts
**Inputs**:
- Customer ID (reference to customer)
- Product ID (reference to configured product)
- Account currency
- Opening balance (optional, defaults to 0)
- Account nickname (optional)

**Outputs**:
- Unique account identifier
- Account number (system-generated)
- Account status (Active, Inactive, Closed, Suspended)
- Opening date/timestamp

**Business Rules**:
- Each account MUST be linked to exactly one product configuration
- Account currency MUST match product configuration currency or be in the list of supported currencies
- Opening balance MUST be >= 0
- Account number MUST be unique across the system

#### 1.1.2 Account Inquiry
**FR-AP-002**: The system SHALL provide account balance and details inquiry
**Information Provided**:
- Account number and ID
- Customer information
- Product type
- Current balance (available balance)
- Ledger balance (actual balance including pending transactions)
- Reserved/held funds
- Overdraft limit
- Overdraft utilized
- Account status
- Currency
- Interest accrued to date
- Last transaction date
- Account opening date

#### 1.1.3 Account Status Management
**FR-AP-003**: The system SHALL support account status transitions
**Supported Statuses**:
- **Active**: Account can process all transactions
- **Inactive**: Account is open but cannot process debits (only credits allowed)
- **Suspended**: Account cannot process any transactions (inquiry only)
- **Closed**: Account is permanently closed (no transactions, inquiry only)

**Valid Transitions**:
- Active ↔ Inactive
- Active → Suspended
- Inactive → Suspended
- Suspended → Active
- Active/Inactive/Suspended → Closed
- Closed → (no transitions allowed)

**Business Rules**:
- Account can only be closed if balance = 0 and no pending transactions exist
- Status changes MUST be audited with timestamp and user

---

### 1.2 Interest Calculation

#### 1.2.1 Credit Interest Calculation
**FR-AP-004**: The system SHALL calculate credit interest on positive balances
**Calculation Method**:
- Daily balance method (interest calculated on end-of-day balance)
- Interest rate from product configuration
- Support for tiered interest rates (balance slabs)
- Support for formula-based interest calculation

**Inputs**:
- Daily end-of-day balance
- Interest rate/formula from product configuration
- Number of days in calculation period
- Day count convention (Actual/360, Actual/365, 30/360)

**Process**:
1. Calculate daily interest: (Balance × Rate × Days) / Day Count Base
2. Accumulate interest daily
3. Post interest to account on configured frequency (daily, monthly, quarterly, annually)

**Outputs**:
- Interest amount accrued
- Interest posting transaction
- Updated interest accrual balance

**Business Rules**:
- Interest SHALL NOT be calculated on negative balances (see Overdraft Interest)
- Interest calculation SHALL use the rate defined in the linked product configuration
- Interest posting frequency is defined at product level
- Partial period interest calculation must be supported

#### 1.2.2 Interest Accrual Tracking
**FR-AP-005**: The system SHALL maintain interest accrual records
**Information Tracked**:
- Accrual date
- Balance used for calculation
- Interest rate applied
- Interest amount accrued
- Cumulative interest accrued (current period)
- Last posting date

#### 1.2.3 Interest Posting
**FR-AP-006**: The system SHALL post accrued interest to account
**Posting Frequency Options**:
- Daily
- Monthly (on specified day)
- Quarterly
- Annually
- On account closure

**Process**:
1. Sum all accrued interest since last posting
2. Create credit transaction for interest amount
3. Update account balance
4. Reset interest accrual counter
5. Create ledger entries

**Business Rules**:
- Interest posting MUST create an auditable transaction
- Posted interest becomes part of the account balance
- Interest posting date is configurable at product level

---

### 1.3 Overdraft Management

#### 1.3.1 Overdraft Limit Assignment
**FR-AP-007**: The system SHALL support overdraft facilities on accounts
**Inputs**:
- Overdraft limit amount (from product configuration or account-specific override)
- Overdraft start date
- Overdraft expiry date (optional)

**Outputs**:
- Assigned overdraft limit
- Available overdraft amount
- Overdraft utilized amount

**Business Rules**:
- Overdraft limit can be set at product level (default) or account level (override)
- Account-level overdraft limit takes precedence over product-level
- Overdraft limit MUST be >= 0
- Expired overdrafts SHALL prevent further overdraft usage

#### 1.3.2 Overdraft Utilization
**FR-AP-008**: The system SHALL allow transactions that utilize overdraft
**Process**:
1. Check if account balance is sufficient
2. If insufficient, check available overdraft limit
3. If combined (balance + overdraft) is sufficient, allow transaction
4. Update overdraft utilized amount
5. Flag transaction as utilizing overdraft

**Outputs**:
- Transaction approval/rejection
- Updated overdraft utilized amount
- Overdraft utilization flag in transaction

**Business Rules**:
- Transaction amount MUST NOT exceed (balance + available overdraft)
- Overdraft can only be used if account status is Active
- Overdraft utilization MUST be tracked separately from balance

#### 1.3.3 Overdraft Interest Calculation
**FR-AP-009**: The system SHALL calculate interest on overdraft utilization
**Calculation Method**:
- Daily balance method on negative balance (overdraft amount)
- Overdraft interest rate from product configuration
- Support for formula-based overdraft interest calculation
- Typically higher rate than credit interest

**Inputs**:
- Daily overdraft utilized amount
- Overdraft interest rate/formula from product configuration
- Number of days overdrawn
- Day count convention

**Process**:
1. Calculate daily overdraft interest: (Overdraft Amount × Rate × Days) / Day Count Base
2. Accumulate overdraft interest daily
3. Post overdraft interest as debit on configured frequency

**Outputs**:
- Overdraft interest amount accrued
- Overdraft interest posting transaction (debit)
- Updated overdraft interest accrual balance

**Business Rules**:
- Overdraft interest is calculated only on negative balance portion
- Overdraft interest rate is typically higher than credit interest rate
- Overdraft interest posting increases the overdraft utilized amount

---

### 1.4 Fees and Charges

#### 1.4.1 Fee Application
**FR-AP-010**: The system SHALL apply fees and charges to accounts
**Fee Types**:
- **Transaction Fees**: Charged per transaction (e.g., withdrawal fee, transfer fee)
- **Periodic Fees**: Charged at regular intervals (e.g., monthly maintenance fee)
- **Event-Based Fees**: Charged on specific events (e.g., overdraft usage fee, statement fee)
- **Tiered Fees**: Fees based on balance or transaction amount slabs

**Inputs**:
- Fee configuration from product setup
- Transaction amount (for percentage-based fees)
- Account balance (for tiered fees)
- Transaction count (for volume-based fees)

**Process**:
1. Identify applicable fees based on trigger (transaction type, event, schedule)
2. Calculate fee amount using formula or fixed amount from product configuration
3. Create debit transaction for fee amount
4. Update account balance
5. Create ledger entries

**Outputs**:
- Fee transaction
- Updated account balance
- Fee tracking record

**Business Rules**:
- Fees MUST be configured at product level
- Fee formulas can reference account balance, transaction amount, and other variables
- Fees SHALL NOT cause account to exceed overdraft limit (optional: configurable behavior)
- All fees MUST be auditable with timestamps

#### 1.4.2 Fee Calculation Formulas
**FR-AP-011**: The system SHALL support formula-based fee calculation
**Supported Formula Elements**:
- Fixed amounts (e.g., $5.00)
- Percentages (e.g., 0.5% of transaction amount)
- Tiered/slab-based (e.g., $10 for balance < $1000, $5 for balance >= $1000)
- Conditional logic (e.g., fee waived if balance > $5000)
- Mathematical operations (+, -, ×, ÷)
- Minimum and maximum fee caps

**Examples**:
```
Fee = MAX(5.00, TransactionAmount * 0.01)  // $5 minimum or 1% of amount
Fee = IF(Balance < 1000, 15.00, 0.00)      // $15 if balance below $1000
Fee = TIER(Balance, [0:10, 1000:5, 5000:0]) // Tiered based on balance
```

#### 1.4.3 Fee Waiver and Reversal
**FR-AP-012**: The system SHALL support fee waiver and reversal
**Capabilities**:
- Waive fees based on account criteria (e.g., minimum balance maintained)
- Manually reverse posted fees (with authorization)
- Automatic fee waivers based on product rules

**Process**:
1. Identify fee reversal request or waiver condition
2. Validate authorization (for manual reversals)
3. Create credit transaction to reverse fee
4. Update account balance
5. Link reversal to original fee transaction

**Business Rules**:
- Fee reversals MUST reference the original fee transaction
- Fee waivers MUST be auditable
- Automatic waivers follow product configuration rules

---

### 1.5 Transaction Ledger

#### 1.5.1 Ledger Entry Creation
**FR-AP-013**: The system SHALL maintain a complete transaction ledger for each account
**Ledger Entry Information**:
- Transaction ID (unique)
- Account ID
- Transaction date/timestamp
- Value date (effective date for balance calculation)
- Transaction type (Debit/Credit)
- Transaction category (Deposit, Withdrawal, Transfer, Fee, Interest, etc.)
- Amount
- Currency
- Running balance (balance after transaction)
- Description/narrative
- Reference number (external reference)
- Channel (API, UI, Batch, etc.)
- Status (Pending, Posted, Reversed, Failed)

**Business Rules**:
- Every account operation MUST create ledger entries
- Ledger entries are immutable once posted (reversals create new entries)
- Ledger MUST maintain chronological order
- Running balance MUST be recalculated on each entry

#### 1.5.2 Ledger Inquiry
**FR-AP-014**: The system SHALL provide ledger inquiry capabilities
**Query Capabilities**:
- By date range
- By transaction type
- By transaction category
- By amount range
- By status
- By reference number
- Pagination support for large result sets

**Outputs**:
- List of ledger entries matching criteria
- Summary totals (debits, credits, net)
- Opening and closing balances for period

#### 1.5.3 Ledger Balance Reconciliation
**FR-AP-015**: The system SHALL support ledger balance reconciliation
**Capabilities**:
- Calculate ledger balance from opening balance + all transactions
- Compare calculated balance with stored balance
- Identify and report discrepancies
- Support for date-specific balance verification

**Process**:
1. Retrieve opening balance (or balance at start date)
2. Sum all credit transactions
3. Sum all debit transactions
4. Calculate: Opening Balance + Credits - Debits = Expected Balance
5. Compare with actual stored balance
6. Report any discrepancies

---

### 1.6 Funds Authorization

#### 1.6.1 Authorization Request
**FR-AP-016**: The system SHALL support funds authorization (hold) requests
**Purpose**: Reserve funds for future clearing without immediate debiting

**Inputs**:
- Account ID
- Authorization amount
- Authorization reference (merchant ID, transaction ID, etc.)
- Authorization expiry time/date
- Authorization type (Payment, Pre-authorization, etc.)

**Process**:
1. Validate account exists and is active
2. Check if sufficient funds available (balance + overdraft - existing holds)
3. If sufficient, create authorization record
4. Update available balance (reduce by authorization amount)
5. Do NOT update ledger balance (funds not yet moved)
6. Return authorization code

**Outputs**:
- Authorization code (unique identifier for this hold)
- Authorization status (Approved/Declined)
- Available balance after hold
- Expiry date/time

**Business Rules**:
- Authorizations MUST NOT exceed available balance + overdraft
- Authorizations have a maximum validity period (configurable)
- Expired authorizations are automatically released
- Multiple authorizations can exist on same account simultaneously
- Account balance shows: Ledger Balance - Total Authorizations = Available Balance

#### 1.6.2 Authorization Release
**FR-AP-017**: The system SHALL support authorization release (cancellation)
**Process**:
1. Locate authorization by authorization code
2. Validate authorization is in "Active" status
3. Mark authorization as "Released"
4. Restore authorized amount to available balance
5. Audit release with timestamp and reason

**Outputs**:
- Release confirmation
- Updated available balance

**Business Rules**:
- Only active authorizations can be released
- Released authorizations cannot be re-used or cleared
- Partial releases are supported (release portion of authorized amount)

#### 1.6.3 Authorization Inquiry
**FR-AP-018**: The system SHALL provide authorization inquiry
**Query Capabilities**:
- By authorization code
- By account ID (all active authorizations)
- By date range
- By status (Active, Cleared, Released, Expired)

**Outputs**:
- Authorization details (amount, date, reference, status)
- Total authorized amount for account
- Available balance after authorizations

---

### 1.7 Funds Clearing (Debit and Credit APIs)

#### 1.7.1 Debit Transaction Processing
**FR-AP-019**: The system SHALL process debit (withdrawal) transactions
**Debit Types**:
- **Direct Debit**: Immediate withdrawal without prior authorization
- **Authorization Clearing**: Debit against existing authorization

**Inputs**:
- Account ID
- Debit amount
- Transaction reference
- Description/narrative
- Authorization code (if clearing an authorization)
- Value date (optional, defaults to today)

**Process - Direct Debit**:
1. Validate account exists and is active
2. Check sufficient funds (balance + overdraft)
3. Apply any transaction fees
4. Create debit transaction in ledger
5. Update account balance
6. Update overdraft utilized (if applicable)
7. Return transaction confirmation

**Process - Authorization Clearing**:
1. Locate authorization by authorization code
2. Validate authorization is active and not expired
3. Validate clearing amount <= authorized amount
4. Mark authorization as "Cleared" (or partially cleared)
5. Create debit transaction in ledger (no additional balance check needed)
6. Update account balance
7. Update overdraft utilized (if applicable)
8. Release any unused authorization amount
9. Return transaction confirmation

**Outputs**:
- Transaction ID
- Transaction status (Posted, Failed)
- Updated account balance
- Updated available balance
- Transaction timestamp

**Business Rules**:
- Direct debits MUST NOT exceed available balance + overdraft
- Authorization clearing MUST match authorization code
- Clearing amount can be less than or equal to authorized amount
- Partial clearings reduce the authorization by the cleared amount
- Multiple partial clearings are allowed until full authorization is consumed
- Fees are applied after debit amount

#### 1.7.2 Credit Transaction Processing
**FR-AP-020**: The system SHALL process credit (deposit) transactions
**Credit Types**:
- **Direct Credit**: Immediate deposit to account
- **Reversal Credit**: Credit to reverse a previous debit

**Inputs**:
- Account ID
- Credit amount
- Transaction reference
- Description/narrative
- Value date (optional, defaults to today)
- Original transaction ID (if reversal)

**Process**:
1. Validate account exists
2. Account can be in any status except Closed for credits
3. Create credit transaction in ledger
4. Update account balance (increase)
5. Reduce overdraft utilized (if account was overdrawn)
6. Return transaction confirmation

**Outputs**:
- Transaction ID
- Transaction status (Posted)
- Updated account balance
- Updated available balance
- Transaction timestamp

**Business Rules**:
- Credits are always allowed (unless account is closed)
- Credits reduce overdraft utilized amount first, then increase positive balance
- Reversal credits MUST reference original transaction ID
- No fees on credit transactions (configurable at product level)

---

### 1.8 Internal Transfers

#### 1.8.1 Internal Transfer Processing
**FR-AP-021**: The system SHALL support internal transfers between accounts
**Purpose**: Move funds between two accounts within the system

**Inputs**:
- Source account ID
- Destination account ID
- Transfer amount
- Transfer reference
- Description/narrative
- Value date (optional)

**Process**:
1. Validate both accounts exist
2. Validate source account is active and has sufficient funds
3. Validate destination account is not closed
4. Create debit transaction on source account
5. Create credit transaction on destination account
6. Link both transactions with transfer reference
7. Update both account balances
8. Apply transfer fee if configured (debited from source account)
9. Create ledger entries for both accounts
10. Return transfer confirmation

**Outputs**:
- Transfer ID (unique identifier linking both transactions)
- Source transaction ID
- Destination transaction ID
- Transfer status (Completed, Failed)
- Updated balances for both accounts
- Transfer timestamp

**Business Rules**:
- Both accounts MUST be in the same currency (or currency conversion is applied)
- Source account debit follows same rules as regular debit (sufficient funds check)
- Internal transfers are atomic (both succeed or both fail)
- Transfer fees are configured at product level
- Transfers create two linked ledger entries

#### 1.8.2 Internal Transfer Reversal
**FR-AP-022**: The system SHALL support reversal of internal transfers
**Process**:
1. Locate original transfer by transfer ID
2. Validate transfer is in "Completed" status
3. Validate both accounts still exist
4. Create reverse debit on destination account
5. Create reverse credit on source account
6. Link reversal transactions to original transfer
7. Update both account balances
8. Reverse any transfer fees (optional, configurable)
9. Mark original transfer as "Reversed"

**Outputs**:
- Reversal confirmation
- Updated balances for both accounts
- Reversal timestamp

**Business Rules**:
- Reversals are time-limited (configurable, e.g., within 24 hours)
- Destination account MUST have sufficient funds for reversal debit
- Reversals create new transactions (original transactions remain in ledger)
- Reversal reason MUST be provided and audited

---

### 1.9 Balance Management

#### 1.9.1 Balance Types
**FR-AP-023**: The system SHALL maintain multiple balance types
**Balance Types**:
- **Ledger Balance**: Actual balance including all posted transactions
- **Available Balance**: Ledger balance minus authorizations and holds
- **Cleared Balance**: Balance including only cleared (value-dated) transactions
- **Overdraft Utilized**: Amount of overdraft currently in use
- **Overdraft Available**: Remaining overdraft limit available

**Calculations**:
```
Ledger Balance = Opening Balance + Sum(Credits) - Sum(Debits)
Available Balance = Ledger Balance - Sum(Active Authorizations) - Overdraft Utilized
Overdraft Utilized = MAX(0, ABS(MIN(0, Ledger Balance)))
Overdraft Available = Overdraft Limit - Overdraft Utilized
```

#### 1.9.2 Real-Time Balance Updates
**FR-AP-024**: The system SHALL update balances in real-time
**Requirements**:
- Balance updates MUST be atomic (transactional)
- Balance updates MUST be immediate (no batch delays)
- Concurrent transactions MUST be serialized to prevent race conditions
- Balance updates MUST be auditable

---

### 1.10 Account Reporting

#### 1.10.1 Account Statement
**FR-AP-025**: The system SHALL generate account statements
**Statement Information**:
- Account details (number, product, currency)
- Statement period (from - to date)
- Opening balance
- All transactions in period (date, description, debit, credit, balance)
- Closing balance
- Interest earned in period
- Fees charged in period
- Overdraft usage summary

**Statement Frequency Options**:
- Daily
- Weekly
- Monthly
- Quarterly
- On-demand

#### 1.10.2 Transaction History Export
**FR-AP-026**: The system SHALL support transaction history export
**Export Formats**:
- CSV
- PDF
- JSON
- Excel (XLSX)

**Export Filters**:
- Date range
- Transaction type
- Amount range
- Transaction category

---

## Module 2: Product Configuration

### 2.1 Product Management

#### 2.1.1 Product Creation
**FR-PC-001**: The system SHALL allow creation of account product configurations
**Inputs**:
- Product name (unique identifier)
- Product description
- Product code (system-generated or manual)
- Product status (Active, Inactive, Retired)
- Effective date (when product becomes available)
- End date (optional, when product is retired)

**Outputs**:
- Unique product ID
- Product configuration record

**Business Rules**:
- Product name MUST be unique
- Product code MUST be unique
- Only Active products can be assigned to new accounts
- Existing accounts on Inactive/Retired products continue to operate

#### 2.1.2 Product Inquiry
**FR-PC-002**: The system SHALL provide product inquiry capabilities
**Information Provided**:
- Product details (name, code, description)
- Product status
- Effective and end dates
- Number of accounts using this product
- All configuration parameters (interest, fees, overdraft, etc.)

#### 2.1.3 Product Status Management
**FR-PC-003**: The system SHALL support product status changes
**Supported Statuses**:
- **Active**: Product available for new accounts
- **Inactive**: Product not available for new accounts (existing accounts unaffected)
- **Retired**: Product permanently retired (existing accounts may need migration)

**Business Rules**:
- Status changes MUST be audited
- Retiring a product with active accounts MUST trigger a warning
- Status changes do not affect existing accounts immediately

---

### 2.2 Product Interest Configuration

#### 2.2.1 Credit Interest Setup
**FR-PC-004**: The system SHALL support credit interest configuration
**Configuration Parameters**:
- **Interest Calculation Method**:
  - Simple interest
  - Compound interest
  - Tiered interest (different rates for balance slabs)
- **Interest Rate**: Percentage value (e.g., 2.5% = 0.025)
- **Interest Formula**: Optional formula for complex calculations
- **Day Count Convention**:
  - Actual/360
  - Actual/365
  - 30/360
- **Interest Posting Frequency**:
  - Daily
  - Monthly (specify day of month)
  - Quarterly (specify month and day)
  - Annually (specify month and day)
  - On account closure
- **Minimum Balance for Interest**: Balance threshold to earn interest
- **Interest Rounding Rules**: Round up, down, or nearest (decimals)

**Interest Rate Tiers** (Optional):
- Define balance slabs with different rates
- Example:
  - 0 - 1,000: 1.0%
  - 1,001 - 5,000: 1.5%
  - 5,001+: 2.0%

**Business Rules**:
- If formula is provided, it takes precedence over fixed rate
- Tiered rates require both lower and upper balance bounds (except last tier)
- Interest rate changes require product versioning
- Negative interest rates are supported (penalty rates)

#### 2.2.2 Interest Rate Formula Support
**FR-PC-005**: The system SHALL support formula-based interest calculation
**Formula Capabilities**:
- Reference account balance
- Reference external rate indices (e.g., Base Rate + Spread)
- Mathematical operations (+, -, ×, ÷)
- Conditional logic (IF statements)
- Date-based formulas (seasonal rates)
- Tiered calculations

**Formula Examples**:
```
Rate = 0.025                                    // Fixed 2.5%
Rate = BaseRate + 0.01                          // Base rate + 1% spread
Rate = IF(Balance > 5000, 0.03, 0.02)          // 3% if balance > 5000, else 2%
Rate = TIER(Balance, [0:0.01, 1000:0.015, 5000:0.02])  // Tiered rates
Rate = BaseRate * 1.2                          // 120% of base rate
```

**Formula Variables**:
- `Balance`: Current account balance
- `AverageBalance`: Average balance over period
- `BaseRate`: External reference rate
- `DaysInPeriod`: Number of days in calculation period
- `MinimumBalance`: Minimum balance over period

**Business Rules**:
- Formulas MUST be validated before saving
- Invalid formulas MUST be rejected with error message
- Formula evaluation errors MUST be logged and reported
- Default to fixed rate if formula evaluation fails

#### 2.2.3 Overdraft Interest Setup
**FR-PC-006**: The system SHALL support overdraft interest configuration
**Configuration Parameters**:
- **Overdraft Interest Rate**: Percentage (typically higher than credit interest)
- **Overdraft Interest Formula**: Optional formula
- **Day Count Convention**: Same options as credit interest
- **Overdraft Interest Posting Frequency**: Same options as credit interest
- **Overdraft Interest Calculation Method**: Simple or compound
- **Grace Period**: Days before overdraft interest starts accruing (optional)

**Business Rules**:
- Overdraft interest rate is typically higher than credit interest rate
- Formula support same as credit interest formulas
- Grace period allows customers to clear overdraft without penalty

---

### 2.3 Product Overdraft Configuration

#### 2.3.1 Overdraft Limit Setup
**FR-PC-007**: The system SHALL support overdraft limit configuration
**Configuration Parameters**:
- **Default Overdraft Limit**: Standard overdraft amount for accounts using this product
- **Overdraft Allowed**: Boolean (true/false) to enable/disable overdraft
- **Overdraft Approval Required**: Whether overdraft usage requires pre-approval
- **Maximum Overdraft Limit**: Upper bound for account-specific overrides
- **Overdraft Buffer**: Small buffer amount before overdraft fees trigger (optional)

**Business Rules**:
- Overdraft limit can be 0 (no overdraft allowed)
- Account-level overdraft limits can override product-level (up to maximum)
- Disabling overdraft on product prevents new overdraft assignments

#### 2.3.2 Overdraft Fees Configuration
**FR-PC-008**: The system SHALL support overdraft-specific fee configuration
**Fee Types**:
- **Overdraft Usage Fee**: One-time fee when overdraft is first used
- **Overdraft Daily Fee**: Daily fee while account is overdrawn
- **Overdraft Excess Fee**: Fee when overdraft limit is exceeded (if allowed)

**Configuration Parameters**:
- Fee amount (fixed or formula-based)
- Fee frequency (one-time, daily, monthly)
- Fee waiver conditions

**Business Rules**:
- Overdraft fees are separate from regular transaction fees
- Fees can be waived based on customer relationship or balance history

---

### 2.4 Product Fees and Charges Configuration

#### 2.4.1 Fee Type Setup
**FR-PC-009**: The system SHALL support configuration of multiple fee types
**Fee Categories**:
- **Maintenance Fees**:
  - Monthly maintenance fee
  - Annual fee
  - Minimum balance fee (charged if balance falls below threshold)
- **Transaction Fees**:
  - Withdrawal fee
  - Deposit fee (rare, but supported)
  - Transfer fee (internal and external)
  - Check processing fee
- **Event-Based Fees**:
  - Overdraft usage fee
  - Statement fee (paper statements)
  - Account closure fee
  - Dormancy fee (inactive account)
- **Service Fees**:
  - ATM withdrawal fee
  - Foreign transaction fee
  - Stop payment fee

**Configuration Parameters for Each Fee**:
- Fee name and description
- Fee category
- Fee trigger (transaction type, event, schedule)
- Fee calculation method (fixed, percentage, formula, tiered)
- Fee amount or formula
- Minimum fee amount (if percentage-based)
- Maximum fee amount (cap)
- Fee waiver conditions

**Business Rules**:
- Multiple fees can be configured per product
- Fees can be enabled/disabled independently
- Fee changes create new product version

#### 2.4.2 Fee Formula Configuration
**FR-PC-010**: The system SHALL support formula-based fee calculation
**Formula Capabilities**:
- Fixed amounts
- Percentage of transaction amount
- Percentage of account balance
- Tiered/slab-based fees
- Conditional fees (IF-THEN logic)
- Combined formulas (fixed + percentage)
- Date-based fees (different fees for different periods)

**Formula Examples**:
```
Fee = 5.00                                              // Fixed $5 fee
Fee = TransactionAmount * 0.01                          // 1% of transaction
Fee = MAX(5.00, TransactionAmount * 0.01)               // $5 or 1%, whichever is higher
Fee = IF(Balance < 1000, 15.00, 0.00)                   // $15 if balance < $1000
Fee = TIER(TransactionAmount, [0:1.00, 100:2.50, 500:5.00])  // Tiered by amount
Fee = 10.00 + (TransactionAmount * 0.005)               // $10 + 0.5% of amount
Fee = IF(TransactionCount > 10, 2.00, 0.00)             // $2 per transaction after 10
```

**Formula Variables**:
- `TransactionAmount`: Amount of current transaction
- `Balance`: Current account balance
- `AverageBalance`: Average balance over period
- `TransactionCount`: Number of transactions in period
- `MinimumBalance`: Minimum balance maintained in period
- `DaysInPeriod`: Days in the fee calculation period

**Business Rules**:
- Formulas MUST be validated before saving
- Formula evaluation errors default to fixed fee or waive fee (configurable)
- Complex formulas MUST be documented with examples
- Formula changes are versioned with the product

#### 2.4.3 Fee Waiver Conditions
**FR-PC-011**: The system SHALL support automatic fee waiver conditions
**Waiver Conditions**:
- Minimum balance threshold (waive if balance > X)
- Average balance threshold (waive if avg balance > X)
- Transaction volume threshold (waive if transactions < X)
- Account age (waive for accounts newer than X days)
- Customer relationship (waive for premium customers)
- Promotional periods (waive during specified dates)

**Configuration**:
- Each fee can have multiple waiver conditions
- Waiver conditions can be combined with AND/OR logic
- Waiver conditions are evaluated before fee is applied

**Business Rules**:
- If any waiver condition is met (OR logic), fee is waived
- If all waiver conditions must be met (AND logic), configure accordingly
- Fee waivers are auditable

#### 2.4.4 Fee Tier Configuration
**FR-PC-012**: The system SHALL support tiered fee structures
**Tier Definition**:
- Lower bound (inclusive)
- Upper bound (exclusive, except last tier)
- Fee amount or formula for this tier

**Example Tier Structure**:
```
Transaction Amount Tiers:
- $0 - $100: $1.00
- $100.01 - $500: $2.50
- $500.01+: $5.00

Balance Tiers:
- $0 - $1,000: $15/month
- $1,000 - $5,000: $10/month
- $5,000+: $0/month (waived)
```

**Business Rules**:
- Tiers MUST be contiguous (no gaps)
- Last tier has no upper bound (represents "and above")
- Tiers can be based on transaction amount, balance, or transaction count
- Each tier can have a fixed amount or formula

---

### 2.5 Product Currency Configuration

#### 2.5.1 Currency Setup
**FR-PC-013**: The system SHALL support currency configuration for products
**Configuration Parameters**:
- **Primary Currency**: Default currency for accounts using this product
- **Supported Currencies**: List of additional currencies allowed (multi-currency products)
- **Currency Conversion Rules**: For multi-currency operations
- **Currency Decimal Places**: Number of decimal places (e.g., 2 for USD, 3 for KWD)

**Business Rules**:
- Every product MUST have exactly one primary currency
- Multi-currency support is optional
- Accounts inherit currency from product (or choose from supported list)
- Currency cannot be changed once account is created

#### 2.5.2 Multi-Currency Support
**FR-PC-014**: The system SHALL support multi-currency product configuration
**Capabilities**:
- Define list of supported currencies for a product
- Configure currency-specific parameters (interest rates, fees per currency)
- Define currency conversion rates (if internal transfers between currencies)
- Specify base currency for reporting

**Business Rules**:
- Currency-specific rates override default product rates
- Currency conversion for internal transfers uses configured rates
- Exchange rate changes are versioned and auditable

---

### 2.6 Product Versioning and Audit

#### 2.6.1 Product Version Management
**FR-PC-015**: The system SHALL maintain version history of product configurations
**Versioning Triggers**:
- Interest rate changes
- Fee changes
- Overdraft parameter changes
- Any configuration parameter change

**Version Information**:
- Version number (auto-incremented)
- Effective date (when this version becomes active)
- Changed by (user who made the change)
- Change timestamp
- Change description/reason
- Previous values and new values (diff)

**Business Rules**:
- All changes create new version (immutable history)
- Existing accounts can remain on old version or migrate to new version
- Version effective date determines when new accounts use the new configuration
- Historical versions are retained for audit and compliance

#### 2.6.2 Product Change Impact Analysis
**FR-PC-016**: The system SHALL provide impact analysis for product changes
**Analysis Information**:
- Number of accounts affected
- Total balances affected
- Projected interest impact (if rate change)
- Projected fee impact (if fee change)
- List of affected accounts

**Business Rules**:
- Impact analysis MUST be shown before saving changes
- High-impact changes MAY require additional approval
- Changes affecting large account populations should be scheduled

---

### 2.7 Product Templates and Cloning

#### 2.7.1 Product Template Creation
**FR-PC-017**: The system SHALL support product templates
**Capabilities**:
- Save product configuration as template
- Create new product from template
- Template library with common product types (Basic Checking, Premium Checking, etc.)

**Business Rules**:
- Templates are read-only after creation
- Templates can be cloned and modified
- Templates do not create actual products until instantiated

#### 2.7.2 Product Cloning
**FR-PC-018**: The system SHALL support product cloning
**Process**:
1. Select existing product to clone
2. System copies all configuration parameters
3. User modifies product name and code (must be unique)
4. User modifies any parameters as needed
5. Save as new product

**Business Rules**:
- Cloned products are independent (changes to original don't affect clone)
- Cloning preserves all formulas and configurations
- Product name and code MUST be changed (cannot duplicate)

---

### 2.8 Product Reporting and Analytics

#### 2.8.1 Product Performance Reporting
**FR-PC-019**: The system SHALL provide product performance reports
**Report Metrics**:
- Number of accounts per product
- Total balances per product
- Interest paid out per product
- Fees collected per product
- Overdraft utilization per product
- Account growth/attrition per product

**Report Filters**:
- Date range
- Product status
- Currency

#### 2.8.2 Product Comparison
**FR-PC-020**: The system SHALL support product comparison
**Comparison Capabilities**:
- Side-by-side comparison of configuration parameters
- Highlight differences between products
- Compare rate structures
- Compare fee structures
- Performance metrics comparison

---

## Cross-Module Requirements

### 3.1 Integration Requirements

#### 3.1.1 Product-Account Linkage
**FR-INT-001**: Account processing MUST reference product configuration
**Requirements**:
- Every account MUST be linked to exactly one product
- Account inherits all configuration from product at creation time
- Product changes (new versions) MAY apply to existing accounts (configurable)
- Account can override certain product parameters (e.g., overdraft limit)

#### 3.1.2 Configuration Inheritance
**FR-INT-002**: Accounts SHALL inherit configuration from products
**Inherited Parameters**:
- Interest rates and formulas
- Fee structures and formulas
- Overdraft limits and rates
- Currency settings
- Posting frequencies

**Override Capability**:
- Account-level overdraft limit can override product default
- Account-level fee waivers can override product fees
- All overrides MUST be audited

---

### 3.2 Audit and Compliance

#### 3.2.1 Audit Trail
**FR-AUD-001**: The system SHALL maintain comprehensive audit trails
**Audited Events**:
- All account transactions
- Balance changes
- Status changes
- Product configuration changes
- Fee applications and waivers
- Interest calculations and postings
- Authorization and clearing operations
- User actions and timestamps

**Audit Information**:
- Event timestamp (with millisecond precision)
- User ID (who performed the action)
- Event type and description
- Before and after values (for changes)
- IP address or channel
- Success/failure status

**Business Rules**:
- Audit records are immutable
- Audit retention period is configurable (minimum 7 years for compliance)
- Audit logs MUST be tamper-proof

#### 3.2.2 Regulatory Compliance
**FR-AUD-002**: The system SHALL support regulatory compliance requirements
**Compliance Features**:
- Transaction reporting (SAR, CTR)
- Interest calculation transparency
- Fee disclosure
- Balance verification
- Customer statement generation
- Data retention policies

---

### 3.3 Security and Access Control

#### 3.3.1 Role-Based Access Control
**FR-SEC-001**: The system SHALL implement role-based access control
**Roles**:
- **Account Officer**: Create accounts, process transactions
- **Product Manager**: Configure products, manage fees and rates
- **Supervisor**: Approve high-value transactions, fee reversals
- **Auditor**: Read-only access to all records
- **System Administrator**: Full access, user management

**Permissions**:
- Account creation, modification, closure
- Transaction processing (debit, credit, transfer)
- Fee reversal and waiver
- Product configuration changes
- Report generation
- Audit log access

#### 3.3.2 Transaction Authorization Limits
**FR-SEC-002**: The system SHALL support transaction authorization limits
**Limit Types**:
- Per-transaction limit (single transaction amount)
- Daily limit (cumulative transactions per day)
- User role limit (based on user role)

**Business Rules**:
- Transactions exceeding limits require supervisor approval
- Limits are configurable per role and transaction type
- Limit breaches are logged and reported

---

### 3.4 Performance and Scalability

#### 3.4.1 Real-Time Processing
**FR-PERF-001**: The system SHALL process transactions in real-time
**Performance Targets**:
- Transaction processing: < 500ms response time
- Balance inquiry: < 200ms response time
- Authorization: < 300ms response time
- Ledger query: < 1 second for 1000 records

#### 3.4.2 Concurrent Transaction Handling
**FR-PERF-002**: The system SHALL handle concurrent transactions safely
**Requirements**:
- Optimistic or pessimistic locking for balance updates
- Transaction isolation (ACID compliance)
- Deadlock detection and resolution
- Queue management for high-volume periods

---

## Data Model Overview

### 4.1 Core Entities

**Account**:
- Account ID (PK)
- Account Number
- Customer ID (FK)
- Product ID (FK)
- Currency
- Status
- Opening Date
- Closing Date
- Ledger Balance
- Available Balance
- Overdraft Limit
- Overdraft Utilized

**Product**:
- Product ID (PK)
- Product Name
- Product Code
- Description
- Status
- Effective Date
- End Date
- Currency
- Interest Configuration (JSON/nested)
- Fee Configuration (JSON/nested)
- Overdraft Configuration (JSON/nested)

**Transaction**:
- Transaction ID (PK)
- Account ID (FK)
- Transaction Date
- Value Date
- Type (Debit/Credit)
- Category
- Amount
- Currency
- Running Balance
- Description
- Reference
- Status
- Channel

**Authorization**:
- Authorization ID (PK)
- Account ID (FK)
- Authorization Code
- Amount
- Status
- Created Date
- Expiry Date
- Cleared Amount
- Cleared Date

**Fee Configuration**:
- Fee ID (PK)
- Product ID (FK)
- Fee Name
- Fee Type
- Trigger
- Calculation Method
- Formula
- Amount
- Waiver Conditions

**Interest Configuration**:
- Interest Config ID (PK)
- Product ID (FK)
- Interest Type (Credit/Overdraft)
- Rate
- Formula
- Day Count Convention
- Posting Frequency
- Minimum Balance

---

## Appendix

### A.1 Formula Expression Language

**Supported Operators**:
- Arithmetic: `+`, `-`, `*`, `/`, `%` (modulo), `^` (power)
- Comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical: `AND`, `OR`, `NOT`
- Functions: `IF()`, `MAX()`, `MIN()`, `ABS()`, `ROUND()`, `TIER()`

**Supported Functions**:
```
IF(condition, value_if_true, value_if_false)
MAX(value1, value2, ...)
MIN(value1, value2, ...)
ABS(value)
ROUND(value, decimals)
TIER(value, [lower_bound:amount, ...])
```

**Example Formulas**:
```
// Interest rate based on balance
Rate = IF(Balance > 10000, 0.03, IF(Balance > 5000, 0.02, 0.01))

// Fee with minimum and maximum
Fee = MAX(5, MIN(50, TransactionAmount * 0.02))

// Tiered fee structure
Fee = TIER(TransactionAmount, [0:0, 100:2.5, 500:5, 1000:10])

// Combined fixed and percentage fee
Fee = 3.50 + (TransactionAmount * 0.015)

// Conditional fee waiver
Fee = IF(AverageBalance > 5000, 0, 15)

// Overdraft interest with grace period
Rate = IF(DaysOverdrawn <= 3, 0, 0.15)
```

### A.2 Currency Codes

**Supported Currencies** (ISO 4217):
- USD (US Dollar) - 2 decimals
- EUR (Euro) - 2 decimals
- GBP (British Pound) - 2 decimals
- JPY (Japanese Yen) - 0 decimals
- CHF (Swiss Franc) - 2 decimals
- CAD (Canadian Dollar) - 2 decimals
- AUD (Australian Dollar) - 2 decimals
- KWD (Kuwaiti Dinar) - 3 decimals
- BHD (Bahraini Dinar) - 3 decimals

### A.3 Day Count Conventions

**Actual/360**:
```
Interest = (Principal × Rate × Actual Days) / 360
```

**Actual/365**:
```
Interest = (Principal × Rate × Actual Days) / 365
```

**30/360**:
```
Interest = (Principal × Rate × Days Calculated as 30-day months) / 360
```

---

**Document Control**:
- **Version**: 1.0
- **Status**: Draft
- **Author**: System Architect
- **Approval**: Pending
- **Next Review**: TBD

---

**Change History**:

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-04 | System Architect | Initial draft |
