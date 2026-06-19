import json, urllib.request, urllib.error, traceback, time
from urllib.parse import urljoin
from app.database.db import get_connection
from app.utils.password import hash_password
from app.utils.jwt_handler import create_access_token

BASE = "http://127.0.0.1:8000"
REPORT = []


def http_request(path, method='GET', data=None, headers=None):
    url = urljoin(BASE, path)
    bdata = None
    if data is not None:
        bdata = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=bdata, method=method)
    req.add_header('Content-Type', 'application/json')
    if headers:
        for k,v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode()
            try:
                body_json = json.loads(body)
            except Exception:
                body_json = body
            return r.status, body_json
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            body_json = json.loads(body)
        except Exception:
            body_json = body
        return e.code, body_json
    except Exception as e:
        return 0, str(e)


def record(endpoint, req_body, status, resp):
    REPORT.append({
        'endpoint': endpoint,
        'request': req_body,
        'status': status,
        'response': resp,
        'pass': 200 <= status < 300
    })


# Helpers

def ensure_product_exists():
    # try to get products
    status, resp = http_request('/api/products/all')
    if status == 200 and isinstance(resp, dict) and resp.get('items'):
        items = resp.get('items')
        return items[0]
    # otherwise insert a product directly via DB
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PRODUCT_SEQ.NEXTVAL FROM DUAL")
        pid = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) VALUES (:id, :name, :price, :description, :category, :brand, :stock, :image_url, :rating)",
            {"id": pid, "name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": "", "rating": 4.5}
        )
        conn.commit()
        return {"product_id": pid, "product_name": "Test Product", "price": 9.99}
    finally:
        cursor.close()
        conn.close()


def ensure_admin_user():
    # check if any admin exists
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID, EMAIL FROM USERS WHERE ROLE='ADMIN'")
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        # create admin user
        cursor.execute("SELECT USERS_SEQ.NEXTVAL FROM DUAL")
        uid = cursor.fetchone()[0]
        pwd = hash_password('AdminPass123!')
        cursor.execute("INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE) VALUES (:id, :name, :email, :pwd, :role, :mobile, :addr, :city, :state, :pin)",
                       {"id": uid, "name": "Admin User", "email": f"admin_{int(time.time())}@example.com", "pwd": pwd, "role": 'ADMIN', "mobile": '9999999999', "addr": 'Admin HQ', "city": 'City', "state": 'ST', "pin": '000000'})
        conn.commit()
        return uid, f"admin_{int(time.time())}@example.com"
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    timestamp = int(time.time())
    test_email = f"apitest_{timestamp}@example.com"
    test_password = "TestPass123!"

    # 1. Register
    reg_payload = {
        "name": "API Test User",
        "email": test_email,
        "password": test_password,
        "mobile": "9876543210",
        "address": "123 Test St",
        "city": "Hyderabad",
        "state": "TS",
        "pincode": "500001"
    }
    status, resp = http_request('/api/auth/register', method='POST', data=reg_payload)
    record('/api/auth/register', reg_payload, status, resp)

    # If registration failed due to duplicate or server error, try to login with existing
    token = None
    user_id = None
    if status == 201 and isinstance(resp, dict):
        token = resp.get('access_token')
        user = resp.get('user')
        if user:
            user_id = user.get('id')
    else:
        # try login
        login_payload = {"email": test_email, "password": test_password}
        status2, resp2 = http_request('/api/auth/login', method='POST', data=login_payload)
        record('/api/auth/login_attempt', login_payload, status2, resp2)
        if status2 == 200 and isinstance(resp2, dict):
            token = resp2.get('access_token')
            user = resp2.get('user')
            if user:
                user_id = user.get('id')

    # 2. Login (if not yet executed)
    if not token:
        login_payload = {"email": test_email, "password": test_password}
        status, resp = http_request('/api/auth/login', method='POST', data=login_payload)
        record('/api/auth/login', login_payload, status, resp)
        if status == 200 and isinstance(resp, dict):
            token = resp.get('access_token')
            user = resp.get('user')
            if user:
                user_id = user.get('id')

    # 3. Profile
    if user_id and token:
        headers = {"Authorization": f"Bearer {token}"}
        status, resp = http_request(f'/api/users/{user_id}', method='GET', headers=headers)
        record(f'/api/users/{user_id}', 'GET with auth', status, resp)
    else:
        record('/api/users/{id}', 'skipped', 0, 'No user id/token available')

    # 4. Products
    status, resp = http_request('/api/products/all')
    record('/api/products/all', 'GET', status, resp)

    prod = None
    if status == 200 and isinstance(resp, dict) and resp.get('items'):
        prod = resp['items'][0]
    else:
        prod = ensure_product_exists()
        record('product_insert', 'inserted via DB', 201, prod)

    # Product detail
    if prod:
        pid = prod.get('product_id') or prod.get('PRODUCT_ID') or prod.get('id')
        status, resp = http_request(f'/api/products/{pid}')
        record(f'/api/products/{pid}', 'GET', status, resp)
    
    # 5. Cart
    if token and prod:
        headers = {"Authorization": f"Bearer {token}"}
        cart_payload = {"product_id": pid, "quantity": 1}
        status, resp = http_request('/api/cart/add', method='POST', data=cart_payload, headers=headers)
        record('/api/cart/add', cart_payload, status, resp)

        # get cart
        status, resp = http_request('/api/cart/', method='GET', headers=headers)
        record('/api/cart/', 'GET', status, resp)

        # delete a cart item if exists
        if status == 200 and isinstance(resp, list) and resp:
            cart_id = resp[0][0] if isinstance(resp[0], (list, tuple)) else resp[0].get('CART_ID')
            status, resp = http_request(f'/api/cart/delete/{cart_id}', method='DELETE', headers=headers)
            record(f'/api/cart/delete/{cart_id}', 'DELETE', status, resp)
    else:
        record('/api/cart', 'skipped', 0, 'No token or product')

    # 6. Wishlist
    if token and prod:
        headers = {"Authorization": f"Bearer {token}"}
        wl_payload = {"product_id": pid}
        status, resp = http_request('/api/wishlist/add', method='POST', data=wl_payload, headers=headers)
        record('/api/wishlist/add', wl_payload, status, resp)

        status, resp = http_request('/api/wishlist/', method='GET', headers=headers)
        record('/api/wishlist/', 'GET', status, resp)

        if status == 200 and isinstance(resp, list) and resp:
            wl_id = resp[0][0] if isinstance(resp[0], (list, tuple)) else resp[0].get('WISHLIST_ID')
            status, resp = http_request(f'/api/wishlist/delete/{wl_id}', method='DELETE', headers=headers)
            record(f'/api/wishlist/delete/{wl_id}', 'DELETE', status, resp)
    else:
        record('/api/wishlist', 'skipped', 0, 'No token or product')

    # 7. Orders
    order_id = None
    if token and prod:
        headers = {"Authorization": f"Bearer {token}"}
        # place order
        order_payload = {
            "items": [{"product_id": pid, "quantity": 1, "price": float(prod.get('price') or prod.get('PRICE') or 9.99)}],
            "shipping_address": "123 Test St",
            "billing_address": "123 Test St",
            "payment_method": "Test",
            "notes": ""
        }
        status, resp = http_request('/api/orders/create', method='POST', data=order_payload, headers=headers)
        record('/api/orders/create', order_payload, status, resp)
        if status == 200 or status == 201:
            order_id = resp.get('order_id')

        # get user orders
        status, resp = http_request(f'/api/orders/user/{user_id}', method='GET', headers=headers)
        record(f'/api/orders/user/{user_id}', 'GET', status, resp)
    else:
        record('/api/orders', 'skipped', 0, 'No token or product')

    # 8. Payments
    pay_id = None
    if token and order_id:
        headers = {"Authorization": f"Bearer {token}"}
        pay_payload = {"order_id": order_id, "payment_method": "Test", "payment_status": "PAID", "amount": 9.99}
        status, resp = http_request('/api/payments/pay', method='POST', data=pay_payload, headers=headers)
        record('/api/payments/pay', pay_payload, status, resp)
        if status == 200 or status == 201:
            pay_id = resp.get('payment_id')

        status, resp = http_request(f'/api/payments/order/{order_id}', method='GET', headers=headers)
        record(f'/api/payments/order/{order_id}', 'GET', status, resp)
    else:
        record('/api/payments', 'skipped', 0, 'No token or order')

    # 9. Dashboard (admin only) - ensure admin exists and get a token
    admin_uid, admin_email = ensure_admin_user()
    # create admin token
    admin_payload = {"user_id": admin_uid, "email": admin_email, "role": "ADMIN"}
    admin_token = create_access_token(admin_payload)
    headers = {"Authorization": f"Bearer {admin_token}"}
    status, resp = http_request('/api/dashboard/stats', method='GET', headers=headers)
    record('/api/dashboard/stats', 'GET as admin', status, resp)

    # Write report
    with open('TEST_REPORT.md', 'w', encoding='utf-8') as f:
        f.write('# API Test Report\n\n')
        pass_count = 0
        for r in REPORT:
            ok = r['pass']
            if ok:
                pass_count += 1
            f.write(f"- **Endpoint**: {r['endpoint']}\n")
            f.write(f"  - **Request**: {json.dumps(r['request'])}\n")
            f.write(f"  - **Status**: {r['status']}\n")
            f.write(f"  - **Response**: {json.dumps(r['response'])}\n")
            f.write(f"  - **Result**: {'PASS' if ok else 'FAIL'}\n\n")
        f.write(f"\nTotal: {len(REPORT)}, Passed: {pass_count}, Failed: {len(REPORT)-pass_count}\n")

    print('Test run complete. Report written to TEST_REPORT.md')
