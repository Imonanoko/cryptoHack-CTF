from Crypto.Cipher import AES
import hashlib

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}

ciphertext_hex = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"

with open("words") as f:
    for line in f:
        word = line.strip()
        key_bytes = hashlib.md5(word.encode()).digest()
        key_hex = key_bytes.hex()
        
        result = decrypt(ciphertext_hex, key_hex)

        if "plaintext" in result:
            try:
                flag = bytes.fromhex(result["plaintext"]).decode()
                if flag.startswith("crypto"):
                    print(f"[+] Found! Password: {word}")
                    print(f"[+] Flag: {flag}")
                    break
            except UnicodeDecodeError:
                continue
        