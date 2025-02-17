from pwn import *

context.log_level = "DEBUG"

CHALLENGE = "ez_target"
PORT = 1203
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

p.recvuntil(b"me?\n")

p.interactive()

