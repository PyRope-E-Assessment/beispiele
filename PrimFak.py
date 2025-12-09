from pyrope import *

import random as rd
import numpy as np
from sympy import Symbol
from fractions import Fraction

x = Symbol('x')

#Large lightgrey font for preamble
def titel(txt):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def makeProd():
    [mini, maxi] = [3, 9]
    anz = rd.randint(mini, maxi)
    highest = 24 - 3*(anz - mini) #größere Anzahl --> kleinere Primz
    P = 1
    pFac = []
    for i in range (anz):
        fac = rd.choice(primes[:highest+1])
        P = P * fac
        pFac.append(fac)
    pFac.sort()
    return P, pFac


class Primes(Exercise):

    preamble = titel('Find Primes')

    def parameters(self):
        start = rd.randint(5, 15)
        stop = start + 10
        return {'start': start, 'stop': stop, 'primes': primes[start-1 : stop]}

    def problem(self):
        return Problem('''
        Ermitteln Sie mit dem *Sieb des Erathostenes* alle Primzahlen bis 100 aufsteigend geordnet 
        und tragen Sie die Primzahlen von der $<<start:latex>>$. bis zur $<<stop:latex>>.$ 
        in die Liste ein:\n\n<<primes_>>''',
        primes_= List(widget = Text(width = 40))
        )

    def scores(self,primes_, primes):
        primes_.sort()
        return (primes_ ==primes, 1)
    

class PrimFac(Exercise):

    preamble = titel('Prime Factorization')

    def parameters(self):
        P, pFac = makeProd()
        return {'P': P, 'pFac': pFac}

    def problem(self):
        return Problem('''
        Zerlegen Sie die Zahl $<<P:latex>>$ in ihre Primfaktoren. Geben Sie die Lösung als Liste ein.\\
        Mehrfach vorkommende Faktoren müssen auch mehrfach in die Liste eingetragen werden!\n\n
        Lösung: <<pFac_>>''',
        pFac_= List(widget = Text(width = 30))
        )
            
    def hints(self):
        return('Alle Primfaktoren sind kleiner als 100')

    def scores(self, pFac, pFac_):
        pFac_.sort()
        return (pFac_ == pFac, 1)
   

class Cancel(Exercise):

    preamble = titel('Cancel Down Rational Number')

    def parameters(self):
        P01, pFac1 = makeProd()
        P02, pFac2 = makeProd()
        return {'P01': P01, 'P02': P02, 'R':Fraction(P01,P02)}

    def problem(self):
        return Problem('''
        Kürzen Sie den Bruch $\\Large{\\frac{<<P01:latex>>}{<<P02:latex>>}}$ so weit wie möglich!\n\n
        Lösung:$~~~$<<R_>>''',
        R_= Rational(widget = Text(width = 10))
        )
