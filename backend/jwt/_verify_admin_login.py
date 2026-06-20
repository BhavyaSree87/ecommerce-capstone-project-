import requests
import json

BASE_URL = "http://127.0.0.1:8000"

email = "admin_jwt_test@example.com"
password = "Admin@123"

print(f"Testing login for: {email}")
print(f"Password: {password}")
print()

# Test 1: Login endpoint
print("=== Test 1: /api/auth/login ===")
login_data = {
    "email": email,
    "password": password
}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    token = response.json().get("access_token")
    print(f"\n✅ LOGIN SUCCESSFUL")
    print(f"Token: {token[:50]}...")
    
    # Test 2: Use token to access protected endpoint
    print("\n=== Test 2: Access protected endpoint with token ===")
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = requests.get(f"{BASE_URL}/api/users/{response.json().get('user_id')}", headers=headers)
    print(f"Status: {protected_response.status_code}")
    print(f"Response: {json.dumps(protected_response.json(), indent=2)}")
else:
    print(f"\n❌ LOGIN FAILED")
