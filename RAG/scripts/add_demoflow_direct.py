#!/usr/bin/env python3
"""
Directly add demoflow documents to vector database using correct collection names
"""
import sys
from pathlib import Path

# Add RAG backend to path
sys.path.insert(0, str(Path(__file__).parent / "RAG/backend"))

from src.models.document import Document
from datetime import datetime

def main():
    print("="*80)
    print("Adding demoflow documents to vector database")
    print("="*80)

    # Import here to avoid loading issues
    from src.services.vector_store import get_vector_store

    # Read the documents
    demoflow_path = Path(__file__).parent / "Accounts/docs/examples/demoflow"

    readme_path = demoflow_path / "README.md"
    flowoutput_path = demoflow_path / "flowoutput.txt"

    print(f"\nReading documents from: {demoflow_path}")

    # Read README
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Read flowoutput - split into chunks since it's large
    with open(flowoutput_path, 'r', encoding='utf-8') as f:
        flowoutput_content = f.read()

    # Create documents
    documents = []

    # README document
    documents.append(Document(
        id="demoflow_readme",
        content=readme_content,
        metadata={
            "source": "examples/demoflow/README.md",
            "category": "examples",
            "title": "API Flow Demonstration README",
            "created_at": datetime.now().isoformat(),
            "type": "documentation"
        }
    ))

    # Split flowoutput into meaningful chunks (by steps)
    flow_sections = flowoutput_content.split("################################################################################")

    for i, section in enumerate(flow_sections):
        if section.strip():
            documents.append(Document(
                id=f"demoflow_flowoutput_section_{i}",
                content=section.strip(),
                metadata={
                    "source": "examples/demoflow/flowoutput.txt",
                    "category": "examples",
                    "title": f"API Flow Output Section {i}",
                    "created_at": datetime.now().isoformat(),
                    "chunk_index": i,
                    "type": "api_example"
                }
            ))

    print(f"Created {len(documents)} document chunks")

    # Get vector store
    print("\nInitializing vector store...")
    vector_store = get_vector_store()

    # Add to "examples" collection (used by API consumer and developer personas)
    collection_name = "examples"
    print(f"\nAdding documents to '{collection_name}' collection...")

    try:
        vector_store.add_documents(collection_name, documents)
        print(f"✓ Successfully added {len(documents)} documents")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return

    # Show stats
    stats = vector_store.get_collection_stats()
    print(f"\nCollection stats after ingestion:")
    for collection, count in stats.items():
        if count > 0:
            print(f"  {collection}: {count} documents")

    print("\n" + "="*80)
    print("Ingestion complete! RAG can now provide curl examples.")
    print("="*80)

if __name__ == "__main__":
    main()
