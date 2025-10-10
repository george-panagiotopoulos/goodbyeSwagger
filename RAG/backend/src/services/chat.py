"""Chat service with RAG"""
import logging
from typing import List, Dict, Any
from openai import AzureOpenAI
from src.config import settings
from src.models.chat import ChatMessage, ChatResponse, SourceDocument
from src.models.persona import Persona
from src.services.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class ChatService:
    """Service for RAG-based chat using Azure OpenAI"""

    def __init__(self):
        """Initialize Azure OpenAI client"""
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.deployment = settings.azure_openai_deployment_name
        self.vector_store = get_vector_store()
        logger.info(f"Initialized ChatService with deployment: {self.deployment}")

    def generate_response(
        self,
        persona: Persona,
        user_message: str,
        conversation_history: List[ChatMessage]
    ) -> ChatResponse:
        """
        Generate a chat response using RAG

        Args:
            persona: Persona configuration
            user_message: User's message
            conversation_history: Previous messages in conversation

        Returns:
            ChatResponse with answer and sources
        """
        try:
            # 1. Retrieve relevant context from knowledge vectors
            context_docs = self._retrieve_context(persona, user_message)

            # 2. Build prompt with context
            messages = self._build_messages(
                persona,
                user_message,
                conversation_history,
                context_docs
            )

            # 3. Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=persona.temperature,
                max_tokens=persona.max_tokens,
                top_p=persona.top_p
            )

            assistant_message = response.choices[0].message.content

            # 4. Format sources
            sources = self._format_sources(context_docs)

            logger.info(f"Generated response for persona '{persona.id}' ({len(assistant_message)} chars)")

            return ChatResponse(
                persona_id=persona.id,
                message=assistant_message,
                sources=sources
            )

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise

    def _retrieve_context(
        self,
        persona: Persona,
        query: str,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from persona's knowledge vectors

        Args:
            persona: Persona configuration
            query: User query
            max_results: Maximum results to return

        Returns:
            List of relevant documents
        """
        # Get collections for this persona
        collections = [kv.collection for kv in persona.knowledge_vectors]

        # Search across multiple collections
        results = self.vector_store.multi_collection_search(
            collections=collections,
            query=query,
            n_results_per_collection=2  # Get top 2 from each collection
        )

        # Apply persona weights and re-rank
        weighted_results = []
        for result in results:
            # Find weight for this collection
            weight = 1.0
            for kv in persona.knowledge_vectors:
                if kv.collection == result.get('collection'):
                    weight = kv.weight
                    break

            result['weighted_score'] = result['relevance_score'] * weight
            weighted_results.append(result)

        # Sort by weighted score and take top results
        weighted_results.sort(key=lambda x: x['weighted_score'], reverse=True)
        top_results = weighted_results[:max_results]

        logger.info(f"Retrieved {len(top_results)} context documents for query")
        return top_results

    def _build_messages(
        self,
        persona: Persona,
        user_message: str,
        conversation_history: List[ChatMessage],
        context_docs: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Build messages array for Azure OpenAI API

        Args:
            persona: Persona configuration
            user_message: Current user message
            conversation_history: Previous messages
            context_docs: Retrieved context documents

        Returns:
            List of message dictionaries
        """
        messages = []

        # System prompt with context
        context_text = self._format_context(context_docs)
        system_prompt = f"""{persona.system_prompt}

CONTEXT INFORMATION:
You have access to the following relevant documentation:

{context_text}

Use this context to answer the user's question accurately. If the context doesn't contain enough information, say so honestly."""

        messages.append({
            "role": "system",
            "content": system_prompt
        })

        # Add conversation history (limited to avoid token limits)
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages

    def _format_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """
        Format context documents into a string

        Args:
            context_docs: List of context documents

        Returns:
            Formatted context string
        """
        if not context_docs:
            return "No specific context available for this query."

        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            source = doc.get('metadata', {}).get('source', 'unknown')
            content = doc.get('document', '')
            score = doc.get('weighted_score', 0.0)

            context_parts.append(
                f"[Document {i}] (Source: {source}, Relevance: {score:.2f})\n{content}\n"
            )

        return "\n---\n".join(context_parts)

    def _format_sources(self, context_docs: List[Dict[str, Any]]) -> List[SourceDocument]:
        """
        Format context documents as SourceDocument objects

        Args:
            context_docs: List of context documents

        Returns:
            List of SourceDocument objects
        """
        sources = []
        for doc in context_docs[:3]:  # Top 3 sources
            sources.append(SourceDocument(
                content=doc.get('document', '')[:200] + "...",  # First 200 chars
                source=doc.get('metadata', {}).get('source', 'unknown'),
                relevance_score=doc.get('weighted_score', 0.0)
            ))

        return sources


# Singleton instance
_chat_service = None


def get_chat_service() -> ChatService:
    """Get singleton ChatService instance"""
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service
