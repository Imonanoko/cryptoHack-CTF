from pwn import *
import json
from Crypto.Util.number import inverse
import fastecdsa
from fastecdsa.point import Point
from fastecdsa.curve import P256
# Because the public key is computed as Q = d * G in the elliptic curve group,
#we can recover G by computing G = d⁻¹ * Q, where d⁻¹ is the modular inverse of d modulo q, the order of the group.
G = P256.G
q = P256.q
print(q)
public_key = Point(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A, curve=P256)
d = 2
d_inv = inverse(d, q)
print(d_inv*d % q)
fake_gen = d_inv*public_key

# conn = remote("socket.cryptohack.org", 13382)
# register = {
#     "host": "www.bing.com",
#     "private_key": d,
#     "curve": "secp256r1",
#     "generator": [fake_gen.x, fake_gen.y]
# }
# _ = conn.recvline()
# conn.sendline(json.dumps(register).encode())
# data = conn.recvline().decode()
# print(data)
# conn.close()
# print(conn.recvline())
