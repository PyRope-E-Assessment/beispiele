from pyrope import *

import random as rd
from random import randint as rdi
import numpy as np
from sympy import Symbol, simplify, solve
import matplotlib.pyplot as plt

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x = Symbol('x')

prTxt1 = '''Berechnen Sie mittels Newton-Verfahren eine Nullstelle der Funktion f(x). (Genauigkeit >= 2 NK-Stellen)\\
         Find using Newtons Method a root of the function f(x). (accuracy >= 2 decimal places)\n\n'''
prTxt2 = '''Berechnen Sie nun mittels Newton-Verfahren eine weitere Nullstelle dieser Funktion.\\
         Now compute using Newtons Method another root of this function.\n\n'''

def squareFunc0Null():
    a = rdi(1, 5)*rd.choice([-1,1])
    c = rdi(1, 5)*np.sign(a)
    b = rdi(0, int(2*np.sqrt(a*c)-0.1))*rd.choice([-1,1])
    return a*x**2 + b*x + c

def cubFunc1Null():
    x0 = 1/4*rdi(1, 10)
    f2 = squareFunc0Null()
    f = simplify(f2*x - f2*x0)
    return f, x0

def quadFunc2Null():
    f3, x0 = cubFunc1Null()
    null = [x0, 1/4*rdi(-10, -1)]
    f = simplify(f3*x - f3*null[1])
    return f, null

def plotGraph(f, null):
    X = list(np.arange(min(null) - 0.5, max(null) + 0.6, .1))
    Y = []
    for xi in X:
        Y.append (f.evalf(subs={x: xi}))
    figure, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('auto')
    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='major')
    plt.plot(X,Y,'b')
    for x0 in null:
        plt.plot(x0, 0, 'r', marker = '*')
    plt.title('Graph of f(x)')
    return figure


class Newton1(Exercise):

    preamble = titel('Newtons Method 1')
    
    def parameters(self):
        f, x0 = cubFunc1Null()
        return {'f': f, 'x0': x0, 'fig': plotGraph(f, [x0])}

    def problem(self, x0):
        return  Problem (
                f'$f(x) =$ <<f>>\n\n {prTxt1} $x_0 = $ <<x0_>>\n\n',
                x0_ = Real(atol = 0.0050000001, widget = Text(width = 6))
                )
    
    def feedback(self):
        return '<<fig>>'


class Newton2(Exercise):
    
    preamble = titel('Newtons Method 2')
        
    def parameters(self):
        f, null = quadFunc2Null()
        return {'f': f, 'x01': null[0], 'x02': null[1], 'fig': plotGraph(f, null)}

    def problem(self):
        return  Problem (
        f'$f(x) =$ <<f>>\n\n {prTxt1}' 
        '$x_{01}= $ <<x01_>> \n\n'+f'{prTxt2}'
        '$x_{02}= $ <<x02_>>',
        x01_ = Real(widget = Text(width = 6)),
        x02_ = Real(widget = Text(width = 6))
        )
    
    def hints(self):
        return 'Verwenden Sie Polynomdivision -  use Polynomial Division'
        
    def scores(self, x01_, x02_, x01, x02):
        null = [x01, x02].copy()
        score = 0
        if x01_ is not None:
            if round(x01_,2) in null:
                score += 1; null.remove(round(x01_,2))
        if x02_ is not None:
            score += round(x02_,2) in null
        return (score, 2)
    
    def feedback(self):
        return '<<fig>>'
