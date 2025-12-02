from pyrope import *

import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

primes1 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
#chars =  [A, B, C, D,  E,  F,  G,  H,  I,  J,  K,  L,  M,  N,  O,  P,  Q,  R,  S,  T,  U,  V,  W,  X,  Y,   Z]

wordList1 = ['ANTILOPE', 'BONOBO', 'BUEFFEL', 'DROMEDAR', 'ELEFANT', 'FLAMINGO', 'GEPARD',
             'GIRAFFE', 'GORILLA', 'HYAENE', 'KROKODIL', 'LEOPARD', 'MARABU',
             'NASHORN', 'NILPFERD', 'PAPAGEI', 'PAVIAN', 'PELIKAN', 'SCHAKAL', 'STRAUSS']

def makeProd(word): #Umwandlung word in PZ-Produkt
    P = 1
    for i in range (len(word)):
        fac = primes1[ord(word[i])-65]
        P = P * fac
    return P


class Crypto1(Exercise):

    preamble = titel('Find African Animal encrypted by Prime Number Code')
    
    def parameters(self):
        word = wordList1[rd.randint(0,len(wordList1)-1)]
        P = makeProd(word)
        lList = []
        for l in word: lList.append(l)
        lList.sort()
        letters = ''
        for l in lList: letters += l
        return {'code': P, 'letters': letters, 'word': word}

    def problem(self):
        return Problem('''
        Entschlüsseln Sie das über Primfaktoren verschlüsselte afrikanische Tier 
        nach dem Substitutionsverfahren mittels Primzahlenalphabet!\\
        Verwenden Sie, wenn nötig, die $~\\rightarrow$*Faktorisierungsmethode von Fermat*! 
        $~~~Tipp:$ Es kommen nur die ersten 26 Primzahlen vor.\n\n
        Code: $<<code:latex>>$\n\n
        Ermitteln Sie zunächst die Buchstaben in alphabetischer Reihenfolge:$~~~~~~~~$
        Buchstaben (Großbuchstaben): <<letters_>>\n\n
        Bilden Sie nun das Wort durch Anordnen der Buchstaben in geeigneter Reihenfolge:$~~~~~~~~$
        Wort (in Großbuchstaben): <<word_>>''',
        letters_= String(widget = Text(width = 20)),
        word_= String(widget = Text(width = 20))
        )
    

class Crypto2(Exercise):

    preamble = titel('Encrypt African Animal by Prime Number Code')
    
    def parameters(self):
        word = wordList1[rd.randint(0,len(wordList1)-1)]
        code = makeProd(word)
        return {'code': code, 'word': word}

    def problem(self):
        return Problem('''
        Verschlüsseln Sie das Wort nach dem Substitutionsverfahren über Primfaktoren 
        mittels Primzahlenalphabet!\n\n
        Wort: $<<word:latex>>~~~~~~~~$Code : <<code_>>''',
        code_= Int(widget = Text(width = 20))
        )
