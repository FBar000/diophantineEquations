'''
Code to interpret equations of form

"Ax + By + Cz + ... = const"

'''
from tempfile import tempdir
import numpy as np
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
            print(f"{i}: {terms}")
            for e in terms:
                var = re.findall("[a-zA-Z]", e[1])[0] if re.search("[a-zA-Z]", e[1]) else 0
                val = int(re.findall("\d+", e[1])[0]) if re.search("\d+", e[1]) else 1
                val = -val if e[0] == "-" else val                                  # make negative if signed
                val = -val if i == 1 else val                                       # invert value if on right hand side
                d_dict[var] = (d_dict[var] + val) if (var in d_dict) else val       # add to existing value or intitialize
        self.eq = dict(d_dict)

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
            if val > 0:
                tmp += "+"
            if isinstance(key, str):
                tmp += str(val) + key
        tmp += "=" + str(self.eq[0])
        if tmp[0] =="+": tmp = tmp[1:]
        return tmp

    def reduce(self):

        return
            
a = diophantineEquation("3x - 2y = 3")
