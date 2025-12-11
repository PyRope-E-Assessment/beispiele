from pyrope import *

import random as rd
import numpy as np
from numpy import pi
from sympy import Symbol, sign, sqrt, sin, cos
import matplotlib.pyplot as plt


#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x = Symbol('x')

def getPos(r, l, s):
    if s <= l/4:
        phi = s/(l/2)*pi
        yM = r*sin(phi)
        xM = r - r*cos(phi)
    elif s<= l/2:
        phi = pi - s/(l/2)*pi
        yM = r*sin(phi)
        xM = r + r*cos(phi)
    elif s<= 3/4*l:
        phi = (s-l/2)/(l/2)*pi
        yM = -r*sin(phi)
        xM = 3*r - r*cos(phi)
    else:
        phi = pi - (s-l/2)/(l/2)*pi
        yM = -r*sin(phi)
        xM = 3*r + r*cos(phi)
    return xM, yM

def plotGraph(f, ab, M):
    X = list(np.arange(ab[0], ab[1]+.1, .1))
    Y = []
    for xi in X:
        Y.append (f.evalf(subs={x: xi}))
    #print(ab,Y)
    figure, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='major')
    plt.plot(X,Y,'b')
    for i, name in enumerate(['A', 'B']):
        plt.plot(ab[i], 0, 'go')
        plt.annotate(name, (ab[i], 0))
    plt.plot(M[0], M[1], 'r*')
    plt.annotate('M', (M[0], M[1]))
    plt.title('Wriggle')
    return figure

D_ = Real(atol = 0.0005000001, widget = Text(width = 7))


class Meeting1(Exercise):
    
    preamble = titel('Begegnung auf dem Fluss 1')
    
    def parameters(self):
        def valT(i, l):
            valT = [restTime, l/(v[1]+v[2]), restTime, l/(v[0]+v[2])]
            return valT[i]
        L = rd.randint(7,15)*1000 #Gesamtstrecke in m
        restTime = rd.randint(1, 3) #Ruhezeit Vogel
        v = [rd.randint(10, 20), rd.randint(3, 6)]
        v.append(rd.randint(max(v[0],v[1])+2, 24))
        v = [vi *1000/3600 for vi in v] ##Geschw. Ruderachter, Kajak, Vogel in m/sec
        tM = L/(v[0] + v[1])
        posM = tM * v[0]
        sBird = 0
        i = 0
        l = L
        while l > 0:
            t = valT(i, l)
            s = [v[0]*t, v[1]*t, (v[2]*t)*(i%2==1)]
            sBird += s[2]
            l = l - s[0] - s[1] #Reststrecke
            i += 1; i = i%4 
        return {'L': int(L/1000), 'v1': int(v[0]*3.6),  'v2': int(v[1]*3.6), 'v3': int(v[2]*3.6), 'rT': restTime, 'tM': round(tM/60), 'pM': round(posM/1000,3), 's': round(sBird/1000,3)}

    def problem(self):
        return  Problem('''
        An einem auf dieser Strecke geradlinig verlaufenden Fluss liegen die Orte Aaldorf und Barschbach 
        im Abstand von $<<L:latex>>$ km. In Aaldorf fährt ein Ruderachter los und strebt mit $<<v1:latex>>$ km/h 
        flussaufwärts in Richtung Barschbach, wo zum gleichen Zeitpunkt ein Urlauber im Kajak startet und 
        mit $<<v2:latex>>$ km/h gemächlich flussabwärts treibt.\n\n Ein kleiner Vogel hat sich auf der Spitze 
        des Ruderbootes niedergelassen und fliegt $<<rT:latex>>$ sec nach Fahrtbeginn auf und mit einer 
        konstanten Geschwindigkeit von $<<v3:latex>>$ km/h flussaufwärts davon, bis er auf das 
        entgegenkommende Kajak trifft, dort für $<<rT:latex>>$ sec verweilt und in Richtung Ruderboot 
        zurückfliegt, wo er wiederum $<<rT:latex>>$ sec ausruht und so fort, bis die beiden Boote sich begegnen 
        und der Vogel erschöpft auf die nächste Uferweide zusteuert.\n\n
        Berechnen Sie Zeit und Ort des Zusammentreffens der Boote, und die Gesamtstrecke, 
        die der Vogel in dieser Zeit zurückgelegt hat !\n\n
        Sie treffen sich nach <<tM_>> min $~~~$ in <<pM_>> km  Entfernung von Aaldorf\n\n
        Der Vogel ist in dieser Zeit <<s_>> km geflogen. $~~~~$
        (Ganze Minuten, Entfernungsangaben auf mind. 3 NK-Stellen gerundet)''',
        tM_ = Int(widget = Text(width = 4)),
        pM_ = D_,
        s_ = D_
        )


class Meeting2(Exercise):
    
    preamble = titel('Begegnung auf dem Fluss 2')

    def parameters(self):
        def min2places(t):
            return (t<10)*'0' + str(t)
        v1 = rd.randint(6, 14)
        v2 = rd.randint(20, 30)
        t01 = [rd.randint(6,18), rd.randint(1,5)*10]
        min01 = t01[0]*60 + t01[1]
        r = rd.randint(5,10)
        l = 2*pi*r
        first = max(0,int(min01 - (l-5)/v2*60))
        latest = min(int(min01 + (l-5)/v1*60),24*60)
        min02 = rd.randint(first, latest)
        t02 = [int(min02/60), min02 - int(min02/60)*60]
        s = (min02 - min01 + l/v2*60)/(1/v1 + 1/v2)/60
        t = min01 + (s/v1*60) #in Minuten
        h = int(t/60) #Stunden
        m = round(t - 60*h) #Minuten
        if m==60: [h, m] = [h+1, 0] #Rundungsfehler von Python ausbügeln
        f = sign(2*r-x)*sqrt(r**2 - (x - r*(2 + sign(x-2*r)))**2)
        showF = [sign(2*r-x), sqrt(r**2 - (x - r*(2 + sign(x-2*r)))**2)]
        xM, yM = getPos(r, l, s)
        return {'l': l, 'v1': v1, 'v2': v2, 'xB': 4*r, 'yB': 0, 
                'h01': t01[0], 'm01': t01[1], 'h02': t02[0], 'm02': min2places(t02[1]),
                'f': f, 'showF0': showF[0], 'showF1': showF[1],
                'xM': round(float(xM),3), 'yM': round(float(yM),3),
                'h': h, 'm': min2places(m),
                'fig': plotGraph(f, [0, 4*r], [xM, yM])}

    def problem(self):
        return  Problem('''
        Durch die Berglandschaft eines nicht näher bezeichneten Landes windet sich der Fluß *Wriggle* 
        entsprechend folgender Funktionsgleichung:\n\n$y = <<showF0:latex>>\\cdot<<showF1:latex>>$\n\n
        An der Position $[0,0]$ liegt der Ort *Apesburg*, in  $[<<xB:latex>>, <<yB:latex>>]$  
        der Flecken *Barracudawater*. Ein Motorboot startet um $<<h01:latex>>:<<m01:latex>>$ Uhr 
        in Apesburg und fährt mit $<<v1:latex>>$ km/h flussaufwärts in Richtung Barracudawater.\n\n
        Um $<<h02:latex>>:<<m02:latex>>$ Uhr startet in Barracudawater ein Schnellboot und fährt 
        mit $<<v2:latex>>$ km/h flussabwärts. Die beiden kommen just im selben Moment in der 
        Poststation *Mosquito Place* an, die auch am Wriggle liegt.\n\n
        Wo liegt Mosquito Place? [ <<xM_>>, <<yM_>>] $~~~$ ([x, y], Genauigkeit >= 3 NK-Stellen) $~~$ und...\n\n
        wann treffen sich die beiden Boote dort? <<h_>>: <<m_>> $~~~$ (ganze Minuten) ''',
        xM_ = D_,
        yM_ = D_,
        h_ = Int(widget = Text(width = 3)),
        m_ = String(widget = Text(width = 3))
        )
       
    def scores(self, xM_, xM, yM_, yM, h_, h, m_, m):
        plt.close()
        correctPlace = 0
        if xM_ is not None and yM_ is not None:
            correctPlace = (round(xM_,3)==xM) and (round(yM_,3)==yM)
        correctTime = 0
        if h_ is not None and m_ is not None:
            correctTime = (h_==h) and (m_ == m or (m[0]=='0' and m_==m[1]))
        return {'xM_': correctPlace, 'yM_': correctPlace, 'h_': correctTime, 'm_': correctTime}

    def feedback(self):
        return '<<fig>>'