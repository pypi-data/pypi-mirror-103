def factorization(self, n: int, function_name: str)->dict:
         """[function to generate a number factorization based on function name]

         Args:
             n (int): [number to factorize]
             function_name (str): [Factorization function name used to get the factors]

         Returns:
             dict: [dictionary of each factor's multiplicity]
         """
         factors = {}
         for p1 in eval("self."+function_name+"("+str(n)+")"):
             try:
                 factors[p1] += 1
             except KeyError:
                 factors[p1] = 1
         return factors