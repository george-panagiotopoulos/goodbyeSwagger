#!/usr/bin/env python3
"""Quick test of RAG system"""
import requests
import json

API_BASE = "http://localhost:6603/api"

print("=" * 80)
print("RAG System Test")
print("=" * 80)

# Test 1: Health check
print("\n1. Health Check...")
response = requests.get(f"{API_BASE}/health")
health = response.json()
print(f"   Status: {health['status']}")
print(f"   Total Documents: {health['vector_store']['total_documents']}")

# Test 2: List personas
print("\n2. List Personas...")
response = requests.get(f"{API_BASE}/personas")
personas = response.json()
print(f"   Found {len(personas)} personas:")
for p in personas:
    print(f"   - {p['avatar']} {p['name']}: {p['description'][:50]}...")

# Test 3: Chat (with empty knowledge base)
print("\n3. Test Chat (Note: knowledge base may be empty)...")
chat_request = {
    "persona_id": "general",
    "message": "Hello! Can you tell me what you can help me with?",
    "conversation_history": []
}

response = requests.post(
    f"{API_BASE}/chat",
    headers={"Content-Type": "application/json"},
    json=chat_request
)

if response.status_code == 200:
    chat_response = response.json()
    print(f"   Persona: {chat_response['persona_id']}")
    print(f"   Response: {chat_response['message'][:200]}...")
    print(f"   Sources: {len(chat_response['sources'])} documents")
else:
    print(f"   Error: {response.status_code}")
    print(f"   {response.text}")

print("\n" + "=" * 80)
print("Test Complete!")
print("=" * 80)
print("\nNext Steps:")
print("1. Complete document ingestion: cd RAG && source backend/.venv/bin/activate && python3 scripts/ingest_documents.py")
print("2. Open UI: http://localhost:6604")
print("3. Try API Docs: http://localhost:6603/api/docs")
print("=" * 80)
