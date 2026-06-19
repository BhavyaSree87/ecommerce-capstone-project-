import json
import urllib.request
import urllib.parse
from app.database.db import get_connection
from app.utils.password import hash_password

BASE = 'http://127.0.0.1:8000'

conn = get_connection()
cur = conn.cursor()
try:
    cur.execute("SELECT ID, EMAIL FROM USERS WHERE ROLE='ADMIN'")
    row = cur.fetchone()
    if row:
        admin_id, admin_email = row
    else:
        cur.execute("SELECT USERS_SEQ.NEXTVAL FROM DUAL")
        admin_id = cur.fetchone()[0]
        admin_email = f"admin_{admin_id}@example.com"
        cur.execute(
            "INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE) VALUES (:id,:name,:email,:pwd,:role,:mobile,:addr,:city,:state,:pin)",
            {
                'id': admin_id,
                'name': 'Admin User',
                'email': admin_email,
                'pwd': hash_password('Admin123!'),
                'role': 'ADMIN',
                'mobile': '9999999999',
                'addr': 'Admin HQ',
                'city': 'City',
                'state': 'ST',
                'pin': '000000'
            }
        )
        conn.commit()
finally:
    cur.close()
    conn.close()

print('admin_email', admin_email)

form_data = urllib.parse.urlencode({'username': admin_email, 'password': 'Admin123!'}).encode('utf-8')
req = urllib.request.Request(f'{BASE}/api/auth/token', data=form_data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
with urllib.request.urlopen(req, timeout=10) as r:
    token_resp = json.load(r)
print('token_resp', token_resp)

token = token_resp['access_token']
print('token len', len(token))

payload = {
    'product_name': 'Swagger Test',
    'price': 1.23,
    'description': 'Test Generated Product',
    'category': 'Test',
    'brand': 'Test',
    'stock': 10,
    'image_url': '',
    'rating': 4.2
}
req = urllib.request.Request(f'{BASE}/api/products/add', data=json.dumps(payload).encode('utf-8'), method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization', f'Bearer {token}')
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        resp_body = r.read().decode('utf-8')
        print('add status', r.status)
        print('add resp', resp_body)
except urllib.error.HTTPError as e:
    print('add failed', e.code, e.read().decode())
