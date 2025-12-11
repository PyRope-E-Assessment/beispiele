from pyrope import *

import matplotlib.pyplot as plt
import random as rd
import numpy as np
from sympy import symbols
import numbers

lan = 0 #Sprache 0=D 1=E

def titel(txt):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

tTxt =  [['Eigenschaften der Rosenbrock Funktion', 'Properties of the Rosenbrock Function'],
         ['Rosenbrock Funktion: Gradientenverfahren mit Armijo','Rosenbrock Function: Gradient Method with Armijo Rule'],
         ['Verallgemeinerte Rosenbrock Funktion: Gradientenverfahren mit Armijo', 'Generalized Rosenbrock Function: Gradient Method with Armijo Rule']]

prTxt1 = [['Bestimmen Sie den kritischen Punkt der Rosenbrock-Funktion ', 'Find the critical point of the Rosenbrock Function '],
         ['Berechnen Sie die Hesse-Matrix der Funktion!', 'Calculate the Hesse matrix of the function!'],
         ['\n\nBestimmen Sie die Eigenwerte der Hesse-Matrix $w=[w_1, w_2]$ und den daraus folgenden Typ des kritischen Punktes  (Min/ Max/ S)!',
          '\n\nDetermine the eigenvalues of the Hesse matrix $w=[w_1, w_2]$ and the consequential type of the critical point $ (Min/ Max/ S)!$']]

prTxt2 = [['Gegeben ist die Rosenbrock-Funktion ', 'Given is the Rosenbrock Function '],
          ['Führen Sie den ersten Schritt des Gradientenverfahrens mit dem Startpunkt ',
           'Execute the first step of Gradient Method with start point '],
          [''' aus!\\
           Bestimmen Sie dafür zuerst mittels Armijo-Verfahren die Schrittweite $\\sigma$.\n\n''',
           '$~~~~~$For this purpose first determine by Armijo Rule the step size $\\sigma$.\n\n']]

prTxt3 = ['Gegeben ist die verallgemeinerte Rosenbrock-Funktion ', 'Given is the generalized Rosenbrock Function ']

prTxtF1 = '$~~~~~~~~$(Format: [x, y])\n\n'
prTxtF2 = '$~~~~~~~~$((Format: [[ , ], [ , ]])\n\n'

x, y = symbols('x, y')

def F(a,b,x,y):
    return b*(y-x**2)**2 + (a-x)**2

def nablaF(a,b,x,y):
    return [-4*b*x*(y-x**2) - 2*(a-x), 2*b*(y-x**2)]
        
def getParam(a, b, x0, y0):
    f = b*(y-x**2)**2 + (a-x)**2
    beta = .5
    gamma = 10**(-4)
    left = 1; right = 0
    i = 0
    while left > right:
        sigma =  beta**i
        left = F(a, b, x0 - sigma*nablaF(a,b,x0,y0)[0], y0 - sigma*nablaF(a,b,x0,y0)[1]) - F(a,b,x0,y0)
        right = sigma*gamma*(-nablaF(a,b,x0,y0)[0]**2-nablaF(a,b,x0,y0)[1]**2)
        i+=1
    x1 = round(x0 - sigma*nablaF(a,b,x0,y0)[0],4)
    y1 = round(y0 - sigma*nablaF(a,b,x0,y0)[1],4)
    return f, sigma, [x1, y1]

def plotFunc(coeffs, pKrit, env):
    x = np.outer(np.linspace(pKrit[0]-env[0], pKrit[0]+env[0], 20), np.ones(20))
    y = np.outer(np.linspace(pKrit[1]-env[1], pKrit[1]+env[1], 20), np.ones(20)).T
    [a,b] = coeffs
    R = b*(y-x**2)**2 + (a-x)**2
    fig = plt.figure(figsize=(6, 4))
    ax = plt.axes(projection ='3d')
    ax.plot_surface(x, y, R, cmap ='viridis', edgecolor ='yellow')
    ax.set_title('Rosenbrock-Funktion',fontsize = 9)
    return fig


#Weg von Startpkt bis krit. Punkt in 2d plotten, Startpkt und 1. Pkt rot markieren
def plotXY(a, b):
    [x,y] = [a-2.2, a**2] #Startpkt
    eps = 10**(-3)
    beta = .5
    gamma = 10**(-4)
    k=1
    X = [x]; Y = [y]  #Liste der Zielwerte aller Schritte
    while np.linalg.norm(nablaF(a,b,x,y)) > eps:
        i = 0
        left = 1; right = 0
        while left > right:
            sigma =  beta**i
            left = F(a,b,x - sigma*nablaF(a,b,x,y)[0], y - sigma*nablaF(a,b,x,y)[1]) - F(a,b,x,y)
            right = sigma*gamma*(-nablaF(a,b,x,y)[0]**2-nablaF(a,b,x,y)[1]**2)
            i+=1
        [x,y] = [x - sigma*nablaF(a,b,x,y)[0], y - sigma*nablaF(a,b,x,y)[1]]
        X.append(x); Y.append(y)
        k+=1
    fig = plt.figure(figsize=(3, 2))
    plt.plot(X,Y,'-b')
    plt.plot(X[:2],Y[:2],'ro')
    plt.plot(X[-1],Y[-1],'go')
    plt.title('Rosenbrock Gradient Method  ' + str(k-1) + ' Steps', fontsize = 9)
    return fig


class Rosenbrock1(Exercise):
    
    preamble = titel(tTxt[0][lan])

    def parameters(self):
        f = 100*(y-x**2)**2 + (1-x)**2
        H = [[801, -400], [-400, 200]]
        w, v = np.linalg.eig(H); w = [round(w[0],1), round(w[1],1)]
        pType = 'Min'
        return {'f': f, 'pKrit': [1,1], 'H': H, 'w': w, 'pType': pType, 'fbPlot': plotFunc([1,100], [1,1], [.1,1])}

    def problem(self):
        return Problem(f'''
        {prTxt1[0][lan]}$f(x,y) =$ <<f>>. {prTxtF1}
        $pKrit = $ <<pKrit_>>$~~~~$\n\n
        {prTxt1[1][lan]} {prTxtF2}
        $H(f(pKrit)) = $ <<H_>> $~~~~$\n\n
        {prTxt1[2][lan]}\n\n
        $w = $ <<w_>> $~~~$(round to X.X)$~~~~~~~~~~Type(pKrit):~~~$<<pType_>>''',
        pKrit_= Vector(count=2, sub_dtype=numbers.Integral, widget = Text(width = 8)),
        H_ = Matrix(nrows=2, ncols=2, sub_dtype=numbers.Integral),
        w_ = Vector(count=2, sub_dtype=numbers.Real, widget = Text(width = 12)),
        pType_ = String(widget=RadioButtons('Min', 'Max', 'S', vertical=False))
        )

    def feedback(self):
        return '<<fbPlot>>'
    

class Rosenbrock2(Rosenbrock1):
    
    preamble = titel(tTxt[1][lan])
    
    def parameters(self):
         [a,b] = [1,100]
         [x0,y0] = [-1.2, 1] #Startpkt
         f, sigma, xy1 = getParam(a, b, x0, y0)
         return {'f': f, 'sigma': sigma, 'xy1': xy1, 'fbPlot': plotXY(1, 100)}

    def problem(self):
        return Problem(f'''
        {prTxt2[0][lan]}$f(x,y) =$ <<f>>.\n\n
        {prTxt2[1][lan]}$[x_0, y_0] = [-1.2, 1]$ {prTxt2[2][lan]}
        $\\sigma = $ <<sigma_>>$~~~~~~~[x_1,y_1]$ =  <<xy1_>> (round to at least X.XXXX)''',
        sigma_= Real(),
        xy1_ = Vector(count=2, sub_dtype=numbers.Real, atol = 0.00005000001)
        )


class Rosenbrock3(Rosenbrock2):
    
    preamble = titel(tTxt[2][lan])

    def parameters(self):
        [a,b] = [rd.randint(1,3), rd.randint(1,100)]
        [x0,y0] = [a-2.2, a**2] #Startpkt
        f, sigma, xy1 = getParam(a, b, x0, y0)
        return {'f': f, 'sigma': sigma, 'xy1': xy1, 'a': a, 'b': b, 'start': [round(a-2.2,1), a**2], 'fbPlot': plotXY(a, b)}

    def problem(self):
        return Problem(f'''
        {prTxt3[lan]} $f(x,y) =$ <<f>>.\n\n
        {prTxt2[1][lan]} $[x_0, y_0] = <<start:latex>>$ {prTxt2[2][lan]}\n\n
        $\\sigma = $ <<sigma_>>$~~~~~~~[x_1,y_1]$ =  <<xy1_>> (round to at least X.XXXX)''',
        sigma_= Real(),
        xy1_ = Vector(count=2, sub_dtype=numbers.Real, atol = 0.00005000001)
        )
