// Application configuration

use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub database_url: String,
    pub log_level: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        AppConfig {
            database_url: "../Database/accounts.db".to_string(),
            log_level: "info".to_string(),
        }
    }
}

impl AppConfig {
    /// Create configuration from environment variables or defaults
    pub fn from_env() -> Self {
        AppConfig {
            database_url: std::env::var("DATABASE_URL")
                .unwrap_or_else(|_| "../Database/accounts.db".to_string()),
            log_level: std::env::var("RUST_LOG").unwrap_or_else(|_| "info".to_string()),
        }
    }

    /// Get absolute path to database
    pub fn database_path(&self) -> PathBuf {
        PathBuf::from(&self.database_url)
    }

    /// Validate configuration
    pub fn validate(&self) -> Result<(), String> {
        if self.database_url.is_empty() {
            return Err("Database URL cannot be empty".to_string());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config() {
        let config = AppConfig::default();
        assert_eq!(config.database_url, "../Database/accounts.db");
        assert_eq!(config.log_level, "info");
    }

    #[test]
    fn test_validate_config() {
        let config = AppConfig::default();
        assert!(config.validate().is_ok());

        let invalid_config = AppConfig {
            database_url: "".to_string(),
            log_level: "info".to_string(),
        };
        assert!(invalid_config.validate().is_err());
    }
}
