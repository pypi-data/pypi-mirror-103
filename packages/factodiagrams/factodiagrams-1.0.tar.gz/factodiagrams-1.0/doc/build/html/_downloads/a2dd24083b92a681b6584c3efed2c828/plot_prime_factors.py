"""
Factorization examples
=========================

This page provides examples using the methods prime factors and Pollard Rho.
"""
# %%
# prime factors method
# ------------------------
from Factorization import *
factorisation=Factorization()
print(factorisation.prime_factors(70))

###############################################################################

# %%
# Pollard Rho  method
# ------------------------
from Factorization import *
factorisation=Factorization()
print(factorisation.pollardrho(70))