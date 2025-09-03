from pwn import *
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
import hashlib

def sha1(data):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(data)
        return sha1_hash.digest()
conn = remote("socket.cryptohack.org", 13381)
conn.recvline()

send_data = {
    "option": "sign_time",
    "msg": "unlock",
    "r": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "s": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
conn.sendline(json.dumps(send_data).encode())
data = json.loads(conn.recvline())
msg = data["msg"]
n = int(msg.split(":")[-1])
h = bytes_to_long(sha1(msg.encode()))
r = int(data["r"], 16)
s = int(data["s"],16)
print(f"n={n}, h={h}, r={r}, s={s}")
target_msg = "unlock"
target_h = bytes_to_long(sha1(target_msg.encode()))
g = generator_192
q = g.order()
send_data = {
    "option": "verify",
    "msg": target_msg,
    "r": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "s": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
for k in range(1, n):
    r_inv = inverse(r, q)
    d = ((k * s - h) * r_inv) % q

    pubkey = Public_key(g, g * d)
    privkey = Private_key(pubkey, d)
    sig = privkey.sign(target_h, k)

    send_data["r"] = hex(sig.r)
    send_data["s"] = hex(sig.s)
    conn.sendline(json.dumps(send_data).encode())
    result = json.loads(conn.recvline())
    print(f"Trying k={k}, result={result}")

    if 'flag' in result.keys():
        print(f"[+] Success! d = {hex(d)}")
        break
conn.close()