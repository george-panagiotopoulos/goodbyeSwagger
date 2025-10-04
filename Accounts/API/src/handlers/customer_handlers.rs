use actix_web::{web, HttpResponse, Result};
use accounts_application::repositories::CustomerRepository;
use accounts_application::domain::customer::CustomerType;
use crate::app_state::AppState;
use crate::models::common::ApiResponse;
use crate::models::customer_models::*;

pub async fn list_customers(state: web::Data<AppState>) -> Result<HttpResponse> {
    let repo = CustomerRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let customers = repo
        .list_all()
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response: Vec<CustomerResponse> = customers
        .into_iter()
        .map(|c| CustomerResponse {
            customer_id: c.customer_id,
            external_customer_id: c.external_customer_id,
            customer_name: c.customer_name,
            customer_type: c.customer_type.as_str().to_string(),
            status: c.status.as_str().to_string(),
            email: c.email,
            phone: c.phone,
            created_at: c.created_at.to_rfc3339(),
            updated_at: c.updated_at.to_rfc3339(),
        })
        .collect();

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}

pub async fn get_customer(
    state: web::Data<AppState>,
    customer_id: web::Path<String>,
) -> Result<HttpResponse> {
    let repo = CustomerRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    match repo.find_by_id(&customer_id).map_err(|e| actix_web::error::ErrorInternalServerError(e))? {
        Some(c) => {
            let response = CustomerResponse {
                customer_id: c.customer_id,
                external_customer_id: c.external_customer_id,
                customer_name: c.customer_name,
                customer_type: c.customer_type.as_str().to_string(),
                status: c.status.as_str().to_string(),
                email: c.email,
                phone: c.phone,
                created_at: c.created_at.to_rfc3339(),
                updated_at: c.updated_at.to_rfc3339(),
            };
            Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
        }
        None => Ok(HttpResponse::NotFound().json(ApiResponse::<()>::error(
            "NOT_FOUND".to_string(),
            format!("Customer {} not found", customer_id),
        ))),
    }
}

pub async fn create_customer(
    state: web::Data<AppState>,
    req: web::Json<CreateCustomerRequest>,
) -> Result<HttpResponse> {
    use accounts_application::domain::customer::Customer;

    let customer_type = CustomerType::from_str(&req.customer_type)
        .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let customer = Customer::new(
        req.customer_name.clone(),
        customer_type,
        req.external_customer_id.clone(),
        req.email.clone(),
        req.phone.clone(),
    )
    .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let repo = CustomerRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    repo.create(&customer)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response = CustomerResponse {
        customer_id: customer.customer_id.clone(),
        external_customer_id: customer.external_customer_id,
        customer_name: customer.customer_name,
        customer_type: customer.customer_type.as_str().to_string(),
        status: customer.status.as_str().to_string(),
        email: customer.email,
        phone: customer.phone,
        created_at: customer.created_at.to_rfc3339(),
        updated_at: customer.updated_at.to_rfc3339(),
    };

    Ok(HttpResponse::Created().json(ApiResponse::success(response)))
}
