from pyrope import *

import numpy as np
import random as rd
import math
from sympy import Symbol

x = Symbol('x')

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

C8 = Complex(atol=.000500001, widget = Text(width=8))
R8 = Real(atol=.000500001, widget = Text(width=8))


class ComplexNumbers1(Exercise):

    preamble = titel('Divide 2 complex numbers')

    def parameters(self):
        c1 = complex(rd.randint(1,9), rd.randint(1,9))
        c2 = complex(rd.randint(1,9), rd.randint(1,9))
        Q = np.round(c1/c2,3)
        return {'c1': c1, 'c2': c2, 'Q': Q}

    def problem(self, Q):
        return Problem(
        '$\\Large{\\frac{<<c1:latex>>}{<<c2:latex>>}} =$ <<Q_>>$~~~$(precision at least 3 dec. places)',
        Q_= C8
        )
    
    def hints(self):
        return 'Use the conjugate'


class ComplexNumbers2(Exercise):

    preamble = titel('Transform complex numbers 1')

    def parameters(self):
        c = complex(rd.randint(1,9), rd.randint(1,9))
        r = math.sqrt(c.real**2+c.imag**2)
        if c.real==0: phi=math.pi/2
        else: phi = math.atan(c.imag/c.real)
        return {'c': c, 'r': round(r,3), 'phi': round(phi,3)}

    def problem(self):
        return Problem('''
        Transform into polar form: $~~~<<c:latex>> = r*e^{φj}~~~$(precision at least 3 dec. places)\n\n
        $ r = $ <<r_>>$~~~~~~ φ = $ <<phi_>> $~~~$Give the angle measured in radians!''',
        r_= R8,
        phi_ = R8
        )


class ComplexNumbers3(Exercise):

    preamble = titel('Transform complex numbers 2')

    def parameters(self):
        r = rd.randint(1,9)
        phi = rd.randint(1,360)
        C = complex(r*math.cos(phi*math.pi/180), r*math.sin(phi*math.pi/180))
        return {'r': r, 'phi': phi,'C': np.round(C, 3)}

    def problem(self):
        return Problem('''
        Transform into cartesian form (a + bj):\n\n
        $<<r:latex>>*(cos(<<phi:latex>>°) +  sin(<<phi:latex>>°)j) = $ <<C_>>$~~~$(precision at least 3 dec. places)''',
        C_= C8
        )
    

class ComplexNumbers4(Exercise):

    preamble = titel('Raise a complex number to a given power')

    def parameters(self):
        c = complex(rd.randint(1,9), rd.randint(1,9))
        n = rd.randint(2, 9)
        P = c**n
        return {'c': c, 'n': n, 'P': np.round(P, 3)}

    def problem(self, n):
        return Problem(       
        '$<<c:latex>>^<<n:latex>> =$ <<P_>>$~~~$\n\n',
        P_= C8
        )