#euclidean gcd algorithm
def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

#storage efficient exponantiation modulo
def exponentiationModulo(base, exp, n):
    if(exp == 0):
        return 1

    result = 1
    for _ in range(exp):
        result = (result * base) % n
    
    return result