// Validation utility functions

use rust_decimal::Decimal;

/// Validate currency code (must be 3 uppercase letters)
pub fn validate_currency_code(code: &str) -> Result<(), String> {
    if code.len() != 3 {
        return Err(format!(
            "Currency code must be exactly 3 characters, got: {}",
            code
        ));
    }
    if !code.chars().all(|c| c.is_ascii_uppercase()) {
        return Err(format!(
            "Currency code must be uppercase letters, got: {}",
            code
        ));
    }
    Ok(())
}

/// Validate email address (basic validation)
pub fn validate_email(email: &str) -> Result<(), String> {
    if email.trim().is_empty() {
        return Err("Email cannot be empty".to_string());
    }
    if !email.contains('@') {
        return Err("Email must contain @".to_string());
    }
    if !email.contains('.') {
        return Err("Email must contain a domain".to_string());
    }
    Ok(())
}

/// Validate account number (must be numeric and specific length)
pub fn validate_account_number(account_number: &str) -> Result<(), String> {
    if account_number.trim().is_empty() {
        return Err("Account number cannot be empty".to_string());
    }
    if !account_number.chars().all(|c| c.is_ascii_digit()) {
        return Err("Account number must contain only digits".to_string());
    }
    if account_number.len() != 10 {
        return Err(format!(
            "Account number must be exactly 10 digits, got: {} digits",
            account_number.len()
        ));
    }
    Ok(())
}

/// Validate positive amount
pub fn validate_positive_amount(amount: Decimal) -> Result<(), String> {
    if amount <= Decimal::ZERO {
        return Err("Amount must be positive".to_string());
    }
    Ok(())
}

/// Validate non-negative amount
pub fn validate_non_negative_amount(amount: Decimal) -> Result<(), String> {
    if amount < Decimal::ZERO {
        return Err("Amount cannot be negative".to_string());
    }
    Ok(())
}

/// Validate percentage (0.0 to 1.0)
pub fn validate_percentage(rate: Decimal) -> Result<(), String> {
    if rate < Decimal::ZERO || rate > Decimal::ONE {
        return Err(format!("Percentage must be between 0 and 1, got: {}", rate));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_validate_currency_code() {
        assert!(validate_currency_code("USD").is_ok());
        assert!(validate_currency_code("EUR").is_ok());
        assert!(validate_currency_code("GBP").is_ok());

        assert!(validate_currency_code("US").is_err());  // Too short
        assert!(validate_currency_code("USDD").is_err());  // Too long
        assert!(validate_currency_code("usd").is_err());  // Lowercase
    }

    #[test]
    fn test_validate_email() {
        assert!(validate_email("test@example.com").is_ok());
        assert!(validate_email("user.name@domain.co.uk").is_ok());

        assert!(validate_email("invalid").is_err());  // No @
        assert!(validate_email("test@").is_err());  // No domain
        assert!(validate_email("").is_err());  // Empty
    }

    #[test]
    fn test_validate_account_number() {
        assert!(validate_account_number("1234567890").is_ok());

        assert!(validate_account_number("123456789").is_err());  // Too short
        assert!(validate_account_number("12345678901").is_err());  // Too long
        assert!(validate_account_number("123456789A").is_err());  // Contains letter
        assert!(validate_account_number("").is_err());  // Empty
    }

    #[test]
    fn test_validate_positive_amount() {
        assert!(validate_positive_amount(dec!(100.00)).is_ok());
        assert!(validate_positive_amount(dec!(0.01)).is_ok());

        assert!(validate_positive_amount(dec!(0.00)).is_err());  // Zero
        assert!(validate_positive_amount(dec!(-10.00)).is_err());  // Negative
    }

    #[test]
    fn test_validate_percentage() {
        assert!(validate_percentage(dec!(0.025)).is_ok());  // 2.5%
        assert!(validate_percentage(dec!(0.0)).is_ok());  // 0%
        assert!(validate_percentage(dec!(1.0)).is_ok());  // 100%

        assert!(validate_percentage(dec!(1.5)).is_err());  // > 100%
        assert!(validate_percentage(dec!(-0.1)).is_err());  // Negative
    }
}
