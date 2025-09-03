from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import inverse
import math
import hashlib
from sage.all import *
def extract_json_from_prefixed_line(line: bytes):
    text = line.decode().strip()
    while not text.strip().startswith("{"):
        text = text.split(":", 1)[1].strip()
    return json.loads(text)
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

# import shelve
# def discrete_log_disk(g, A, p):
#     m = int(math.isqrt(p)) + 1
#     with shelve.open("bsgs_table.db") as table:
#         e = 1
#         for j in range(m):
#             table[str(e)] = j
#             e = (e * g) % p

#         factor = pow(inverse(g, p), m, p)
#         e = A
#         for i in range(m):
#             if str(e) in table:
#                 return i * m + table[str(e)]
#             e = (e * factor) % p
#     raise ValueError("log not found")
conn = remote("socket.cryptohack.org",13379)
alice_data = extract_json_from_prefixed_line(conn.recvline())
supported ="DH64"
alice_data["supported"] = [supported]
# print(f"Supported: {supported}")
conn.sendline(json.dumps(alice_data).encode())

bob_data = extract_json_from_prefixed_line(conn.recvline())
chosen = bob_data["chosen"]
# print(f"Chosen: {chosen}")
conn.sendline(json.dumps(bob_data).encode())

response = extract_json_from_prefixed_line(conn.recvline())
p = int(response["p"], 16)
g = int(response["g"], 16)
A = int(response["A"], 16)
# print(f"p = {p}")
# print(f"g = {g}")
# print(f"A = {A}")
response = extract_json_from_prefixed_line(conn.recvline())
B = int(response["B"], 16)
# print(f"B = {B}")
response = extract_json_from_prefixed_line(conn.recvline())
iv = response["iv"]
ciphertext = response["encrypted_flag"]
conn.close()
# print(f"IV: {iv}")
# print(f"Encrypted flag: {ciphertext}")
F = GF(p)
g, A = F(g), F(A)
a = discrete_log(A, g)
shared_secret = pow(B, int(a), p)
flag = decrypt_flag(shared_secret, iv, ciphertext)
print(f"FLAG: {flag}")