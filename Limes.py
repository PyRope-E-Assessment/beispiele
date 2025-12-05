from pyrope import *

import random as rd
from sympy import Symbol, sin, cos, exp, limit, oo
import math

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x = Symbol('x')
inf = math.inf
ninf = -math.inf

#Polynom n. Grades
def polynom(n):
    f = (-1)**rd.randint(0,1)*rd.randint(1,5)*x**n
    for i in range (n):
        p = rd.randint(-5,5)*x**(n-1-i)
        f = f + p
    return  f

def getLim(f, x, a):
    try: #wenn kein GW ex. kommt Expression zurück
        limF = float(limit(f, x, a))
    except:
        limF = '-'
    if limF == inf:
        limF = '∞' #"\u221E"
    elif limF == ninf:
        limF = '-∞' #"-"\u221E"
    elif not limF == '-':
        limF = round(limF,2)
    return str(limF)

l = [0, 0, 1, 1, oo, -oo]; symbL = ['-0', '+0', '1-0', '1+0', '∞', '-∞']


class Limes1(Exercise):
    
    preamble = titel('Limes 1 - Grenzwerte von gebrochenrationalen Funktionen')

    def parameters(self):
        p1 = polynom(rd.randint(2,3))
        p2 = p1
        while p2 == p1:
            p2 = polynom(rd.randint(2,3))
        f = p1/p2
        i = rd.randint(0, len(l)-1)
        a = l[i]
        symbA = symbL[i]
        limF = getLim(f, x, a)
        return {'f': f, 'symbA': symbA, 'limF': limF}

    def problem(self, limF):
        return Problem('''
        Bestimmen Sie den Grenzwert der Funktion $f(x) = <<f:latex>>~~~~$ für $~~$
        $x → <<symbA:latex>>~~~$(Genauigkeit >= 2 NK-Stellen)\\
        Use the infinity symbol ∞\n\n
        $lim f(x)_{x→<<symbA:latex>>} =$ <<limF_>>''',
        limF_=String()
        )

    def scores(self, limF, limF_):
        score = 0
        if limF_ in ['-∞' ,'∞', '-']:
            score = limF_ == limF
        else:
            try: score =  round(float(limF_),2) == float(limF)
            except: pass
        return (score, 1)
    


class Limes2(Exercise):
    
    preamble = titel('Limes 2 - Grenzwerte von gebrochenrationalen, trigonometrischen und Exponentialfunktionen')

    def parameters(self):
        functions = [polynom(2), polynom(3), sin(x), cos(x), exp(x)]
        f1 = rd.choice(functions)
        functions.remove(f1)
        f2 = rd.choice(functions)
        f = f1/f2
        i = rd.randint(0, len(l)-1)
        a = l[i]
        symbA = symbL[i]
        limF = getLim(f, x, a)
        return {'f': f, 'symbA': symbA, 'limF': limF}

    def problem(self, symbA, limF):
        return Problem('''
        Bestimmen Sie den Grenzwert der Funktion $f(x) = <<f:latex>>~~~~$ für $~~$
        $x →<<symbA:latex>>~~~$(Genauigkeit >= 2 NK-Stellen)\\
        Use the infinity symbol ∞$~~~~$\\
        Falls kein Grenzwert existiert, geben Sie "$-$" ein.\n\n
        $lim f(x)_{x→<<symbA:latex>>} =$ <<limF_>>''',
        limF_=String()
        )
        
    def scores(self, limF, limF_):
        return Limes1().scores(limF, limF_)
    
