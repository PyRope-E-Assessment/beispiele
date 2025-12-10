from pyrope import *

import random as rd
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as ig
from sympy import Symbol, sin, cos, exp, diff, integrate, simplify

x = Symbol('x')

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

def makeFunction(op):
    def polynom(n): #Polynom n. Grades
        f = (-1)**rd.randint(0,1)*rd.randint(1,5)*x**n
        for i in range (n):
            p = rd.randint(-5,5)*x**(n-1-i) #Auswahl Koeffizienten
            f = f + p
        return  f
    def function(id, p): #Auswahl Funktionstyp
        options = {0: polynom(p), 1: sin(x)**p, 2: cos(x)**p, 3: exp(x)**p}
        return options[id]
    id1 = int(op=='diff')*rd.randint(0, 3)
    p = rd.randint(1, 3)
    f1 = function(id1, p)
    id2 = id1
    while id2==id1:
        id2 = rd.randint(int(op=='intg'), 3)
    p = 1 + int(op=='diff' or id2==3)*rd.randint(0, 4) #Auswahl Potenz
    f2 = function(id2, p)
    join = {0: f1/f2, 1: f1, 2: f2, 3: f1*f2}
    id = rd.randint(int(op=='intg'), 3) #Auswahl Verknüpfung: bei Intg kein Quotient
    return id in [0,3], join[id]

#Function plot    
def plotGraph(f, null):
    x = np.arange(null[0]-.1, null[2]+.2, .1)
    y = []
    for i in x:
        y.append(f(i))
    fig, ax = plt.subplots(figsize=(3, 3))
    plt.grid()
    plt.plot(x,y,'-b')
    plt.fill_between(x, 0*x, y, color='gray', alpha = 0.25)
    plt.title('Graph of f(x)')
    return fig

#Rundet einen Wert x in Abhängigkeit von seiner Größe
#auf n relevante Stellen (n Ziffern ab 1. von 0 verschiedener)
def relRound(x, n):
    p = 0
    while x >= 1:
        x = x/10
        p+=1
    x = round(x,n)
    return x*10**p

        
class Derivative(Exercise):
    
    preamble = titel('Differenzieren')

    def parameters(self):
        composed, f = makeFunction('diff')
        sol = simplify(diff(f))
        return {'f': f, 'dif': diff(f), 'sol': sol, 'composed': composed}
    
    def problem(self, sol):
        return Problem(
            'Differenzieren Sie:  $~~~f(x) = <<f:latex>>$\n\n'
            "$f'(x) =$ <<sol_>>",
            sol_=Expression(symbols = 'x', widget = Text(width = 80))
        )
        
    def scores(self, sol_, sol, composed):
        score = 0
        if simplify(sol_ - sol) == 0:
            score = 1 + composed
        return {'sol_': score}


class Integral(Exercise):
    
    preamble = titel('Unbestimmtes Integral')

    def parameters(self):
        composed, diffF = makeFunction('intg')
        sol = integrate(diffF)
        return {'sol': sol, 'df': diffF, 'composed': composed}

    def problem(self):
        return Problem(
            'Berechnen Sie eine Stammfunktion von $~~~f(x) = <<df:latex>>$\n\n'
            '$∫f(x)dx =$  <<F_>> ',
            F_=Expression(symbols='x', widget = Text(width = 80))
        )
    
    def a_solution(self, sol):
        return {'F_': sol}
    
    def hints(self):
        return 'Verwenden Sie bei Bedarf partielle Integration'

    def scores(self, F_, sol, composed):
        score = 0
        if simplify(diff(F_) - diff(sol)) == 0:
            score = 1 + composed
        return {'F_': score}


class SurfaceArea(Exercise):
    
    preamble = titel('Flächenberechnung durch Integration')

    def parameters(self):
        null = [0., 0., 0.]
        while not (null[0] < null[1] < null[2]):
            null = [rd.randint(-9,9), rd.randint(-9,9), rd.randint(-9,9)]
            null.sort()       
        F = ''
        for n in null:
            if n<0: F = F + '(x + ' + str(-n)
            elif n>0: F = F + '(x - ' + str(n)
            else: F = F + '(x '
            F = F + ')'
        def f(x):
            return (x-null[0])*(x-null[1])*(x-null[2])
        A1 = ig.quad(f, null[0],null[1])
        A2 = ig.quad(f, null[1],null[2])
        A = relRound(A1[0] - A2[0], 4)
        return {'F': F, 'A': A, 'pltGraph': plotGraph (f, null)}

    def problem(self, F):

        return  Problem (
                '<<pltGraph>>\n\n'
                'Berechnen Sie die durch die Funktion $y = f(x) =$ $<<F:latex>>~~~$'
                'und die x-Achse eingeschlossene Fläche! Runden Sie auf mindestens 4 relevante Stellen.\n\n'
                'Lösung: <<A_>>',
                A_=Real(),
                )
    
    def scores(self, A_, A):
        score = 0
        if relRound(A_, 4) == A:
            score = 1
        return {'A_': score}
    