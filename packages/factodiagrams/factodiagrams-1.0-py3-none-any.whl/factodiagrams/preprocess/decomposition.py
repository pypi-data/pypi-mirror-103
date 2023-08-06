import math
from .Factorisation import Factorization


# grouping of 2x2s into 4
def fours(n):
    """Returns the formatted list of prime factors of n.
    
    If two numbers 2 follow each other in the prime number decomposition, this function returns an array where the 2x2 have been transformed into 4. Useful for a better representation.

    :param n: number to decompose.
    :type n: int

    :Example:
        prime_factors(12) [2, 2, 3] become [4, 3]
    """
    if n == 1:
        return [1]
    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4
    return factors + Factorization().prime_factors(n)


# Compute radius of a point
def radius(n):
    """Returns the radius of circles according to n.

    :param n: number to decompose.
    :type n: int
    """
    # n = number of small circles
    if n == 1:
        return 1
    s = math.sin(math.pi / n)
    return s / (s + 1)

