use actix_web::{web, HttpResponse, Result};
use accounts_application::repositories::ProductRepository;
use crate::app_state::AppState;
use crate::models::common::ApiResponse;
use crate::models::product_models::*;

pub async fn list_products(state: web::Data<AppState>) -> Result<HttpResponse> {
    let repo = ProductRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let products = repo
        .list_all()
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response: Vec<ProductResponse> = products
        .into_iter()
        .map(|p| ProductResponse {
            product_id: p.product_id,
            product_name: p.product_name,
            product_code: p.product_code,
            description: p.description,
            status: p.status.as_str().to_string(),
            currency: p.currency,
            interest_rate: p.interest_rate,
            minimum_balance_for_interest: p.minimum_balance_for_interest,
            monthly_maintenance_fee: p.monthly_maintenance_fee,
            transaction_fee: p.transaction_fee,
            created_at: p.created_at.to_rfc3339(),
            updated_at: p.updated_at.to_rfc3339(),
        })
        .collect();

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}

pub async fn get_product(
    state: web::Data<AppState>,
    product_id: web::Path<String>,
) -> Result<HttpResponse> {
    let repo = ProductRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    match repo.find_by_id(&product_id).map_err(|e| actix_web::error::ErrorInternalServerError(e))? {
        Some(p) => {
            let response = ProductResponse {
                product_id: p.product_id,
                product_name: p.product_name,
                product_code: p.product_code,
                description: p.description,
                status: p.status.as_str().to_string(),
                currency: p.currency,
                interest_rate: p.interest_rate,
                minimum_balance_for_interest: p.minimum_balance_for_interest,
                monthly_maintenance_fee: p.monthly_maintenance_fee,
                transaction_fee: p.transaction_fee,
                created_at: p.created_at.to_rfc3339(),
                updated_at: p.updated_at.to_rfc3339(),
            };
            Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
        }
        None => Ok(HttpResponse::NotFound().json(ApiResponse::<()>::error(
            "NOT_FOUND".to_string(),
            format!("Product {} not found", product_id),
        ))),
    }
}

pub async fn create_product(
    state: web::Data<AppState>,
    req: web::Json<CreateProductRequest>,
) -> Result<HttpResponse> {
    use accounts_application::domain::product::Product;

    let product = Product::new(
        req.product_name.clone(),
        req.product_code.clone(),
        req.description.clone(),
        req.currency.clone(),
        req.interest_rate,
        req.minimum_balance_for_interest,
        req.monthly_maintenance_fee,
        req.transaction_fee,
        None, // created_by - TODO: get from auth context
    )
    .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let repo = ProductRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    repo.create(&product)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response = ProductResponse {
        product_id: product.product_id.clone(),
        product_name: product.product_name,
        product_code: product.product_code,
        description: product.description,
        status: product.status.as_str().to_string(),
        currency: product.currency,
        interest_rate: product.interest_rate,
        minimum_balance_for_interest: product.minimum_balance_for_interest,
        monthly_maintenance_fee: product.monthly_maintenance_fee,
        transaction_fee: product.transaction_fee,
        created_at: product.created_at.to_rfc3339(),
        updated_at: product.updated_at.to_rfc3339(),
    };

    Ok(HttpResponse::Created().json(ApiResponse::success(response)))
}

pub async fn list_active_products(state: web::Data<AppState>) -> Result<HttpResponse> {
    let repo = ProductRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let products = repo
        .list_active()
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response: Vec<ProductResponse> = products
        .into_iter()
        .map(|p| ProductResponse {
            product_id: p.product_id,
            product_name: p.product_name,
            product_code: p.product_code,
            description: p.description,
            status: p.status.as_str().to_string(),
            currency: p.currency,
            interest_rate: p.interest_rate,
            minimum_balance_for_interest: p.minimum_balance_for_interest,
            monthly_maintenance_fee: p.monthly_maintenance_fee,
            transaction_fee: p.transaction_fee,
            created_at: p.created_at.to_rfc3339(),
            updated_at: p.updated_at.to_rfc3339(),
        })
        .collect();

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}
