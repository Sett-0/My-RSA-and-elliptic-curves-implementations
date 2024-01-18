def inv(n, q):
    # n*inv % q = 1 => n*inv = q*m + 1 => n*inv + q*-m = 1
    # => egcd(n, q) = (inv, -m, 1) => inv = egcd(n, q)[0] (mod q)
    return egcd(n, q)[0] % q

def egcd(a, b):
    # extended GCD
    # returns: (s, t, gcd) as a*s + b*t == gcd
    # s, t, gcd = egcd(a, b)
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
    return s0, t0, a

def inverse_point(x, y, p):
    if x == None or y == None:
        return (None, None)
    if y != 0:
        return (x, -y % p)
    else:
        return (x, y)

def sum_of_points(x1, y1, x2, y2, a):
    if (x1, y1) == (0, 0): return (x2, y2)
    if (x2, y2) == (0, 0): return (x1, y1)
    if x1 == x2 and (y1 != y2 or y1 == 0):
        # p1 + -p1 == 0
        return (0, 0)
    if x1 == x2:
        # p1 + p1: use tangent line of p1 as (p1, p1) line
        l = (3 * x1 * x1 + a) * inv(2 * y1, p) % p
    else:
        l = (y2 - y1) * inv(x2 - x1, p) % p
    x = (l * l - x1 - x2) % p
    y = (l * (x1 - x) - y1) % p
    return (x, y)

def multiply_point(x, y, n):
    r = (0, 0)
    for _ in range(n):
        r = sum_of_points(r[0], r[1], x, y, a)
    return r

def order(G_x, G_y, p):
    # order of point G
    for i in range(1, p + 1):
            if multiply_point(G_x, G_y, i) == (0, 0):
                return i

# Алгоритм подсчёта числа c = b^e % m
def modular_pow(base, power, modulus):
    if modulus == 1: return 0
    res = 1
    base %= modulus
    while power > 0:
        if power % 2 == 1:
            res = (res * base) % modulus
        power = power >> 1
        base = (base * base) % modulus
    return res 

def sqrt(num, p):
    assert num < p
    for i in range(1, p):
        if modular_pow(i, 2, p) == num:
            return (i, p - i)
    raise Exception("Not found")

def find_points_on_curve(a, b, p):
    # find points on curve at x
    for x in range(p):
        y_sqare = (x ** 3 + a * x + b) % p
        y, my = sqrt(y_sqare, p)
        return (x, y), (x, my)


a = 1021
b = 1201
p = 10007
    
if (4 * (a ** 3) + 27 * (b ** 2)) % p == 0:
    print("Параметры не прошли проверку на сингулярность\n")
    exit()
    
x0, y0 = find_points_on_curve(a, b, p)[0]

G_x = x0
G_y = y0

n = order(G_x, G_y, p)
key = int(input("Пожалуйста, введите небольшой закрытый ключ (<{}): ".format(n)))

KEY_x, KEY_y = multiply_point(G_x, G_y, key)
k = int(input("Введите целое число k (<{}), чтобы найти kG и kQ: ".format(n)))

k_G_x, k_G_y = multiply_point(G_x, G_y, k)                         # kG
k_Q_x, k_Q_y = multiply_point(KEY_x, KEY_y, k)                     # kQ

M = """RSA (Rivest-Shamir-Adleman) is a public-key cryptosystem, one of the oldest that is widely used for secure data 
transmission. The initialism "RSA" comes from the surnames of Ron Rivest, Adi Shamir and Leonard Adleman, who publicly 
described the algorithm in 1977. An equivalent system was developed secretly in 1973 at Government Communications 
Headquarters (GCHQ), the British signals intelligence agency, by the English mathematician Clifford Cocks. 
That system was declassified in 1997. In a public-key cryptosystem, the encryption key is public and distinct from the 
decryption key, which is kept secret (private). An RSA user creates and publishes a public key based on two large prime 
numbers, along with an auxiliary value. The prime numbers are kept secret. Messages can be encrypted by anyone, via the 
public key, but can only be decoded by someone who knows the private key."""

M = list(M)
for i, el in enumerate(M):
    M[i] = ord(el)

encr_M = []
for el in M:
    encr_ch = el + k_Q_x
    encr_M.append((k_G_x, k_G_y, encr_ch))
    # print("({},{}),{}".format(k_G_x, k_G_y, cipher), end="-")

decr_M = []
for encr_ch in encr_M:
    decrypt_x, decrypt_y = multiply_point(encr_ch[0], encr_ch[1], key)
    decr_M.append(chr(encr_ch[2] - decrypt_x))
    
decr_M = ''.join(decr_M)
print("Расшифрованный текст: ")
print(decr_M)
