import math
from math import factorial

def calculate_nCr(n,r):
    """Calculate the number of combinations (nCr)."""
    if r > n or n < 0 or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def calculate_nPr(n,r):
    """Calculate the number of permutations (nPr)."""
    if r > n or n < 0 or r < 0:
        return 0
    return factorial(n) // factorial(n - r)

if __name__ == "__main__":
    n = 5
    r = 3
    print(f"{n}C{r} = {calculate_nCr(n, r)}")
    print(f"{n}P{r} = {calculate_nPr(n, r)}")