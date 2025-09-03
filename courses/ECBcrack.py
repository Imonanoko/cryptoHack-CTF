import requests
import time
URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
BLOCK_SIZE = 16

def get_ciphertext(hex_input: str) -> str:
    url = f"https://aes.cryptohack.org/ecb_oracle/encrypt/{hex_input}/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # 若是 HTTP 錯誤會丟 exception

        data = response.json()
        return data["ciphertext"]

    except requests.exceptions.JSONDecodeError:
        print("[!] JSON 解碼錯誤，可能被 rate limit 或伺服器無回應，稍後重試")
        time.sleep(1)
        return get_ciphertext(hex_input)

    except Exception as e:
        print(f"[!] 發生錯誤：{e}")
        time.sleep(1)
        return get_ciphertext(hex_input)

def recover_flag():
    known_bytes = b"crypto{p3n6u1n5_"

    while True:
        pad_len = BLOCK_SIZE - (len(known_bytes) % BLOCK_SIZE) - 1
        prefix = b"A" * pad_len
        block_index = len(known_bytes) // BLOCK_SIZE

        # 真實密文（含 FLAG）對應區塊
        real_ciphertext = get_ciphertext(prefix.hex())
        target_block = real_ciphertext[block_index*32:(block_index+1)*32]

        found = False
        for b in range(256):
            guess = prefix + known_bytes + bytes([b])
            guess_ciphertext = get_ciphertext(guess.hex())
            guess_block = guess_ciphertext[block_index*32:(block_index+1)*32]

            if guess_block == target_block:
                known_bytes += bytes([b])
                print(f"[+] Found byte: {bytes([b])} | So far: {known_bytes.decode(errors='ignore')}")
                found = True
                break

        if not found:
            print("\n[*] No match found. FLAG likely complete.")
            break

    print(f"\n🏁 Final FLAG: {known_bytes.decode(errors='ignore')}")

if __name__ == "__main__":
    recover_flag()
