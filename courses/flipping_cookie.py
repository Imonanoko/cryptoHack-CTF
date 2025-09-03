cookie = "d63073c282929c4d61be580875fa645e6486b4ef16329965fcb9de6bd2013b27aa92867baf137e8635e3814f01f9322e"
before = b"admin=False;expi"
after = b"admin=True;expir"
iv = cookie[:32]
print(cookie[32:])
ivbytes = bytes.fromhex(iv)
def xor(a, b):
    return bytes([a ^ b for a, b in zip(a, b)])

c1 = xor(before, ivbytes)
c2 = xor(after, c1)
print(c2.hex())