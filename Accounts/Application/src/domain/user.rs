// User domain model

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum UserRole {
    Admin,
    Officer,
    Viewer,
}

impl UserRole {
    pub fn as_str(&self) -> &str {
        match self {
            UserRole::Admin => "admin",
            UserRole::Officer => "officer",
            UserRole::Viewer => "viewer",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "admin" => Ok(UserRole::Admin),
            "officer" => Ok(UserRole::Officer),
            "viewer" => Ok(UserRole::Viewer),
            _ => Err(format!("Invalid user role: {}", s)),
        }
    }
}

impl std::fmt::Display for UserRole {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub user_id: String,
    pub username: String,
    #[serde(skip_serializing)]  // Never serialize password hash
    pub password_hash: String,
    pub full_name: String,
    pub email: String,
    pub role: UserRole,
    pub status: String,  // "active" or "inactive"

    // Audit fields
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl User {
    /// Create a new user (password should already be hashed)
    pub fn new(
        username: String,
        password_hash: String,
        full_name: String,
        email: String,
        role: UserRole,
    ) -> Result<Self, String> {
        // Validation
        if username.trim().is_empty() {
            return Err("Username cannot be empty".to_string());
        }
        if password_hash.is_empty() {
            return Err("Password hash cannot be empty".to_string());
        }
        if full_name.trim().is_empty() {
            return Err("Full name cannot be empty".to_string());
        }
        if email.trim().is_empty() || !email.contains('@') {
            return Err("Invalid email address".to_string());
        }

        let now = Utc::now();
        let user_id = format!("USR-{}", uuid::Uuid::new_v4());

        Ok(User {
            user_id,
            username,
            password_hash,
            full_name,
            email,
            role,
            status: "active".to_string(),
            created_at: now,
            updated_at: now,
        })
    }

    /// Check if user is active
    pub fn is_active(&self) -> bool {
        self.status == "active"
    }

    /// Check if user is admin
    pub fn is_admin(&self) -> bool {
        self.role == UserRole::Admin
    }

    /// Check if user is officer
    pub fn is_officer(&self) -> bool {
        self.role == UserRole::Officer
    }

    /// Deactivate user
    pub fn deactivate(&mut self) {
        self.status = "inactive".to_string();
        self.updated_at = Utc::now();
    }

    /// Activate user
    pub fn activate(&mut self) {
        self.status = "active".to_string();
        self.updated_at = Utc::now();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_valid_user() {
        let user = User::new(
            "admin".to_string(),
            "$2b$12$hash...".to_string(),
            "Admin User".to_string(),
            "admin@example.com".to_string(),
            UserRole::Admin,
        );

        assert!(user.is_ok());
        let u = user.unwrap();
        assert_eq!(u.username, "admin");
        assert!(u.is_active());
        assert!(u.is_admin());
    }

    #[test]
    fn test_invalid_email() {
        let user = User::new(
            "admin".to_string(),
            "$2b$12$hash...".to_string(),
            "Admin User".to_string(),
            "invalid-email".to_string(),  // No @ symbol
            UserRole::Admin,
        );

        assert!(user.is_err());
    }

    #[test]
    fn test_user_status_change() {
        let mut user = User::new(
            "testuser".to_string(),
            "$2b$12$hash...".to_string(),
            "Test User".to_string(),
            "test@example.com".to_string(),
            UserRole::Officer,
        ).unwrap();

        assert!(user.is_active());

        user.deactivate();
        assert!(!user.is_active());

        user.activate();
        assert!(user.is_active());
    }

    #[test]
    fn test_user_roles() {
        let admin = User::new(
            "admin".to_string(),
            "$2b$12$hash...".to_string(),
            "Admin".to_string(),
            "admin@example.com".to_string(),
            UserRole::Admin,
        ).unwrap();

        let officer = User::new(
            "officer".to_string(),
            "$2b$12$hash...".to_string(),
            "Officer".to_string(),
            "officer@example.com".to_string(),
            UserRole::Officer,
        ).unwrap();

        assert!(admin.is_admin());
        assert!(!admin.is_officer());
        assert!(!officer.is_admin());
        assert!(officer.is_officer());
    }
}
