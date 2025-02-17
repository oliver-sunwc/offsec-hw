from pwn import *
from decimal import Decimal, getcontext

CHALLENGE = "rsa_1"
PORT = 1515
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

getcontext().prec = 1000

p.recvuntil(b"e = ")
e = p.recvuntil(b"\n")
#convert e from raw into int
e = int(e.decode().strip())
print("e = ", e)
p.recvuntil(b"n = ")
n = p.recvuntil(b"\n")
#convert n from raw into int
n = int(n.decode().strip())
print("n = ", n)
p.recvuntil(b"c = ")
c = p.recvuntil(b"\n")
#convert c from raw into int
c = int(c.decode().strip())
print("c = ", c)

dc = Decimal(c)

m = dc ** (Decimal(1)/e)
m = int(m)

print("m = ", m)

# Calculate how many bytes are required
byte_length = (m.bit_length() + 7) // 8

# Convert the integer back to bytes (big-endian)
original_bytes = m.to_bytes(byte_length, 'big')

# Decode the bytes into a string
original_string = original_bytes.decode()

print(original_string)

p.interactive()