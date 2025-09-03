from sympy import isprime, factorint

def find_primitive_roots(p):
    if not isprime(p):
        raise ValueError("p 必須是質數")

    phi = p - 1
    prime_factors = list(factorint(phi).keys())  # 質因數

    primitive_roots = []
    for g in range(2, p):
        is_primitive = True
        for q in prime_factors:
            if pow(g, phi // q, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            primitive_roots.append(g)
    return primitive_roots

# ✅ 使用範例：
if __name__ == "__main__":
    p = int(input("請輸入質數 p："))
    if not isprime(p):
        print("輸入的 p 不是質數，請重新輸入。")
    else:
        roots = find_primitive_roots(p)
        print(f"\n原根個數：{len(roots)}")
        print(f"所有原根：{roots}")
