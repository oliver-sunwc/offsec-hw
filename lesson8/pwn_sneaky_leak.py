from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]

CHALLENGE = "sneaky_leak"
PORT = 1210
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)


p.recvuntil(b'> ')

def sendindex(index):
    ind = b'' + str(index).encode()
    p.recvuntil(b'> ')
    p.sendline(ind)

def free(index):
    p.sendline(b'1')
    sendindex(index)
    p.recvuntil(b'> ')
    log.info(f"Freed buffer at index {index}")

def read(index):
    p.sendline(b'2')
    sendindex(index)
    p.recvuntil(b'data: ')
    return(p.recvuntil(b'\n'))


def alloc(index):
    p.sendline(b'3')
    sendindex(index)
    p.recvuntil(b'> ')
    log.info(f"Allocated buffer at index {index}")

p.interactive()
