import unittest
import sys
sys.path.insert(1,"../src/")
from Factorisation import *
import os
import warnings


class FactorizationTest(unittest.TestCase):

    def test_prime_factors(self):
        actual=Factorization().prime_factors(30)
        expected=[2,3,5]
        self.assertEqual(actual,expected)

    def test_pollardrho(self):
        actual=Factorization().pollardrho(30)
        expected=[3,10]
        self.assertEqual(actual,expected)

    def test_draw_factor_prime_factors(self):
        actual=Factorization().draw_factor(30,"prime_factors",False,False)
        self.assertTrue(actual)
    
    def test_draw_factor_pollardrho(self):
        actual=Factorization().draw_factor(30,"pollardrho",False,False)
        self.assertTrue(actual)

    def test_draw_factor_poster(self):
        Factorization().draw_factor_poster(list(range(1,10)),"prime_factors")
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