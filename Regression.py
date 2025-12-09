from pyrope import *

import matplotlib.pyplot as plt
import random as rd
import numpy as np
from scipy import stats
from sympy import symbols

### switch between version with/without HTML code #############################
def withHTML():                                             ###################
    x = True #True/False: Code with/without HTML            ###################
    if not isinstance(x, bool): return 0                    ###################
    return x                                                ###################
###############################################################################

def titel(txt):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

x, y = symbols('x, y')

prTxt1_1 = ['Gegeben ist die folgende Wertetabelle einer zufälligen Verteilung:', 'The following table shows the values of a random distribution:']
prTxt1_2 = ['Berechnen Sie die lineare Regressionsfunktion $f(x)$ (vertikaler Abstand) und die Summe der Abweichungsquadrate $s$ !$~~~~$',
           'Find the linear regression function $f(x)$ (vertical distance) and the sum of deviation squares $s$ !$~~~~$']
prTxt2 = ['Berechnen Sie nun für die gleichen Werte die quadratische Ausgleichsfunktion $f(x)$ (vertikaler Abstand)\n\nund deren Summe der Abweichungsquadrate $s$!$~~~~$',
          'Find now with the same values the quadratic smoothing function $f(x)$ (vertical distance) and its sum of deviation squares $s$!$~~~~$']
rdTxt = ['Runden Sie auf mind. 2 NK-Stellen.', 'Round to at least 2 decimal places.']

def sp(n):
    return '$'+n*'~'+'$'

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

###################################################################
### Method ValTab (value tab):                                  ###
### makes a value table as special case of table using Markdown ###
###################################################################
# Give a list, containing one list of items for each line of the table or,
# alternativly, all line text in one string, separated by comma
def ValTab(lines):
    valTab = '\n\n'
    for i in range (len(lines)):
        valTab+='|'+lines[i][0]+'|'
        for j in range (1, len(lines[i])):
            valTab+=str(lines[i][j])+'|'
        if i==0:
            valTab+='\n|---|---|'
            for j in range (len(lines[0])-2):
                valTab+='---|'
        valTab+='\n'
    valTab+='\n\n'
    return valTab

#Function plot    
def plotregFunc(x1,x2,valF):
    fig = plt.figure(figsize=(3, 2))
    plt.plot(x1,x2,'ro')
    x = np.arange(0,x1[-1]+1,len(x1)/len(valF))
    plt.plot(x,valF,'-b')
    plt.title('Random Distribution '+str(n)+' values with regression function', fontsize = 9)
    return fig

lan = 1

class LinRegression(Exercise):

    preamble = titel('Regression 1')
    
    def parameters(self):
        global n, x1, x2
        n = rd.randint(6,10) #Anzahl Messwerte
        x1 = list(np.arange(0, n, dtype=int))
        x2 = []
        for i in range(len(x1)): x2.append(rd.randint(-5,5))
        #Methode kleinste Quadrate - vertikaler Abstand
        slope, intercept, r, p, std_err = stats.linregress(x1, x2)
        s = 0
        valF = []
        for i in range(len(x1)):
            valF.append(slope*x1[i] + intercept)
            s += (slope*x1[i] + intercept - x2[i])**2
            s = round(s,2)
        f = round(slope,2)*x + round(intercept,2)
        return {'x': x, 'x1': x1, 'x2': x2, 'valF': valF, 'sl': slope, 'ic': intercept,
                'f': f, 'deg': 2, 's': s, 'fbPlot': plotregFunc(x1,x2,valF)}   

    def problem(self, f, s):
        args = [['$x$']+x1,['$y$']+x2]
        Tab = [ValTab(args), BlockTab(args)][withHTML()]
        return  Problem (f'''
        {prTxt1_1[lan]} {Tab} {prTxt1_2[lan]} {rdTxt[lan]}\n\n
        $f(x) = $ <<f_>>{sp(8)}$s = $ <<s_>>''',
        f_ = Expression(symbols='x'),
        s_ = Real(widget=Text(width=8))
        )

    def scores(self, f_, f, s, s_, deg):
        score = [0, 0]
        if f_ is not None:
            coeff = [0,0,0]
            for i in range(deg):
                coeff[i] = round(float(f_.coeff(x,i)),2)
            [c,b,a] = coeff
            score[0] = a*x**2 + b*x + c == f
        if s_ is not None:
            score[1] = round(float(s_), 2) == s
        return {'f_': score[0], 's_': score[1]}

    def feedback(self, f_, f, s, s_, deg):
        if sum(self.scores(f_, f, s, s_, deg).values()) < 2:
            return '<<fbPlot>>\n\nDa war nicht alles richtig! - Hilfe findest Du hier: https://studyflix.de/statistik/regression-4814'
        return '<<fbPlot>>'


class QuadRegression(LinRegression):
    
    preamble = titel('Regression 2')
    
    def parameters(self):
        s = 0
        #Methode kleinste Quadrate - vertikaler Abstand
        coeff3 = np.polyfit(x1, x2, 2)
        for i in range(len(x1)):
            s += (coeff3[0]*x1[i]**2 + coeff3[1]*x1[i] + coeff3[2] - x2[i])**2
        s = round(s,2)
        valF = []
        dist = 10
        for i in range(len(x1)):
            for j in range (dist):
                valF.append(coeff3[0]*(x1[i]+j/dist)**2 + coeff3[1]*(x1[i]+j/dist) + coeff3[2])
        f = round(coeff3[0],2)*x**2 + round(coeff3[1],2)*x + round(coeff3[2],2)
        return {'x': x, 'x1': x1, 'x2': x2, 'valF': valF, 'f': f, 'deg': 3, 's': s, 'fbPlot': plotregFunc(x1,x2,valF)}
      
    def problem(self, f, s):
        return  Problem (
        f'{prTxt2[lan]} {rdTxt[lan]}\n\n$f(x) =  $ <<f_>>{sp(8)}$s =  $ <<s_>>',
        f_ = Expression(symbols='x', widget=Text(width=30)),
        s_ = Real(widget=Text(width=8))
        )
