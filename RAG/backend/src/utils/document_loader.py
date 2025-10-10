"""Document loader for ingesting documentation"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import re
from datetime import datetime
from src.models.document import Document

logger = logging.getLogger(__name__)


# Knowledge category mapping based on file paths
CATEGORY_MAPPINGS = {
    "architecture": "architecture_knowledge",
    "design": "architecture_knowledge",
    "adr": "architecture_knowledge",
    "api": "api_knowledge",
    "swagger": "api_knowledge",
    "openapi": "api_knowledge",
    "endpoints": "api_knowledge",
    "business": "business_knowledge",
    "product": "business_knowledge",
    "marketing": "business_knowledge",
    "use-case": "business_knowledge",
    "developer": "developer_knowledge",
    "setup": "developer_knowledge",
    "installation": "developer_knowledge",
    "devops": "devops_knowledge",
    "deployment": "devops_knowledge",
    "infrastructure": "devops_knowledge",
    "database": "data_knowledge",
    "schema": "data_knowledge",
    "migration": "data_knowledge",
    "data-model": "data_knowledge",
    "example": "code_examples_knowledge",
    "snippet": "code_examples_knowledge",
    "sample": "code_examples_knowledge",
    "domain": "domain_knowledge",
    "business-logic": "domain_knowledge",
    "rules": "domain_knowledge",
}


def categorize_document(file_path: str) -> str:
    """
    Determine category for a document based on its path

    Args:
        file_path: Path to the file

    Returns:
        Category name (collection name)
    """
    file_path_lower = file_path.lower()

    # Check path components
    for keyword, category in CATEGORY_MAPPINGS.items():
        if keyword in file_path_lower:
            return category

    # Default to developer knowledge
    return "developer_knowledge"


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
