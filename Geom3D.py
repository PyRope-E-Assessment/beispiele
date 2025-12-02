from pyrope import *

import random as rd
import numpy as np
from sympy import symbols, solve, simplify#, latex

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x, y, z, s = symbols('x, y, z, s')

#3 nicht kollineare Punkte erstellen
def makePoints():
    p1 = []
    for i in [0,1,2]:
        p1.append(rd.randint(-9,9))
    p2 = p1.copy() 
    while p1 == p2:#[0]==p2[0] and p1[1]==p2[1] and p1[2]==p2[2]:
        for i in [0,1,2]:
            p2[i] = rd.randint(-9,9)
    p3 = p2.copy();  s = 1
    while (p3[0]-p1[0]) == s*(p2[0]-p1[0]) and (p3[1]-p1[1]) == s*(p2[1]-p1[1]) and (p3[2]-p1[2]) == s*(p2[2]-p1[2]):
        for i in [0,1,2]:
            p3[i] = rd.randint(-9,9)
            try:
                s = (p3[i]-p1[i])/(p2[i]-p1[i])
            except:
                pass
    return [p1, p2, p3]
        
#Normalenvektor bilden
def normV(points):
    [p1, p2, p3] = points
    return np.cross(np.array(p2)-np.array(p1), np.array(p3)-np.array(p1))

def isInIntv(val,borders):
    isIn = min(borders) <= val <= max(borders)
    return isIn

def lRound(L,k): #Round all elements of a list to k dec. places
    for i in range (len(L)):
        L[i] = round(L[i], k)
    return L

dp2 = 0.005000000001 #2 dec. places

#global points1, points2, points3

class Geometry_3D_1(Exercise):
    
    preamble = titel('Compiling plane equation in vector form ax + by + cz = d')

    def parameters(self):
        global points1, nv, d
        points1 = makePoints()
        nv = list(normV(points1))
        d = np.dot(points1[0], nv)
        strE = str(nv[0])+'\\*'+'x'+int(nv[1]>=0)*'+'+str(nv[1])+'\\*'+'y'+int(nv[2]>=0)*'+'+str(nv[2])+'*'+'z'
        return {'P1': points1[0], 'P2': points1[1], 'P3': points1[2], 'd': d, 'E': nv[0]*x+nv[1]*y+nv[2]*z, 'strE': strE}

    def problem(self):
        return Problem ('''
        Find the equation of the plane containing the points:
        $~~~~~~P_1=<<P1:latex>>~~~~~P_2 = <<P2:latex>>~~~~~P_3 = <<P3:latex>>$\n\n
        Insert only left side of equation ax + by + cz = d, such that d = $<<d:latex>>$.\n\n
        $E:~~~$ <<E_>> $= <<d:latex>>$''',
        E_= Expression(symbols='x, y, z')
        )
        
    def scores(self, E_, E):
        return simplify(E_ - E) == 0


class Geometry_3D_2(Exercise):

    preamble = titel('Plane and Line:')
 
    def parameters(self):
        global points2, IP
        [a,b,c] = nv
        #2 außerhalb der Ebene in unterschiedlichen R3-Hälften liegende Punkte ergänzen:
        p4 = []; p5 = []
        for i in range(3):
            p4.append(round(points1[0][i] + nv[i]))
            p5.append(round(points1[1][i] - nv[i]))
        points2 = points1.copy()
        points2.append(p4)
        points2.append(p5)
        g = []
        for i in range (3):
            g.append(points2[3][i] + s*(points2[4][i] - points2[3][i]))
        valS = float(solve(a*g[0] + b*g[1] + c*g[2] -d, s)[0])
        IP = []
        for i in range (3):
            IP.append(points2[0][i] + valS*(points2[1][i] - points2[0][i]))
        E = nv[0]*x+nv[1]*y+nv[2]*z
        return {'E': E, 'P4': points2[3], 'P5': points2[4], 'IP': lRound(IP,2)}
    
    def problem(self):       
        return  Problem ('''
        Find the intersection $P_I$ of the line $g$ given by the points $P_4 = <<P4:latex>>$ 
        and $P_5 = <<P5:latex>>$ and the Plane $E.~~~$
        Round to at least 2 decimal places.\n\n
        $P_I =$ <<IP_>>''',
        IP_ = Vector(orientation = 'row', count = 3, atol = dp2)
        )


class Geometry_3D_3(Exercise):

    preamble = titel('2 Planes:')

    def parameters(self):
        P = points1[0]
        points3 = points2.copy()
        points3.append(P)
        nv2 = list(np.round(normV(points3[3:]),2))
        slopeH = list(np.cross(nv,nv2))
        i = 0
        while slopeH[i] == 0 and i<2: i+=1
        Q = slopeH[i]
        for j in range(3):
            slopeH[j] = round(slopeH[j]/Q,2)
        return {'P': P, 'points3': points3, 'nv2': nv2, 'IP': IP, 'slopeH': slopeH}
   
    def problem(self):
        return  Problem ('''
        Find the intersection line $h$ of plane $E$ with the plane $F$, 
        given by line $g$ und the point $P = <<P:latex>>$
        in 2-point form h: P0 + s$\\cdot$(P1 - P0).\\
        Round to at least 2 decimal places.\n\n
        $h:~~~<<P:latex>> + s\\cdot$ <<slopeH_>>''',
        slopeH_ = Vector(orientation = 'row', count = 3, atol = dp2, compare = 'up_to_multiple'),
        )

