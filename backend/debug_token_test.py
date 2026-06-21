import requests
url = 'http://127.0.0.1:8000/api/auth/token'
payload = {'username':'debuguser1@example.com','password':'DebugPass123!','grant_type':'password'}
r = requests.post(url, data=payload)
print('STATUS', r.status_code)
print('CONTENT-TYPE', r.headers.get('content-type'))
print(r.text)
