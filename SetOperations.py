from pyrope import *

import random as rd
from sympy import symbols

#Large lightgrey font for preamble
def titel(txt):
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

ops = ['∪','∩','∖']#['\u222A', '\u2229', '\u2216']
setOps = ['|', '&', '-']#Union, Intersection, Difference
cmp = ['⊂', '⊆', '∈', '∉', '∅']#[ '\u2282', '\u2286', '\u2208','\u2209','\u2205']

A,B,C,D,E,F,G,H,J,K = symbols("A,B,C,D,E,F,G,H,J,K")
varSet = [A,B,C,D,E,F,G,H,J,K]

#Operator-Symbole durch wirksame Operatoren ersetzen
def cOp(op):
    setOp = setOps[ops.index(op)]
    return setOp

class SetTheory1(Exercise):
    
    preamble = titel('Mengenlehre: Operationen auf Mengen ausführen')
    
    def parameters(self):
        S1 = set(rd.sample(varSet, rd.randint(3,len(varSet))))
        S2 = set(rd.sample(varSet, rd.randint(1, 3)))
        sol = []
        for op in ops[:3]:
            s = eval(str(S1)+cOp(op)+str(S2))
            if s == set(): s = '∅'
            sol.append(str(s))
        return {'S1': S1, 'S2':S2, 'op': op[:3], 'sol1': sol[0], 'sol2': sol[1], 'sol3': sol[2]}
    
    def problem(self):
        iF = String(widget = Text(width = 30))
        return  Problem ('''
        Gegeben sind die Mengen $S1 = \\{<<S1:latex>>\\}$ und $S2 = \\{<<S2:latex>>\\}$.\\
        Berechnen Sie Vereinigungsmenge, Schnittmenge und Differenzmenge von $S1$ und $S2$ !$~~~$
        Geben Sie die leere Menge als ∅ oder $\\{\\}$ ein.\n\n
        $S1 ∪ S2 = $ <<sol1_>>\n\n
        $S1 ∩ S2 = $ <<sol2_>>\n\n
        $S1 ∖ S2 = $ <<sol3_>>''',
        sol1_= iF, sol2_= iF, sol3_ = iF
        )
    
    def scores(self, sol1_, sol2_, sol3_,sol1, sol2, sol3):
        score = [0,0,0]
        for i in range (3):
            S_ = [sol1_, sol2_, sol3_][i]
            S = [sol1, sol2, sol3][i]
            if S_ is not None:
                S_ = ''.join(S_.split()); S = ''.join(S.split())
                if S_ in ['∅', '{}']:
                    score[i] += S=='∅'
                elif len(S_) > 2:
                    if S_[0]=='{' and S_[-1]=='}':
                        S_ = S_[1:-1]; S = S[1:-1]
                        S_ = S_.replace(',', ''); S = S.replace(',', '')
                        S_ = set(S_); S = set(S)
                        score[i] += S_==S
        return {'sol1_': score[0], 'sol2_': score[1], 'sol3_': score[2]}
