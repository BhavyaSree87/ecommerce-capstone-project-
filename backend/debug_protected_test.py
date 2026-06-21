import requests
url = 'http://127.0.0.1:8000/api/auth/token'
payload = {'username':'debuguser1@example.com','password':'DebugPass123!','grant_type':'password'}
r = requests.post(url, data=payload)
print('TOKEN STATUS', r.status_code)
data = r.json()
print('TOKEN', data.get('access_token')[:20] + '...')
headers = {'Authorization': f"Bearer {data['access_token']}"}
user_id = data['user']['id']
protected = requests.get(f'http://127.0.0.1:8000/api/users/{user_id}', headers=headers)
print('PROTECTED STATUS', protected.status_code)
print(protected.text)
