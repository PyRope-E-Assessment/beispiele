from pyrope import *

import matplotlib.pyplot as plt
import random as rd
import numpy as np
from sympy import symbols, diff, integrate, simplify, sqrt, sin, cos, exp, asin, acos, ln

#Large lightgrey font for preamble
def titel(txt):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x, y = symbols('x, y')

def makeFunction():
    def polynom(): #Polynom 2. Grades
        [m, n, r] = [rd.choice([-1,1])*rd.randint(1,2), rd.randint(-4,4), rd.randint(-5, 5)]
        p = m*(x-n)**2 + r
        ab = [min(0,n), max(0,n,abs(2/m))]
        return  p, ab, [round(ab[0],3), round(ab[1],3)], (-1)**(n>0)*sqrt((x-r)/m) + n
    def sinus():
        [m,n] = [rd.choice([-1,1])*rd.randint(1,3), rd.randint(1,3)]
        return  m*sin(n*x), [-np.pi/2/n, np.pi/2/n],\
                ['\\frac{-\\pi}{'+str(2*n)+'}', '\\frac{\\pi}{'+str(2*n)+'}'], asin(x/m)/n
    def cosinus():
        [m,n] = [rd.choice([-1,1])*rd.randint(1,3), rd.randint(1,3)]
        endInt = '\\frac{\\pi}{'+str(n)+'}'
        if n==1: endInt = '\\pi'
        return  m*cos(n*x), [0, np.pi/n], [0, endInt], acos(x/m)/n
    def expo():
        [m,n] = [rd.randint(1,3), rd.randint(1,3)]
        return  m*exp(n*x), [1, 2], [1,2], ln(x/m)/n
    options = {0: polynom(), 1: sinus(), 2: cosinus(), 3: expo()}
    return options[rd.randint(0,2)]

#Function plot    
def plotFct(f, ab, uf=None, nr=1):
    X = list(np.arange(ab[0], ab[1], .01))
    Y = []
    for i in range(len(X)):
        Y.append(f.evalf(subs={x: X[i]}))
    fig, ax = plt.subplots(figsize=(3, 3))
    plt.axis('equal')
    plt.grid()
    plt.plot([min(-1,X[0]-1), max(-1, X[-1]+1)],[0,0],'-k') #x-Achse
    plt.plot([0,0],[min(-1, min(Y)-1),max(0-np.sign(max(Y)), max(Y)+1)],'-k') #y-Achse
    plt.plot(X,Y,'-b',label='f(x)') #f
    if nr==1: plt.fill([X[0]] + X + [X[-1]], [0] + Y + [0], color='gray', alpha = 0.3)
    elif nr==3: plt.fill([0] + X + [0], [Y[0]] + Y + [Y[-1]], color='gray', alpha = 0.3)
    if uf != None:
        X = list(np.arange(min(Y), max(Y), .01))
        uY = []
        for i in range(len(X)):
            uY.append(uf.evalf(subs={x: X[i]}))
        plt.plot([min(-1, min(Y)-1), max(-1,  max(Y)+1)],[0,0],'-k') #x-Achse
        plt.plot([0,0],[min(-1, X[0]-1, min(uY)-1), max(-1, X[-1]+1, max(uY)+1)],'-k') #y-Achse
        plt.plot([min(-1, min(Y)-1), max(-1, max(Y)+1), 1],[min(-1, min(Y)-1), max(-1,  max(Y)+1), 1], color='gray') #y = x
        plt.plot(X,uY,'-g',label='$\\overline{f}(x)$') #uf
    plt.legend()
    return fig

def plotFig(fct, ab, title):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # Make data
    phi = np.linspace(0, 2 * np.pi, 100)
    X = np.linspace(ab[0], ab[1], 100)
    f = np.zeros(100)
    for i in range (len(X)):
        f[i] = float(fct.evalf(subs={x: X[i]}))
    Y = np.outer(f, np.cos(phi))
    Z = np.outer(f, np.sin(phi))
    X = np.outer(X, np.ones(np.size(phi)))
    ax.plot_surface(X, Y, Z, cmap ='viridis')
    plt.xlabel('x'); plt.ylabel('y')
    plt.title(title)
    return fig


class RotationX(Exercise):

    preamble = titel('Volumen von Rotationskörpern - Rotation um die x-Achse')
    
    def parameters(self):
        fct, ab, ab4Out, noNeed = makeFunction()
        figure = (x**2-y**2)**.5
        env = [[ab[0], ab[1]], [ab[0], ab[1]]]
        F = np.pi*integrate(fct**2)
        V = float(F.evalf(subs={x: ab[1]}) - F.evalf(subs={x: ab[0]}))
        figTitle = 'Rotation of f(x) around the x-Axis'
        return {'f': fct, 'ab': ab4Out, 'V': round(V,3), 'fbPlot': plotFct(fct, ab), 
                'figPlot': plotFig(fct, ab, figTitle)}
            
    def problem(self, ab):
        return Problem('<<fbPlot>>\n\n'
        'Berechnen Sie das Volumen $V$ des Körpers, der durch die Rotation der Funktion '
        '$f(x) = <<f:latex>>~~~$ im Intervall $['+ str(ab[0]) + ', ' + str(ab[1]) +']$ '
        'um die x-Achse entsteht\n\n$V =$ <<V_>> $~~~$(Genauigkeit >= 3 NK-Stellen)',
        V_ = Real(atol = 0.0005000000001, widget = Text(width = 10))
        )
        
    def feedback(self):
        return '<<figPlot>>'


class Inverse(Exercise):

    preamble = titel('Umkehrfunktionen')
    
    def parameters(self):
        fct, ab, ab4Out, ufct = makeFunction()
        figure = (x**2-y**2)**.5
        env = [[ab[0], ab[1]], [ab[0], ab[1]]]
        return {'f': fct, 'ab': ab4Out, 'ufct': ufct, 'fbPlot': plotFct(fct, env[0], ufct, 2)}
            
    def problem(self, ab):
        return Problem('<<fbPlot>>'
        '\n\nBilden Sie die Umkehrfunktion $\\overline{f}$ der Funktion $f(x) = <<f:latex>>$ '
        'im Intervall $['+ str(ab[0]) + ', ' + str(ab[1]) +']$\n\n'
        '$\\overline{f} =$ <<ufct_>>',
        ufct_ = Expression(symbols='x')
        )


class RotationY(Exercise):

    preamble = titel('Volumen von Rotationskörpern - Rotation um die y-Achse')
    
    def parameters(self):
        fct, ab, ab4Out, ufct = makeFunction()
        figure = (x**2-y**2)**.5
        env = [[ab[0], ab[1]], [ab[0], ab[1]]]
        F = np.pi*integrate(ufct**2)
        borders = [float(fct.evalf(subs={x: ab[0]})), float(fct.evalf(subs={x: ab[1]}))]; borders.sort()
        V = float(F.evalf(subs={x: borders[1]}) - F.evalf(subs={x: borders[0]}))
        figTitle = 'Rotation of $\\overline{f}(x)$ around the x-Axis'
        return {'f': fct, 'ab': ab4Out, 'V': round(V,3), 'fbPlot': plotFct(fct, env[0], ufct, 3), 
                'figPlot': plotFig(ufct, borders, figTitle)}

    def problem(self, ab):
        return Problem('<<fbPlot>>\n\n'
        'Berechnen Sie das Volumen $V$ des Körpers, der durch die Rotation der Funktion '
        '$f(x) = <<f:latex>>$ im Intervall $['+ str(ab[0]) + ', ' + str(ab[1]) +']$ '
        'um die y-Achse entsteht\n\n$V =$ <<V_>> $~~~$(Genauigkeit >= 3 NK-Stellen)',
        V_ = Real(atol = 0.0005000000001, widget = Text(width = 10))
        )
        
    def feedback(self):
        return '<<figPlot>>'