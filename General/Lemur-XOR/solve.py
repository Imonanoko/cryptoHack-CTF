from PIL import Image

# 開啟兩張圖
img1 = Image.open("flag.png").convert("RGB")
img2 = Image.open("lemur.png").convert("RGB")

# 確保大小一致
if img1.size != img2.size:
    raise ValueError("圖片大小不同，無法逐像素 XOR")

# 取出像素 bytes
bytes1 = img1.tobytes()
bytes2 = img2.tobytes()

# XOR 每個 byte
xor_bytes = bytes(a ^ b for a, b in zip(bytes1, bytes2))

# 轉回新圖
out = Image.frombytes("RGB", img1.size, xor_bytes)
out.save("xor_result.png")
print("輸出完成: xor_result.png")
