import requests
def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])
url = f"https://aes.cryptohack.org/bean_counter/encrypt/"
response = requests.get(url)
data = response.json()['encrypted']
png_header = "89504e470d0a1a0a0000000d49484452"
keystream = xor(bytes.fromhex(data[:32]), bytes.fromhex(png_header))

plaintext = b""
for i in range(0, len(data), 32):  # 每次 32 hex chars = 16 bytes
    block = bytes.fromhex(data[i:i+32])
    decrypted = xor(block, keystream[:len(block)])
    plaintext += decrypted

# 5. 存成 PNG 檔案
with open("recovered.png", "wb") as f:
    f.write(plaintext)

print("✅ Done! 已寫入 recovered.png")