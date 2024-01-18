from math import sqrt

n = 21102001
q, p = 947, 22283 # gdc = 2
phi_n = (q-1) * (p-1)

e1 = 1021
e2 = 1201

# Проверка на простоту
def is_prime(n):
    if n < 2:
        return False 
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False 
    return True 

print(f'{is_prime(n) = }', f'{is_prime(q) = }', f'{is_prime(p) = }', f'{is_prime(e1) = }', f'{is_prime(e2) = }', 
      sep='\n', end='\n\n')

# d*e = 1 (mod phi(n))
# Вычисление обратного при помощи расширенного алгоритма Евклида
def find_d(e, phi_n):
    (d, new_d) = (0, 1)
    (r, new_r) = (phi_n, e)
    
    while(new_r != 0):
        quotient = r // new_r
        # print(quotient)
        
        (d, new_d) = (new_d, d - quotient * new_d)
        (r, new_r) = (new_r, r - quotient * new_r)
        # print(r, new_r)
        
    if (r > 1):
        print('Не обратимо')
        return None 
    if (d < 0):
        d = phi_n + d
    
    return d

d1 = find_d(e1, phi_n)
d2 = find_d(e2, phi_n)
# print(d1, d2)

# Алиса --> Боб
# Сообщение
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

# Шифруем сообщение с помощью открытого ключа Боба и создаём цифровую подпись Алисы
encr_M = []
for el in M:
    encr_ch = modular_pow(el, e2, n)
    sign = modular_pow(el, d1, n)
    encr_M.append((encr_ch, sign))

print(encr_M, end='\n\n')

# Проверяем цифровую подпись и дешифруем сообщение с помощью закрытого ключа Боба
decr_M = []
for el, s in encr_M:
    check_sign = modular_pow(s, e1, n)
    decr_ch = modular_pow(el, d2, n)
    if check_sign == decr_ch: 
        decr_M.append(chr(decr_ch))
    else:
        print('Цифровая подпись не совпадает!')
        decr_M = []
        break
    
decr_M = ''.join(decr_M)
print("Расшифрованный текст: ")
print(decr_M)