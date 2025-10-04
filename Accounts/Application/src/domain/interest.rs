// Interest accrual domain model

use chrono::{DateTime, NaiveDate, Utc};
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InterestAccrual {
    pub accrual_id: String,
    pub account_id: String,

    // Accrual details
    pub accrual_date: NaiveDate,
    pub balance: Decimal,
    pub annual_rate: Decimal,

    // Calculated interest
    pub daily_interest: Decimal,
    pub cumulative_accrued: Decimal,

    // Audit fields
    pub created_at: DateTime<Utc>,
}

impl InterestAccrual {
    /// Create a new interest accrual record
    pub fn new(
        account_id: String,
        accrual_date: NaiveDate,
        balance: Decimal,
        annual_rate: Decimal,
        daily_interest: Decimal,
        cumulative_accrued: Decimal,
    ) -> Result<Self, String> {
        // Validation
        if account_id.trim().is_empty() {
            return Err("Account ID cannot be empty".to_string());
        }
        if balance < Decimal::ZERO {
            return Err("Balance cannot be negative".to_string());
        }
        if annual_rate < Decimal::ZERO || annual_rate > Decimal::ONE {
            return Err("Annual rate must be between 0 and 1".to_string());
        }
        if daily_interest < Decimal::ZERO {
            return Err("Daily interest cannot be negative".to_string());
        }
        if cumulative_accrued < Decimal::ZERO {
            return Err("Cumulative accrued cannot be negative".to_string());
        }

        let accrual_id = format!("ACCRUAL-{}", uuid::Uuid::new_v4());

        Ok(InterestAccrual {
            accrual_id,
            account_id,
            accrual_date,
            balance,
            annual_rate,
            daily_interest,
            cumulative_accrued,
            created_at: Utc::now(),
        })
    }

    /// Calculate daily interest using Actual/365 day count convention
    /// Formula: (Balance × Annual Rate × 1) / 365
    pub fn calculate_daily_interest(balance: Decimal, annual_rate: Decimal) -> Decimal {
        // Using 365 for Actual/365 day count convention (MVP)
        let days_in_year = Decimal::from(365);
        (balance * annual_rate) / days_in_year
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;
    use rust_decimal_macros::dec;

    #[test]
    fn test_create_interest_accrual() {
        let accrual = InterestAccrual::new(
            "ACC-001".to_string(),
            NaiveDate::from_ymd_opt(2025, 10, 4).unwrap(),
            dec!(1000.00),
            dec!(0.025),  // 2.5% annual rate
            dec!(0.068),  // Daily interest
            dec!(2.04),   // Cumulative
        );

        assert!(accrual.is_ok());
        let a = accrual.unwrap();
        assert_eq!(a.balance, dec!(1000.00));
        assert_eq!(a.annual_rate, dec!(0.025));
    }

    #[test]
    fn test_calculate_daily_interest() {
        // Test: $1000 balance at 2.5% annual rate
        // Expected: (1000 × 0.025) / 365 = 0.0684931...
        let balance = dec!(1000.00);
        let annual_rate = dec!(0.025);

        let daily_interest = InterestAccrual::calculate_daily_interest(balance, annual_rate);

        // Round to 2 decimal places for comparison
        let rounded = daily_interest.round_dp(2);
        assert_eq!(rounded, dec!(0.07));  // Approximately $0.07 per day
    }

    #[test]
    fn test_calculate_daily_interest_high_balance() {
        // Test: $10000 balance at 4% annual rate
        // Expected: (10000 × 0.04) / 365 = 1.0958904...
        let balance = dec!(10000.00);
        let annual_rate = dec!(0.04);

        let daily_interest = InterestAccrual::calculate_daily_interest(balance, annual_rate);

        let rounded = daily_interest.round_dp(2);
        assert_eq!(rounded, dec!(1.10));  // Approximately $1.10 per day
    }

    #[test]
    fn test_calculate_daily_interest_zero_balance() {
        let balance = dec!(0.00);
        let annual_rate = dec!(0.025);

        let daily_interest = InterestAccrual::calculate_daily_interest(balance, annual_rate);

        assert_eq!(daily_interest, dec!(0.00));
    }

    #[test]
    fn test_invalid_annual_rate() {
        let accrual = InterestAccrual::new(
            "ACC-001".to_string(),
            NaiveDate::from_ymd_opt(2025, 10, 4).unwrap(),
            dec!(1000.00),
            dec!(1.5),  // Invalid: > 1
            dec!(0.068),
            dec!(2.04),
        );

        assert!(accrual.is_err());
    }
}
