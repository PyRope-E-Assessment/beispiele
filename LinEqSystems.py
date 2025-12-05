from pyrope import *

import random as rd
import numpy as np
from itertools import combinations
from sympy import symbols

x, y, z = symbols('x, y, z')

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

def pStyle(x):
    return '${:.2f}$'.format(round(x,2))+' €.'


class LinGLS1(Exercise):
    
    preamble = titel('Lineare GLS erstellen und lösen 1 - fruchtig')

    def parameters(self):
        def price():
            return round(rd.triangular(.99,4.99),1)
        [A, B, C] = [price(), price(), price()]
        mass = rd.choices([1,2,3], k=6)
        txt4Duo = ['$'+str(mass[0])+'$ kg Äpfel und $'+str(mass[1])+'$ kg Birnen kosten zusammen ',
                   '$'+str(mass[2])+'$ kg Birnen und $'+str(mass[3])+'$ kg Clementinen kosten zusammen ',
                   '$'+str(mass[4])+'$ kg Äpfel und $'+str(mass[5])+'$ kg Clementinen kosten zusammen ']
        sum4Duo = [pStyle(mass[0]*A +mass[1]* B), pStyle(mass[2]*B + mass[3]*C), pStyle(mass[4]*A + mass[5]*C)]
        clPos = rd.randint(0,2)
        txt4Duo.pop(clPos)
        sum4Duo.pop(clPos)
        r = rd.randint(2,6)*5
        sale = pStyle(2*(A + B + C)*(100-r)/100)
        return {'A': A, 'B': B, 'C': C, 'txt4Duo': txt4Duo, 'sum4Duo': sum4Duo, 'r': r, 'sale': sale}

    def problem(self, txt4Duo, sum4Duo):
        P_ = Real(widget = Text(width = 6))
        return  Problem(f'''
        Am Obststand auf dem Wochenmarkt ist heute Aktionstag.\\
        {txt4Duo[0]}{sum4Duo[0]}$~~~~${txt4Duo[1]}{sum4Duo[1]}\n\n
        Als Tagesangebot gibt es den großen Obstkorb mit je 2 kg Äpfeln, Birnen und Clementinen 
        mit $<<r:latex>>\\%$ Rabatt auf den Normalpreis für nur <<sale:latex>>\n\n
        Berechnen Sie die Einzelpreise für je 1 kg Äpfel, Birnen und Clementinen!\n\n
        Äpfel: <<A_>>$~~~~~$Birnen: <<B_>>$~~~~~$Clementinen: <<C_>>''',
        A_ = P_, B_ = P_, C_ = P_
        )


allNames = ['Anna', 'Paula', 'Clara', 'Hannes', 'Eric', 'Tom']
fNames = ['Lehmann', 'Meier', 'Schulze', 'Schmidt']
diffAge = ['älter', 'jünger']

def makePairs(names, ages):
    Det = 0
    while Det==0:
        pairs = list(combinations(np.arange(len(names)), 2))
        listPairs = []
        mtrx = [[1,1,1,1,1]]
        for i in range(len(names)-1):
            pair = [0,0]
            while ages[pair[0]]==ages[pair[1]]: #kein gleichaltriges pair
                pair = rd.choice(pairs)
            [p,q] = pair
            if rd.choice([0,1]): [q,p] = pair
            line = [0,0,0,0,0]
            line[p] = 1; line[q] = -1
            mtrx.append(line)
            pairs.remove(pair)
            listPairs.append(names[p]+' ist $'+str(abs(ages[p]-ages[q]))+'$ Jahre '\
                             +diffAge[ages[p]<=ages[q]]+' als '+names[q])
        Det = np.linalg.det(mtrx)
    return listPairs


class LinGLS2(Exercise):
    
    preamble = titel('Lineare GLS erstellen und lösen 2 - familiär')

    def parameters(self):
        V = rd.randint(40, 50)
        M = rd.randint(35, 45)
        K3 = rd.randint(3, 7); K2 = rd.randint(K3+2, K3+5); K1 = rd.randint(K2+2, 15)
        ages = [V, M, K1, K2, K3]
        sumAge = sum(ages)
        K = [K1, K2, K3]
        names = ['Vater', 'Mutter']
        spaces = [31,29]
        possNames = allNames.copy()
        for i in range (len(K)):
            names.append(possNames[rd.randint(0,len(possNames)-1)])
            spaces.append(33-2*(len(names[-1])-4))
            possNames.remove(names[-1])
        listPairs = makePairs(names, ages)
        d = {'fName': rd.choice(fNames), 'sumAge': sumAge, 'names': names, 'listPairs': listPairs}
        for i in range (len(ages)): d.update({'age'+str(i+1): ages[i]})
        return d

    def problem(self, names, listPairs):
        iF = Int(widget = Text(width = 5))
        return  Problem(f'''
        Familie $<<fName:latex>>$ besteht aus 5 Personen:$~~~$ Vater, Mutter und die 3 Kinder 
        ${names[2]}, {names[3]}$ und ${names[4]}.~~~$ Alle zusammen sind $<<sumAge:latex>>$ Jahre alt.\n\n
        {listPairs[0]}\\
        {listPairs[1]}\\
        {listPairs[2]}\\
        {listPairs[3]}.\n\n
        Wie alt sind ...\n\n
        Vater <<age1_>>$~~~~~$
        Mutter <<age2_>>$~~~~~$
        {names[2]} <<age3_>>$~~~~~$
        {names[3]} <<age4_>>$~~~~~$
        {names[4]} <<age5_>>  ?''',
        age1_= iF, age2_= iF, age3_= iF, age4_= iF, age5_= iF
        )
        

class LinGLS3(Exercise):
    
    preamble = titel('Lineare GLS mit Gauss-Algorithmus lösen')

    def parameters(self):
        def n(a,b):
            return rd.randint(a,b)
        sol = [n(-9,9), n(-9,9), n(-9,9)]
        M = [[1,0,0, sol[0]],[0,1,0, sol[1]],[0,0,1,sol[2]]]
        for i in range (len(M)):
            for k in range (len(M)):
                if k != i:
                    f = (-1)**n(0,1)*n(1,3)
                    M[k] = np.add(M[k],[a*f for a in M[i]])
            f = (-1)**n(0,1)*n(1,3)
            M[i] = [a*f for a in M[i]]
        Gl = []; r = []
        for i in range (len(M)):
            Gl.append(M[i][0]*x + M[i][1]*y + M[i][2]*z)
            r.append(M[i][3])
        return {'x': sol[0], 'y': sol[1], 'z': sol[2],
                'gl1': Gl[0], 'gl2': Gl[1], 'gl3': Gl[2],
                'r1': r[0], 'r2': r[1], 'r3': r[2]}
    
    def problem(self):
        return  Problem('''
        Lösen Sie das folgende lineare Gleichungssystem mittels Gauss-Algorithmus!\n\n
        <<gl1>> $= <<r1:latex>>$\n\n<<gl2>> $= <<r2:latex>>$\n\n<<gl3>> $= <<r3:latex>>$\n\n
        $x =$ <<x_>> $~~~~~y =$ <<y_>> $~~~~~z =$ <<z_>>''',
        x_= Int(widget = Text(width = 6)),
        y_= Int(widget = Text(width = 6)),
        z_= Int(widget = Text(width = 6))
        )
