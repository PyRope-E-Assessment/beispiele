from pyrope import *

import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

person = ['Fußgänger', 'Jogger', 'Radfahrer', 'Mopedfahrer', 'Autofahrer']
speed =  [[2,5],       [5, 10],  [10,20],     [30,50],       [60,100]]

class Meeting1(Exercise):
    
    preamble = titel('Begegnung 1')

    def parameters(self):
        l = rd.randint(20,60)
        [P1, P2] = rd.sample(person, 2)
        v1 = rd.randint(speed[person.index(P1)][0], speed[person.index(P1)][1])
        v2 = rd.randint(speed[person.index(P2)][0], speed[person.index(P2)][1])
        t0 = [rd.randint(6,20), rd.randint(1,5)*10]
        t = round(l/(v1+v2)*60)
        M = round(v1*t/60,3)
        return {'l': l, 'P1': P1, 'v1': v1, 'P2': P2, 'v2': v2, 'h0': t0[0], 'm0': t0[1], 't': t, 'M': M}

    def problem(self):
        return  Problem('''
        Zwischen den Orten Altdorf und Beerfeld verläuft die geradlinige 
        Beerfelder Chaussee mit einer Länge von $<<l:latex>>$ km.\\ 
        Um $<<h0:latex>>$:$<<m0:latex>>$ Uhr startet in Altdorf ein $<<P1:latex>>$ 
        und bewegt sich mit einer konstanten Geschwindigkeit von $<<v1:latex>>$ km/h in Richtung Beerfeld.\\
        Aus Beerfeld kommt ihm mit $<<v2:latex>>$ km/h ein $<<P2:latex>>$ entgegen, 
        der dort zum gleichen Zeitpunkt gestartet ist.\\
        Nach wieviel Minuten und an welcher Stelle treffen sich die beiden auf der Beerfelder Chaussee ?\n\n
        Sie treffen sich nach <<t_>> Minuten (ganze Min)$~~~~~$in <<M_>> km Entfernung von Altdorf. 
        (Genauigkeit mind. 3 NK-Stellen)''',
        t_=Int(widget = Text(width = 7)),
        M_=Real(atol = 0.0005000001, widget = Text(width = 7))
        )


class Meeting2(Exercise):
    
    preamble = titel('Begegnung 2')

    def parameters(self):
        def min2places(m):
            return (m<10)*'0' + str(m)
        [P1, P2] = ['Fußgänger', 'Autofahrer']#rd.sample(person, 2)
        if person.index(P1) <= 1 and person.index(P2) <= 1: #2 Läufer-nicht überfordern
           l = rd.randint(10,20) 
        else: l = rd.randint(20,60)
        v1 = rd.randint(speed[person.index(P1)][0], speed[person.index(P1)][1])
        v2 = rd.randint(speed[person.index(P2)][0], speed[person.index(P2)][1])
        t01 = [rd.randint(6,18), rd.randint(1,5)*10] #Startzeit 1 in [h, min]
        min01 = t01[0]*60 + t01[1] ##Startzeit 1 in min
        first = max(0,int(min01 - (l-5)/v2*60))
        latest = min(int(min01 + (l-5)/v1*60),24*60)
        if person.index(P1) <= 1 or person.index(P2) <= 1: #Läufer nicht überfordern
            first = max(first, min01 - 60)
            latest = min(latest, min01 + 60)
        min02 = rd.randint(first, latest)
        t02 = [int(min02/60), min02 - int(min02/60)*60]
        tT = (l + min01/60*v1 + min02/60*v2)/(v1 + v2) #Treffzeit in Stunden
        hT = int(tT) #Treffzeit ganze Stunden
        minT = round((tT - hT)*60) #Treffzeit restl. Minuten
        s1 = (tT - min01/60)*v1
        s2 = (tT - min02/60)*v2
        if minT==60: [hT, minT] = [hT+1, 0] #Rundungsfehler von Python ausbügeln
        return {'l': l, 'P1': P1, 'v1': v1, 'P2': P2, 'v2': v2, 'h01': t01[0], 'm01': t01[1],
                'h02': t02[0], 'm02': min2places(t02[1]), 'h': hT, 'm': min2places(minT), 's': round(s1,3)}

    def problem(self):
        return  Problem('''
        Zwischen den Orten Angelbach und Baumweiler verläuft die geradlinige 
        Angelbacher Landstraße mit einer Länge von $<<l:latex>>$ km.\\
        Um $<<h01:latex>>$:$<<m01:latex>>$ Uhr startet in Angelbach ein $<<P1:latex>>$ 
        und bewegt sich mit einer konstanten Geschwindigkeit von $<<v1:latex>>$ km/h in Richtung Baumweiler.\\
        Aus Baumweiler kommt ihm mit $<<v2:latex>>$ km/h ein $<<P2:latex>>$ entgegen, 
        der dort um $<<h02:latex>>$:$<<m02:latex>>$ Uhr gestartet ist.\\
        Um welche Uhrzeit und an welcher Stelle treffen sich die beiden auf der Angelbacher Landstraße ?\n\n
        Sie treffen sich um <<h_>> : <<m_>> Uhr (ganze Min)$~~~~~$
        in <<s_>> km Entfernung von Angelbach.$~~~$(Genauigkeit mind. 3 NK-Stellen)''',
        h_=Int(widget = Text(width = 3)),
        m_=String(widget = Text(width = 3)),
        s_=Real(atol = 0.0005000001, widget = Text(width = 7))
        )
        
    def scores(self, h_, h, m_, m):
        correctTime = 0
        if h_ != None and m_ != None:
            correctTime = (h_==h) and (m_ == m or (m[0]=='0' and m_==m[1]))
        return {'h_': correctTime, 'm_': correctTime}
