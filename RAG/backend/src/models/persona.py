"""Persona data models"""
from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum
import json
import os
from pathlib import Path


class KnowledgeVector(BaseModel):
    """Knowledge vector with weight for persona"""

    collection: str = Field(..., description="ChromaDB collection name")
    weight: float = Field(1.0, ge=0.0, le=1.0, description="Weight for this knowledge area")


class PersonaType(str, Enum):
    """Available persona types"""

    DEVELOPER = "developer"
    DEVOPS = "devops"
    BUSINESS = "business"
    API_CONSUMER = "api_consumer"
    ARCHITECT = "architect"
    DBA = "dba"
    GENERAL = "general"
    KID = "kid"


class Persona(BaseModel):
    """AI Assistant Persona configuration"""

    id: str = Field(..., description="Unique persona identifier")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Persona description")
    avatar: str = Field("🤖", description="Emoji avatar")
    knowledge_vectors: List[KnowledgeVector] = Field(..., description="Knowledge areas this persona can access")
    system_prompt: str = Field(..., description="System prompt for this persona")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="LLM temperature")
    max_tokens: int = Field(2000, ge=100, le=4000, description="Max response tokens")
    top_p: float = Field(0.95, ge=0.0, le=1.0, description="Top-p sampling")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "developer",
                "name": "Dev Assistant",
                "description": "Helps developers with setup, coding, and debugging",
                "avatar": "👨‍💻",
                "knowledge_vectors": [
                    {"collection": "developer_knowledge", "weight": 1.0},
                    {"collection": "architecture_knowledge", "weight": 0.8}
                ],
                "system_prompt": "You are a senior developer mentor...",
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 0.95
            }
        }


def load_system_prompts() -> Dict[str, Dict]:
    """Load system prompts from JSON file"""
    json_path = Path(__file__).parent.parent.parent / "system_prompts.json"
    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)
    return {}


def load_persona_mappings() -> Dict:
    """Load persona-vector mappings from JSON file"""
    json_path = Path(__file__).parent.parent.parent / "persona_vector_mapping.json"
    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)
    return {}


# Load prompts and mappings
SYSTEM_PROMPTS = load_system_prompts()
PERSONA_MAPPINGS = load_persona_mappings()


# Predefined personas (using JSON configuration)
PERSONAS: Dict[str, Persona] = {
    "developer": Persona(
        id="developer",
        name=SYSTEM_PROMPTS.get("developer", {}).get("name", "Dev Assistant"),
        description="Helps developers with setup, coding, debugging, and understanding the codebase",
        avatar="👨‍💻",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("developer", {}).get("knowledge_vectors", [
                {"collection": "user_guides", "weight": 0.9},
                {"collection": "api", "weight": 1.0},
                {"collection": "examples", "weight": 1.0},
                {"collection": "data_models", "weight": 0.8},
                {"collection": "architecture", "weight": 0.7},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("developer", {}).get("system_prompt", "You are a developer assistant."),
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95
    ),

    "devops": Persona(
        id="devops",
        name=SYSTEM_PROMPTS.get("devops", {}).get("name", "Ops Assistant"),
        description="Helps with deployment, infrastructure, database operations, and system administration",
        avatar="🔧",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("devops", {}).get("knowledge_vectors", [
                {"collection": "devops", "weight": 1.0},
                {"collection": "data_models", "weight": 0.9},
                {"collection": "user_guides", "weight": 0.7},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("devops", {}).get("system_prompt", "You are a DevOps assistant."),
        temperature=0.5,
        max_tokens=2000,
        top_p=0.95
    ),

    "business": Persona(
        id="business",
        name=SYSTEM_PROMPTS.get("business", {}).get("name", "Business Expert"),
        description="Explains business features, use cases, and product functionality from a user perspective",
        avatar="💼",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("business", {}).get("knowledge_vectors", [
                {"collection": "business", "weight": 1.0},
                {"collection": "user_guides", "weight": 0.9},
                {"collection": "api", "weight": 0.4},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("business", {}).get("system_prompt", "You are a business expert."),
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95
    ),

    "api_consumer": Persona(
        id="api_consumer",
        name=SYSTEM_PROMPTS.get("api_consumer", {}).get("name", "API Guide"),
        description="Helps external developers integrate with the REST API, with examples and best practices",
        avatar="🔌",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("api_consumer", {}).get("knowledge_vectors", [
                {"collection": "api", "weight": 1.0},
                {"collection": "examples", "weight": 1.0},
                {"collection": "user_guides", "weight": 0.6},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("api_consumer", {}).get("system_prompt", "You are an API guide."),
        temperature=0.6,
        max_tokens=2000,
        top_p=0.95
    ),

    "architect": Persona(
        id="architect",
        name=SYSTEM_PROMPTS.get("architect", {}).get("name", "Architecture Advisor"),
        description="Explains system architecture, design decisions, patterns, and technical trade-offs",
        avatar="🏛️",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("architect", {}).get("knowledge_vectors", [
                {"collection": "architecture", "weight": 1.0},
                {"collection": "data_models", "weight": 0.8},
                {"collection": "api", "weight": 0.7},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("architect", {}).get("system_prompt", "You are an architecture advisor."),
        temperature=0.6,
        max_tokens=2000,
        top_p=0.95
    ),

    "dba": Persona(
        id="dba",
        name=SYSTEM_PROMPTS.get("dba", {}).get("name", "Data Expert"),
        description="Helps with database schema, queries, migrations, and data integrity",
        avatar="🗄️",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("dba", {}).get("knowledge_vectors", [
                {"collection": "data_models", "weight": 1.0},
                {"collection": "devops", "weight": 0.7},
                {"collection": "api", "weight": 0.5},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("dba", {}).get("system_prompt", "You are a data expert."),
        temperature=0.5,
        max_tokens=2000,
        top_p=0.95
    ),

    "general": Persona(
        id="general",
        name=SYSTEM_PROMPTS.get("general", {}).get("name", "Universal Helper"),
        description="General assistant that can answer any question about the system",
        avatar="🤖",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("general", {}).get("knowledge_vectors", [
                {"collection": "user_guides", "weight": 0.8},
                {"collection": "api", "weight": 0.7},
                {"collection": "business", "weight": 0.7},
                {"collection": "architecture", "weight": 0.6},
                {"collection": "data_models", "weight": 0.6},
                {"collection": "devops", "weight": 0.6},
                {"collection": "examples", "weight": 0.5},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("general", {}).get("system_prompt", "You are a general assistant."),
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95
    ),

    "kid": Persona(
        id="kid",
        name=SYSTEM_PROMPTS.get("kid", {}).get("name", "Kid Explainer"),
        description="Explains technical concepts using toys, cartoons, and superheroes - fun for everyone!",
        avatar="🎮",
        knowledge_vectors=[
            KnowledgeVector(collection=v["collection"], weight=v["weight"])
            for v in PERSONA_MAPPINGS.get("personas", {}).get("kid", {}).get("knowledge_vectors", [
                {"collection": "user_guides", "weight": 0.9},
                {"collection": "business", "weight": 0.8},
                {"collection": "api", "weight": 0.7},
                {"collection": "architecture", "weight": 0.7},
                {"collection": "data_models", "weight": 0.6},
                {"collection": "examples", "weight": 0.6},
                {"collection": "devops", "weight": 0.5},
            ])
        ],
        system_prompt=SYSTEM_PROMPTS.get("kid", {}).get("system_prompt", "You are a kid explainer."),
        temperature=0.9,  # Higher temperature for more creative comparisons
        max_tokens=2500,  # More tokens for storytelling
        top_p=0.95
    ),
}
