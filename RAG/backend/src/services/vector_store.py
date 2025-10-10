"""ChromaDB vector store service"""
import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from src.config import settings
from src.models.document import Document
from src.services.embeddings import get_embedding_service

logger = logging.getLogger(__name__)


# Knowledge vector collection names
KNOWLEDGE_COLLECTIONS = [
    "architecture_knowledge",
    "api_knowledge",
    "business_knowledge",
    "developer_knowledge",
    "devops_knowledge",
    "data_knowledge",
    "code_examples_knowledge",
    "domain_knowledge",
]


class VectorStore:
    """Service for managing ChromaDB vector database"""

    def __init__(self):
        """Initialize ChromaDB client"""
        logger.info(f"Initializing ChromaDB at: {settings.chroma_path}")

        # Create ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        self.embedding_service = get_embedding_service()
        logger.info("VectorStore initialized successfully")

    def get_or_create_collection(self, collection_name: str):
        """
        Get existing collection or create new one

        Args:
            collection_name: Name of the collection

        Returns:
            ChromaDB collection
        """
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Collection '{collection_name}' ready (count: {collection.count()})")
            return collection
        except Exception as e:
            logger.error(f"Error getting/creating collection '{collection_name}': {e}")
            raise

    def add_documents(self, collection_name: str, documents: List[Document]) -> None:
        """
        Add documents to a collection

        Args:
            collection_name: Name of the collection
            documents: List of documents to add
        """
        if not documents:
            logger.warning(f"No documents to add to collection '{collection_name}'")
            return

        collection = self.get_or_create_collection(collection_name)

        # Extract data for ChromaDB
        ids = [doc.id for doc in documents]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # Generate embeddings
        logger.info(f"Generating embeddings for {len(documents)} documents...")
        embeddings = self.embedding_service.generate_embeddings(texts)

        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        logger.info(f"Added {len(documents)} documents to collection '{collection_name}'")

    def search(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents in a collection

        Args:
            collection_name: Name of the collection
            query: Query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of search results with documents and metadata
        """
        try:
            collection = self.get_or_create_collection(collection_name)

            # Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(query)

            # Search
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )

            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                })

            logger.debug(f"Found {len(formatted_results)} results in '{collection_name}'")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching collection '{collection_name}': {e}")
            return []

    def multi_collection_search(
        self,
        collections: List[str],
        query: str,
        n_results_per_collection: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search across multiple collections

        Args:
            collections: List of collection names to search
            query: Query text
            n_results_per_collection: Number of results per collection

        Returns:
            Combined and sorted list of results
        """
        all_results = []

        for collection_name in collections:
            results = self.search(collection_name, query, n_results_per_collection)
            for result in results:
                result['collection'] = collection_name
                all_results.append(result)

        # Sort by relevance score
        all_results.sort(key=lambda x: x['relevance_score'], reverse=True)

        logger.info(f"Multi-collection search returned {len(all_results)} total results")
        return all_results

    def get_collection_stats(self) -> Dict[str, int]:
        """
        Get document counts for all collections

        Returns:
            Dictionary mapping collection names to document counts
        """
        stats = {}
        for collection_name in KNOWLEDGE_COLLECTIONS:
            try:
                collection = self.client.get_collection(collection_name)
                stats[collection_name] = collection.count()
            except Exception:
                stats[collection_name] = 0

        return stats

    def reset_collection(self, collection_name: str) -> None:
        """
        Delete and recreate a collection

        Args:
            collection_name: Name of the collection to reset
        """
        try:
            self.client.delete_collection(collection_name)
            logger.info(f"Deleted collection '{collection_name}'")
        except Exception:
            logger.warning(f"Collection '{collection_name}' does not exist")

        self.get_or_create_collection(collection_name)
        logger.info(f"Reset collection '{collection_name}'")


# Singleton instance
_vector_store = None


def get_vector_store() -> VectorStore:
    """Get singleton VectorStore instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
