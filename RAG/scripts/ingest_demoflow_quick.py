#!/usr/bin/env python3
"""Quick ingestion of demoflow documents directly"""
import sys
from pathlib import Path

# Add RAG backend to path
sys.path.insert(0, str(Path(__file__).parent / "RAG/backend"))

from src.utils.document_loader import load_documents_from_directory
from src.services.vector_store import get_vector_store

def main():
    print("="*80)
    print("Ingesting demoflow documents into vector database")
    print("="*80)

    # Path to demoflow
    demoflow_path = Path(__file__).parent / "Accounts/docs/examples/demoflow"

    if not demoflow_path.exists():
        print(f"ERROR: Demoflow path not found: {demoflow_path}")
        return

    print(f"\nLoading documents from: {demoflow_path}")

    # Load documents
    documents = load_documents_from_directory(
        directory=demoflow_path,
        chunk_size=2000,  # Larger chunks for complete examples
        chunk_overlap=300
    )

    print(f"Loaded {len(documents)} document chunks")

    if not documents:
        print("No documents found!")
        return

    # Show what we're ingesting
    for doc in documents:
        print(f"  - {doc.metadata.get('source')} (chunk {doc.metadata.get('chunk_index')}): {len(doc.content)} chars")

    # Get vector store
    print("\nInitializing vector store...")
    vector_store = get_vector_store()

    # Add to examples collection
    print("\nAdding documents to 'examples' collection...")
    vector_store.add_documents("examples", documents)

    print("✓ Successfully ingested demoflow documents")

    # Show stats
    stats = vector_store.get_collection_stats()
    print(f"\nCollection stats:")
    for collection, count in stats.items():
        print(f"  {collection}: {count} documents")

    print("\n" + "="*80)
    print("Ingestion complete!")
    print("="*80)

if __name__ == "__main__":
    main()
