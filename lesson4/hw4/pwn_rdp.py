from pwn import *

#context.log_level = "DEBUG"

CHALLENGE = "rdp"
PORT = 1272
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

connect_packet = b'\x03' + b'\x01' + b'\x00'
print(connect_packet)

p.interactive()