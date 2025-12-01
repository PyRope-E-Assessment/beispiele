from pyrope import *

import random as rd
import math

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

I8 = Int(widget = Text(width = 8))

class Combi1(Exercise):
    
    preamble = titel('Combinatorics for Beginners - 1: Geradewegs zur Lösung ')

    def parameters(self):
        s = rd.choice([1,1,1,1,1,2,2,2,2,3,3,3,4,4,5])
        l = rd.randint(5, 10-s)
        z = []
        for i in range (s,s+l): z.append(i)
        R = (int(l/2) + (int(l/2)!=l/2 and int(s/2)==s/2))*math.factorial(l-1)
        return {'s': s, 'l': l, 'z': str(z)[1:-1], 'R': R}

    def problem(self):
        return  Problem ('''
        Gegeben sind die Ziffern $<<z:latex>>.$\\
        Wieviele verschiedene gerade Zahlen, in denen jede Ziffer 
        genau einmal vorkommt, lassen sich aus diesen Ziffern bilden?\n\n
        Lösung: <<R_>>''',
        R_= I8
        )


class Combi2(Exercise):
    
    preamble = titel('Combinatorics for Beginners - 2: Wortschöpfer')

    def parameters(self):
        l = rd.choice([5,6,6,7,7,7,8,8,8,8,9,9,9,9,9,9])
        a = rd.randint(1, l-2)
        b = rd.randint(1, l-a-1)
        c = l - a - b 
        R = int(math.factorial(l)/(math.factorial(a)*math.factorial(b)*math.factorial(c)))
        return {'l': l, 'a': a, 'b': b, 'c': c, 'R': R}

    def problem(self):
        return  Problem ('''
        Wieviele verschiedene "Wörter" kann man mit folgenden Buchstaben bilden: 
        $~~~<<a:latex>>$ x "A",   $<<b:latex>>$ x "B",  $ <<c:latex>>$ x "C" ?\\
        Es sollen immer alle $<<l:latex>>$ Buchstaben verwendet werden.\n\n
        Lösung: <<R_>>''',
        R_= I8
        )


class Combi3(Exercise):
    
    preamble = titel('Combinatorics for Beginners - 3: Dreierei')
    
    def parameters(self):
        s = rd.choice([1,1,1,1,1,2,2,2,2,3,3,3,4,4,5])
        l = rd.randint(5, 10-s)
        z = []
        for i in range (s,s+l): z.append(i)
        listR = [24, 48, 78, 120, 180]
        R = listR[l-5]        
        return {'z': str(z)[1:-1], 'R': R}

    def problem(self):
        return  Problem ('''
        Gegeben sind die Ziffern $<<z:latex>>.~~~~$
        Man betrachte alle 3-stelligen Zahlen, die sich aus je 3 von diesen Ziffern bilden lassen.\\
        Wieviele der so gebildeten Zahlen sind durch 3 teilbar?\n\n
        Lösung: <<R_>>''',
        R_= I8
        )


class Combi4(Exercise):
    
    preamble = titel('Combinatorics for Beginners - 4: Fakultäten')
    
    def parameters(self):
        fak = rd.choice(["Informatik", "Digitale Transformation", "Medien"])
        n = rd.randint(10,50)
        p = 1 - math.factorial(365)/(365**(n)*math.factorial(365-n))
        return {'fak': fak, 'n': n, 'p': round(p, 3)}
    
    def problem(self):
        return  Problem ('''
        An der Fakultät $<<fak:latex>>$ studieren $<<n:latex>>$ Personen.\\
        Wir nehmen an, dass niemand am Schalttag (29.02.) Geburtstag hat, es sich nicht um ein Schaltjahr handelt und 
        dass die Geburtstage in dieser Personengruppe übers Jahr gleichverteilt sind. 
        Wie groß ist die Wahrscheinlichkeit, dass an mindestens einem Tag 
        mindestens 2 Personen Geburtstag haben?  (Genauigkeit mind. 3 NK-Stellen)\n\n
        Lösung: <<p_>>''',
        p_= Real(atol=.000500001, widget = Text(width = 12))
        )
                    
    def hints(self):
        return 'Berechnen Sie die Wahrscheinlichkeit des Gegenereignisses'        
           

class Combi5(Exercise):
    
    preamble = titel('Combinatorics for Beginners - 5: noch mehr Fakultäten')
    
    def parameters(self):
        p = int(rd.randint(2,9))*10
        for n in range(14, 42):
            if 1 - math.factorial(365)/(365**(n)*math.factorial(365-n)) >= p/100:
                break
        return {'p': p, 'n': n}
    
    def problem(self):
        return  Problem ('''
        Wieviele Personen müssen mindestens an einer der o.g. Fakultäten studieren, damit die Wahrscheinlichkeit 
        für das in Aufgabe 4 beschriebene Ereignis mindestens $<<p:latex>>$ % beträgt?\n\n
        Lösung: <<n_>>''',
        n_= I8
        )

    