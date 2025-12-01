from pyrope import *

import numpy as np
import random as rd
import matplotlib.pyplot as plt

from sympy import Symbol, simplify

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'


x = Symbol('x')

#Polynom 2. Grades
def polynomial2():
    b = rd.choice([-1,1])*rd.randint(1,3)
    c = rd.randint(-2,2)*2*b #für ganzzahl. sP
    d = rd.randint(-5,5)
    [b,c,d] = [1,0,-1]
    xs = int(-c/2/b)
    f = b*x**2 + c*x + d
    xP = [xs, -1, 1]
    yP = [b*xs**2 + c*xs + d, b-c+d, b+c+d]
    return  f, [xP, yP]

#Polynom 3. Grades
def polynomial3():
    a = rd.choice([-1,1])*rd.randint(1,3)
    b = rd.randint(-2,2)*3*a #für ganzzahl. iP
    c = rd.randint(-5,5)
    d = rd.randint(-5,5)
    xi = int(-b/3/a)
    f = a*x**3 + b*x**2 + c*x + d
    xP = [xi, -1, 0, 2] #2 to avoid point symmetry problem 
    yP = [a*xi**3 + b*xi**2 + c*xi + d, -a+b-c+d, d,  8*a+4*b+2*c+d]
    return  f, [xP, yP]

def plotGraph(f, points):
    if points[0][0] not in points[0][1:]: 
        points = [points[0][:-1], points[1][:-1]] #überflüssige Information entfernen
    X = list(np.arange(np.min(points[0]) - 1.5, np.max(points[0]) + .2, .1))
    Y = []
    for xi in X:
        Y.append (f.evalf(subs={x: xi}))
    figure, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('auto')
    ax.set_yticks(points[1], minor=False)
    ax.yaxis.grid(True, which='major')
    ax.set_xticks(points[0], minor=False)
    ax.xaxis.grid(True, which='major')
    plt.plot(X,Y,'b')
    for i in range (len(points[0])):
        plt.plot(points[0][i], points[1][i], 'go')
    plt.plot(points[0][0], points[1][0], 'r', marker = 's')
    plt.title('Graph of f(x)')
    return figure

    
class curveFeatures3(Exercise):
    
    preamble = titel('Polynomial of degree 2')
    
    def parameters(self):
        f, points = polynomial2()
        return {'f': f, 'points': points, 'fig': plotGraph(f, points)}
    
    def problem(self, f, points):
        return Problem(
                '<<fig>>\n\n'
                'Find out the equation of the polynomial of degree 2 shown in the diagram above.\n\n'
                '$f(x) =$ <<f_>>',
                f_ = Expression(symbols='x')
                )
    
    def hints(self):
        return 'All values at marked points are integers. The red square one is the turning point.'
    
    def scores(self, f_, f):
        return (3*(simplify(f_-f) == 0), 3)   


class curveFeatures4(Exercise):
    
    preamble = titel('Polynomial of degree 3')

    def parameters(self):
        f, points = polynomial3()
        return {'f': f, 'points': points, 'fig': plotGraph(f, points)}
    
    def problem(self, f, points):
        return Problem(
                '<<fig>>\n\n'
                'Find out the equation of polynomial of degree 3 shown in diagram above.\n\n'
                '$f(x) =$ <<f_>>',
                f_ = Expression(symbols='x')
                )
    
    def hints(self):
        return 'All values at marked points are integers. The red square one is the inflection point.'
 
    def scores(self, f_, f):
        return (4*(simplify(f_-f) == 0), 4)