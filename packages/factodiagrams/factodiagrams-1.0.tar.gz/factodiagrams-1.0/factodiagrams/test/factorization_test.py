import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + "..") * 2)
import warnings
import factodiagrams as fd

class FactorizationTest(unittest.TestCase):

    def test_prime_factors(self):
        actual = fd.preprocess.decomposition.prime_factors(12)
        expected = [2, 2, 3]
        self.assertEqual(actual,expected)
    
    def test_fours(self):
        actual = fd.preprocess.decomposition.fours(12)
        expected = [4, 3]
        self.assertEqual(actual,expected)
    
    def test_radius(self):
        actual = fd.preprocess.decomposition.radius(12)
        expected = 0.20560464675956822
        self.assertEqual(actual,expected)

if __name__ == "__main__":
    unittest.main()
