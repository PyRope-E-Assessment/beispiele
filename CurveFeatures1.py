from pyrope import *

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sympy import Symbol, diff, Eq, solve

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x = Symbol('x')

#Polynom n. Grades
def polynomial(n):
    f = rd.choice([-1, 1])*rd.randint(1,5)*x**n
    for i in range (n-1,-1,-1):
        f = f + rd.randint(-5,5)*x**i
    return  f

def noCmplx(x):
    if len(x)>1: #complex values?
        try: float(x[0])
        except: x = []
    return x

#Extremstellen
def turningPoints(f):
    xE = noCmplx(solve(Eq(diff(f),0)))
    for i in range (len(xE)):
        if np.isclose(float(diff(diff(f)).evalf(subs={x: xE[i]})), 0, rtol=0, atol=10**-100):
            xE.remove(xE[i]) #Sattelpunkt
        else:
            xE[i] = float(xE[i])
    return [round(x,2) for x in xE]

#Wendestellen
def inflectionPoint(f):
    return round(float(solve(Eq(diff(diff(f)),0))[0]),3)

def plotGraph(f, nP, tp):
    if len(nP) > 1:
        [l, r] = [min(nP)-1, max(nP)+1.1]
    else:
        [l, r] = [round(tp, 1)-3, round(tp, 1)+3.1]
    X = list(np.arange(l, r, .1))
    Y = []
    for xi in X:
        Y.append (f.evalf(subs={x: xi}))
    fig, axes = plt.subplots(figsize=(3, 3))
    axes.set_aspect('auto')
    plt.grid(True)
    plt.plot(X,Y,'b')
    plt.plot(tp, f.evalf(subs={x: tp}), 'ro')
    if len(nP) > 1:
        plt.plot(nP, [f.evalf(subs={x: nP[0]}),f.evalf(subs={x: nP[1]})], 'go')
    plt.title('Graph of f(x)', fontsize = 9)
    return fig


class curveFeatures1(Exercise):
    
    preamble = titel('Curve Features 1')

    def parameters(self):
        f = polynomial(2)
        nP = noCmplx(solve(Eq(f,0)))
        nP = [round(float(n), 2) for n in nP]; nP.sort()
        tP = turningPoints(f)[0]
        typeTp = ['Min', 'Max'][round(float(diff(diff(f)).evalf(subs={x: tP})),100) < 0]
        return {'f': f, 'nP': nP, 'tP': tP,'typeTp':typeTp, 'fbPlot1': plotGraph(f, nP, tP)}
    
   
    def problem(self):
        return Problem('''
        Find out the x values of null point(s) and turning point of a polynomial of degree 2!\n\n
        $f(x) =$ <<f>>\n\n
        The x-values of the null points of f(x) are:$~~~x_0 =$ <<nP_>>$~~~$
        Insert as list: [$x_1$, $x_2$] or [$x_0$] or []. Round to at least 2 decimal places.\n\n
        The x-value of the turning point of f(x) is:$~~~x_t =$ <<tP_>>$~~~$
        Round to at least 2 decimal places.\n\n
        What kind of turning point is it?$~~~$<<typeTp_>>''',
        nP_= List(),
        tP_= Real(atol = 0.005, widget = Text(width=8)),
        typeTp_ = String(widget=RadioButtons('Min', 'Max', vertical=False)),
        )
    
    def scores(self, nP_, nP):
        score = 2*(nP_==nP==[])
        if nP_ is not None:
            if len(nP_)==len(nP):
                for xn in nP:
                    score +=  xn in [round(xn_, 2) for xn_ in nP_]
                if len(nP)==1: score *= 2
        return {'nP_': score}

    def feedback(self):
        return '<<fbPlot1>>'


class curveFeatures2(Exercise):
    
    preamble = titel('Curve Features 2')

    def parameters(self):
        f = polynomial(3)
        tP = turningPoints(f)
        iP = inflectionPoint(f)
        return {'f': f, 'tP': tP, 'iP': iP, 'fbPlot2':plotGraph(f, tP, iP)}
    
    def problem(self):
        return Problem('''
        Find out the x values of turning points and inflection point of a polynomial of degree 3!\n\n
        $f(x) =$ <<f>>\n\n
        The x-values of the turning points of f(x) are:$~~~x_t =$ <<tP_>>$~~~$
        Insert as list: [$x_{t1}, x_{t2}$] or []. Round to at least 2 decimal places.\n\n
        The x-value of the inflection point of f(x) is:$~~~x_i =$ <<iP_>>$~~~$
        Round to at least 3 decimal places.''',
        tP_= List(),
        iP_= Real(atol=0.005, widget = Text(width=8))
        )
    
    def scores(self, tP_, tP):
        score = 2*(tP_==tP==[])
        if tP_ is not None:
            if len(tP_)==len(tP)==2:
                for xt in tP:
                    score += xt in [round(xt_, 2) for xt_ in tP_]
        return {'tP_': score}   
    
    def feedback(self):
       return '<<fbPlot2>>'
    
