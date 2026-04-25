import requests, sys

urls = [
    'https://nutricoach-ai.onrender.com/',
    'https://nutricoach.onrender.com/',
    'https://nutri-coach-ai.onrender.com/',
]

for url in urls:
    try:
        r = requests.get(url, timeout=15)
        print(f'{url} -> Status: {r.status_code}, Content-Type: {r.headers.get("Content-Type")}, Length: {len(r.text)}')
        if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
            print(f'  -> LIVE: {url}')
            sys.exit(0)
    except Exception as e:
        print(f'{url} -> Error: {e}')

print('No live deployment found at expected URLs.')
