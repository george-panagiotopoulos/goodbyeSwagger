use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<ApiError>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiError {
    pub code: String,
    pub message: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ErrorResponse {
    pub error: ApiError,
}

impl ErrorResponse {
    pub fn new(code: &str, message: &str) -> Self {
        ErrorResponse {
            error: ApiError {
                code: code.to_string(),
                message: message.to_string(),
            },
        }
    }

    pub fn internal_error(message: &str) -> Self {
        Self::new("INTERNAL_ERROR", message)
    }
}

impl<T> ApiResponse<T> {
    pub fn success(data: T) -> Self {
        ApiResponse {
            success: true,
            data: Some(data),
            error: None,
        }
    }

    pub fn error(code: String, message: String) -> ApiResponse<()> {
        ApiResponse {
            success: false,
            data: None,
            error: Some(ApiError { code, message }),
        }
    }
}
