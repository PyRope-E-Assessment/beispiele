from pyrope import *

import random as rd


#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

def sp(n):
    return n*' $ $ '

#Define Input Field
def defF(length, acc=3, type=Real):
    return type(atol = (acc>0)*5*10**(-acc-1), widget=Text(width = length)) 


class Folgen_A(Exercise):

    preamble = titel('Zahlenfolgen 1 - Arithmetische Folgen')
   
    def parameters(self):
        diff = rd.randint (2,7)
        a = [1] #aF 1. Ordnung
        for i in range (1, rd.randint(50, 100)):
            a.append(a[-1] + diff)
        b = [1] #Dreiecksfolge: aF 2. Ordnung
        for i in range (1, rd.randint(50, 100)):
            b.append(b[-1] + i)
        c = [1] #Tetraederfolge: : aF 3. Ordnung
        for i in range (2, rd.randint(10, 10)):
            c.append(int(i*(i+1)*(i+2)/6))
        dict = {'a': a, 'b': b, 'c': c}
        for s in [a, b, c]:
            name = ['a','b','c'][[a, b, c].index(s)]
            for i in range(4, 7):
                dict[name+str(i)] = s[i]
            dict[name+'n'] = s[-1]
        return dict
    
    def problem(self,a,b,c):
        F = defF(6, 0, Int)
        return  Problem (
        f'''Gegeben ist die Folge $~{a[0]}, {a[1]}, {a[2]}, {a[3]},...${sp(5)}
        Die nächsten 3 Folgenglieder sind: {sp(4)}$a_4 =$ <<a4_>>{sp(4)}$a_5 =$ <<a5_>>{sp(4)}$a_6 =~$<<a6_>>\\
        Berechnen Sie das ${len(a)}$. Folgenglied: {sp(5)}''' '$a_{'+str(len(a)-1)+'}~=~$<<an_>>\n\n'
        f'''Gegeben ist die Folge $~{b[0]}, {b[1]}, {b[2]}, {b[3]},...${sp(5)}
        Die nächsten 3 Folgenglieder sind: {sp(4)}$b_4 =~$<<b4_>>{sp(4)}$b_5 =~$<<b5_>>{sp(4)}$b_6 =~$<<b6_>>\\
        Berechnen Sie das ${len(b)}$. Folgenglied: {sp(5)}''' '$b_{'+str(len(b)-1)+'}~=~$<<bn_>>\n\n'
        f'''Gegeben ist die Folge $~{c[0]}, {c[1]}, {c[2]}, {c[3]},...${sp(5)}
        Die nächsten 3 Folgenglieder sind: {sp(4)}$c_4 =~$<<c4_>>{sp(4)}$c_5 =~$<<c5_>>{sp(4)}$c_6 =~$<<c6_>>\\
        Berechnen Sie das ${len(c)}$. Folgenglied: {sp(5)}''' '$c_{'+str(len(c)-1)+'}~=~$<<cn_>>$~~~~~~$Tipp: $\\rightarrow$ *Tetraederfolge*',
        a4_= F, a5_= F, a6_= F, an_= F,
        b4_= F, b5_= F, b6_=F, bn_= F,
        c4_= F, c5_= F, c6_=F, cn_= F
        )


class Folgen_G(Exercise):

    preamble = titel('Zahlenfolgen 1 - Geometrische Folgen')
   
    def parameters(self):
        fak = rd.randint(2,4)
        a = [1] #gF steigend
        for i in range (1, rd.randint(10, 15)):
            a.append(a[-1] * fak)

        fak = rd.randint(2,4)
        b = [fak**(rd.randint(1,4))] #gF fallend
        for i in range (1, rd.randint(10, 15)):
            b.append(b[-1] * (fak-1)/fak)
            b[-2] = round(b[-2], 3)
        b[-1] = round(b[-1], 6)
            
        decr = rd.choice([1, 0])
        fak = rd.randint(2,4)
        c = [(fak**(rd.randint(1,4)))**decr] #gF alternierend
        for i in range (rd.randint(7, 10)):
            c.append(-c[-1] * fak**(1 - 2*decr))
            c[-2] = round(c[-2], 3)
        c[-1] = round(c[-1], 6)
        dict = {'a': a, 'b': b, 'c': c}
        for s in [a, b, c]:
            name = ['a','b','c'][[a, b, c].index(s)]
            for i in range(4, 7):
                dict[name+str(i)] = s[i]
            dict[name+'n'] = s[-1]
        return dict
    
    def problem(self, a, b, c):
        F = defF(8)
        return  Problem (
        f'''Gegeben ist die Folge $~{a[0]}, {a[1]}, {a[2]}, {a[3]},...$\\
        Die nächsten 3 Folgenglieder sind: {sp(4)}$a_4 =$ <<a4_>>{sp(4)}$a_5 =$ <<a5_>>{sp(4)}$a_6 =~$<<a6_>>\\
        Berechnen Sie das ${len(a)}$. Folgenglied: {sp(5)}''' '$a_{'+str(len(a)-1)+'}~=~$<<an_>>' f'''\n\n
        Gegeben ist die Folge $~{b[0]}, {b[1]}, {b[2]}, {b[3]},...$\\
        Die nächsten 3 Folgenglieder sind: {sp(4)}$b_4 =~$<<b4_>>{sp(4)}$b_5 =~$<<b5_>>{sp(4)}$b_6 =~$<<b6_>>{sp(5)}(Genauigkeit >= 3 NK-Stellen)\\
        Berechnen Sie das ${len(b)}$. Folgenglied: {sp(5)}''' '$b_{'+str(len(b)-1)+'}~=~$<<bn_>>' f'''{sp(5)}(Genauigkeit >= 6 NK-Stellen)\n\n
        Gegeben ist die Folge $~{c[0]}, {c[1]}, {c[2]}, {c[3]},...$\\
        Die nächsten 3 Folgenglieder sind: {sp(4)}$c_4 =~$<<c4_>>{sp(4)}$c_5 =~$<<c5_>>{sp(4)}$c_6 =~$<<c6_>>{sp(5)}(Genauigkeit >= 3 NK-Stellen)\\
        Berechnen Sie das ${len(c)}$. Folgenglied: {sp(5)}''' '$c_{'+str(len(c)-1)+'}~=~$<<cn_>>' f'''{sp(5)}(Genauigkeit >= 6 NK-Stellen)''',
        a4_= defF(8, 0, Int), a5_= defF(8, 0, Int), a6_= defF(8, 0, Int), an_=defF(12, 0, Int),
        b4_= F, b5_= F, b6_=F, bn_=defF(12, 6),
        c4_= F, c5_= F, c6_=F, cn_=defF(12, 6)
        )

