// Account domain model

use chrono::{DateTime, NaiveDate, Utc};
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum AccountStatus {
    Active,
    Closed,
}

impl AccountStatus {
    pub fn as_str(&self) -> &str {
        match self {
            AccountStatus::Active => "Active",
            AccountStatus::Closed => "Closed",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Active" => Ok(AccountStatus::Active),
            "Closed" => Ok(AccountStatus::Closed),
            _ => Err(format!("Invalid account status: {}", s)),
        }
    }
}

impl std::fmt::Display for AccountStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Account {
    pub account_id: String,
    pub account_number: String,
    pub customer_id: String,
    pub product_id: String,
    pub currency: String,
    pub status: AccountStatus,

    // Balance fields
    pub balance: Decimal,
    pub interest_accrued: Decimal,

    // Dates
    pub opening_date: NaiveDate,
    pub closing_date: Option<NaiveDate>,

    // Audit fields
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub created_by: Option<String>,
}

impl Account {
    /// Create a new account
    pub fn new(
        account_number: String,
        customer_id: String,
        product_id: String,
        currency: String,
        opening_balance: Decimal,
        created_by: Option<String>,
    ) -> Result<Self, String> {
        // Validation
        if account_number.trim().is_empty() {
            return Err("Account number cannot be empty".to_string());
        }
        if customer_id.trim().is_empty() {
            return Err("Customer ID cannot be empty".to_string());
        }
        if product_id.trim().is_empty() {
            return Err("Product ID cannot be empty".to_string());
        }
        if currency.len() != 3 {
            return Err("Currency code must be exactly 3 characters".to_string());
        }
        if opening_balance < Decimal::ZERO {
            return Err("Opening balance cannot be negative".to_string());
        }

        let now = Utc::now();
        let account_id = format!("ACC-{}", uuid::Uuid::new_v4());

        Ok(Account {
            account_id,
            account_number,
            customer_id,
            product_id,
            currency,
            status: AccountStatus::Active,
            balance: opening_balance,
            interest_accrued: Decimal::ZERO,
            opening_date: now.date_naive(),
            closing_date: None,
            created_at: now,
            updated_at: now,
            created_by,
        })
    }

    /// Check if account is active
    pub fn is_active(&self) -> bool {
        self.status == AccountStatus::Active
    }

    /// Check if account is closed
    pub fn is_closed(&self) -> bool {
        self.status == AccountStatus::Closed
    }

    /// Close account (only if balance is zero)
    pub fn close(&mut self) -> Result<(), String> {
        if self.balance != Decimal::ZERO {
            return Err(format!(
                "Cannot close account with non-zero balance: {}",
                self.balance
            ));
        }

        if self.is_closed() {
            return Err("Account is already closed".to_string());
        }

        self.status = AccountStatus::Closed;
        self.closing_date = Some(Utc::now().date_naive());
        self.updated_at = Utc::now();

        Ok(())
    }

    /// Credit account (increase balance)
    pub fn credit(&mut self, amount: Decimal) -> Result<(), String> {
        if amount <= Decimal::ZERO {
            return Err("Credit amount must be positive".to_string());
        }

        self.balance += amount;
        self.updated_at = Utc::now();

        Ok(())
    }

    /// Debit account (decrease balance)
    pub fn debit(&mut self, amount: Decimal) -> Result<(), String> {
        if amount <= Decimal::ZERO {
            return Err("Debit amount must be positive".to_string());
        }

        if !self.is_active() {
            return Err("Cannot debit from non-active account".to_string());
        }

        if self.balance < amount {
            return Err(format!(
                "Insufficient balance: available {}, required {}",
                self.balance, amount
            ));
        }

        self.balance -= amount;
        self.updated_at = Utc::now();

        Ok(())
    }

    /// Accrue interest
    pub fn accrue_interest(&mut self, amount: Decimal) -> Result<(), String> {
        if amount < Decimal::ZERO {
            return Err("Interest amount cannot be negative".to_string());
        }

        self.interest_accrued += amount;
        self.updated_at = Utc::now();

        Ok(())
    }

    /// Post accrued interest to balance and reset accrual
    pub fn post_interest(&mut self) -> Result<Decimal, String> {
        let interest_amount = self.interest_accrued;

        if interest_amount > Decimal::ZERO {
            self.balance += interest_amount;
            self.interest_accrued = Decimal::ZERO;
            self.updated_at = Utc::now();
        }

        Ok(interest_amount)
    }

    /// Check if account has sufficient balance
    pub fn has_sufficient_balance(&self, amount: Decimal) -> bool {
        self.balance >= amount
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_create_valid_account() {
        let account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(1000.00),
            Some("USR-001".to_string()),
        );

        assert!(account.is_ok());
        let acc = account.unwrap();
        assert_eq!(acc.balance, dec!(1000.00));
        assert!(acc.is_active());
        assert!(!acc.is_closed());
    }

    #[test]
    fn test_credit_account() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(1000.00),
            None,
        ).unwrap();

        assert!(account.credit(dec!(500.00)).is_ok());
        assert_eq!(account.balance, dec!(1500.00));
    }

    #[test]
    fn test_debit_account() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(1000.00),
            None,
        ).unwrap();

        assert!(account.debit(dec!(300.00)).is_ok());
        assert_eq!(account.balance, dec!(700.00));
    }

    #[test]
    fn test_insufficient_balance() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(100.00),
            None,
        ).unwrap();

        let result = account.debit(dec!(200.00));
        assert!(result.is_err());
        assert_eq!(account.balance, dec!(100.00));  // Balance unchanged
    }

    #[test]
    fn test_close_account_with_balance() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(100.00),
            None,
        ).unwrap();

        let result = account.close();
        assert!(result.is_err());
        assert!(account.is_active());
    }

    #[test]
    fn test_close_account_with_zero_balance() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(0.00),
            None,
        ).unwrap();

        assert!(account.close().is_ok());
        assert!(account.is_closed());
        assert!(account.closing_date.is_some());
    }

    #[test]
    fn test_interest_accrual_and_posting() {
        let mut account = Account::new(
            "1234567890".to_string(),
            "CUST-001".to_string(),
            "PROD-001".to_string(),
            "USD".to_string(),
            dec!(1000.00),
            None,
        ).unwrap();

        // Accrue interest over time
        account.accrue_interest(dec!(0.68)).unwrap();
        account.accrue_interest(dec!(0.68)).unwrap();
        account.accrue_interest(dec!(0.68)).unwrap();

        assert_eq!(account.interest_accrued, dec!(2.04));
        assert_eq!(account.balance, dec!(1000.00));

        // Post interest
        let posted = account.post_interest().unwrap();
        assert_eq!(posted, dec!(2.04));
        assert_eq!(account.balance, dec!(1002.04));
        assert_eq!(account.interest_accrued, dec!(0.00));
    }
}
