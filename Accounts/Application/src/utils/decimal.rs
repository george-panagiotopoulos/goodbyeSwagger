// Decimal utility functions for financial calculations

use rust_decimal::Decimal;

/// Round decimal to 2 decimal places (for currency)
pub fn round_currency(value: Decimal) -> Decimal {
    value.round_dp(2)
}

/// Round decimal to specified decimal places
pub fn round_to(value: Decimal, decimal_places: u32) -> Decimal {
    value.round_dp(decimal_places)
}

/// Check if two decimal values are equal (with tolerance for floating point precision)
pub fn are_equal(a: Decimal, b: Decimal) -> bool {
    a == b
}

/// Format decimal as currency string
pub fn format_currency(value: Decimal, currency_code: &str) -> String {
    format!("{} {:.2}", currency_code, value)
}

#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_round_currency() {
        assert_eq!(round_currency(dec!(10.456)), dec!(10.46));
        assert_eq!(round_currency(dec!(10.454)), dec!(10.45));
    }

    #[test]
    fn test_format_currency() {
        assert_eq!(format_currency(dec!(1000.50), "USD"), "USD 1000.50");
        assert_eq!(format_currency(dec!(99.99), "EUR"), "EUR 99.99");
    }
}
