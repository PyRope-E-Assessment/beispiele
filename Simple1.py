from pyrope import *

import random as rd
import numpy as np

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'


class Multiplikation(Exercise):
    
    preamble = titel('2 ganze Zahlen multiplizieren')

    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        P = z1*z2
        return {'z1': z1, 'z2': z2, 'P': P}
    
    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt\n\n$<<z1:latex>>$*$<<z2:latex>> =$  <<P_>>',
        P_ = Int()
        )


class Division1(Exercise):
    
    preamble = titel('Aufgabentyp Division: 2 ganze Zahlen dividieren')
    
    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        Q = z1/z2
        return {'z1': z1, 'z2': z2, 'Q': Q}
    
    def problem(self):
        return  Problem (
        'Berechnen Sie den Quotienten\n\n$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>>',
        Q_ = Real(),
        )
            

class Division2(Exercise):
    
    preamble = titel('Aufgabentyp Division: 2 ganze Zahlen dividieren')+\
                     '\n\n* Näherungslösung zulassen'

    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        Q = z1/z2
        return {'z1': z1, 'z2': z2, 'Q': Q}       
    
    def problem(self):
        return  Problem (
        'Berechnen Sie den Quotienten\n\n$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>> (Genauigkeit >= 2 NK-Stellen)',
        Q_ = Real(atol=.0050001)
        )
        

class MultiDivi1(Exercise):
    
    preamble = titel('Aufgabentyp Multiplikation und Division: 2 ganze Zahlen multiplizieren und dividieren')+\
                     '\n\n* bei Division Näherungslösung zulassen'
    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        P = z1*z2
        Q = z1/z2
        return {'z1': z1, 'z2': z2, 'P': P, 'Q': Q}       
    
    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt und den Quotienten\n\n$ <<z1:latex>>$*$<<z2:latex>> =$ <<P_>>\n\n'
        '$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>> (Genauigkeit >= 2 NK-Stellen)',
        P_ = Int(),
        Q_ = Real(atol=.0050001)
        )


class MultiDivi2(Exercise):
    
    preamble = f'''{titel('Aufgabentyp Multiplikation und Division: 2 ganze Zahlen multiplizieren und dividieren')}\n\n
               * bei Division Näherungslösung zulassen
               * *scores*-Methode um Aufgaben unterschiedlich zu bewerten'''

    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        P = z1*z2
        Q = z1/z2
        return {'z1': z1, 'z2': z2, 'P': P, 'Q': Q}       
  
    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt und den Quotienten\n\n $<<z1:latex>> * <<z2:latex>> =$ <<P_>>\n\n'
        '$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>> (Genauigkeit >= 2 NK-Stellen)',
        P_ = Int(),
        Q_ = Real()
        )
          
    def scores(self, Q, Q_):
        score = 0
        if Q_ is not None: 
            score = np.isclose(Q, Q_, atol=.0050001)
        return {'Q_': 2*score}
        