#!/usr/bin/env python3
"""
Account Processing System API Demonstration Flow

This script demonstrates a complete workflow using the Accounts API:
1. Authenticate with the system
2. Create a new customer
3. Create an account for the customer
4. Process 5 transactions (debits and credits)
5. Retrieve customer details
6. Retrieve transaction list

All requests and responses are logged to flowoutput.txt
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional


class APIFlowDemo:
    def __init__(self, base_url: str = "http://localhost:6600"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.log_file = "flowoutput.txt"
        self.session_data = {
            "customer_id": None,
            "account_id": None,
            "transaction_ids": []
        }

        # Initialize log file
        with open(self.log_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("Account Processing System - API Flow Demonstration\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Base URL: {base_url}\n")
            f.write("="*80 + "\n\n")

    def log_request(self, method: str, url: str, headers: Dict, body: Optional[Dict] = None):
        """Log HTTP request details"""
        with open(self.log_file, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"REQUEST: {method} {url}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Headers:\n")
            for key, value in headers.items():
                # Mask token for security in logs
                if key.lower() == 'authorization' and 'Bearer' in value:
                    f.write(f"  {key}: Bearer <token>\n")
                else:
                    f.write(f"  {key}: {value}\n")
            if body:
                f.write(f"\nBody:\n")
                f.write(json.dumps(body, indent=2))
            f.write("\n")

    def log_response(self, status_code: int, response_data: Any, description: str = ""):
        """Log HTTP response details"""
        with open(self.log_file, 'a') as f:
            f.write(f"\nRESPONSE: {status_code}\n")
            f.write(f"{'-'*80}\n")
            if description:
                f.write(f"Description: {description}\n\n")
            if isinstance(response_data, dict) or isinstance(response_data, list):
                f.write(json.dumps(response_data, indent=2))
            else:
                f.write(str(response_data))
            f.write("\n")

    def log_step(self, step_number: int, step_title: str):
        """Log a step in the flow"""
        with open(self.log_file, 'a') as f:
            f.write(f"\n\n{'#'*80}\n")
            f.write(f"# STEP {step_number}: {step_title}\n")
            f.write(f"{'#'*80}\n")

    def get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get HTTP headers for requests"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def step1_login(self):
        """Step 1: Authenticate with the API"""
        self.log_step(1, "Authentication - Login")

        url = f"{self.base_url}/api/auth/login"
        body = {
            "username": "demo_user",
            "password": "demo_pass123"
        }
        headers = self.get_headers(include_auth=False)

        self.log_request("POST", url, headers, body)

        response = requests.post(url, json=body, headers=headers)
        response_data = response.json() if response.text else {}

        self.log_response(response.status_code, response_data,
                         "Authenticate and obtain JWT token")

        if response.status_code == 200:
            self.token = response_data.get('token')
            print(f"✓ Step 1: Successfully logged in as {body['username']}")
            return True
        else:
            print(f"✗ Step 1: Login failed with status {response.status_code}")
            return False

    def step2_create_customer(self):
        """Step 2: Create a new customer"""
        self.log_step(2, "Create Customer")

        url = f"{self.base_url}/api/customers"
        body = {
            "customer_name": "John Demo Customer",
            "customer_type": "Individual",
            "external_customer_id": f"EXT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "email": "john.demo@example.com",
            "phone": "+1-555-0123"
        }
        headers = self.get_headers()

        self.log_request("POST", url, headers, body)

        response = requests.post(url, json=body, headers=headers)
        response_data = response.json() if response.text else {}

        self.log_response(response.status_code, response_data,
                         "Create a new individual customer in the system")

        if response.status_code == 201:
            self.session_data['customer_id'] = response_data['data']['customer_id']
            print(f"✓ Step 2: Created customer {self.session_data['customer_id']}")
            return True
        else:
            print(f"✗ Step 2: Failed to create customer - status {response.status_code}")
            return False

    def step3_create_account(self):
        """Step 3: Create an account for the customer"""
        self.log_step(3, "Create Account")

        # First, get available products
        url = f"{self.base_url}/api/products"
        headers = self.get_headers()

        self.log_request("GET", url, headers)
        response = requests.get(url, headers=headers)
        products = response.json() if response.text else {}
        self.log_response(response.status_code, products,
                         "Retrieve available products to select one for the account")

        if response.status_code != 200 or not products.get('data'):
            print(f"✗ Step 3: Failed to retrieve products")
            return False

        # Use the first savings product
        product_id = None
        for product in products['data']:
            if 'savings' in product.get('product_name', '').lower():
                product_id = product['product_id']
                break

        if not product_id and products['data']:
            product_id = products['data'][0]['product_id']

        # Now create the account
        url = f"{self.base_url}/api/accounts"
        body = {
            "customer_id": self.session_data['customer_id'],
            "product_id": product_id,
            "opening_balance": "1000.00"
        }

        self.log_request("POST", url, headers, body)

        response = requests.post(url, json=body, headers=headers)
        response_data = response.json() if response.text else {}

        self.log_response(response.status_code, response_data,
                         "Create a new account for the customer with an opening balance")

        if response.status_code == 201:
            self.session_data['account_id'] = response_data['data']['account_id']
            print(f"✓ Step 3: Created account {self.session_data['account_id']}")
            return True
        else:
            print(f"✗ Step 3: Failed to create account - status {response.status_code}")
            return False

    def step4_process_transactions(self):
        """Step 4: Process 5 transactions (mix of debits and credits)"""
        self.log_step(4, "Process Transactions")

        transactions = [
            {
                "type": "credit",
                "amount": "500.00",
                "description": "Salary deposit",
                "reference": "SAL-001"
            },
            {
                "type": "debit",
                "amount": "150.00",
                "description": "Utility payment",
                "reference": "UTIL-001"
            },
            {
                "type": "credit",
                "amount": "250.00",
                "description": "Bonus payment",
                "reference": "BONUS-001"
            },
            {
                "type": "debit",
                "amount": "75.50",
                "description": "Restaurant payment",
                "reference": "REST-001"
            },
            {
                "type": "credit",
                "amount": "100.00",
                "description": "Refund received",
                "reference": "REF-001"
            }
        ]

        headers = self.get_headers()
        success_count = 0

        for i, txn in enumerate(transactions, 1):
            txn_type = txn.pop('type')
            url = f"{self.base_url}/api/accounts/{self.session_data['account_id']}/{txn_type}"

            self.log_request("POST", url, headers, txn)

            response = requests.post(url, json=txn, headers=headers)
            response_data = response.json() if response.text else {}

            self.log_response(response.status_code, response_data,
                             f"Process {txn_type} transaction #{i}")

            if response.status_code in [200, 201]:
                # Extract transaction ID if available
                if 'data' in response_data and 'transaction_id' in response_data['data']:
                    self.session_data['transaction_ids'].append(
                        response_data['data']['transaction_id']
                    )
                success_count += 1
                print(f"  ✓ Transaction {i}: {txn_type.upper()} ${txn['amount']}")
            else:
                print(f"  ✗ Transaction {i}: Failed - status {response.status_code}")

        print(f"✓ Step 4: Processed {success_count}/{len(transactions)} transactions")
        return success_count > 0

    def step5_get_customer_details(self):
        """Step 5: Retrieve customer details"""
        self.log_step(5, "Retrieve Customer Details")

        url = f"{self.base_url}/api/customers/{self.session_data['customer_id']}"
        headers = self.get_headers()

        self.log_request("GET", url, headers)

        response = requests.get(url, headers=headers)
        response_data = response.json() if response.text else {}

        self.log_response(response.status_code, response_data,
                         "Retrieve the customer details including contact information")

        if response.status_code == 200:
            print(f"✓ Step 5: Retrieved customer details")
            return True
        else:
            print(f"✗ Step 5: Failed to retrieve customer - status {response.status_code}")
            return False

    def step6_get_transactions(self):
        """Step 6: Retrieve account transaction history"""
        self.log_step(6, "Retrieve Transaction History")

        url = f"{self.base_url}/api/accounts/{self.session_data['account_id']}/transactions"
        headers = self.get_headers()

        self.log_request("GET", url, headers)

        response = requests.get(url, headers=headers)
        response_data = response.json() if response.text else {}

        self.log_response(response.status_code, response_data,
                         "Retrieve complete transaction history for the account")

        if response.status_code == 200:
            txn_count = len(response_data.get('data', []))
            print(f"✓ Step 6: Retrieved {txn_count} transactions")
            return True
        else:
            print(f"✗ Step 6: Failed to retrieve transactions - status {response.status_code}")
            return False

    def run_complete_flow(self):
        """Execute the complete API demonstration flow"""
        print("\n" + "="*80)
        print("Account Processing System - API Flow Demonstration")
        print("="*80 + "\n")

        steps = [
            ("Authentication", self.step1_login),
            ("Create Customer", self.step2_create_customer),
            ("Create Account", self.step3_create_account),
            ("Process Transactions", self.step4_process_transactions),
            ("Get Customer Details", self.step5_get_customer_details),
            ("Get Transaction History", self.step6_get_transactions)
        ]

        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n⚠ Flow stopped at: {step_name}")
                    break
            except Exception as e:
                print(f"\n✗ Error in {step_name}: {str(e)}")
                break
        else:
            print("\n" + "="*80)
            print("✓ Complete flow executed successfully!")
            print("="*80)

        print(f"\nAll requests and responses logged to: {self.log_file}\n")

        # Write summary
        with open(self.log_file, 'a') as f:
            f.write(f"\n\n{'#'*80}\n")
            f.write("# FLOW SUMMARY\n")
            f.write(f"{'#'*80}\n")
            f.write(f"Customer ID: {self.session_data['customer_id']}\n")
            f.write(f"Account ID: {self.session_data['account_id']}\n")
            f.write(f"Transactions Processed: {len(self.session_data['transaction_ids'])}\n")
            f.write(f"Completion Time: {datetime.now().isoformat()}\n")


def main():
    """Main entry point"""
    demo = APIFlowDemo()
    demo.run_complete_flow()


if __name__ == "__main__":
    main()
