from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]
context.arch = "amd64"

e = ELF("./execve_shellcode", checksec=False)
p = gdb.debug("./execve_shellcode", '''
b *(main + 102)
continue
''')
p.recvuntil(b"exec!\n")

s = asm('''
mov rax, 0x0
''')

p.send(s)

p.interactive()