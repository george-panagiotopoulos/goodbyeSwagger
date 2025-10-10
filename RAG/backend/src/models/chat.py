"""Chat-related data models"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role in conversation"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Single chat message"""

    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "How do I set up the development environment?",
                "timestamp": "2025-10-10T12:00:00"
            }
        }


class ChatRequest(BaseModel):
    """Chat request from client"""

    persona_id: str = Field(..., description="Persona to use for this chat")
    message: str = Field(..., description="User message", min_length=1)
    conversation_history: List[ChatMessage] = Field(default_factory=list, description="Previous messages in conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "persona_id": "developer",
                "message": "How do I run the tests?",
                "conversation_history": [
                    {
                        "role": "user",
                        "content": "How do I set up the project?",
                        "timestamp": "2025-10-10T12:00:00"
                    },
                    {
                        "role": "assistant",
                        "content": "To set up the project, follow these steps...",
                        "timestamp": "2025-10-10T12:00:05"
                    }
                ]
            }
        }


class SourceDocument(BaseModel):
    """Source document used in RAG response"""

    content: str = Field(..., description="Document content excerpt")
    source: str = Field(..., description="Source file path")
    relevance_score: float = Field(..., description="Relevance score from vector search")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "To run tests, use: cargo test",
                "source": "/docs/guides/testing.md",
                "relevance_score": 0.92
            }
        }


class ChatResponse(BaseModel):
    """Chat response to client"""

    persona_id: str = Field(..., description="Persona that generated the response")
    message: str = Field(..., description="Assistant response")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "persona_id": "developer",
                "message": "To run tests, navigate to the Application directory and run `cargo test`...",
                "sources": [
                    {
                        "content": "Run tests with: cargo test",
                        "source": "/docs/guides/testing.md",
                        "relevance_score": 0.92
                    }
                ],
                "timestamp": "2025-10-10T12:00:10"
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid persona_id",
                "detail": "Persona 'unknown' does not exist. Available personas: developer, devops, business, api_consumer, architect, dba, general",
                "timestamp": "2025-10-10T12:00:00"
            }
        }
