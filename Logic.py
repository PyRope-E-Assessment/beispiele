from pyrope import *

import random as rd
import numpy as np


#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

#Several spaces for well-arranged text
def sp(n):
    return '$'+n*'~'+'$'

ops =    ['\\neg', '\\land', '\\lor', '\\to', u'\u22BB', '\\leftrightarrow']
logOps = ['not',   'and',    'or',    '<=',   '!=',      '==']

#################################################################
### Method BlockTab: makes a Tab with border around each cell ###
#################################################################
# Give a list, containing one list of items for each line of the table or, alternativly,
# all line text in one string, separated by commas
def BlockTab(lines):
    tabTxt = '<br><table style = "margin-left: 0px">'
    for line in lines:
        if type(line)==str:
            line = line.split(',')
        tabTxt += '<tr>'
        for cell in line:
            tabTxt += '<td  style = "background-color: white; border:1px solid black; text-align: right">'+sp(3)+str(cell)+sp(2)+'</td>'
        tabTxt += '</tr>'
    tabTxt += '</table>\n\n'
    return tabTxt
        
#Aufbau einer logischen Funktion aus n Binomen:
#Randomisierte Auswahl der Binomglieder aus len(vars) Variablen
#Randomisierte Auswahl der Operatoren aus 5 Möglichkeiten
#Randomisierte Verneinung vor den Binomen
def logFunc(vars, n):
    F = ''
    no = ['','\\neg']
    for i in range (n):
        op = ops[rd.randint(1, len(ops)-1)]
        V = vars.copy()
        v1 = V[rd.randint(0,len(V)-1)]
        V.remove(v1)
        v2 = V[rd.randint(0,len(V)-1)]
        f = no[rd.randint(0,1)] + '(' + v1 + ' ' + op + ' ' + v2 + ')'
        op = ops[(rd.randint(1, 2))]
        F = (0<i<n-1)*'(' + F + f + (0<i<n-1)*')' + (i<n-1)*(' ' + op + ' ')
    return F

#Operator-Symbole durch wirksame Operatoren ersetzen
def changeOps(F):
    Fct = F
    for op in ops:
        Fct = Fct.replace(op, logOps[ops.index(op)])
    return Fct


class LogicalProblems1(Exercise):
    
    preamble = titel('Aussagenlogik 1: Wahrheitwert eines logischen Ausdrucks bestimmen')

    def parameters(self):
        vars = ['A', 'B', 'C']
        F = logFunc(vars, 3)
        Fct = changeOps(F)
        [A, B, C] = rd.choices([0, 1], k = len(vars))
        sol = int(eval(Fct))
        return {'vals': [A, B, C], 'F': F, 'sol': sol}
    
    def problem(self, F):
        return  Problem (f'''
        Gegeben sind die logischen Variablen{sp(3)}$[A, B, C] = <<vals:latex>>$.{sp(3)} 
        Berechnen Sie den Wahrheitswert der Funktion{sp(3)} $<<F:latex>>$\n\n
        Lösung:{sp(3)}<<sol_>>''',
        sol_ = Int(widget=RadioButtons('0', '1', description='Logical', vertical=False))
        )
        

class LogicalProblems2(Exercise):
    
    preamble = titel('Aussagenlogik 2: Wahrheitstafel eines logischen Ausdrucks erstellen')

    def parameters(self):
        vars = ['A', 'B']
        F = logFunc(vars, 3)        
        Fct = changeOps(F)
        sol = []
        for m in range (2):
            linSol = []
            for n in range (2):
                [B, A] = [m,n]
                linSol.append(int(eval(Fct)))
            sol.append (linSol)
        return {'F': F, 'sol00': sol[0][0], 'sol01': sol[0][1], 'sol10': sol[1][0], 'sol11': sol[1][1]}
    
    def problem(self, F):
        iF = Int(minimum=0, maximum=1, widget=Text(width = 3))
        return  Problem (f'''
        Gegeben ist die Funktion $F = <<F:latex>>${sp(3)}
        Stellen Sie die  Wahrheitstafel dieser Funktion auf!
        {BlockTab(['$B$ $^{\\LARGE{\\backslash}}$ $^{\\Large{A}}$, 0, 1','0,<<sol00_>>,<<sol01_>>','1,<<sol10_>>,<<sol11_>>'])}''',
        sol00_ = iF,
        sol01_ = iF,
        sol10_ = iF,
        sol11_ = iF
        )


class LogicalProblems3(Exercise):
    
    preamble = titel('Aussagenlogik - 3: Wahrheitwerte zweier logischer Ausdrücke vergleichen')

    def parameters(self):
        vars = ['A', 'B', 'C']
        [A, B, C] = rd.choices([0, 1], k = len(vars))
        FF = []; sol = []
        for i in [1, 2]:
            F = logFunc(vars, 3)
            Fct = changeOps(F)
            FF.append(F)
            sol.append(int(eval(Fct)))
        res = 'J'*(sol[0] == sol[1]) + 'N'*(sol[0] != sol[1])
        return {'vals': [A, B, C], 'F1': FF[0], 'F2': FF[1], 'res': res}
    
    def problem(self, F1, F2, res):
        return  Problem (f'''
        Gegeben sind die logischen Variablen{sp(3)}$[A, B, C] = <<vals:latex>>.$\n\n
        Untersuchen Sie, ob die Wahrheitswerte der Funktionen\n\n
        $F1 = <<F1:latex>>${sp(3)}und{sp(3)}$F2 = <<F2:latex>>${sp(3)}identisch sind!\n\n
        Identisch? {sp(3)}<<res_>>''',
        res_ = String(widget=RadioButtons('J', 'N', vertical=False))
        )
        