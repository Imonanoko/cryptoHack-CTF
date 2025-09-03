from sympy import sqrt_mod
# E: by^2 = x^3 + Ax^2 +x
def addition(P:list,Q:list,a:int,b:int,p:int):
    if P == None:
        return Q
    elif Q == None:
        return P
    if P[0] ==Q[0] and (P[1] + Q[1]) % p == 0:
        return None
    else:
        alpha = None
        if P == Q:
            alpha = (((3*P[0]*P[0] + 2*a*P[0] + 1) % p) * pow(2*b*P[1],-1,p)) % p
            
        else:
            alpha = ((Q[1] - P[1]) * pow(Q[0] - P[0],-1,p)) % p
        x3 = b*alpha*alpha - a - P[0] - Q[0]
        y3 = alpha*(P[0] - x3) - P[1]
        return [x3 % p, y3 % p]
def montgomeryBinary(P:list,k:int,a:int,b:int,p:int):
    k_bin = bin(k)[2:]
    R0,R1 = P,addition(P,P,a,b,p)
    for bit in k_bin[1:]:
        if bit == '0':
           R0,R1 = addition(R0,R0,a,b,p),addition(R0,R1,a,b,p)
        else:
            R0,R1 = addition(R0,R1,a,b,p),addition(R1,R1,a,b,p)
    return R0
x = 9
y = sqrt_mod(x**3 + 486662*x*x + x, pow(2,255)-19)
G = [x,y]
k = "1337c0decafe"
a = 486662
b = 1
p = pow(2,255)-19
Q = montgomeryBinary(G,int(k,16),a,b,p)
print(Q[0])