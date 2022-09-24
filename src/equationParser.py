'''
Code to interpret equations of form

"Ax + By + Cz + ... = const"

'''
import copy
from decimal import Decimal
import functools
import math
import re


class diophantineEquation():
    def __init__(self, equation: str):
        """
        Create a diophantineEquation from a string represenation.
        """
        tmp = [x.strip() for x in re.split("[=]", equation)]
        d_dict = {}
        for i in range(len(tmp)):
            terms = re.findall(r"([-+]|^)(\s*\d*\w)", tmp[i])
            for e in terms:
                var = re.findall("[a-zA-Z]", e[1])[0] if re.search("[a-zA-Z]", e[1]) else 0
                val = int(re.findall("\d+", e[1])[0]) if re.search("\d+", e[1]) else 1
                val = -val if e[0] == "-" else val                                  # make negative if signed
                val = -val if i == 1 else val                                       # invert value if on right hand side
                d_dict[var] = (d_dict[var] + val) if (var in d_dict) else val       # add to existing value or intitialize
        self.eq = dict(d_dict)
        self.simplify()

    def evaluate(self, values):
        """
        Check if a list of values satisfies the equation
        """
        # counters for lhs, rhs values 
        ct = 0
        for var, val in values.items():
            try: ct += val * self.eq[var]
            except KeyError: pass
        ct += self.eq[0]
        return ct == 0

    def __str__(self) -> str:
        tmp = ""
        for key, val in self.eq.items():
            if key == 0: continue
            if val > 0:
                tmp += "+"
            tmp += str(val) + key if val != 1 else key
        tmp += "=" + str(-self.eq[0])
        if tmp[0] =="+": tmp = tmp[1:]
        return tmp

    def reduced(self):
        """
        Returns the latent diophantine equation.
        """
        prod = copy.deepcopy(self)
        searchable_subset = [(key, abs(val)) for key, val in prod.eq.items() if isinstance(key, str)]
        min_key, min_abs_val = min(searchable_subset, key=lambda x: x[1])
        if min_abs_val == 1: return None        # Exit
        # get underlying equation
        for key, value in prod.eq.items():
            if key != min_key:
                prod.eq[key] =  -(value % min_abs_val) if value < 0 else value % min_abs_val
        prod.simplify()
        return prod

    def simplify(self):
        """
        Simplifies the equation by removing any common factors.
        """
        fc = self.find_gcd([val for key, val in self.eq.items()])
        for key, value in self.eq.items():
            self.eq[key] = int(value / fc)

    def find_gcd(self, list):
        """
        Helper method for simplify
        """
        x = functools.reduce(math.gcd, list)
        return x


    def reduce_unknowns(self, information):
        """
        Return a new equation by performing known calculations.

        `information` is a dict with variables' values.
        """
        new_eq = copy.deepcopy(self)
        sliding_vars = set(self.eq.keys()) - set(information.keys())
        ct = 0
        for var, val in information.items():
            try: ct += val * self.eq[var]
            except KeyError: pass
        ct += self.eq[0]
        new_eq.eq = dict([(key, self.eq[key]) for key in sliding_vars] + [(0, ct)])
        new_eq.simplify()
        return new_eq




# n = diophantineEquation("147x - 258y= 369")
# while n:
#     print(n)
#     n = n.reduce()

obj = diophantineEquation("3x+2y=15")

n = 0
x_val = 10000
sols = []

while x_val > 0:
    a = obj.reduce_unknowns({'y': n})
    print(a.eq)
    print(a)
    if a.eq[0] % a.eq['x'] == 0:
        x_val = int(-a.eq[0] / a.eq['x'])
        sols.append((n, x_val))
    else:
        print('no integer solution')
    print("-")
    n += 1
print(sols)