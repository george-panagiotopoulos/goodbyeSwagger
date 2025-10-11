#!/usr/bin/env python3
"""Test that the curl command from RAG actually works"""

import requests

# Step 1: Login
response = requests.post('http://localhost:6600/api/auth/login', json={
    'username': 'demo_user',
    'password': 'demo_pass123'
})
print('Login Status:', response.status_code)
token = response.json().get('token')

# Step 2: Get products
response = requests.get('http://localhost:6600/api/products', headers={'Authorization': f'Bearer {token}'})
products = response.json()['data']
product_id = [p['product_id'] for p in products if 'Savings' in p['product_name']][0]

# Step 3: Create customer
response = requests.post('http://localhost:6600/api/customers',
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    json={'customer_name': 'RAG Test Customer', 'customer_type': 'Individual', 'email': 'rag@test.com'})
print('Create Customer Status:', response.status_code)
customer_id = response.json()['data']['customer_id']

# Step 4: Use the EXACT fields from RAG response (from demoflow)
response = requests.post('http://localhost:6600/api/accounts',
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    json={
        'customer_id': customer_id,
        'product_id': product_id,
        'opening_balance': '1000.00'  # This field name is from demoflow!
    })
print('Create Account Status:', response.status_code)
if response.status_code == 201:
    account = response.json()['data']
    print(f'Account created: {account["account_number"]}')
    print(f'Balance: ${account["balance"]}')
    print('\n✅ CURL COMMAND FROM RAG WORKS!')
else:
    print('Error:', response.text)
