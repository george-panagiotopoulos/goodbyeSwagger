// Domain models module

pub mod product;
pub mod account;
pub mod transaction;
pub mod user;
pub mod customer;
pub mod interest;

// Re-export domain types for easier imports
pub use product::Product;
pub use account::{Account, AccountStatus};
pub use transaction::{Transaction, TransactionType, TransactionCategory};
pub use user::{User, UserRole};
pub use customer::{Customer, CustomerType, CustomerStatus};
pub use interest::InterestAccrual;
