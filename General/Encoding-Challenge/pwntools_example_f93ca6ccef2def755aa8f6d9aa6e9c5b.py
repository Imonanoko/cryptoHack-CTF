from pwn import * # pip install pwntools
import json
import base64, codecs
from Crypto.Util.number import long_to_bytes

r = remote('socket.cryptohack.org', 13377)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

for i in range(100):
    received = json_recv()
    type=received['type']
    encoded = received["encoded"]
    if type == "base64":
        decoded = base64.b64decode(encoded).decode()

    elif type == "hex":
        decoded = bytes.fromhex(encoded).decode()

    elif type == "rot13":
        decoded = codecs.decode(encoded, 'rot_13')

    elif type == "bigint":
        # 去掉 "0x" 再轉回 bytes
        decoded = long_to_bytes(int(encoded, 16)).decode()

    elif type == "utf-8":
        decoded = bytes(encoded).decode("utf-8")
    to_send = {
        "decoded": decoded,
    }
    json_send(to_send)
    
print(json_recv())
