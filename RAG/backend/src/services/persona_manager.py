"""Persona management service"""
import logging
from typing import Dict, List, Optional
from src.models.persona import Persona, PERSONAS

logger = logging.getLogger(__name__)


class PersonaManager:
    """Service for managing AI personas"""

    def __init__(self):
        """Initialize persona manager with predefined personas"""
        self.personas: Dict[str, Persona] = PERSONAS
        logger.info(f"Initialized PersonaManager with {len(self.personas)} personas")

    def get_persona(self, persona_id: str) -> Optional[Persona]:
        """
        Get a persona by ID

        Args:
            persona_id: Persona identifier

        Returns:
            Persona object or None if not found
        """
        persona = self.personas.get(persona_id)
        if persona:
            logger.debug(f"Retrieved persona: {persona_id}")
        else:
            logger.warning(f"Persona not found: {persona_id}")
        return persona

    def list_personas(self) -> List[Persona]:
        """
        Get all available personas

        Returns:
            List of all Persona objects
        """
        return list(self.personas.values())

    def get_persona_ids(self) -> List[str]:
        """
        Get list of all persona IDs

        Returns:
            List of persona IDs
        """
        return list(self.personas.keys())

    def persona_exists(self, persona_id: str) -> bool:
        """
        Check if a persona exists

        Args:
            persona_id: Persona identifier

        Returns:
            True if persona exists, False otherwise
        """
        return persona_id in self.personas


# Singleton instance
_persona_manager = None


def get_persona_manager() -> PersonaManager:
    """Get singleton PersonaManager instance"""
    global _persona_manager
    if _persona_manager is None:
        _persona_manager = PersonaManager()
    return _persona_manager
