"""
Diagrams generating example
===========================

"""
# %%
# Diagram generating using Prime factors
# ------------------------

from Factorization import *

factorisation=Factorization()
factorisation.draw_factor(70,"prime_factors",True,True)


# %%
# Diagram generating using Pollard Rho
# ------------------------

from Factorization import *

factorisation=Factorization()
factorisation.draw_factor(70,"pollardrho",True,True)
