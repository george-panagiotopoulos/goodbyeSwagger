#!/usr/bin/env python3
"""
Document ingestion script
Loads documents from /docs directory and populates ChromaDB vector database
"""
import sys
import logging
from pathlib import Path

# Add backend src to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from src.config import settings
from src.utils.document_loader import load_documents_from_directory
from src.services.vector_store import get_vector_store, KNOWLEDGE_COLLECTIONS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main ingestion function"""
    logger.info("="*80)
    logger.info("RAG Document Ingestion")
    logger.info("="*80)

    # Get docs path
    docs_path = Path(settings.docs_absolute_path)
    logger.info(f"Docs directory: {docs_path}")

    if not docs_path.exists():
        logger.error(f"Docs directory does not exist: {docs_path}")
        logger.info("Please ensure the docs directory exists with documentation files")
        return

    # Load documents
    logger.info("Loading documents...")
    documents = load_documents_from_directory(
        directory=docs_path,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )

    if not documents:
        logger.warning("No documents found to ingest")
        return

    logger.info(f"Loaded {len(documents)} document chunks")

    # Group documents by category
    documents_by_category = {}
    for doc in documents:
        category = doc.metadata.get('category', 'developer_knowledge')
        if category not in documents_by_category:
            documents_by_category[category] = []
        documents_by_category[category].append(doc)

    logger.info("\nDocument distribution by category:")
    for category, docs in documents_by_category.items():
        logger.info(f"  {category}: {len(docs)} chunks")

    # Initialize vector store
    logger.info("\nInitializing vector store...")
    vector_store = get_vector_store()

    # Optionally reset collections
    reset = input("\nReset existing collections? (yes/no): ").lower()
    if reset in ['yes', 'y']:
        logger.info("Resetting collections...")
        for collection_name in KNOWLEDGE_COLLECTIONS:
            vector_store.reset_collection(collection_name)

    # Ingest documents
    logger.info("\nIngesting documents into ChromaDB...")
    for category, docs in documents_by_category.items():
        logger.info(f"Ingesting {len(docs)} documents into '{category}'...")
        try:
            vector_store.add_documents(category, docs)
            logger.info(f"  ✓ Successfully ingested into '{category}'")
        except Exception as e:
            logger.error(f"  ✗ Error ingesting into '{category}': {e}")

    # Show final stats
    logger.info("\n" + "="*80)
    logger.info("Ingestion Complete")
    logger.info("="*80)
    stats = vector_store.get_collection_stats()
    logger.info("\nFinal collection stats:")
    for collection, count in stats.items():
        logger.info(f"  {collection}: {count} documents")

    logger.info("\n" + "="*80)
    logger.info("RAG system is ready to use!")
    logger.info("="*80)


if __name__ == "__main__":
    main()
