
#%%
import math
from math import sqrt
import warnings
import sympy as smp
import sys
from itertools import count
import random
from subprocess import check_call
import os
from PIL import Image
from random import randint
#%%
try:
    number = int(input('Enter a number : '))
except(ValueError) :
    print('Please enter an integer !')
num = number
wilson_factor = []
if smp.isprime(number) :
    wilson_factor.append(number)
else :
    for i in range(2, int(number/2) + 1) :   
        """while figuring out prime factors of a given number, n
        keep in mind that a number can itself be prime or if not, 
        then all its prime factors will be less than or equal to its int(n/2 + 1)"""
        if smp.isprime(i) and number % i == 0 :
            while(number % i == 0) :
                wilson_factor.append(i)
                number = number  / i
print('wilson factor of ' + str(num) + ' - ')
for i in wilson_factor :
    print(i)
#%%
# resultat du test avec un nombre =24
wilson factor of 24 - 
2
2
2
3
#%%
def test_fermat(self):
        actual=Factorization().fermat(24)
        expected=[12,2]
        self.assertEqual(actual,expected)



#%%
 def test_draw_factor_fermat(n):
        actual=Factorization().draw_factor(24,"fermat",False,False)
        assertTrue(actual)
#%%  
    def test_draw_wilson_factor(self):
        actual=Factorization().draw_factor(24,"wilson_factor",False,False)
        self.assertTrue(actual)
#%%
    def test_draw_factor_poster(self):
        Factorization().draw_factor_poster(list(range(1,10)),"fermat")
        exists= os.path.exists("../poster")
        self.assertTrue(exists)
        expected=[]
        for i in list(range(1,10)):
            expected.append(str(i)+"\'s_Diagram.png")
        expected.sort()
        actual=os.listdir("../poster/")
        actual.sort()
        self.assertEqual(actual,expected)
if __name__=='__main__':
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
    unittest.main()

    # %%
    def test_draw_factor_poster(self):
        Factorization().draw_factor_poster(list(range(1,10)),"wilson_factor")
        exists= os.path.exists("../poster")
        self.assertTrue(exists)
        expected=[]
        for i in list(range(1,10)):
            expected.append(str(i)+"\'s_Diagram.png")
        expected.sort()
        actual=os.listdir("../poster/")
        actual.sort()
        self.assertEqual(actual,expected)
if __name__=='__main__':
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
    unittest.main()
# %%
