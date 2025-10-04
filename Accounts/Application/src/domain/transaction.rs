// Transaction domain model

use chrono::{DateTime, NaiveDate, Utc};
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum TransactionType {
    Debit,
    Credit,
}

impl TransactionType {
    pub fn as_str(&self) -> &str {
        match self {
            TransactionType::Debit => "Debit",
            TransactionType::Credit => "Credit",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Debit" => Ok(TransactionType::Debit),
            "Credit" => Ok(TransactionType::Credit),
            _ => Err(format!("Invalid transaction type: {}", s)),
        }
    }
}

impl std::fmt::Display for TransactionType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum TransactionCategory {
    Deposit,
    Withdrawal,
    Fee,
    Interest,
    Opening,
}

impl TransactionCategory {
    pub fn as_str(&self) -> &str {
        match self {
            TransactionCategory::Deposit => "Deposit",
            TransactionCategory::Withdrawal => "Withdrawal",
            TransactionCategory::Fee => "Fee",
            TransactionCategory::Interest => "Interest",
            TransactionCategory::Opening => "Opening",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Deposit" => Ok(TransactionCategory::Deposit),
            "Withdrawal" => Ok(TransactionCategory::Withdrawal),
            "Fee" => Ok(TransactionCategory::Fee),
            "Interest" => Ok(TransactionCategory::Interest),
            "Opening" => Ok(TransactionCategory::Opening),
            _ => Err(format!("Invalid transaction category: {}", s)),
        }
    }
}

impl std::fmt::Display for TransactionCategory {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transaction {
    pub transaction_id: String,
    pub account_id: String,

    // Transaction details
    pub transaction_date: DateTime<Utc>,
    pub value_date: NaiveDate,
    pub transaction_type: TransactionType,
    pub category: TransactionCategory,

    // Amounts
    pub amount: Decimal,
    pub currency: String,
    pub running_balance: Decimal,

    // Description and reference
    pub description: String,
    pub reference: Option<String>,

    // Channel and status
    pub channel: String,  // "API", "UI", "Batch"
    pub status: String,   // "Posted" (MVP only has Posted)

    // Audit fields
    pub created_at: DateTime<Utc>,
    pub created_by: Option<String>,
}

impl Transaction {
    /// Create a new transaction
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        account_id: String,
        transaction_type: TransactionType,
        category: TransactionCategory,
        amount: Decimal,
        currency: String,
        running_balance: Decimal,
        description: String,
        reference: Option<String>,
        channel: String,
        created_by: Option<String>,
    ) -> Result<Self, String> {
        // Validation
        if account_id.trim().is_empty() {
            return Err("Account ID cannot be empty".to_string());
        }
        if amount <= Decimal::ZERO {
            return Err("Transaction amount must be positive".to_string());
        }
        if currency.len() != 3 {
            return Err("Currency code must be exactly 3 characters".to_string());
        }
        if running_balance < Decimal::ZERO {
            return Err("Running balance cannot be negative (no overdraft in MVP)".to_string());
        }
        if description.trim().is_empty() {
            return Err("Description cannot be empty".to_string());
        }

        let now = Utc::now();
        let transaction_id = format!("TXN-{}", uuid::Uuid::new_v4());

        Ok(Transaction {
            transaction_id,
            account_id,
            transaction_date: now,
            value_date: now.date_naive(),
            transaction_type,
            category,
            amount,
            currency,
            running_balance,
            description,
            reference,
            channel,
            status: "Posted".to_string(),
            created_at: now,
            created_by,
        })
    }

    /// Check if transaction is a debit
    pub fn is_debit(&self) -> bool {
        self.transaction_type == TransactionType::Debit
    }

    /// Check if transaction is a credit
    pub fn is_credit(&self) -> bool {
        self.transaction_type == TransactionType::Credit
    }

    /// Check if transaction is a fee
    pub fn is_fee(&self) -> bool {
        self.category == TransactionCategory::Fee
    }

    /// Check if transaction is interest
    pub fn is_interest(&self) -> bool {
        self.category == TransactionCategory::Interest
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_create_debit_transaction() {
        let txn = Transaction::new(
            "ACC-001".to_string(),
            TransactionType::Debit,
            TransactionCategory::Withdrawal,
            dec!(100.00),
            "USD".to_string(),
            dec!(900.00),
            "ATM Withdrawal".to_string(),
            Some("ATM-REF-123".to_string()),
            "API".to_string(),
            Some("USR-001".to_string()),
        );

        assert!(txn.is_ok());
        let t = txn.unwrap();
        assert!(t.is_debit());
        assert!(!t.is_credit());
        assert_eq!(t.amount, dec!(100.00));
        assert_eq!(t.running_balance, dec!(900.00));
    }

    #[test]
    fn test_create_credit_transaction() {
        let txn = Transaction::new(
            "ACC-001".to_string(),
            TransactionType::Credit,
            TransactionCategory::Deposit,
            dec!(500.00),
            "USD".to_string(),
            dec!(1500.00),
            "Salary Deposit".to_string(),
            Some("PAYROLL-001".to_string()),
            "API".to_string(),
            None,
        );

        assert!(txn.is_ok());
        let t = txn.unwrap();
        assert!(t.is_credit());
        assert!(!t.is_debit());
        assert_eq!(t.amount, dec!(500.00));
    }

    #[test]
    fn test_invalid_amount() {
        let txn = Transaction::new(
            "ACC-001".to_string(),
            TransactionType::Debit,
            TransactionCategory::Withdrawal,
            dec!(0.00),  // Invalid: must be positive
            "USD".to_string(),
            dec!(900.00),
            "Test".to_string(),
            None,
            "API".to_string(),
            None,
        );

        assert!(txn.is_err());
    }

    #[test]
    fn test_fee_transaction() {
        let txn = Transaction::new(
            "ACC-001".to_string(),
            TransactionType::Debit,
            TransactionCategory::Fee,
            dec!(2.00),
            "USD".to_string(),
            dec!(898.00),
            "Transaction fee".to_string(),
            Some("TXN-REF-123".to_string()),
            "API".to_string(),
            Some("USR-001".to_string()),
        ).unwrap();

        assert!(txn.is_fee());
        assert!(txn.is_debit());
    }

    #[test]
    fn test_interest_transaction() {
        let txn = Transaction::new(
            "ACC-001".to_string(),
            TransactionType::Credit,
            TransactionCategory::Interest,
            dec!(2.50),
            "USD".to_string(),
            dec!(1002.50),
            "Interest for September 2025".to_string(),
            None,
            "Batch".to_string(),
            None,
        ).unwrap();

        assert!(txn.is_interest());
        assert!(txn.is_credit());
    }
}
