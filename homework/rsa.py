from math import isqrt
from sympy import mod_inverse

N = 8633
e = 655
ciphertext = [4856, 2793, 4004]


def fermat_factor(n):
    """Fermat's factorization: returns (p, q) if factors found"""
    a = isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return (a - b, a + b)
        a += 1


p, q = fermat_factor(N)
print(f"Factors found: p = {p}, q = {q}")

phi = (p - 1) * (q - 1)

d = mod_inverse(e, phi)
print(f"Private exponent d = {d}")

plaintext_blocks = [pow(c, d, N) for c in ciphertext]
print(f"Decrypted blocks: {plaintext_blocks}")

num_to_char = {i + 11: chr(65 + i) for i in range(26)}


def decode_block(block):
    s = str(block)
    message = ""
    i = 0
    while i < len(s):
        num = int(s[i : i + 2])  # take 2 digits
        if num in num_to_char:
            message += num_to_char[num]
            i += 2
        else:
            num = int(s[i])
            message += num_to_char.get(num, "?")
            i += 1
    return message


message = "".join(decode_block(b) for b in plaintext_blocks)
print("Decrypted message:", message)
