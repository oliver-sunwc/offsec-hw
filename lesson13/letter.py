import ctypes
import time
from pwn import *

context.log_level = "DEBUG"
libc = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")

# Define the time function
libc.time.argtypes = [ctypes.POINTER(ctypes.c_long)]  # time returns a long
libc.srand.argtypes = [ctypes.c_uint]  # srand takes an unsigned int

# Call time(NULL) to get the current time
current_time = ctypes.c_long()
libc.time(ctypes.byref(current_time))
# Seed the random number generator with the current time
libc.srand(ctypes.c_uint(current_time.value + 0x19))
# rand returns an int
libc.rand.restype = ctypes.c_int
random1 = libc.rand()
print("Random number 1 from Python: ", random1)

CHALLENGE = "./super_secure_letter"
PORT = 1517
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)

p.interactive()