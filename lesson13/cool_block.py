from pwn import *

BLOCK_SIZE = 16

def oracle(iv, ciphertext):
    iv = iv.hex()
    ciphertext = ciphertext.hex()
    p.sendline(iv + ciphertext)
    response = p.recvline()
    if b"bad" not in response:
        p.recvuntil(b"message!\n")
        return True
    else:
        p.recvuntil(b"message!\n")
        return False
    
def single_block(block, oracle):
    zero_iv = [0]*BLOCK_SIZE

    for pad_val in range(1, BLOCK_SIZE + 1):
        pad_iv = [pad_val ^ b for b in zero_iv]
        for i in range(256):
            pad_iv[-pad_val] = i
            iv = bytes(pad_iv)
            if oracle(iv, block):
                if pad_val == 1:
                    pad_iv[-2] ^= 1
                    iv = bytes(pad_iv)
                    if not oracle(iv, block):
                        continue
                break
        else:
            raise Exception("no valid padding byte found")
        
        zero_iv[-pad_val] = i ^ pad_val

    print(zero_iv)
    return zero_iv

def attack(iv, ct, oracle):
    assert len(iv) == BLOCK_SIZE and len(ct) % BLOCK_SIZE == 0

    msg = iv + ct
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    result = b''

    iv = blocks[0]
    for ct in blocks[1:]:
        dec = single_block(ct, oracle)
        pt = bytes(iv_byte ^ dec_byte for iv_byte, dec_byte in zip(iv, dec))
        result += pt
        print(result)
        iv = ct
    return result

CHALLENGE = "cool_block"
PORT = 1512
NETID = b"os2178"
LOCAL = False
if LOCAL:
    p = process(CHALLENGE)
else:
    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", PORT)
    p.recvuntil(b"NetID (something like abc123): ")
    p.sendline(NETID)



p.recvuntil(b"IV = ")
iv = p.recvuntil(b"\n").decode().strip()
p.recvuntil(b"Ciphertext = ")
ciphertext = p.recvuntil(b"\n").decode().strip()
print("Ciphertext = " + ciphertext)
print("IV = " + iv)
print(type(iv))

print(p.recvuntil(b"message!\n").strip())

print("ATTACK")
print(attack(bytes.fromhex(iv), bytes.fromhex(ciphertext), oracle))



print("CHECK START")

p.interactive()

#iv and ciphertext are hex strings padded to length 16 with the 0x omitted


