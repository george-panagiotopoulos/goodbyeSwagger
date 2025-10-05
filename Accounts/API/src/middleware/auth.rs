use actix_web::{dev::ServiceRequest, error::ErrorUnauthorized, Error, HttpMessage};
use actix_web_httpauth::extractors::bearer::BearerAuth;
use jsonwebtoken::{decode, DecodingKey, Validation, Algorithm};
use serde::{Deserialize, Serialize};
use std::env;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Claims {
    pub sub: String,      // user_id
    pub username: String,
    pub role: String,
    pub exp: usize,       // expiration time
    pub iat: usize,       // issued at
}

impl Claims {
    pub fn new(user_id: String, username: String, role: String, expiration_hours: i64) -> Self {
        let iat = chrono::Utc::now().timestamp() as usize;
        let exp = (chrono::Utc::now() + chrono::Duration::hours(expiration_hours)).timestamp() as usize;

        Self {
            sub: user_id,
            username,
            role,
            exp,
            iat,
        }
    }
}

pub async fn validator(
    req: ServiceRequest,
    credentials: BearerAuth,
) -> Result<ServiceRequest, (Error, ServiceRequest)> {
    let token = credentials.token();
    let secret = env::var("JWT_SECRET").unwrap_or_else(|_| "your-secret-key-change-in-production".to_string());

    match decode::<Claims>(
        token,
        &DecodingKey::from_secret(secret.as_bytes()),
        &Validation::new(Algorithm::HS256),
    ) {
        Ok(token_data) => {
            // Insert claims into request extensions for use in handlers
            req.extensions_mut().insert(token_data.claims.clone());
            Ok(req)
        }
        Err(err) => {
            log::error!("JWT validation error: {:?}", err);
            Err((ErrorUnauthorized("Invalid token"), req))
        }
    }
}

pub fn generate_token(user_id: String, username: String, role: String) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration_hours = env::var("JWT_EXPIRATION_HOURS")
        .unwrap_or_else(|_| "24".to_string())
        .parse::<i64>()
        .unwrap_or(24);

    let claims = Claims::new(user_id, username, role, expiration_hours);
    let secret = env::var("JWT_SECRET").unwrap_or_else(|_| "your-secret-key-change-in-production".to_string());

    jsonwebtoken::encode(
        &jsonwebtoken::Header::default(),
        &claims,
        &jsonwebtoken::EncodingKey::from_secret(secret.as_bytes()),
    )
}
