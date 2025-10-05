use actix_web::{web, HttpResponse};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use crate::app_state::AppState;
use crate::middleware::auth::generate_token;
use crate::models::common::ErrorResponse;

#[derive(Debug, Deserialize)]
pub struct LoginRequest {
    pub username: String,
    pub password: String,
}

#[derive(Debug, Serialize)]
pub struct LoginResponse {
    pub token: String,
    pub user: UserInfo,
}

#[derive(Debug, Serialize)]
pub struct UserInfo {
    pub user_id: String,
    pub username: String,
    pub full_name: String,
    pub email: String,
    pub role: String,
}

#[derive(Debug, Deserialize)]
pub struct RegisterRequest {
    pub username: String,
    pub password: String,
    pub full_name: String,
    pub email: String,
    pub role: Option<String>,
}

pub async fn login(
    state: web::Data<AppState>,
    request: web::Json<LoginRequest>,
) -> HttpResponse {
    let conn = match state.get_connection() {
        Ok(c) => c,
        Err(e) => {
            log::error!("Database connection error: {}", e);
            return HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Database connection failed"
            ));
        }
    };

    // Query user from database
    let query = "SELECT user_id, username, password_hash, full_name, email, role, status FROM users WHERE username = ?1";
    let user_result: Result<(String, String, String, String, String, String, String), _> =
        conn.query_row(query, [&request.username], |row| {
            Ok((
                row.get(0)?,
                row.get(1)?,
                row.get(2)?,
                row.get(3)?,
                row.get(4)?,
                row.get(5)?,
                row.get(6)?,
            ))
        });

    match user_result {
        Ok((user_id, username, password_hash, full_name, email, role, status)) => {
            // Check if user is active
            if status != "active" {
                return HttpResponse::Forbidden().json(ErrorResponse::new(
                    "USER_INACTIVE",
                    "User account is not active",
                ));
            }

            // Verify password
            match bcrypt::verify(&request.password, &password_hash) {
                Ok(valid) if valid => {
                    // Generate JWT token
                    match generate_token(user_id.clone(), username.clone(), role.clone()) {
                        Ok(token) => {
                            log::info!("User {} logged in successfully", username);
                            HttpResponse::Ok().json(LoginResponse {
                                token,
                                user: UserInfo {
                                    user_id,
                                    username,
                                    full_name,
                                    email,
                                    role,
                                },
                            })
                        }
                        Err(e) => {
                            log::error!("Token generation error: {}", e);
                            HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                                "Failed to generate authentication token"
                            ))
                        }
                    }
                }
                Ok(_) => {
                    log::warn!("Failed login attempt for user: {}", request.username);
                    HttpResponse::Unauthorized().json(ErrorResponse::new(
                        "INVALID_CREDENTIALS",
                        "Invalid username or password",
                    ))
                }
                Err(e) => {
                    log::error!("Password verification error: {}", e);
                    HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                        "Authentication error"
                    ))
                }
            }
        }
        Err(_) => {
            log::warn!("Failed login attempt for user: {}", request.username);
            HttpResponse::Unauthorized().json(ErrorResponse::new(
                "INVALID_CREDENTIALS",
                "Invalid username or password",
            ))
        }
    }
}

pub async fn register(
    state: web::Data<AppState>,
    request: web::Json<RegisterRequest>,
) -> HttpResponse {
    // Validate inputs
    if request.username.trim().is_empty() || request.password.len() < 8 {
        return HttpResponse::BadRequest().json(ErrorResponse::new(
            "VALIDATION_ERROR",
            "Username is required and password must be at least 8 characters",
        ));
    }

    if request.email.trim().is_empty() || !request.email.contains('@') {
        return HttpResponse::BadRequest().json(ErrorResponse::new(
            "VALIDATION_ERROR",
            "Valid email address is required",
        ));
    }

    let conn = match state.get_connection() {
        Ok(c) => c,
        Err(e) => {
            log::error!("Database connection error: {}", e);
            return HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Database connection failed"
            ));
        }
    };

    // Hash password
    let password_hash = match bcrypt::hash(&request.password, bcrypt::DEFAULT_COST) {
        Ok(hash) => hash,
        Err(e) => {
            log::error!("Password hashing error: {}", e);
            return HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Failed to process registration"
            ));
        }
    };

    // Generate user ID
    let user_id = format!("USR-{}", Uuid::new_v4());
    let role = request.role.as_deref().unwrap_or("viewer");

    // Insert user into database
    let insert_query = "
        INSERT INTO users (user_id, username, password_hash, full_name, email, role, status, created_at, updated_at)
        VALUES (?1, ?2, ?3, ?4, ?5, ?6, 'active', datetime('now'), datetime('now'))
    ";

    match conn.execute(
        insert_query,
        (
            &user_id,
            &request.username,
            &password_hash,
            &request.full_name,
            &request.email,
            role,
        ),
    ) {
        Ok(_) => {
            log::info!("New user registered: {}", request.username);

            // Generate token for the new user
            match generate_token(user_id.clone(), request.username.clone(), role.to_string()) {
                Ok(token) => {
                    HttpResponse::Created().json(LoginResponse {
                        token,
                        user: UserInfo {
                            user_id,
                            username: request.username.clone(),
                            full_name: request.full_name.clone(),
                            email: request.email.clone(),
                            role: role.to_string(),
                        },
                    })
                }
                Err(e) => {
                    log::error!("Token generation error: {}", e);
                    HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                        "Registration successful but failed to generate token"
                    ))
                }
            }
        }
        Err(e) => {
            if e.to_string().contains("UNIQUE constraint failed") {
                return HttpResponse::Conflict().json(ErrorResponse::new(
                    "USER_EXISTS",
                    "Username or email already exists",
                ));
            }

            log::error!("User registration error: {}", e);
            HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Failed to register user"
            ))
        }
    }
}

pub async fn me(
    claims: web::ReqData<crate::middleware::auth::Claims>,
) -> HttpResponse {
    let claims = claims.into_inner();

    HttpResponse::Ok().json(serde_json::json!({
        "user_id": claims.sub,
        "username": claims.username,
        "role": claims.role,
    }))
}
