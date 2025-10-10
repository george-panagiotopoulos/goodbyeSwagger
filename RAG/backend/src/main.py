"""FastAPI application entry point"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.routes import personas, chat, health

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="Persona-based RAG system for the Account Processing System documentation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(personas.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG System API",
        "docs": "/api/docs",
        "health": "/api/health"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("="*80)
    logger.info("RAG System API Starting")
    logger.info("="*80)
    logger.info(f"API Host: {settings.rag_api_host}")
    logger.info(f"API Port: {settings.rag_api_port}")
    logger.info(f"ChromaDB Path: {settings.chroma_path}")
    logger.info(f"CORS Origins: {settings.cors_origins_list}")
    logger.info("="*80)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("RAG System API Shutting Down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.rag_api_host,
        port=settings.rag_api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
