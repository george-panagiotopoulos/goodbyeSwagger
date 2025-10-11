#!/usr/bin/env python3
"""Test RAG API with debugging"""

import requests
import json

url = "http://localhost:6603/api/chat"
payload = {
    "message": "give me a curl command to open an account in your localhost",
    "persona_id": "api_consumer"
}

print("="*80)
print("Testing API Consumer Persona with Debugging")
print("="*80)
print(f"\nQuery: {payload['message']}\n")

response = requests.post(url, json=payload)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    print("Full JSON Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
