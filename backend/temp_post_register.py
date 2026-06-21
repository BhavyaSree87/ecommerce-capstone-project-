import urllib.request, json, sys
url='http://127.0.0.1:8000/api/auth/register'
data={
  'name':'RazorTest User',
  'email':'razor_test_user@example.com',
  'password':'TestPass123',
  'mobile':'9876543210',
  'address':'123 Test St',
  'city':'Hyderabad',
  'state':'Telangana',
  'pincode':'500001'
}
req=urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('STATUS', r.status)
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print('HTTPERR', e.code)
    try:
        print(e.read().decode())
    except:
        pass
except Exception as e:
    print('ERR', e)
    sys.exit(1)
