from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sympy import sqrt_mod


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
# E: y^2 = x^3 + ax + b
# P = [x1, y1]
# Q = [x2, y2]
def addition(P:list,Q:list,a:int,p:int):
    if P == None:
        return Q
    elif Q == None:
        return P
    if P[0] ==Q[0] and (P[1] + Q[1]) % p == 0:
        return None
    else:
        lambda_ = None
        if P == Q:
            lambda_ = ((3 * P[0] * P[0] + a) * pow(2 * P[1],-1,p) )%p
        else:
            lambda_ = ((Q[1] - P[1]) * pow(Q[0] - P[0],-1,p)) % p
        x3 = lambda_ * lambda_ - P[0] - Q[0]
        y3 = lambda_ * (P[0] - x3) - P[1]
        return [x3 % p, y3 % p]
def doubleAndAdd(P:list,n:int,a:int,p:int):
    assert n > 0
    Q = P
    R = None
    while n > 0:
        if n % 2 == 1:
            R = addition(R,Q,a,p)
        Q = addition(Q,Q,a,p)
        n = n//2    
    return R
def montgomeryBinary(P:list,k:int,a:int,p:int):
    k_bin = bin(k)[2:]
    R0,R1 = P,addition(P,P,a,p)
    for bit in k_bin[1:]:
        if bit == '0':
           R0,R1 = addition(R0,R0,a,p),addition(R0,R1,a,p)
        else:
            R0,R1 = addition(R0,R1,a,p),addition(R1,R1,a,p)
    return R0
     
a = 497
b = 1768
p = 9739
G = [1804,5368]

# add test
# P=[493,5564]
# Q=[1539,4742]
# R=[4403,5202]
# two_p = addition(P,P,a,p)
# two_p_add_q = addition(two_p,Q,a,p)
# S = addition(two_p_add_q,R,a,p)
# print(S) #[4215, 2162]

#double and add test
# X = [5323,5438]
# assert [1089,6931] == doubleAndAdd(X,1337,a,p)

# P = [2339,2213]
# Q = doubleAndAdd(P,7863,a,p)
# print(Q) #[9467, 2742]

# key exchange
# QA = [815,3190]
# nb=1829
# secret_key = doubleAndAdd(QA,nb,a,p)
# x = secret_key[0]
# x_str = str(x)
# x_bytes = x_str.encode()
# digest = hashlib.sha1(x_bytes).hexdigest()
# print(digest)

# iv = "cd9da9f1c60925922377ea952afc212c"
# encrypted_flag = "febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8"
# QA_x = 4726
# nb = 6534

# y = (QA_x**3 + a*QA_x + b) % p
# y_values = sqrt_mod(y, p, all_roots=True)
# QA1 = [QA_x,y_values[0]]
# QA2 = [QA_x,y_values[1]]
# skey1 = doubleAndAdd(QA1,nb,a,p)[0]
# skey2 = doubleAndAdd(QA2,nb,a,p)[0]
# print(skey1,skey2)
# print(decrypt_flag(skey1,iv,encrypted_flag))
# print(decrypt_flag(skey2,iv,encrypted_flag))