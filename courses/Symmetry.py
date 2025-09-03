import requests
def xor(a, b):
    return bytes([a ^ b for a, b in zip(a, b)])

ciphertext = "56c8c960fed2ffe06a85f2a7298df75a9092ddfc84e1072284c8209d52d5777cb370ab06d74d53f981852bde2d44879cce"
iv = ciphertext[:32]
c = ciphertext[32:]
zero_plaintext = "00" * (len(c) // 2)
# print(iv)
print(len(c))
url = f"https://aes.cryptohack.org/symmetry/encrypt/{zero_plaintext}/{iv}/"
response = requests.get(url)
keystream = response.json()['ciphertext']
flag_bytes = xor(bytes.fromhex(keystream), bytes.fromhex(c))
print("FLAG:", flag_bytes.decode())