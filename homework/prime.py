import math


def is_prime(n: int):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    limit = int(math.sqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False, i
    return True


if __name__ == "__main__":
    result = is_prime(587)
    print(result)
