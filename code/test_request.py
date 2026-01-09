import requests

token = 'abcd1234'

data = requests.post(
    f'http://127.0.0.1:5000/{token}/settings',
)
print(data.json())