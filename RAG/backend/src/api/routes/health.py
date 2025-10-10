"""Health check routes"""
from fastapi import APIRouter
from src.services.vector_store import get_vector_store
from typing import Dict, Any

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    try:
        # Check vector store
        vector_store = get_vector_store()
        collection_stats = vector_store.get_collection_stats()

        total_docs = sum(collection_stats.values())

        return {
            "status": "healthy",
            "vector_store": {
                "status": "connected",
                "collections": collection_stats,
                "total_documents": total_docs
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
