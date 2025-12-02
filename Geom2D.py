from pyrope import *

import matplotlib.pyplot as plt
import random as rd
import numpy as np
import math
from sympy import symbols, Symbol, solve
from fractions import Fraction as frac
from numpy.linalg import norm


#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'
    
x, y = symbols('x, y')


#Output Txt
prTxt1_1 = ['Gegeben sind die 3 Geraden', 'Given the 3 lines']
prTxt1_2 = ['Bestimmen Sie die 3 Schnittpunkte der Geraden! (Alle Koordinaten sind ganzzahlig)', 'Find the 3 intersection points of the lines!']
prTxt2 = ['Berechnen Sie nun den Flächeninhalt des Dreiecks. (Genauigkeit >= 2 NK-Stellen)', 'Now compute the area of the triangle']
prTxt3 = ['Berechnen Sie den Schwerpunkt SP sowie Mittelpunkt M und Radius r des Umkreises des Dreiecks. (Genauigkeit >= 2 NK-Stellen)',
          'Compute the centroid SP as well as circumcenter M and radius r of the circumcircle of the triangle!']

def getSlope(p1,p2):
    return frac((p2[1]-p1[1]),(p2[0]-p1[0]))

def isValid(p1, p2, p3):
    valid = p1[0] != p2[0] and p1[0] != p3[0] and p2[0] != p3[0]
    valid *= (abs(p1[0]-p3[0]) + abs(p1[1]-p3[1]) > 2)
    valid *= (abs(p2[0]-p1[0]) + abs(p2[1]-p1[1]) > 2)
    valid *= (abs(p3[0]-p2[0]) + abs(p3[1]-p2[1]) > 2)
    return valid

def minWinkel(triangle):
    phi = []
    [p1, p2, p3] = triangle
    [a1,b1] = [[p2[0]-p1[0], p2[1]-p1[1]], [p3[0]-p1[0], p3[1]-p1[1]]]
    [a2,b2] = [[p1[0]-p2[0], p1[1]-p2[1]], [p3[0]-p2[0], p3[1]-p2[1]]]
    [a3,b3] = [[p1[0]-p3[0], p1[1]-p3[1]], [p2[0]-p3[0], p2[1]-p3[1]]]
    ab = [[a1,b1], [a2,b2],[a3,b3]]
    for [a, b] in ab:
        phi.append(np.arccos(np.dot(a,b)/(norm(a)*norm(b)))*180/np.pi)
    return min(phi)

def makeTriangle(dim):
    listX = list(np.arange(dim[1]))
    listY = list(np.arange(dim[1]))   
    XY = []
    for x in listX:
        for y in listY:
            XY.append([x,y])
    Triangles = []
    for i in range(len(XY)):
        for j in range(i+1, len(XY)):
            for k in range(j+1, len(XY)):
                   [p1, p2, p3] = [XY[i], XY[j], XY[k]]
                   if isValid(p1, p2, p3):
                       if minWinkel([p1, p2, p3]) > 15:
                           Triangles.append([p1, p2, p3])
    return rd.choice(Triangles)
  
def plotTriangle():
    figure, axes = plt.subplots(figsize=(3, 3))
    axes.set_aspect(1)
    for k in range (3):
        plt.plot([X[k],X[(k+1) % 3]], [Y[k],Y[(k+1) % 3]], 'b', linewidth=2)
    plt.plot(X,Y,'ro')
    plt.title('Correct Triangle',fontsize=9)
    return figure, axes

def plotCircle(M,r):
    figure, axes = plotTriangle()
    plt.plot(M[0],M[1],'r+')
    angle = np.linspace( 0 , 2 * np.pi , 150 ) 
    x = M[0] + r * np.cos( angle ) 
    y = M[1] + r * np.sin( angle )
    axes.plot( x, y, 'g' )
    plt.title('Triangle with Circumcircle', fontsize=9)
    return figure

    
def lRound(L,k): #Round all elements of a list to k dec. places
    for i in range (len(L)):
        L[i] = round(L[i], k)
    return L

dp2 = 0.005000000001 #dec. places

lan = 0


class Geometry_2D_1(Exercise):

    preamble = titel('Lines and Triangles 1:')  
                     
    def parameters(self):
        global P, X, Y
        dim = [5,5]
        P = makeTriangle(dim)
        X = [P[0][0], P[1][0], P[2][0]]
        Y = [P[0][1], P[1][1], P[2][1]]
        lines = []
        for k in range (3):
            slope = getSlope(P[k], P[(k+1)%3])
            intercept = P[k][1] - slope*P[k][0]
            lines.append([slope, intercept])
        g1 = lines[0][0]*x + lines[0][1]
        g2 = lines[1][0]*x + lines[1][1]
        g3 = lines[2][0]*x + lines[2][1]
        figure, axes = plotTriangle()
        return {'g1': g1, 'g2': g2, 'g3': g3, 'P': P, 'P1': P[0], 'P2': P[1], 'P3': P[2], 'fbPlot1': figure}    
    
    def problem(self):
        P = List(count = 2, widget = Text(width = 8))
        return  Problem (
        prTxt1_1[lan] + '$~~~~g_1:~y(x)=$ <<g1>>$~~~~~~~g_2:~y(x)=$ <<g2>>$~~~~~~~g_3:~y(x)=$ <<g3>>\n\n'
        + prTxt1_2[lan] + '\n\n$P_1 =$ <<P1_>>$~~~~P_2 =$ <<P2_>>$~~~~P_3 =$ <<P3_>>',
        P1_ = P, P2_ = P, P3_ = P
        )
        
    def scores(self, P, P1_, P2_, P3_):
        P_ = [P1_, P2_, P3_]
        score = 0
        pTmp = P.copy()
        for p in P_:
           if p in pTmp:
              score += 1
              pTmp.remove(lRound(p,0))
        return score
    
    def feedback(self):
        return '<<fbPlot1>>'
        

class Geometry_2D_2(Exercise):

    preamble = titel('Lines and Triangles 2:')
    
    def parameters(self):
        a = np.sqrt((X[0]-X[1])**2 + (Y[0]-Y[1])**2)
        b = np.sqrt((X[1]-X[2])**2 + (Y[1]-Y[2])**2)
        [m1, m2] = [(Y[0]-Y[1])/(X[0]-X[1]), (Y[1]-Y[2])/(X[1]-X[2])]
        if m1*m2 == -1: Phi = np.pi/2
        else: Phi = abs(np.arctan((m2 - m1)/(1 + m1*m2)))
        F = .5*a*b*np.sin(Phi)
        return {'F': round(F,2)}    

    def problem(self, F):
        return  Problem (
        prTxt2[lan] + '\n\n$F =$ <<F_>>',
        F_ = Real(atol = dp2, widget = Text(width = 8))
        )
    

class Geometry_2D_3(Exercise):

    preamble = titel('Lines and Triangles 3:')

    def parameters(self):
        #Schwerpunkt SP:
        A = [X[0], Y[0]]
        mBC = [(X[1]+X[2])/2, (Y[1]+Y[2])/2]
        SP = lRound([A[0]/3 + 2/3*mBC[0], A[1]/3 + 2/3*mBC[1]], 2)
        #Mittelsenkrechte:
        AB = [X[1]-X[0], Y[1]-Y[0]]
        mAB = [(X[0]+X[1])/2, (Y[0]+Y[1])/2]
        AB_orth = [AB[1], -AB[0]]
        BC = [X[2]-X[1], Y[2]-Y[1]]
        BC_orth = [BC[1], -BC[0]]
        #Schnittpkt M:
        #mAB[0] + s1*AB_orth[0] == mBC[0] + s2*BC_orth[0]
        #mAB[1] + s1*AB_orth[1] == mBC[1] + s2*BC_orth[1]
        #s1 = (mBC[1] + s2*BC_orth[1] - mAB[1])/AB_orth[1]
        s2 = Symbol('s2')
        valS2 = solve(mAB[0] + ((mBC[1] + s2*BC_orth[1] - mAB[1])/AB_orth[1])*AB_orth[0] - (mBC[0] + s2*BC_orth[0]))
        s = float(valS2[0]) #sonst <class 'sympy.core.numbers.Float'>
        M = lRound([mBC[0] + s*BC_orth[0], mBC[1] + s*BC_orth[1]], 2)
        r = round(math.sqrt((M[0]-A[0])**2 + (M[1]-A[1])**2),2)
        return {'SP': SP, 'M': M, 'r': r, 'fbPlot2': plotCircle(M, r)}    
    
    def problem(self, SP, M, r):
        V = Vector(orientation = 'row', count = 2, atol = dp2, widget = Text(width = 12))
        return  Problem (
        prTxt3[lan] + '\n\n$SP =$ <<SP_>>$~~~~~~~M =$ <<M_>>$~~~~~~~r =$ <<r_>>',
        SP_ = V, M_ = V, r_ = Real(atol = dp2, widget = Text(width = 8))
        )

    def feedback(self, M, r):
        return '<<fbPlot2>>'
    