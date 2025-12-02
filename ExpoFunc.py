from pyrope import *

import math
import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

#Rumpftext
atxt = ['Ein Teich der Fläche $<<F:latex>>$ m² ist zu $<<a:latex>>$ %  von einer Algenschicht bedeckt. Diese von Algen bedeckte Fläche ',
' täglich um $<<b:latex>>$ %.\n\nNach wieviel Tagen ',
'? \n\n']

##Austauschbare Textteile, um Aufwand bei ähnlich strukturierten Aufgaben zu minimieren
ins1 = ['wächst', 'schrumpft']
ins2 = ['ist der Teich vollständig von Algen bedeckt', 'hat sich der Algenbestand auf 1 m² reduziert']

#parameters-Problem
def parameters_Tpl(id):
        F = rd.randint(100,1000)
        a = round(rd.randint(1+id*10,30+id*50))
        b = rd.randint(5,20)
        t = id*math.log(100/(F*a), 1-b/100) + (not id)*math.log(100/a, 1+b/100)
        t = round(t,2)
        return id, F, a, b, t
    

class ExpFkt1(Exercise):

    preamble = titel('Exponentialfunktionen - Wachstum')

    def parameters(self):
        id, F, a, b, t = parameters_Tpl(0)
        return {'id': id, 'F': F, 'a': a, 'b': b, 't': t}

    def problem(self, id):
        return Problem(atxt[0] + ins1[id] + atxt[1] + ins2[id] + atxt[2] + 
        'Nach <<t_>> Tagen$~~~$ (Genauigkeit >= 2 NK-Stellen)',
        t_= Real(atol = 0.005000000001, widget=Text(width=10))
        )
    
    def hints(self):
        return 'Nutzen Sie Logarithmen!'


class ExpFkt2(ExpFkt1):
    
    preamble = titel('Exponentialfunktionen - Zerfall')
    
    def parameters(self):
        id, F, a, b, t = parameters_Tpl(1)
        return {'id': id, 'F': F, 'a': a, 'b': b, 't': t}

