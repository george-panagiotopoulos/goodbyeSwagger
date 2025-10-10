"""Document data models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class Document(BaseModel):
    """Represents a document chunk for embedding"""

    id: str = Field(..., description="Unique document ID")
    content: str = Field(..., description="Document text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")

    # Common metadata fields
    source: Optional[str] = Field(None, description="Source file path")
    category: Optional[str] = Field(None, description="Knowledge category")
    title: Optional[str] = Field(None, description="Document title")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    chunk_index: Optional[int] = Field(None, description="Chunk number in source document")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_001_chunk_0",
                "content": "This is a sample document about API authentication...",
                "metadata": {
                    "source": "/docs/api/authentication.md",
                    "category": "api_knowledge",
                    "title": "API Authentication",
                    "created_at": "2025-10-10T00:00:00",
                    "chunk_index": 0
                }
            }
        }


class DocumentChunk(BaseModel):
    """Represents a text chunk from a source document"""

    text: str
    metadata: Dict[str, Any]
    chunk_id: str
    chunk_index: int
