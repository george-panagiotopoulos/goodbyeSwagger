"""Configuration management for RAG system"""
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment_name: str
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_embedding_deployment: str

    # RAG API
    rag_api_port: int = 6603
    rag_api_host: str = "0.0.0.0"

    # ChromaDB
    chroma_persist_directory: str = "../vector_db"

    # Document Processing
    docs_path: str = "../../docs"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_context_tokens: int = 8000

    # LLM Settings
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.95

    # CORS
    cors_origins: str = "http://localhost:6604,http://localhost:5173"

    # Logging
    log_level: str = "INFO"

    class Config:
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def chroma_path(self) -> str:
        """Get absolute path to ChromaDB directory"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, self.chroma_persist_directory)

    @property
    def docs_absolute_path(self) -> str:
        """Get absolute path to docs directory"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, self.docs_path)


# Global settings instance
settings = Settings()
