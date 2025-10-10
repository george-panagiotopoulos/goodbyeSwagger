"""Persona API routes"""
from fastapi import APIRouter, HTTPException
from typing import List
from src.models.persona import Persona
from src.services.persona_manager import get_persona_manager

router = APIRouter(prefix="/personas", tags=["personas"])


@router.get("", response_model=List[Persona])
async def list_personas():
    """Get all available personas"""
    persona_manager = get_persona_manager()
    return persona_manager.list_personas()


@router.get("/{persona_id}", response_model=Persona)
async def get_persona(persona_id: str):
    """Get a specific persona by ID"""
    persona_manager = get_persona_manager()
    persona = persona_manager.get_persona(persona_id)

    if not persona:
        available = ", ".join(persona_manager.get_persona_ids())
        raise HTTPException(
            status_code=404,
            detail=f"Persona '{persona_id}' not found. Available: {available}"
        )

    return persona
