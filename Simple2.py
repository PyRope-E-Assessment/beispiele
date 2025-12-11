from pyrope import *

import random as rd
import numpy as np

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'


class Multiplikation(Exercise):
    
    preamble = titel('Aufgabentyp Multiplikation:  2 ganze Zahlen multiplizieren')
    
    def parameters(self):
        z1 = rd.randint(-99,99)
        z2 = rd.randint(2,99)
        P = z1*z2
        Q = z1/z2
        return {'z1': z1, 'z2': z2, 'P': P, 'Q': Q}
    
    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt\n\n$<<z1:latex>>$*$<<z2:latex>> = $ <<P_>>' ,
        P_ = Int()
        )
                  

class Division1(Multiplikation):
    
    preamble = titel('Aufgabentyp Division:  2 ganze Zahlen dividieren')
    
    def problem(self):
        return  Problem (
        'Berechnen Sie den Quotienten\n\n$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>>' ,
        Q_ = Real()
        )
        

class Division2(Multiplikation):
    
    preamble = titel('Aufgabentyp Division: 2 ganze Zahlen dividieren')+\
               '\n\n*  Näherungslösung zulassen'

    def problem(self):
        return  Problem (
        'Berechnen Sie den Quotienten (Genauigkeit >= 2 NK-Stellen)\n\n'
        '$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>>',
        Q_ = Real(atol=.0050001)
        )
        

class MultiDivi1(Multiplikation):
    
    preamble = titel('Aufgabentyp Multiplikation und Division: 2 ganze Zahlen multiplizieren und dividieren')+\
               '\n\n* bei Division Näherungslösung zulassen'

    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt und den Quotienten (Genauigkeit >= 2 NK-Stellen)\n\n'
        '$<<z1:latex>>$*$<<z2:latex>> = $ <<P_>>'  + '\n\n$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>>' ,
        P_ = Int(),
        Q_ = Real(atol=.00500001)
        )


class MultiDivi2(Multiplikation):
    
    preamble = f'''{titel('Aufgabentyp Multiplikation und Division: 2 ganze Zahlen multiplizieren und dividieren')}\n\n
               * bei Division Näherungslösung zulassen
               * *scores*-Methode um Aufgaben unterschiedlich zu bewerten'''

    def problem(self):
        return  Problem (
        'Berechnen Sie das Produkt und den Quotienten (Genauigkeit >= 2 NK-Stellen)\n\n'
        '$<<z1:latex>>$*$<<z2:latex>> = $ <<P_>>'  + '\n\n$\\LARGE{\\frac{<<z1:latex>>}{<<z2:latex>>}}=$ <<Q_>>' ,
        P_ = Int(),
        Q_ = Real(treat_none_manually=True)
        )
          
    def scores(self, Q, Q_):
        score = 0
        if Q_ is not None:
            score = np.isclose(Q, Q_, atol=.00500001)
        return {'Q_': 2*score}
