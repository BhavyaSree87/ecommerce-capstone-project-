import requests
base = 'http://127.0.0.1:8000'
print('health', requests.get(base + '/health').status_code)
payload = {
    'name': 'Swagger User',
    'email': 'swagger_user_test@example.com',
    'password': 'TestPass123!',
    'mobile': '9876543210',
    'address': '123 Test St',
    'city': 'Hyderabad',
    'state': 'TS',
    'pincode': '500001'
}
register = requests.post(base + '/api/auth/register', json=payload, timeout=10)
print('register', register.status_code, register.text)
if register.status_code == 201:
    token_resp = requests.post(base + '/api/auth/token', data={'username': payload['email'], 'password': payload['password']}, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
    print('token', token_resp.status_code, token_resp.text)
else:
    token_resp = requests.post(base + '/api/auth/token', data={'username': payload['email'], 'password': payload['password']}, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
    print('token', token_resp.status_code, token_resp.text)
