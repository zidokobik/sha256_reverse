"""
MANUAL HASHING OF "abc" USING SHA256
"""

import math


def is_prime(n):
    """
    quick check if a number is prime
    :param n: number to be check
    :return: boolean
    """
    for x in range(2, n):
        if n % x == 0:
            return False
    return True


def right_rotate(n, bits):
    """
    bitwise right rotation
    :param n: integer to be rotated
    :param bits: amount of bits to rotate
    :return: rotated integer
    """
    return (n >> bits) | (n << (32 - bits)) & 0xFFFFFFFF


def mod_add(*args):
    """
    modulo 2**32 addition
    :param args:
    :return:
    """
    return sum(args) % 2**32

# ------------------------------------------MAIN COMPRESSION FUNCTIONS-------------------------------------------------


def sti(string: str):
    return int(string, 2)


def ch(x, y, z):
    return (x & y) ^ ((~x) & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def Sigma0(x):
    return (right_rotate(x, 2)) ^ (right_rotate(x, 13)) ^ (right_rotate(x, 22))


def Sigma1(x):
    return (right_rotate(x, 6)) ^ (right_rotate(x, 11)) ^ (right_rotate(x, 25))


def smallsigma0(x):
    return (right_rotate(x, 7)) ^ (right_rotate(x, 18)) ^ (x >> 3)


def smallsigma1(x):
    return (right_rotate(x, 17)) ^ (right_rotate(x, 19)) ^ (x >> 10)


# ---------------------------------- INITIAL HASH VALUES AND ROUND CONSTANTS ------------------------------------------

# INITIAL HASH VALUES: FIRST 32 BITS OF FRACTIONAL PARTS OF SQUARE ROOT OF FIRST 8 PRIMES:
HASH = [int(math.modf(math.sqrt(num))[0]*(1 << 32)) for num in range(2, 20) if is_prime(num)]

# ROUND CONSTANTS: FIRST 32 BITS OF FRACTIONAL PARTS OF CUBE ROOT OF FIRST 64 PRIMES:
CONSTANTS = [int(math.modf(num**(1/3))[0]*(1 << 32)) for num in range(2, 312) if is_prime(num)]

# ------------------------------------------------- PADDING -----------------------------------------------------------
msg = "abc"
msg = ''.join(format(ord(letter), '08b') for letter in msg) + '1' + '0'*(512 - ((len(msg)*8+65) % 512)) + format(len(msg)*8, '064b')
# msg IS IN STRING WITH LENGTH OF FACTORS OF 512
# ------------------------------------------------ MAIN LOOP ----------------------------------------------------------

for block in range(0, len(msg), 512):
    a = HASH[0]
    b = HASH[1]
    c = HASH[2]
    d = HASH[3]
    e = HASH[4]
    f = HASH[5]
    g = HASH[6]
    h = HASH[7]
    block = msg[block:block+512]
    w = [sti(block[x:x+32]) for x in range(0, 512, 32)]
    for j in range(16, 64):
        w.append(mod_add(smallsigma1(w[j - 2]), w[j - 7], smallsigma0(w[j - 15]), w[j - 16]))
    for loop in range(0, 64):
        temp1 = mod_add(h, ch(e, f, g), Sigma1(e), w[loop], CONSTANTS[loop])
        temp2 = mod_add(maj(a, b, c), Sigma0(a))
        h = g
        g = f
        f = e
        e = mod_add(d, temp1)
        d = c
        c = b
        b = a
        a = mod_add(temp1, temp2)
#        print(format(a, '08x'), format(b, '08x'), format(c, '08x'), format(d, '08x'), format(e, '08x'), format(f, '08x'), format(g, '08x'), format(h, '08x'))
    for x in range(8):
        HASH[x] = mod_add(HASH[x], list([a, b, c, d, e, f, g, h])[x])

DIGEST = ''.join(format(HASH[x], '08x') for x in range(8))
print("DIGEST IS:", DIGEST.upper())
