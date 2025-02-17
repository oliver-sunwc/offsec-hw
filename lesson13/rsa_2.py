import math
import gmpy2
import binascii
from pwn import *

context.log_level = "DEBUG"

CHALLENGE = "rsa_2"
PORT = 1516
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

p.recvuntil(b"e1 = ")
e1 = p.recvuntil(b"\n")
#convert e from raw into int
e1 = int(e1.decode().strip())
print("e1 = ", e1)
p.recvuntil(b"n1 = ")
n1 = p.recvuntil(b"\n")
#convert n from raw into int
n1 = int(n1.decode().strip())
print("n1 = ", n1)
p.recvuntil(b"c1 = ")
c1 = p.recvuntil(b"\n")
#convert c from raw into int
c1 = int(c1.decode().strip())
print("c1 = ", c1)

p.recvuntil(b"e2 = ")
e2 = p.recvuntil(b"\n")
#convert e from raw into int
e2 = int(e2.decode().strip())
print("e2 = ", e2)
p.recvuntil(b"n2 = ")
n2 = p.recvuntil(b"\n")
#convert n from raw into int
n2 = int(n2.decode().strip())
print("n2 = ", n2)
p.recvuntil(b"c2 = ")
c2 = p.recvuntil(b"\n")
#convert c from raw into int
c2 = int(c2.decode().strip())
print("c2 = ", c2)

print("n1 = n2? ", n1==n2)

print("gcd of e1 and e2? ", math.gcd(e1, e2))

m = (pow(c1, 32641, n1) * pow(c2, -128, n2)) % n1
print("m = ", m)
print(binascii.unhexlify(hex(m)[2:]))

p.interactive()