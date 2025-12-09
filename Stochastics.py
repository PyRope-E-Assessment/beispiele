from pyrope import *

import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

#Several spaces for well-arranged text
def sp(n):
    return '$'+n*'~'+'$'

ops = ['not', 'and', 'or', u'\u2192', 'xor', u'\u2194']

############################################################################
### Method BlockTab: makes a Tab with border around each cell using HTML ###
############################################################################
# Give a list, containing one list of items for each line of the table or,
# alternativly, all line text in one string, separated by comma
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
    no = ['','not']
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

def fillTab(A, B, pos):
    sol = [[0,0],[0,0]]
    E1 = [A, 1-A][pos[1]]; E2 = [B, 1-B][pos[0]]
    sol[pos[0]][pos[1]] = rd.randint(max(1, round((E1+E2-1)*10+1)), round( min(E1,E2)*10-1))/10
    P = sol[pos[0]][pos[1]]/E1
    sol[pos[0]][int(not(pos[1]))] = E2 - sol[pos[0]][pos[1]] #gleiche Zeile
    sol[int(not(pos[0]))][pos[1]] = E1 - sol[pos[0]][pos[1]] #gleiche Spalte
    sol[int(not(pos[0]))][int(not(pos[1]))] = 1 - sum(sol[0]) - sum(sol[1])
    P = round(P,3)
    for i in [0,1]:
        for j in [0,1]:
            sol[i][j] = round(sol[i][j],2)
    return P, sol


class Stochastics1(Exercise):
    
    preamble = titel('Stochastik 1')

    def parameters(self):
        A = round(rd.randint(1,9)/10,1)
        B = round(rd.randint(1,9)/10,1)
        sol = [[],[]]
        sol[0].append(round(A*B,2))
        sol[0].append(round((1-A)*B,2))
        sol[1].append(round(A*(1-B),2))
        sol[1].append(round((1-A)*(1-B),2))
        return {'A': A, 'B': B, 'sol00': sol[0][0], 'sol01': sol[0][1], 'sol10': sol[1][0], 'sol11': sol[1][1]}   

    def problem(self, A, B):
        F = Real(widget = Text(width = 5))
        return  Problem (f'''
        Die Ereignisse A und B seien stochastisch unabhängig. 
        Ergänzen Sie die folgende Vierfeldertafel!
        {BlockTab([[' ', '$A$',' $\\bar{A}$',' '],
                   ['$B$','<<sol00_>>','<<sol01_>>',B],
                   ['$\\bar{B}$','<<sol10_>>','<<sol11_>>',round(1-B,1)],
                   [' ',A,round(1-A,1),'$1$']])}''',
        sol00_ = F, sol01_ = F, sol10_ = F, sol11_ = F
        )


class Stochastics2(Exercise):
    
    preamble = titel('Stochastik 2')

    def parameters(self):
        A = round(rd.randint(2,8)/10,1)
        B = round(rd.randint(2,8)/10,1)
        pos = [rd.randint(0,1),rd.randint(0,1)]
        [x,y] = [['$B$','$\\bar{B}$'][pos[0]], ['$A$','$\\bar{A}$'][pos[1]]]
        P, sol = fillTab(A, B, pos)
        dp = ['abhängig', 'unabhängig'][A*B==sol[0][0]]
        return {'A': A, 'B': B, 'x': x, 'y': y, 'P': P, 'sol': sol, 'dp': dp}   

    def problem(self, A, B, sol, x, y):
        return  Problem (f'''
        Gegeben ist die folgende Vierfeldertafel !
        {BlockTab([[' ', '$A$',' $\\bar{A}$',' '],
                   ['$B$',sol[0][0],sol[0][1],B],
                   ['$\\bar{B}$',sol[1][0],sol[1][1],round(1-B,1)],
                   [' ',A,round(1-A,1),'$1$']])}
        Bestimmen Sie die Wahrscheinlichkeit des Ereignisses {x} unter der Bedingung {y} !
        {sp(3)}Runden Sie auf mind. 3 NK-Stellen.\n\n
        $P(\\small{x.replace('$','').replace('B','{B}')}|_{y.replace('$','')}$) = <<P_>>\n\n
        Entscheiden Sie, ob die Ereignisse A und B stochastisch abhängig sind!{sp(3)}
        A und B sind {sp(3)} <<dp_>>''',
        P_ = Real(atol = 0.0005000000001, widget = Text(width = 5)),
        dp_ = String(widget=RadioButtons('abhängig', 'unabhängig', vertical=False))
        )

    
class Stochastics3(Exercise):
    
    preamble = titel('Stochastik 3')

    def parameters(self):
        A = round(rd.randint(2,8)/10,1)
        B = round(rd.randint(2,8)/10,1)
        pos = [rd.randint(0,1),rd.randint(0,1)]
        [x,y] = [['$B$','$\\bar{B}$'][pos[0]], ['$A$','$\\bar{A}$'][pos[1]]]
        P, sol = fillTab(A, B, pos)
        dp = ['abhängig', 'unabhängig'][A*B==sol[0][0]]
        return {'A': A, 'B': B, 'x': x, 'y': y, 'P': P, 'dp': dp,
                'sol00': sol[0][0], 'sol01': sol[0][1], 'sol10': sol[1][0], 'sol11': sol[1][1]}   

    def problem(self, A, B, x, y):
        F = Real(widget = Text(width = 5))
        return  Problem (f'''
        Die Wahrscheinlichkeit des Ereignisses {x} unter der Bedingung {y} betrage $<<P:latex>>$. 
        Ergänzen Sie die folgende Vierfeldertafel !
        {BlockTab([[' ', '$A$',' $\\bar{A}$',' '],
                   ['$B$','<<sol00_>>','<<sol01_>>',B],
                   ['$\\bar{B}$','<<sol10_>>','<<sol11_>>',round(1-B,1)],
                   [' ',A,round(1-A,1),'$1$']])}
        Entscheiden Sie, ob die Ereignisse A und B stochastisch abhängig sind !\n\n
        A und B sind {sp(3)} <<dp_>>''',
        sol00_ = F, sol01_ = F, sol10_ = F, sol11_ = F,
        dp_ = String(widget=RadioButtons('abhängig', 'unabhängig', vertical=False))
        )
