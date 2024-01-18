# Алгоритм находит такие даты, что ддммгггг есть произведение простых чисел p и q и ммдд - простое число
def primfacs(n):
   i = 2
   primfac = []
   while i * i <= n:
       while n % i == 0:
           primfac.append(i)
           n = n // i
       i = i + 1
   if n > 1:
       primfac.append(n)
   return primfac

def find_perfect_birthdate():
    N = []
    n1 = [str(i) for i in range(1, 32)]
    n2 = ['0' + str(i) if i < 10 else str(i) for i in range(1, 13)]
    n3 = ['2000', '2001']
    for i in n3:
        for j in n2:
            for k in n1:
                if len(primfacs(int(j + k))) == 1:
                    N.append(int(k + j + i))

    result = []
    for n in N:
        pfs = primfacs(n)
        if len(pfs) == 2 and len(primfacs(pfs[0])) == 1 and len(primfacs(pfs[1])) == 1:
            result.append([n, pfs[0], pfs[1]])
    return result

primefactors = find_perfect_birthdate()
print(primefactors)