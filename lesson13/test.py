import requests

payload = {'complaint': 'flag'}
r = requests.post('http://34.135.223.176:8449/complaint', json=payload)

print(r.text)