from pyrope import *

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sympy.solvers import solve
from sympy import Symbol, Add, diff
from scipy.integrate import quad

#Large lightgrey font for preamble
def titel(txt):
    return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'

#Gefülltes Polygon mit Polynom plotten
def plotGraph(P, coeff=[]):
    n = len(P)
    fig, axes = plt.subplots(figsize=(4, 4))
    axes.set_aspect('equal')
    plt.grid(True)
    X = []; Y = []
    for i in range (n):
        x = [P[i][0], P[(i+1)%n][0]]
        y = [P[i][1], P[(i+1)%n][1]]
        X.append(P[i][0])
        Y.append(P[i][1])
        plt.plot(x, y, 'b-', linewidth=2)
    labels = ['A','B','C','D', 'E']
    i = 0
    for x,y in zip(X,Y):
        label = labels[i]; i+=1
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    #Figur füllen:
    X.append(P[0][0]) #1.Punkt nochmal ans Ende
    Y.append(P[0][1])
    plt.fill(X, Y, 'lightcyan')
    xVal = []; yVal = []
    for p in P: 
        xVal.append(p[0])
        yVal.append(p[1])
    if len(coeff) > 0: #Kurve plotten
        X = np.arange(min(xVal)-.1, max(xVal)+.2, .1)
        Y = []
        for x in X:
            y = 0
            for i in range (len(coeff)):
                y += coeff[i]*x**(len(coeff)-1-i)
            Y.append(y)
        plt.plot(X, Y, 'r-', linewidth=1)
    plt.xlim([min(xVal)-.2, max(xVal)+.2])
    minY = max(min(Y), min(yVal)-0.5*(max(yVal)-min(yVal)))
    maxY = min(max(Y), max(yVal)+0.5*(max(yVal)-min(yVal)))
    plt.ylim([minY-.2, maxY+.2])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xticks(np.arange(min(xVal), max(xVal)+1, 1))
    plt.yticks(np.arange(minY//1, maxY//1+1, 1))
    plt.title(str(n)+'-Eck mit Polynom', fontsize = 9)
    return fig

###################################################################################################################    
#mögliche Richtungsvektoren für Polygongrenzen    
vectors = [[1,0],[4,1],[2,1],[1,1],[1,2],[1,4],
          [0,1],[-1,4],[-1,2],[-1,1],[-2,1],[-4,1],
          [-1,0],[-4,-1],[-2,-1],[-1,-1],[-1,-2],[-1,-4],
          [0,-1],[1,-4],[1,-2],[1,-1],[2,-1],[4,-1]]
###################################################################################################################
def getPhi(v1,v2): #Winkel zwischen 2 Vektoren (math. positiv) im Gradmaß
    return 180/np.pi*np.arccos(np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2))


#Erzeugt konvexes n-Eck (n<=5) mit ganzzahligen Eckpunkten und
#Steigungen die ganzzahlige Vielfache von 0.25 sind
def makePolygon(n):
    def nextPoints(vonbis, lastPoint):
        Vecs = []
        Points = []
        for v in vectors[vonbis[0]:vonbis[1]]:
            for f in range (1,3):
                P = [lastPoint[0]+f*v[0], lastPoint[1]+f*v[1]]
                if -10<P[0]<10 and -10<P[1]<10:
                    Vecs.append(v)
                    Points.append(P)
        return Vecs, Points
    def noEquals(P):
        xVal = []
        for p in P: xVal.append(p[0])
        noEquals = 1
        for i in range (len(xVal)):
            for j in range (i+1, len(xVal)):
                noEquals = noEquals*(xVal[i]!=xVal[j])
        return noEquals
    polygons = []
    for xa in range (n-5, 7-n):
        for ya in range (n-5, 7-n):
            A = [xa, ya]
            vonbis = [0, 6]
            Vecs1, Points2 = nextPoints(vonbis, A)
            for B in Points2:
                v1 = Vecs1[Points2.index(B)]
                vonbis = [vectors.index(v1)+3, (vectors.index(v1)+6)%len(vectors)]
                Vecs2, Points3 = nextPoints(vonbis, B)
                for C in Points3:
                    v2 = Vecs2[Points3.index(C)]
                    if getPhi(v1,v2) <= 150:
                        if n > 3:
                            vonbis = [vectors.index(v2)+3, (vectors.index(v2)+6)%len(vectors)]
                            Vecs3, Points4 = nextPoints(vonbis, C)
                            for D in Points4:
                                v3 = Vecs3[Points4.index(D)]
                                if getPhi(v2,v3) <= 150:
                                    if n>4:
                                        vonbis = [vectors.index(v3)+3, (vectors.index(v3)+6)%len(vectors)]
                                        Vecs4, Points5 = nextPoints(vonbis, D)
                                        for E in Points5:
                                            v4 = Vecs4[Points5.index(E)]
                                            if getPhi(v3,v4) <= 150:
                                                v5 = [xa-E[0], ya-E[1]]
                                                if np.cross(v5,v4) < 0 and np.cross(v1,v5) < 0:
                                                    if getPhi(v4,v5) <= 150 and getPhi(v5,v1) <= 150:
                                                        if noEquals([A,B,C,D,E]): #alle x-Werte verschieden
                                                            polygons.append([A,B,C,D,E]) 
                                    else: #n==4
                                        v4 = [xa-D[0], ya-D[1]]
                                        if np.cross(v4,v3) < 0 and np.cross(v1,v4) < 0:
                                            if getPhi(v3,v4) <= 150:
                                                if noEquals([A,B,C,D]): #alle x-Werte verschieden
                                                    polygons.append([A,B,C,D])
                        else:
                            v3 = [xa-C[0], ya-C[1]]
                            if getPhi(v2,v3) <= 150 and getPhi(v3,v1) <= 150:
                                polygons.append([A,B,C])
    polygon = rd.choice(polygons)
    return polygon


#Vektoren und Geradengleichungen der Polygongrenzen
def getBorders(P):
    V = []
    mn = []
    for i in range (len(P)):
        vx = P[(i+1)%len(P)][0] - P[i][0]
        vy = P[(i+1)%len(P)][1] - P[i][1]
        V.append([vx, vy])
        try:
            m = vy/vx
            n = P[i][1] - m*P[i][0]
            mn.append([round(m,2),round(n,2)])
        except:
            mn.append(P[i][0]) #Anstieg inf
    return V, mn

#Geradengleichungen für Ausgabetext
def getGln(V, mn):
    li = []
    re = []
    for i in range (len(V)):
        if V[i][0]==0:
            li.append('x')
            re.append(str(mn[i]))
        else:
            li.append('y')
            if mn[i][0] != 0:
                re.append(str(mn[i][0]) + 'x ' + (mn[i][1] >= 0)*'+'+str(mn[i][1]))
            else:
                re.append(str(mn[i][1]))
    return [li, re]

#Umfang
def getPeri(V):
    u = 0
    for v in V:
        u += np.linalg.norm(v)
    return u

#aus n Punkten Polynom vom Grad n-1 bestimmen (n<=5)
def getPolynom(points):
    xVal = []; yVal = []
    for p in points:
        xVal.append(p[0])
        yVal.append(p[1])
    M = []
    n = len(points)
    for i in range (n):
        M.append([])
        for j in range (n):
            M[-1].append(xVal[i]**(n-1-j))
    detM = np.linalg.det(M)
    adjM = []
    for i in range (n):
        adjM.append([])
        for j in range (n):
            Mij = []
            for ii in range (n):
                if ii !=i:
                    Mij.append([])
                    for jj in range (n):
                        if jj != j:
                            Mij[-1].append(M[ii][jj])              
            adjM[-1].append((-1)**(i+j)*np.linalg.det(Mij)/detM)
    adjM = np.transpose(adjM)
    coeff = (5-n)*[0]+list(np.dot(adjM,yVal))
    return coeff, xVal, yVal

#Flächeninhalt Polygon
def getArea(P):
    vecs = []
    dists = []
    for i in range (1, len(P)):
        v = [P[i][0]-P[0][0], P[i][1]-P[0][1]]
        vecs.append(v)
        dists.append(np.linalg.norm(v))
    angles = []
    f = 0
    for i in range (2, len(P)):
        angl = getPhi(vecs[i-2], vecs[i-1])
        angles.append(angl)
        f += 0.5*dists[i-2]*dists[i-1]*np.sin(np.pi/180*angl)
    return f

x = Symbol('x')

#Define Input Field
F = Real(atol = 0.000500000001, widget=Text(width = 6))
P = Vector(count = 2, widget=Text(width = 6))

###################################################################################################################

class Polygon3 (Exercise):

    preamble = titel('Polygone 1 - Dreiecke')

    def parameters(self, points = makePolygon(3)):
        V, mn = getBorders(points) #Vektoren und Geradengleichungen
        u = getPeri(V)
        f1 = getArea(points)
        coeff, xVal, yVal = getPolynom(points)
        
        pNames = 'ABCDE'
        namedPoints = []
        for i in range (len(points)):
            namedPoints.append(points[i] + [pNames[i]])
        namedPoints.sort()
        p1 = namedPoints[0][:2] #Punkt ganz links
        p2 = namedPoints[-1][:2] #Punkt ganz rechts
        notUsed, g = getBorders([p1,p2])
        S = [namedPoints[0][2], namedPoints[-1][2]]
        f = np.dot(coeff, [x**4, x**3, x**2, x, 1])
        ES = solve(diff(f, x), x) #Extremstellen
        WS = solve(diff(diff(f, x)), x) #Wendestellen
        xSP = solve(f-(g[0][0]*x + g[0][1]), x) #Schnittstellen f mit g
        for l in [ES, WS, xSP]:
            for i in range (len(l)): #Typ sympy.core.add.Add --> float 
                l[i] = complex(l[i]).real
            l.sort()
        d = [10000,10000] #aus xSP Streckenendpunkte raussuchen...
        for i in range(len(xSP)):
            d[0] = min(abs(xSP[i]-p1[0]), d[0])
            d[1] = min(abs(xSP[i]-p2[0]), d[1])
        for i in range(len(xSP)): #..und einsetzen
            if abs(xSP[i]-p1[0])==d[0]: #Anfangspkt
                xSP[i] = p1[0]
                i0 = i
            elif abs(xSP[i]-p2[0])==d[1]: #Endpkt
                xSP[i] = p2[0]
                break
            else: xSP[i] = round(xSP[i], 3)
        xSP = xSP[i0:i+1] #nur Schnittpunkte in Strecke verwenden
        func = lambda x: coeff[-1] + coeff[-2]*x + coeff[-3]*x**2 + coeff[-4]*x**3 + coeff[-5]*x**4 - (g[0][0]*x + g[0][1])
        f2 = 0
        for i in range (len(xSP)-1): #f2 zusammenstückeln
            f2 += abs(quad(func, xSP[i], xSP[i+1])[0])
        param = {'points': points, 'V': V, 'mn': mn, 'U': round(u,3), 'F1': round(f1,3),
                'S': S[0]+S[1], 'F2': round(f2,3), 'D_': [], 'E_': [], 'C3_': 0,  'C4_': 0, 
                'ES': [round(es, 3) for es in ES], 'WS': [round(ws, 3) for ws in WS], 
                'fbPlot': plotGraph(points, coeff)}
        keys = [['A', 'B', 'C', 'D', 'E'], ['C0', 'C1', 'C2', 'C3', 'C4']]
        vals = [points, coeff]
        for i in range (len(points)): param.update({keys[0][i]: vals[0][i], keys[1][i]: round(vals[1][-i-1], 3)})
        return param
    
    def problem(self, points, V, mn):
        f='A'
        n = len(points)
        def gpg(n): #Geraden, Punkte, Gleichung
            [li,re] = getGln(V, mn)
            geraden = '$g_1:~'+li[n-1]+'='+re[n-1]+'~~~~~~~~$'
            pNames = 'ABCDE'
            punkte = ''
            pots = ['','$~x$ + ','$~x^2$ + ','$~x^3$ + ','$~x^4$ + ']
            gleichung = '\n\n'
            for i in range (n):
                if i < n-1:
                    geraden += '$g_'+str(i+2)+':~'+li[i]+'='+re[i]+'~~~~~~~~$'
                punkte += '$'+pNames[i]+'=g_'+str(i+1)+'∩ g_'+str((i+2)%(n+1)+(i==n-1))+'=$ <<'+pNames[i]+'_>>'
                if i < n-1:
                    punkte += '$~~~~~~~~$'
                gleichung = '<<C'+str(i)+'_>>'+pots[i] + gleichung
            punkte += '\n\n'
            gleichung = '$y=f(x)=$ '+gleichung
            return geraden, punkte, gleichung
        
        t1 = ['Dreiecks','konvexen Vierecks','konvexen Fünfecks']
        geraden, punkte, gleichung = gpg(n)
        return  Problem (f'''
        Bestimmen Sie die Eckpunkte des {t1[n-3]}, das durch folgende Geraden begrenzt wird:\n\n
        {geraden}\n\n{punkte}
        Bestimmen Sie ferner den Umfang $U$ sowie den Flächeninhalt $F_1$ des {t1[n-3]} (Genauigkeit >= 3 NK-Stellen)\n\n
        $U =$ <<U_>>$~~~~~F_1 =$ <<F1_>>\n\n
        Durch die Eckpunkte des {t1[n-3]} verlaufe ein Polynom {n-1}. Grades. 
        Die Funktionsgleichung lautet (Genauigkeit >= 3 NK-Stellen):\n\n {gleichung}\n\n
        Berechnen Sie die Extremstellen $ES$ sowie die Wendestellen $WS$ von $f(x)$!\n\n
        $ES =$ <<ES_>> $~~~~~WS =$ <<WS_>> (jeweils eine - ggf. leere -  Liste, Genauigkeit >= 3 NK-Stellen)\n\n
        Berechnen Sie zum Schluss noch den Inhalt $F_2$ der Fläche, die vom Graphen von f(x) '''
        'und der Strecke $\\overline{<<S:latex>>}$ begrenzt wird! (Genauigkeit >= 3 NK-Stellen)\n\n' 
        '$F_2 =$ <<F2_>>',
        A_ = P, B_ = P, C_ = P,
        U_ = F, F1_ = F, F2_ = F,
        C2_ = F, C1_ = F, C0_ = F,
        ES_ = List(widget=Text(width = 20)), WS_ = List(widget=Text(width = 20))
        )
    
    def hints(self):
        return 'Alle Eckpunkte haben ganzzahlige Koordinaten'
    
    def scores(self, ES_, WS_, ES, WS):
        plt.close()
        if ES_ is not None: ES_.sort()
        if WS_ is not None: WS_.sort()
        return {'ES_': ES_==ES, 'WS_': WS_==WS}
        
    def feedback(self):
        return '<<fbPlot>>'     

    
class Polygon4(Polygon3):

    preamble = titel('Polygone 2 - Vierecke')
   
    def parameters(self):
        param = Polygon3().parameters(makePolygon(4))
        return param
    
    def problem(self, points, V, mn):
        ifields = Polygon3().problem(points, V, mn).ifields
        ifields.update(D_ = P, C3_ = F)
        return  Problem (Polygon3().problem(points, V, mn).template, **ifields)
    
    def hints(self, S):
        return ['Alle Eckpunkte haben ganzzahlige Koordinaten',
                'Berechnen Sie die fehlende Schnittstelle mittels Polynomdivision',
                f'Bilden Sie die Differenzfunktion von f(x) und der Geraden, die durch {S[0]} und {S[1]} verläuft!',
                'Diese hat 3 Nullstellen, von denen 2 ($x_{01}$ und $x_{02}$) gegeben sind',
                'Die dritte erhalten Sie, indem Sie die Differenzfunktion durch '+
                'die Binome $(x-x_{01})$ und $(x-x_{02})$ dividieren']
        

class Polygon5(Polygon3):

    preamble = titel('Polygone 3 - Fünfecke')
   
    def parameters(self):
        param = Polygon3().parameters(makePolygon(5))
        return param
    
    def problem(self, points, V, mn):
        ifields = Polygon4().problem(points, V, mn).ifields
        ifields.update(E_ = P, C4_ = F)
        return  Problem (Polygon3().problem(points, V, mn).template, **ifields)

    def hints(self):
        return ['Alle Eckpunkte haben ganzzahlige Koordinaten',
                'Gehen Sie vor wie in den Hinweisen zu Aufgabe 2 beschrieben',
                'Sie erhalten nach 2-maliger Polynomdivision ein Polynom 2. Grades',
                'Mit der pq-Formel berechnen Sie dann die fehlenden beiden Schnittstellen']