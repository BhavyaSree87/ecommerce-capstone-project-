import json
import urllib.request
import urllib.parse

BASE = 'http://127.0.0.1:8000'

print('Fetching OpenAPI schema...')
with urllib.request.urlopen(f'{BASE}/openapi.json') as response:
    spec = json.load(response)

print('securitySchemes:', json.dumps(spec.get('components', {}).get('securitySchemes'), indent=2))
print('global security:', json.dumps(spec.get('security'), indent=2))
print('login op present:', '/api/auth/login' in spec['paths'])
print('token op present:', '/api/auth/token' in spec['paths'])
print('product add security:', json.dumps(spec['paths']['/api/products/add'].get('security'), indent=2))

# Validate token endpoint with existing admin user
# This assumes admin user is known or can be created manually.

# Example admin credentials (update if necessary)
admin_email = 'admin@gmail.com'
admin_password = 'Admin123!'

form_data = urllib.parse.urlencode({'username': admin_email, 'password': admin_password}).encode('utf-8')
req = urllib.request.Request(f'{BASE}/api/auth/token', data=form_data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    with urllib.request.urlopen(req, timeout=10) as r:
        token_resp = json.load(r)
    print('token response:', json.dumps(token_resp, indent=2))
    token = token_resp['access_token']

    product_payload = {
        'product_name': 'Swagger Test',
        'price': 1.23,
        'description': 'Test Generated Product',
        'category': 'Test',
        'brand': 'Test',
        'stock': 10,
        'image_url': '',
        'rating': 4.2
    }
    product_req = urllib.request.Request(f'{BASE}/api/products/add', data=json.dumps(product_payload).encode('utf-8'), method='POST')
    product_req.add_header('Content-Type', 'application/json')
    product_req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(product_req, timeout=10) as resp:
        print('product add status:', resp.status)
        print('product add resp:', resp.read().decode())
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print('HTTPError', e.code, body)
except Exception as e:
    print('Exception', type(e), e)
