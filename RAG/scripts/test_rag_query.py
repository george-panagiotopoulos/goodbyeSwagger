#!/usr/bin/env python3
"""Test RAG API with a query about curl commands"""

import requests
import json

def test_api_consumer():
    """Test API consumer persona"""
    url = "http://localhost:6603/api/chat"
    payload = {
        "message": "give me a curl command to open an account in your localhost",
        "persona_id": "api_consumer"
    }

    print("="*80)
    print("Testing API Consumer Persona")
    print("="*80)
    print(f"\nQuery: {payload['message']}\n")

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Response:")
        print("-"*80)
        print(data.get('response', 'No response'))
        print("\n")
        print("="*80)
        return data.get('response', '')
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def test_developer():
    """Test developer persona"""
    url = "http://localhost:6603/api/chat"
    payload = {
        "message": "show me how to create a customer using curl on localhost",
        "persona_id": "developer"
    }

    print("="*80)
    print("Testing Developer Persona")
    print("="*80)
    print(f"\nQuery: {payload['message']}\n")

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Response:")
        print("-"*80)
        print(data.get('response', 'No response'))
        print("\n")
        print("="*80)
        return data.get('response', '')
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    # Test API consumer
    response1 = test_api_consumer()

    print("\n\n")

    # Test developer
    response2 = test_developer()
