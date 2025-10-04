use crate::domain::user::{User, UserRole};
use crate::error::AppError;
use rusqlite::{params, Connection, OptionalExtension, Row};

pub struct UserRepository {
    connection: Connection,
}

impl UserRepository {
    pub fn new(db_path: &str) -> Result<Self, AppError> {
        let connection = Connection::open(db_path)?;
        Ok(UserRepository { connection })
    }

    pub fn create(&self, user: &User) -> Result<(), AppError> {
        self.connection.execute(
            "INSERT INTO users (
                user_id, username, password_hash, role, email, full_name,
                is_active, created_at, updated_at
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)",
            params![
                user.user_id,
                user.username,
                user.password_hash,
                user.role.to_string(),
                user.email,
                user.full_name,
                if user.status == "active" { 1 } else { 0 },
                user.created_at.to_rfc3339(),
                user.updated_at.to_rfc3339(),
            ],
        )?;
        Ok(())
    }

    pub fn find_by_id(&self, user_id: &str) -> Result<Option<User>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT user_id, username, password_hash, role, email, full_name,
                    is_active, created_at, updated_at
             FROM users WHERE user_id = ?1",
        )?;

        let user = stmt
            .query_row(params![user_id], |row| self.row_to_user(row))
            .optional()?;

        Ok(user)
    }

    pub fn find_by_username(&self, username: &str) -> Result<Option<User>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT user_id, username, password_hash, role, email, full_name,
                    is_active, created_at, updated_at
             FROM users WHERE username = ?1",
        )?;

        let user = stmt
            .query_row(params![username], |row| self.row_to_user(row))
            .optional()?;

        Ok(user)
    }

    pub fn find_by_email(&self, email: &str) -> Result<Option<User>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT user_id, username, password_hash, role, email, full_name,
                    is_active, created_at, updated_at
             FROM users WHERE email = ?1",
        )?;

        let user = stmt
            .query_row(params![email], |row| self.row_to_user(row))
            .optional()?;

        Ok(user)
    }

    pub fn list_active(&self) -> Result<Vec<User>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT user_id, username, password_hash, role, email, full_name,
                    is_active, created_at, updated_at
             FROM users WHERE is_active = 1 ORDER BY username",
        )?;

        let users = stmt
            .query_map([], |row| self.row_to_user(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(users)
    }

    pub fn list_all(&self) -> Result<Vec<User>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT user_id, username, password_hash, role, email, full_name,
                    is_active, created_at, updated_at
             FROM users ORDER BY created_at DESC",
        )?;

        let users = stmt
            .query_map([], |row| self.row_to_user(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(users)
    }

    pub fn update(&self, user: &User) -> Result<(), AppError> {
        let rows_affected = self.connection.execute(
            "UPDATE users SET
                email = ?1, full_name = ?2, role = ?3, is_active = ?4, updated_at = ?5
             WHERE user_id = ?6",
            params![
                user.email,
                user.full_name,
                user.role.to_string(),
                if user.status == "active" { 1 } else { 0 },
                user.updated_at.to_rfc3339(),
                user.user_id,
            ],
        )?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "User".to_string(),
                user.user_id.clone()
            ));
        }

        Ok(())
    }

    pub fn update_password(&self, user_id: &str, password_hash: &str) -> Result<(), AppError> {
        let rows_affected = self.connection.execute(
            "UPDATE users SET password_hash = ?1, updated_at = ?2 WHERE user_id = ?3",
            params![password_hash, chrono::Utc::now().to_rfc3339(), user_id],
        )?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "User".to_string(),
                user_id.to_string()
            ));
        }

        Ok(())
    }

    pub fn delete(&self, user_id: &str) -> Result<(), AppError> {
        let rows_affected = self
            .connection
            .execute("DELETE FROM users WHERE user_id = ?1", params![user_id])?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "User".to_string(),
                user_id.to_string()
            ));
        }

        Ok(())
    }

    fn row_to_user(&self, row: &Row) -> rusqlite::Result<User> {
        let role_str: String = row.get(3)?;
        let role = UserRole::from_str(&role_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(3, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let created_at_str: String = row.get(7)?;
        let created_at = chrono::DateTime::parse_from_rfc3339(&created_at_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(7, rusqlite::types::Type::Text, Box::new(e)))?
            .with_timezone(&chrono::Utc);

        let updated_at_str: String = row.get(8)?;
        let updated_at = chrono::DateTime::parse_from_rfc3339(&updated_at_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(8, rusqlite::types::Type::Text, Box::new(e)))?
            .with_timezone(&chrono::Utc);

        let is_active: i32 = row.get(6)?;

        Ok(User {
            user_id: row.get(0)?,
            username: row.get(1)?,
            password_hash: row.get(2)?,
            full_name: row.get(5)?,
            email: row.get(4)?,
            role,
            status: if is_active == 1 { "active".to_string() } else { "inactive".to_string() },
            created_at,
            updated_at,
        })
    }
}
