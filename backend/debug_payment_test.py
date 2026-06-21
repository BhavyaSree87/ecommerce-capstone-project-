import requests
url = 'http://127.0.0.1:8000/api/auth/token'
payload = {'username':'debuguser1@example.com','password':'DebugPass123!'}
login = requests.post(url, data=payload)
print('LOGIN', login.status_code)
if login.ok:
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    create_url = 'http://127.0.0.1:8000/api/payments/razorpay/create-order'
    body = {'amount': 10.0, 'currency': 'INR', 'receipt': 'test_receipt_123', 'notes': {'test': 'yes'}}
    res = requests.post(create_url, json=body, headers=headers)
    print('CREATE ORDER', res.status_code)
    print(res.text)
else:
    print(login.text)
