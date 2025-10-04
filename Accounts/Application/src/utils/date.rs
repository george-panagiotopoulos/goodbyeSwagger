// Date utility functions

use chrono::{DateTime, NaiveDate, Utc};

/// Get current UTC timestamp
pub fn now() -> DateTime<Utc> {
    Utc::now()
}

/// Get current date (naive, no timezone)
pub fn today() -> NaiveDate {
    Utc::now().date_naive()
}

/// Parse date from string (YYYY-MM-DD format)
pub fn parse_date(date_str: &str) -> Result<NaiveDate, String> {
    NaiveDate::parse_from_str(date_str, "%Y-%m-%d")
        .map_err(|e| format!("Invalid date format: {}", e))
}

/// Format date as string (YYYY-MM-DD format)
pub fn format_date(date: &NaiveDate) -> String {
    date.format("%Y-%m-%d").to_string()
}

/// Format timestamp as string (ISO 8601 format)
pub fn format_timestamp(timestamp: &DateTime<Utc>) -> String {
    timestamp.to_rfc3339()
}

/// Calculate number of days between two dates
pub fn days_between(start: &NaiveDate, end: &NaiveDate) -> i64 {
    (*end - *start).num_days()
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Datelike;

    #[test]
    fn test_parse_date() {
        let result = parse_date("2025-10-04");
        assert!(result.is_ok());
        let date = result.unwrap();
        assert_eq!(date.year(), 2025);
        assert_eq!(date.month(), 10);
        assert_eq!(date.day(), 4);
    }

    #[test]
    fn test_format_date() {
        let date = NaiveDate::from_ymd_opt(2025, 10, 4).unwrap();
        assert_eq!(format_date(&date), "2025-10-04");
    }

    #[test]
    fn test_days_between() {
        let start = NaiveDate::from_ymd_opt(2025, 10, 1).unwrap();
        let end = NaiveDate::from_ymd_opt(2025, 10, 31).unwrap();
        assert_eq!(days_between(&start, &end), 30);
    }
}
