import requests

# Login first
r = requests.post('http://127.0.0.1:5000/api/v1/auth/login', json={
    'email': 'test@example.com',
    'password': 'password123'
})
print('Login status:', r.status_code)
print('Login response:', r.json())

token = r.json().get('token')
if token:
    headers = {'Authorization': f'Bearer {token}'}
    r2 = requests.get('http://127.0.0.1:5000/api/v1/dashboard/summary', headers=headers)
    print('Dashboard status:', r2.status_code)
    print('Dashboard text:', r2.text)
