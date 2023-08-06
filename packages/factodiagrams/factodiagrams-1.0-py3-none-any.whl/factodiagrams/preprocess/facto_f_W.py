#%%
def fermat(n):
    if n&1==0:
        return [n>>1, 2]  # if n is even, return the solution
    x = lsqrt(n)
    if x*x==n:
        return [x, x]  #if n is already a perfect square, return the solution
    x += 1  # because we want the integer value immediately above the real square root
    while True:
        y2 = x*x-n
        y = lsqrt(y2)
        if y*y==y2:
            break  #if y2 is a perfect square, we have found a "good" y that goes with the x
        else:
            x += 1
    return [x-y, x+y]
#%%
from math import factorial
#%%
def wilson_factor(n):
    return n > 1 and bool(n == 2 or
                          (n % 2 and (factorial(n - 1) + 1) % n == 0))
 


# %%
