from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import getRandomRange
import hashlib


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


conn = remote("socket.cryptohack.org", 13371)

alice_data = extract_json_from_prefixed_line(conn.recvline())
p = int(alice_data["p"], 16)
g = int(alice_data["g"], 16)
A_original = int(alice_data["A"], 16)
fa = getRandomRange(2, p - 2)
FA=pow(g, fa, p)
alice_data["A"] = hex(FA)

conn.sendline(json.dumps(alice_data).encode())

bob_data = extract_json_from_prefixed_line(conn.recvline())
B_original = int(bob_data["B"], 16)
fb = getRandomRange(2, p - 2)
FB=pow(g, fb, p)
bob_data["B"] = hex(FB)

conn.sendline(json.dumps(bob_data).encode())

final = extract_json_from_prefixed_line(conn.recvline())
iv = final["iv"]
ciphertext = final["encrypted_flag"]
secret = pow(A_original, fb, p)
print(f"IV: {iv}")
print(f"Encrypted flag: {ciphertext}")

flag = decrypt_flag(secret, iv, ciphertext)
print(f"FLAG: {flag}")

conn.close()
