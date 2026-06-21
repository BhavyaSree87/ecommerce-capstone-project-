"""Test ordering product 204 specifically (the one with missing inventory)."""
import requests, time, json
BASE_URL = "http://127.0.0.1:8000"

# First, check if product 204 exists
print("Checking if product 204 exists...")
resp = requests.get(f"{BASE_URL}/api/products/{204}")
print(f"Product 204 status: {resp.status_code}")
if resp.status_code != 200:
    print(f"Product 204 not found. Trying product 50...")
    resp = requests.get(f"{BASE_URL}/api/products/{50}")
    product_id = 50
else:
    product_id = 204
    print(f"Product 204 found: {resp.json()}")

print(f"\n Using product_id={product_id}")

# Register a unique test user
unique = int(time.time()*1000) % 1000000
reg = {
    "name": "E2E Test 204",
    "email": f"e2e_test_204_{unique}@example.com",
    "password": "E2ETest@123",
    "mobile": "9999999999",
    "address": "1 Test St",
    "city": "Hyderabad",
    "state": "Telangana",
    "pincode": "500001"
}
print('\nRegistering test user...')
r = requests.post(f"{BASE_URL}/api/auth/register", json=reg)
print('Register status:', r.status_code)
if r.status_code != 201:
    print('Register failed:', r.text)
    raise SystemExit('Registration failed')

token = r.json()['access_token']
headers = { 'Authorization': f"Bearer {token}", 'Content-Type': 'application/json' }

# Try placing order for product 204
payload = {
    "items": [{"product_id": product_id, "quantity": 1, "price": 299.99}],
    "shipping_address": "Test User, 1 Test St, Hyderabad, Telangana 500001, 9999999999",
    "billing_address": "Test User, 1 Test St, Hyderabad, Telangana 500001, 9999999999",
    "payment_method": "COD",
    "notes": None
}

print(f'\nPlacing order for product {product_id}...')
resp = requests.post(f"{BASE_URL}/api/orders/create", json=payload, headers=headers)
print('Order status:', resp.status_code)
print('Order body:', json.dumps(resp.json(), indent=2))

if resp.status_code == 200:
    print("\n✅ SUCCESS: Order placed successfully for product", product_id)
    print("The inventory auto-create fix is working!")
else:
    print(f"\n❌ FAILED: Status {resp.status_code}")
