from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sage.all import *
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
    
# p = 1331169830894825846283645180581
# a = -35
# b = 98
# E = EllipticCurve(GF(p), [a,b])
# x = 479691812266187139164535778017
# y = 568535594075310466177352868412
# G = E(x, y)
# P1 = E(1110072782478160369250829345256, 800079550745409318906383650948)
# P2 = E(1290982289093010194550717223760,762857612860564354370535420319)
# encrypto_flag = {'iv': 'eac58c26203c04f68d63dc2c58d79aca', 'encrypted_flag': 'bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'}
# iv = encrypto_flag['iv']
# ciphertext = encrypto_flag['encrypted_flag']
# q = G.order()
# # print(factor(q)) # 2 * 7 * 271 * 23687 * 1153763334005213
# n_a = discrete_log(P2, G, operation='+')
# print(n_a)
# S = n_a * P1
# shared_secret = S.xy()[0]
# print(shared_secret)
# print(decrypt_flag(shared_secret, iv, ciphertext))


p  = 1331169830894825846283645180581
a, b = -35, 98
E1 = EllipticCurve(GF(p), [a, b])

G1 = E1((479691812266187139164535778017,
         568535594075310466177352868412))
P1 = E1((1110072782478160369250829345256,
         800079550745409318906383650948))
R1 = E1((1290982289093010194550717223760,
         762857612860564354370535420319))      # Bob 公鑰

q  = G1.order()             # 1036869… (76 bit, 已知因數)
k  = 2                      # 因為 pow(p,2,q) == 1

# -- 1.  φ :  F_p → F_{p^k}  -------------------------------------------------
Fp  = GF(p)
Fpk = GF(p**k, name='v')

# Fp → Fpk 的嵌入（挑任意共軛根即可）
phi = Fp.hom(Fp.gen().minpoly().roots(Fpk)[0][0], Fpk)

E2  = EllipticCurve(Fpk, [a, b])
G2  = E2(phi(G1.xy()[0]), phi(G1.xy()[1]))
P2  = E2(phi(P1.xy()[0]), phi(P1.xy()[1]))
R2  = E2(phi(R1.xy()[0]), phi(R1.xy()[1]))

h = ZZ(E1.order() // q)          # 只算一次 cofactor

while True:
    R  = E2.random_point()
    Q  = h * R                   # 階 | q
    if Q.is_zero() or Q == G2:
        continue                 # 0 點或同線丟掉
    if Q.order() != q:           # 不是「整階」q，換下一個
        continue
    g = G2.weil_pairing(Q, q)    # 現在肯定合法
    if g != 1:                   # 非退化 ⇒ G2, Q 線性獨立
        break

beta = P2.weil_pairing(Q, q)
n_A  = beta.log(g, ord=q, factor=factor(q))

# -- 4.  Pohlig–Hellman (利用 q 的質因數分解) -------------------------------
n_A = beta.log(alpha, ord=q, factor=factor(q))
print(f"Alice private key  n_A = {n_A}")

# -- 5.  共用祕鑰，AES 解密 --------------------------------------------------
iv_hex = 'eac58c26203c04f68d63dc2c58d79aca'
ct_hex = 'bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'
shared = int((n_A * R1).xy()[0])          # n_A * BobPub 仍在 E(F_p)
print(f"shared: {shared}")
print(f"flag: {decrypt_flag(shared, iv_hex, ct_hex)}")
key     = hashlib.sha1(str(shared).encode()).digest()[:16]

iv = bytes.fromhex(iv_hex)
ct = bytes.fromhex(ct_hex)
pt = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16)
print(pt.decode())                                    # => crypto{MOV_attack_turns_ecdlp_into_easy_dlp!}


