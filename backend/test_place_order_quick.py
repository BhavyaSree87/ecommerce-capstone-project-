"""Quick E2E test: register temporary user and place a valid COD order."""
import requests, time, json
BASE_URL = "http://127.0.0.1:8000"
unique = int(time.time()*1000) % 1000000
reg = {
    "name": "E2E Test",
    "email": f"e2e_test_{unique}@example.com",
    "password": "E2ETest@123",
    "mobile": "9999999999",
    "address": "1 Test St",
    "city": "Hyderabad",
    "state": "Telangana",
    "pincode": "500001"
}
print('Registering test user...')
r = requests.post(f"{BASE_URL}/api/auth/register", json=reg)
print('Register status:', r.status_code)
print('Register body:', r.text)
if r.status_code != 201:
    raise SystemExit('Registration failed')
token = r.json()['access_token']
headers = { 'Authorization': f"Bearer {token}", 'Content-Type': 'application/json' }
payload = {
    "items": [{"product_id":1, "quantity":1, "price":299.99}],
    "shipping_address": "Test User, 1 Test St, Hyderabad, Telangana 500001, 9999999999",
    "billing_address": "Test User, 1 Test St, Hyderabad, Telangana 500001, 9999999999",
    "payment_method": "COD",
    "notes": None
}
print('\nPlacing order...')
resp = requests.post(f"{BASE_URL}/api/orders/create", json=payload, headers=headers)
print('Order status:', resp.status_code)
print('Order body:', resp.text)
