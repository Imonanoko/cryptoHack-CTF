import requests
from Crypto.Util.strxor import strxor

c = "455916e902eae4df91d08c4f84e0ce99db3eeec5983ba3bfd6b9592f5de62613711be188ba2c83f1c634391478725994"
iv = bytes.fromhex(c[:32])
c1 = bytes.fromhex(c[32:64])
c2 = bytes.fromhex(c[64:96])

url = "https://aes.cryptohack.org/ecbcbcwtf/decrypt/"

d1_resp = requests.get(url + c1.hex() + "/").json()
d2_resp = requests.get(url + c2.hex() + "/").json()

d1 = bytes.fromhex(d1_resp["plaintext"])
d2 = bytes.fromhex(d2_resp["plaintext"])

p1 = strxor(d1, iv)
p2 = strxor(d2, c1)

flag = p1 + p2
print("FLAG:", flag.decode(errors="ignore"))
