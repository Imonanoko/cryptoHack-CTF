from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


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


shared_secret = 560058414644632715934291436167799484533998332100036005861639378116940608154056613240668195731110477187464060874290998422176927077903593902549042623783123908894496642163287495003455467211073096340530132206308235157395216337415992480804505622898874287443544247817936469769676333354054319991501480472151767281145320754191442787036732973837033933177172716029384898073450370404080776959392241509921321220056231398886909551965191700606317454451980670802310165271913221
iv = "1c7cc00f580986ed4ec3ccdb3ebbbd67"
ciphertext = "29d6a552284c455be3b780c0b86817ee248ae134580832bc5fabd3884bcdf1d4"

print(decrypt_flag(shared_secret, iv, ciphertext))
