import urllib.request, json, traceback
url='http://127.0.0.1:8000/api/auth/register'
data={
  'name':'Debug User',
  'email':'debuguser+1@example.com',
  'password':'TestPass123!',
  'mobile':'9876543210',
  'address':'123 Debug St',
  'city':'Hyderabad',
  'state':'TS',
  'pincode':'500001'
}
req=urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req) as r:
        print('STATUS', r.status)
        print(r.read().decode())
except Exception as e:
    print('CLIENT ERROR', e)
    traceback.print_exc()
