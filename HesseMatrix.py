from pyrope import *

import matplotlib.pyplot as plt
import random as rd
import numpy as np
from sympy import symbols

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

tTxt = ['Bestimmung eines lokalen Extremums mit Hesse Matrix', 'Determining of a local extremum by Hesse matrix']

prTxt = [['Bestimmen Sie den kritischen Punkt der Funktion ', 'Find the critical point of function '],
         ['Entscheiden Sie nun mithilfe der Hesse-Matrix, ob ein lokales Minimum, Maximum oder ein Sattelpunkt vorliegt.',
          'Decide now by means of the Hesse matrix, if there is a local minimum, maximum or saddle point.'],
         ['\n\nBestimmen Sie dafür zunächst die Eigenwerte der Hesse-Matrix: ',
          '\n\nTherefor first determine the eigenvalues of the Hesse matrix: ']]

x, y = symbols('x, y')

def randomFunc(n):
    coeff = []
    for i in range(n):
        coeff.append(rd.choice([-1,1])*rd.randint(1, 6))
    return coeff

def plotFunc(coeffs, pKrit):
    env = 10 #Umgebung lokales Min
    x = np.outer(np.linspace(pKrit[0]-env, pKrit[0]+env, 20), np.ones(20))
    y = np.outer(np.linspace(pKrit[1]-env, pKrit[1]+env, 20), np.ones(20)).T
    [a,b,c,d,e] = coeffs
    z = a*x**2+b*y**2+c*x*y+d*x+e*y
    fig = plt.figure(figsize=(6, 4))
    ax = plt.axes(projection ='3d')
    ax.plot_surface(x, y, z, cmap ='viridis', edgecolor ='yellow')
    ax.set_title('Surface plot f(x,y)', fontsize=9)
    return fig

lan = 0


class Hesse(Exercise):

    preamble = titel(tTxt[0])
    
    def parameters(self):
        pKrit = []
        while pKrit == []:
            coeff = randomFunc(5)
            [a,b,c,d,e] = coeff
            f = a*x**2+b*y**2+c*x*y+d*x+e*y
            if not c**2 == 4*a*b:
                xKrit = (2*b*d - c*e)/(c**2 - 4*a*b)
                yKrit = -(2*a*xKrit + d)/c
                pKrit = [round(xKrit,3),round(yKrit,3)]
                H = np.array([[2*a, c], [c, 2*b]])
                w, v = np.linalg.eig(H)
                w = [round(w[0],3), round(w[1],3)]
                if np.prod(w) < 0:
                    pType = 'S'
                elif w[0] <= 0 and w[1] <= 0:
                    pType = 'Max'
                else:
                    pType = 'Min'
        return {'f': f, 'pKrit': pKrit, 'w': w, 'pType': pType, 'coeff': coeff, 'fbPlot': plotFunc(coeff, pKrit)}
            
    def problem(self):
        return Problem(f'''
        {prTxt[0][lan]} $~~~f(x,y) = <<f:latex>>~~~~$(Format: [x, y] / [ ])\n\n
        pKrit = <<pKrit_>> $~~~$ (Genauigkeit mind. 3 NK-Stellen)\n\n
        {prTxt[1][lan]}$~~~~$(Min/ Max/ S){prTxt[2][lan]}$~~~~$<<w_>>  $~~~$ 
        (Genauigkeit mind. 3 NK-Stellen)(Format: [w1, w2])\n\n
        Type pKrit:$~~~$<<pType_>>''',
        pKrit_= List(widget=Text(width = 12)),
        w_ = List(count=2, widget=Text(width = 12)),
        pType_ = String(widget=RadioButtons('Min', 'Max', 'S', vertical=False))
        )

    def scores(self, w, w_):
        score = 0
        wTmp = w.copy()
        if len(w_) == 2:
            for i in [0,1]:
                if round(w_[i],3) in wTmp:
                    score +=1
                    wTmp.remove(round(w_[i],3))
        return {'w_': score}
    
    def feedback(self):
        return '<<fbPlot>>'