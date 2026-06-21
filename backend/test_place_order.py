"""Test script to trace Place Order request payload and response."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Login first to get a token
login_data = {
    "email": "debuguser+2@example.com",
    "password": "Debug@123"
}

print("Step 1: Logging in...")
login_res = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Login status: {login_res.status_code}")
if login_res.status_code == 200:
    token = login_res.json()["access_token"]
    print(f"Token obtained: {token[:50]}...")
else:
    print(f"Login failed: {login_res.text}")
    exit(1)

# Now try to place an order with Cash On Delivery
print("\nStep 2: Attempting Place Order with COD...")

# This is the payload structure from frontend's createOrderPayload()
order_payload = {
    "items": [
        {
            "product_id": 1,
            "quantity": 1,
            "price": 299.99
        }
    ],
    "shipping_address": "123 Main St, Hyderabad, TS 500001, 9876543210",
    "billing_address": "123 Main St, Hyderabad, TS 500001, 9876543210",
    "payment_method": "COD",  # Frontend maps "Cash On Delivery" to "COD"
    "notes": None
}

print(f"Payload being sent:\n{json.dumps(order_payload, indent=2)}")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

res = requests.post(f"{BASE_URL}/api/orders/create", json=order_payload, headers=headers)
print(f"\nResponse status: {res.status_code}")
print(f"Response body: {res.text}")

if res.status_code != 200 and res.status_code != 201:
    print("\n❌ ERROR: Place Order failed!")
    try:
        error_detail = res.json()
        print(f"Error detail: {json.dumps(error_detail, indent=2)}")
    except:
        pass
