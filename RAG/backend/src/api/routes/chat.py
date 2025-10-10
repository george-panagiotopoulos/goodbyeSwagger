"""Chat API routes"""
from fastapi import APIRouter, HTTPException
from src.models.chat import ChatRequest, ChatResponse, ErrorResponse
from src.services.persona_manager import get_persona_manager
from src.services.chat import get_chat_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get a response from the specified persona
    """
    try:
        # Validate persona
        persona_manager = get_persona_manager()
        persona = persona_manager.get_persona(request.persona_id)

        if not persona:
            available = ", ".join(persona_manager.get_persona_ids())
            raise HTTPException(
                status_code=400,
                detail=f"Invalid persona_id '{request.persona_id}'. Available: {available}"
            )

        # Generate response
        chat_service = get_chat_service()
        response = chat_service.generate_response(
            persona=persona,
            user_message=request.message,
            conversation_history=request.conversation_history
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
