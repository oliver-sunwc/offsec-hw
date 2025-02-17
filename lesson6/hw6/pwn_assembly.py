from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-f", "-h"]
context.arch = "amd64"

CHALLENGE = "assembly"
PORT = 1292
NETID = b"os2178"
LOCAL = True
if LOCAL:
    e = ELF("./assembly", checksec=False)
    p = gdb.debug("./assembly")
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)
