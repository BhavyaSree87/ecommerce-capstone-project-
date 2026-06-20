import json
import urllib.request
import urllib.error
from app.database.db import get_connection
from app.utils.password import hash_password, verify_password

BASE = 'http://127.0.0.1:8000'
ADMIN_EMAIL = 'admin_jwt_test@example.com'
ADMIN_PASSWORD = 'Admin123!'

# Ensure admin exists with known bcrypt hash
conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute("SELECT ID, EMAIL, PASSWORD FROM USERS WHERE EMAIL = :email", {'email': ADMIN_EMAIL})
    row = cursor.fetchone()
    if row:
        user_id, email, stored_hash = row
        try:
            if verify_password(ADMIN_PASSWORD, stored_hash):
                print('Admin exists with valid hash')
            else:
                print('Admin exists but password mismatch, updating hash')
                new_hash = hash_password(ADMIN_PASSWORD)
                cursor.execute("UPDATE USERS SET PASSWORD = :pwd, ROLE = 'ADMIN' WHERE ID = :id", {'pwd': new_hash, 'id': user_id})
                conn.commit()
        except Exception as e:
            print('Admin hash invalid, replacing with bcrypt hash', type(e), e)
            new_hash = hash_password(ADMIN_PASSWORD)
            cursor.execute("UPDATE USERS SET PASSWORD = :pwd, ROLE = 'ADMIN' WHERE ID = :id", {'pwd': new_hash, 'id': user_id})
            conn.commit()
    else:
        cursor.execute('SELECT USERS_SEQ.NEXTVAL FROM DUAL')
        user_id = cursor.fetchone()[0]
        new_hash = hash_password(ADMIN_PASSWORD)
        cursor.execute(
            "INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE) VALUES (:id, :name, :email, :pwd, 'ADMIN', :mobile, :addr, :city, :state, :pin)",
            {'id': user_id, 'name': 'Admin Test', 'email': ADMIN_EMAIL, 'pwd': new_hash, 'mobile': '9999999999', 'addr': 'Admin HQ', 'city': 'City', 'state': 'ST', 'pin': '000000'}
        )
        conn.commit()
        print('Inserted admin user', ADMIN_EMAIL)
finally:
    cursor.close()
    conn.close()

# Login via /api/auth/login
login_payload = json.dumps({'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}).encode('utf-8')
req = urllib.request.Request(f'{BASE}/api/auth/login', data=login_payload, method='POST')
req.add_header('Content-Type', 'application/json')
try:
    with urllib.request.urlopen(req) as r:
        login_resp = json.load(r)
    print('login success', login_resp['access_token'][:20], '...')
    token = login_resp['access_token']
except urllib.error.HTTPError as e:
    print('login error', e.code, e.read().decode())
    raise

# Use admin token against protected product add endpoint
product_payload = json.dumps({
    'product_name': 'Authorize Test Product',
    'price': 11.11,
    'description': 'Created in bearer auth test',
    'category': 'Test',
    'brand': 'Test',
    'stock': 5,
    'image_url': '',
    'rating': 4.5
}).encode('utf-8')
req = urllib.request.Request(f'{BASE}/api/products/add', data=product_payload, method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization', f'Bearer {token}')
try:
    with urllib.request.urlopen(req) as r:
        resp = r.read().decode('utf-8')
        print('product add status', r.status)
        print('product add response', resp)
except urllib.error.HTTPError as e:
    print('product add error', e.code, e.read().decode())
    raise

# Verify insertion with DB query
conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute("SELECT PRODUCT_ID, PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_NAME = :name", {'name': 'Authorize Test Product'})
    rows = cursor.fetchall()
    print('DB rows:', rows)
finally:
    cursor.close()
    conn.close()
