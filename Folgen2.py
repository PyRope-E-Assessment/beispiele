from pyrope import *

import random as rd
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

def sp(n):
    return  '$'+n*'~'+'$'


adr1 = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/FibonacciBlocks.svg/220px-FibonacciBlocks.svg.png'

x = Symbol ('x')

def plotGraph(f, beg, end, coeff):
    X = list(np.arange(beg-.5, end+1.5, .1))
    Y = []
    for xi in X:
        Y.append (f.evalf(subs={x: xi}))
    fig, axes = plt.subplots(figsize=(4, 4))
    axes.set_aspect('auto')
    plt.grid(True)
    plt.plot([beg-1, end+2], [0, 0], 'gray', linewidth=2)
    plt.plot(X,Y,'b')
    plt.title('Graph of f(x) = $'+str(f).replace('**','^')+'$', fontsize = 9)
    return fig


class Folgen1(Exercise):

    preamble = titel('Zahlenfolgen 2 - Collatz-Folge')
   
    def parameters(self):
        c = rd.choice([11, 17, 34, 35, 48, 52, 53, 68, 69, 70, 75, 96, 104, 106, 113, 192])
        C = [c]
        while c !=1:
            if c%2:
                c = 3*c+1
            else:
                c = int(c/2)
            C.append(c)
        dict = {'iMax': len(C)-1, 'c0': C[0]}
        for i in range (3):
            dict['c'+str(i+1)] = C[i+1]
            dict['cx'+str(i+1)] = C[-3+i]
            dict['cy'+str(i+1)] = C[-3+i]
        return dict
    
    def problem(self, iMax):
        F = Int(widget=Text(width = 4))
        return  Problem (
        'Gegeben ist die Folge $(c_n)$ mit $c_0 = <<c0:latex>>$ und der Bildungsvorschrift\n\n'
        '$c_{n+1} = \\LARGE{\\{{^{^{^{\\frac{c_n}{2}~~~falls~c_n~gerade}}}_{_{3c_n+1~~~falls~c_n~ungerade}}}}$\n\n'
        'Berechnen Sie nächsten 3 Folgenglieder: '+sp(5)+
        '$c_1 =~$<<c1_>>'+sp(5)+'$c_2 =~$<<c2_>>'+sp(5)+'$c_3 =~$<<c3_>>'+'\n\n'
        'Berechnen Sie die Folgenglieder'+sp(5)+
        '$c_{'+str(iMax-2)+'} =~$<<cx1_>>'+sp(5)+
        '$c_{'+str(iMax-1)+'} =~$<<cx2_>>'+sp(5)+
        '$c_{'+str(iMax)+'} =~$<<cx3_>>'+sp(5)+
        '$c_{'+str(iMax+1)+'} =~$<<cy1_>>'+sp(5)+
        '$c_{'+str(iMax+2)+'} =~$<<cy2_>>'+sp(5)+
        '$c_{'+str(iMax+3)+'} =~$<<cy3_>>'+'\n\n',
        c1_=F, c2_=F, c3_=F, cx1_= F, cx2_= F, cx3_= F, cy1_= F, cy2_= F, cy3_= F
        )

  

class Folgen2(Exercise):

    preamble = titel('Zahlenfolgen 2 - Fibonacci-Folge')
   
    def parameters(self):
        F = [1, 1]
        for i in range (2, 50):
            F.append (F[-2]+F[-1])
        ijk = rd.sample(list(np.arange(10, 50)), 3)
        ijk.sort()
        dict = {'F': F, 'ijk': ijk}
        for i in range(3):
            dict['f'+str(6+i)] = F[6+i]
            dict['f'+'ijk'[i]] = F[ijk[i]]
        return dict
    
    def problem(self, F, ijk):
        I3 = Int(widget=Text(width = 3)); I16 = Int(widget=Text(width = 16))
        [i,j,k] = ijk
        return  Problem (
        '![]('+adr1+')\n\n'
        'Gegeben ist die Folge $1,1,2,3,5,8,...$'+sp(5)+'Die nächsten 3 Folgenglieder sind: '+sp(5)+
        '$f_6 =~$<<f6_>>'+sp(5)+'$f_7 =~$<<f7_>>'+sp(5)+'$f_8 =~$<<f8_>>\n\n'
        'Berechnen Sie mittels der Formel von $~\\rightarrow$ *Moivre-Binet* die Folgenglieder \n\n'
        '$f_{'+str(i)+'} =~$<<fi_>>'+sp(5)+'$f_{'+str(j)+'} =~$<<fj_>>'+sp(5)+'$f_{'+str(k)+'} =~$<<fk_>>'+'\n\n',
        f6_= I3, f7_= I3, f8_= I3, fi_= I16, fj_= I16, fk_= I16
        )


class Folgen3(Exercise):

    preamble = titel('Zahlenfolgen 2 - Goldene Zahl')
   
    def parameters(self):
        F = [1, 1]
        for i in range (2, 30):
            F.append (F[-2]+F[-1])
        ijk = rd.sample(list(np.arange(3, 10)), 3)
        ijk.sort()
        ijk = [3*n for n in ijk]
        Q = []
        for n in ijk:
            Q.append(round(F[n]/F[n-1],10))
        return {'qi': Q[0], 'qj': Q[1], 'qk': Q[2], 'ijk': ijk}
    
    def problem(self, ijk):
        F16 = Real(atol = .5*10**(-10)+10**(-15), widget=Text(width = 16))
        [i,j,k] = ijk
        return  Problem (
        'Bilden Sie aus den folgenden Gliedern der Fibonacci-Folge die Quotienten (Genauigkeit >= 10 NK-Stellen):\n\n'
        '$\\frac{f_{'+str(i)+'}}{f_{'+str(i-1)+'}} =~$<<qi_>>'+sp(5)+
        '$\\frac{f_{'+str(j)+'}}{f_{'+str(j-1)+'}} =~$<<qj_>>'+sp(5)+
        '$\\frac{f_{'+str(k)+'}}{f_{'+str(k-1)+'}} =~$<<qk_>>'+'\n\n',
        qi_= F16, qj_= F16, qk_= F16
        )


class Folgen4(Exercise):

    preamble = titel('Zahlenfolgen 2 - Goldener Schnitt')
   
    def parameters(self):
        Fi = (1+np.sqrt(5))/2
        sum = rd.randint(10,30)
        A = sum/Fi
        coeff = [round(-(A+sum),4), round(A*sum,4), 0]
        f = x**3 + coeff[0]*x**2 + coeff[1]*x 
        return {'sum': sum, 'A': round(A, 4), 'c2': coeff[0], 'c1': coeff[1], 'c0': coeff[2],
                'fbPlot': plotGraph (f, 0, int(A*(1+1/((1+np.sqrt(5))/2))), coeff)}
   
    def problem(self):
        F6 = Real(atol = 0.00005, widget=Text(width = 8))
        return  Problem ('''
        Berechnen Sie die Koeffizienten des Polynoms 3. Grades, das die x-Achse an den Stellen
        $~x_0= 0,~~x_2 = <<sum:latex>>~$ sowie an einer Stelle $x_1$ > $\\Large{\\frac{x_2}{2}}$ schneidet,\\
        die das Intervall $~[x_0, x_2]~$ im Verhältnis des Goldenen Schnittes (gerundet auf 4 NK-Stellen) teilt. 
        Der Koeffizient von $x^3$ soll dabei 1 sein.\n\n
        Berechnen Sie zunächst $x_1$: $~~x_1 =$ <<A_>> (Genauigkeit >= 4 NK-Stellen)\n\n
        $f(x) =~x^3~+~$<<c2_>> * $x^2~+~$<<c1_>> * $x~+~$<<c0_>> (Genauigkeit jeweils >= 4 NK-Stellen)''',
        A_= F6, c2_= F6, c1_= F6, c0_= F6
        )

    def feedback(self):
        return '<<fbPlot>>'
