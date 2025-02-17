from pwn import *

context.log_level = "DEBUG"

CHALLENGE = "back_to_glibc"
PORT = 1292
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

p.interactive()