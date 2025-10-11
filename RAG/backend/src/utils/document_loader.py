"""Document loader for ingesting documentation"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import re
from datetime import datetime
from src.models.document import Document

logger = logging.getLogger(__name__)


# Knowledge category mapping based on folder structure
# Maps folder names in /Accounts/docs/ to collection names
FOLDER_TO_COLLECTION = {
    "api": "api",
    "architecture": "architecture",
    "business": "business",
    "data_models": "data_models",
    "devops": "devops",
    "examples": "examples",
    "user_guides": "user_guides",
}

# Additional keyword-based mappings for backwards compatibility
KEYWORD_MAPPINGS = {
    "swagger": "api",
    "openapi": "api",
    "endpoint": "api",
    "adr": "architecture",
    "design": "architecture",
    "diagram": "architecture",
    "marketing": "business",
    "product": "business",
    "use-case": "business",
    "schema": "data_models",
    "er-diagram": "data_models",
    "migration": "data_models",
    "deployment": "devops",
    "infrastructure": "devops",
    "operation": "devops",
    "postman": "examples",
    "curl": "examples",
    "snippet": "examples",
    "sample": "examples",
    "getting-started": "user_guides",
    "tutorial": "user_guides",
    "howto": "user_guides",
    "setup": "user_guides",
}


def categorize_document(file_path: str) -> str:
    """
    Determine category for a document based on its path

    Maps folder structure to collection names for better organization.
    E.g., docs/api/ -> "api" collection, docs/business/ -> "business" collection

    Args:
        file_path: Path to the file

    Returns:
        Category name (collection name matching folder structure)
    """
    file_path_lower = file_path.lower()

    # First, check direct folder matches (highest priority)
    for folder_name, collection_name in FOLDER_TO_COLLECTION.items():
        if f"/{folder_name}/" in file_path_lower or file_path_lower.startswith(folder_name + "/"):
            return collection_name

    # Then check keyword-based mappings
    for keyword, collection_name in KEYWORD_MAPPINGS.items():
        if keyword in file_path_lower:
            return collection_name

    # Default to user_guides for unclassified docs
    return "user_guides"


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks

    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            for separator in ['. ', '.\n', '!\n', '?\n']:
                last_sep = text.rfind(separator, start, end)
                if last_sep != -1:
                    end = last_sep + len(separator)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def load_file(file_path: Path) -> str:
    """
    Load content from a file

    Args:
        file_path: Path to the file

    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""


def load_documents_from_directory(
    directory: Path,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Load all documents from a directory recursively

    Args:
        directory: Root directory to scan
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks

    Returns:
        List of Document objects
    """
    documents = []
    supported_extensions = {'.md', '.txt', '.rst', '.json', '.yaml', '.yml'}

    logger.info(f"Scanning directory: {directory}")

    if not directory.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return documents

    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix in supported_extensions:
            logger.debug(f"Processing: {file_path}")

            # Load content
            content = load_file(file_path)
            if not content:
                continue

            # Chunk content
            chunks = chunk_text(content, chunk_size, chunk_overlap)

            # Determine category
            relative_path = str(file_path.relative_to(directory))
            category = categorize_document(relative_path)

            # Create documents for each chunk
            for i, chunk in enumerate(chunks):
                doc_id = f"{file_path.stem}_chunk_{i}"

                doc = Document(
                    id=doc_id,
                    content=chunk,
                    metadata={
                        "source": relative_path,
                        "category": category,
                        "title": file_path.stem,
                        "created_at": datetime.now().isoformat(),
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)

    logger.info(f"Loaded {len(documents)} document chunks from {directory}")
    return documents
