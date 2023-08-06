"""
This is my example script
=========================

This example doesn't do much, it just makes a simple plot
"""
# %%
# This is a section header
# ------------------------
#
# In the built documentation, it will be rendered as rST. All rST lines
# must begin with '# ' (note the space) including underlines below section
# headers.

# These lines won't be rendered as rST because there is a gap after the last
# commented rST block. Instead, they'll resolve as regular Python comments.
# Normal Python code can follow these comments.
from Factorization import *

factorisation=Factorization()
print(factorisation.prime_factors(70))