// Account Processing Application Layer
// Business logic, domain models, and services

pub mod config;
pub mod domain;
pub mod error;
pub mod repositories;
pub mod services;
pub mod utils;

// Re-export commonly used types
pub use config::AppConfig;
pub use error::{AppError, AppResult};

// Re-export domain models
pub use domain::{
    Account, AccountStatus, InterestAccrual, Product, Transaction, TransactionCategory,
    TransactionType, User, UserRole,
};

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
