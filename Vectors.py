from pyrope import *

import random as rd
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import numbers
from sympy import acos

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

def mkPoints(n, dim): #n verschiedene Punkte
    P=[]
    while len(P) < n:
        p = [rd.randint(0,9), rd.randint(0,9), rd.randint(0,9)][:dim]
        if p not in P: #alle verschieden
            P.append(p)
    return P

def mkVectors(n, dim=2): #n verschiedene Punkte P(i) und Vektoren P(i+1)-P(i)
    P = mkPoints(n, dim)
    while len(P) < n:
        p = [rd.randint(0,9), rd.randint(0,9), rd.randint(0,9)][:dim]
        if p not in P: #alle verschieden
            P.append(p)
    vectors = []
    for k in range(len(P)-1):
        vectors.append([P[k+1][i]-P[k][i] for i in range (len(P[0]))])
    return P, vectors

def vec23(V): #Spaltenvektor 2/3-dim
    V = [str(xi) for xi in V]
    hasNeg = any(['-' in xi for xi in V])
    maxLen = max([len(xi) for xi in V])
    V = [(maxLen-len(str(xi)))*'~' + (hasNeg and '-' not in xi)*'~~' +str(xi) for xi in V]
    if len(V)==2:
        return '$\\large{(}^{'+V[0]+'}_{'+V[1]+'}\\large{)}$'
    return '$\\Biggl(\\begin{matrix}'+V[0]+'~\\\\'+V[1]+'\\\\'+V[2]+'\\end{matrix}\\Biggl)$'

def plotVectors1(XY, title):
    fig, axes = plt.subplots(figsize=(3, 3))
    axes.set_aspect('equal')
    plt.grid()
    X = []; Y = []
    for point in XY:
        X.append(point[0]); Y.append(point[1])
    names = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6'][:len(X)]
    
    plt.plot(X,Y,'ro')
    for i, txt in enumerate(names):
        axes.annotate(txt, (X[i], Y[i]))
        if i < len(names)-1:
            plt.arrow(X[i],Y[i],X[i+1]-X[i],Y[i+1]-Y[i], width=0.02,
                      head_width=0.2, length_includes_head=True, ec='b') 
    plt.title(title, fontsize=9)
    return fig
    
def plotVectors2(P, title):
    fig, axes = plt.subplots(figsize=(3, 3))
    axes.set_aspect('equal')
    plt.grid()
    names = [['P0', 'P1'],[ 'P2', 'P3'], ['P4', 'P5']]
    for pointPair in P:
        X = []; Y = []
        X.append(pointPair[0][0]); Y.append(pointPair[0][1])
        X.append(pointPair[1][0]); Y.append(pointPair[1][1])
        plt.plot(X,Y,'ro')
        for i, txt in enumerate(names[P.index(pointPair)]):
            axes.annotate(txt, (X[i], Y[i]))
        plt.arrow(X[0],Y[0],X[1]-X[0],Y[1]-Y[0], width=0.02,
                  head_width=0.3, length_includes_head=True, ec='b')
    plt.title(title, fontsize=9)  
    return fig

def vec23(V): #Spaltenvektor 2/3-dim
    V = [str(xi) for xi in V]
    hasNeg = any(['-' in xi for xi in V])
    maxLen = max([len(xi) for xi in V])
    V = [(maxLen-len(str(xi)))*'~' + (hasNeg and '-' not in xi)*'~~' +str(xi) for xi in V]
    if len(V)==2:
        return '$\\large{(}^{'+V[0]+'}_{'+V[1]+'}\\large{)}$'
    return '$\\Biggl(\\begin{matrix}'+V[0]+'~\\\\'+V[1]+'\\\\'+V[2]+'\\end{matrix}\\Biggl)$'

PV_ = Vector(count = 2, orientation = 'column',  sub_dtype=numbers.Integral, widget = Text(width = 10))


class Vektors1(Exercise):

    preamble = titel('Vektoren 1')
    
    def parameters(self):
        V = [[0,0]]
        while V[0][0] == 0:
            V, noNeed = mkVectors(1)
        V = V[0]
        return {'V': V, 'nV': round(norm(V),3), 'm': round(V[1]/V[0],3), 'gV': [-V[0], -V[1]]} 
            
    def problem(self, V):
        return Problem(f'''
        Bestimmen Sie Betrag (Länge), Richtung und Gegenvektor des Vektors $V = ${vec23(V)}. 
        Geben Sie die Richtung durch den Anstieg m an.\n\n
        |V| = <<nV_>> (3 NK_Stellen) $~~~~~~~$m = <<m_>> (3 NK_Stellen) $~~~~~~~$-V = <<gV_>>''',
        nV_ = Real(atol = 0.000500000001, widget = Text(width = 10)),
        m_ = Real(atol = 0.000500000001, widget = Text(width = 10)),
        gV_ = PV_
        )
    

class Vectors2(Exercise):

    preamble = titel('Vektoren 2')  
                     
    def parameters(self):
        n = rd.randint(4,6)
        XY, vectors = mkVectors(n)
        return {'XY': XY, 'P0': [XY[0][0],XY[0][1]], 'vectors': vectors, 'n': n-1,
                'P': [XY[-1][0], XY[-1][1]], 'fbPlot1': plotVectors1(XY, 'Vectors 1')}    
                
    def problem(self, vectors, n):
        vecs = '$~~~$'
        for i in range(len(vectors)): vecs += f'{vec23(vectors[i])},$~~~$'
        return  Problem ('''
        Gegeben sind die Vektoren '''+vecs[:-6]+'''$~~~$und der Punkt $P_0 = <<P0:latex>>.~~$\n\n
        Addieren Sie die Vektoren ausgehend vom Punkt $P_0$ 
        und bestimmen Sie den Zielpunkt $P_{<<n:latex>>}$ !\n\n
        $P_{<<n:latex>>} =$ <<P_>>''',
        P_ = PV_
        )
    
    def feedback(self):
        return '<<fbPlot1>>'
    

class Vectors3(Exercise):

    preamble = titel('Vektoren 3')
    
    def parameters(self):
        n=2
        P = []
        V = []
        while len(P) < 3: #3 Punktepaare
            p, vs = mkVectors(n); v = vs[0]
            if p not in P:
                multpl = False
                for inV in V:
                    if v[0]*inV[1] == v[1]*inV[0]:
                        multpl = True; break  #Vektor gleicher Ri. schon in V
                if not multpl:
                    P.append(p)
                    V.append(v)
        c2 = (V[2][0]*V[0][1] - V[0][0]*V[2][1])/(V[1][0]*V[0][1] - V[0][0]*V[1][1]) #linCombi
        if V[0][0] == 0:
            c1 = round((V[2][1] - c2*V[1][1])/V[0][1],2)
        else:
            c1 = round((V[2][0] - c2*V[1][0])/V[0][0],2)
        c2 = round(c2,2)
        return {'P': P, 'v0': V[0], 'v1': V[1], 'v2': V[2], 'c1':c1, 'c2': c2, 'fbPlot2': plotVectors2(P, 'Vectors 2')}    
                
    def problem(self, P):
        LK_ = Real(widget = Text(width = 6))
        return  Problem (f'''
        Gegeben sind die 3 Punktepaare $~~~[P_0, P_1] ={P[0]},~~~
        [P_2, P_3] = {P[1]},~~~[P_4, P_5] = {P[2]}$\n\nBilden Sie die Vektoren\n\n'''
        '''$v_1 = \\overrightarrow{P_0P_1} = $ <<v0_>>
        $~~~~v_2 = \\overrightarrow{P_2P_3} = $ <<v1_>>
        $~~~~v_3 = \\overrightarrow{P_4P_5} = $ <<v2_>>\n\n
        Stellen Sie $v_3$ als Linearkombination von $v_1$ und $v_2$ dar!$~~~$
        (Genauigkeit >= 2 NK-Stellen)\n\n
        $v_3 =$ <<c1_>> $\\cdot v_1 + $ <<c2_>> $\\cdot v_2$''',
        v0_ = PV_, v1_ = PV_, v2_ = PV_,
        c1_ = LK_, c2_ = LK_
        )
    
    def scores(self, c1_, c2_, c1, c2):
        if c1_==None or c2_==None: return {'c1_': 0, 'c2_': 0}
        correctLC = round(c1_,2) == c1 and round(c2_,2) == c2
        return {'c1_': correctLC, 'c2_': correctLC}
    
    def feedback(self):
        return '<<fbPlot2>>'
    
    
class Vektors4(Exercise):

    preamble = titel('Vektoren 4')
    
    def parameters(self):
        [V1, V2] = 2*[3*[0]]
        while not any(np.cross(V1, V2)):
            [V1, V2], noNeed = mkVectors(2, 3)
        phi = acos(np.dot(V1, V2)/norm(V1)/norm(V2))*180/np.pi
        return {'V1': V1, 'V2': V2, 'dot': np.dot(V1, V2), 'cross': list(np.cross(V1, V2)), 'phi': int(round(phi))}
            
    def problem(self, V1, V2):
        return Problem(f'''
        Gegeben sind die Vektoren $V_1 =$ {vec23(V1)} und $V_2 =$ {vec23(V2)}. 
        Bilden Sie das Skalarprodukt $V_1 \\circ V_2$ und das Vektorprodukt $V_1 \\times V_2$.\n\n
        $~~~~~~V_1 \\circ V_2 =$  <<dot_>> $~~~~~~~~~~~~V_1 \\times V_2 =$ <<cross_>>\n\n
        Berechnen Sie den Winkel $φ$ zwischen $V_1$ und $V_2$ im Gradmaß. Runden Sie auf ganze Zahlen.\n\n
        $~~~~~~φ =$ <<phi_>> °\n\n''',
        dot_ = Int(widget = Text(width = 6)),
        cross_ = Vector(count=3, orientation = 'column', widget = Text(width = 12)),
        phi_ = Int(widget = Text(width = 4))
        )
        
    def scores(self, phi_, phi):
        return {'phi_': phi_ in [phi, 180-phi]}

