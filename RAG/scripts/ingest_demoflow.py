#!/usr/bin/env python3
"""
Quick script to ingest only the demoflow documents
"""
import sys
import logging
from pathlib import Path

# Add backend src to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from src.utils.document_loader import load_documents_from_directory
from src.services.vector_store import get_vector_store

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Ingest demoflow documents"""
    logger.info("="*80)
    logger.info("Ingesting demoflow documents")
    logger.info("="*80)

    # Path to demoflow folder
    demoflow_path = Path(__file__).parent.parent.parent / "Accounts/docs/examples/demoflow"

    if not demoflow_path.exists():
        logger.error(f"Demoflow directory not found: {demoflow_path}")
        return

    logger.info(f"Loading documents from: {demoflow_path}")

    # Load documents
    documents = load_documents_from_directory(
        directory=demoflow_path,
        chunk_size=1500,  # Larger chunks for API examples
        chunk_overlap=200
    )

    if not documents:
        logger.warning("No documents found")
        return

    logger.info(f"Loaded {len(documents)} document chunks")

    # Initialize vector store
    logger.info("Initializing vector store...")
    vector_store = get_vector_store()

    # Add to examples collection
    logger.info("Adding documents to 'examples' collection...")
    try:
        vector_store.add_documents("examples", documents)
        logger.info("✓ Successfully ingested demoflow documents")
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return

    # Show stats
    stats = vector_store.get_collection_stats()
    logger.info(f"\nExamples collection now has {stats.get('examples', 0)} documents")
    logger.info("="*80)


if __name__ == "__main__":
    main()
