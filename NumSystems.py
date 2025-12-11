from pyrope import *

import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

#Several spaces for well-arranged text
def sp(n):
    return '$'+n*'~'+'$'

cTxt = ['dec to bin', 'bin to dec', 'dec to hex', 'hex to dec', 'bin to hex', 'hex to bin']


class BinAndDec(Exercise):
    
    preamble = titel('Convert decimal numbers to binaries and vice versa')

    def parameters(self):
        D = rd.randint(1,255)
        B = '1' #höchste Position
        for i in range (rd.randint(3, 7)): #mindestens 4 Stellen
            B += str(rd.randint(0,1))
        return {'D': D, 'Db': bin(D)[2:], 'B': B, 'Bd': int(B,2)}

    def problem(self, Db, Bd):
        return  Problem (
                'Convert to binary: $<<D:latex>>$'+sp(3)+'<<Db_>>\n\n'
                'Convert to decimal: $<<B:latex>>$'+sp(3)+'<<Bd_>>' ,
                Db_= String(),
                Bd_= Int(widget = Text(width=8))
                )


class DifferentNumberSystems(Exercise):
    
    preamble = titel('Convert into different number systems: decimal - binaries - hexadecimal')

    def parameters(self):
        D = rd.randint(1,255)
        B = '1' #höchste Position
        for i in range (rd.randint(3, 7)): #mindestens 4 Stellen
            B += str(rd.randint(0,1))
        hexNum = ['a','b','c','d','e','f']
        H = ''
        for i in range (3):
            x = str(rd.randint(1,15))
            if int(x)>9: 
                x = hexNum[int(x)-10]
            H += x
        return {'D': D, 'Db': bin(D)[2:], 'Dh': hex(D)[2:],
                'B': B, 'Bd': int(B,2), 'Bh': hex(int(B,2))[2:],
                'H': H, 'Hd': int(H,16), 'Hb':bin(int(H,16))[2:]}

    def problem(self, Db, Bd, Dh, Hd, Bh, Hb):
        return  Problem (
                'Convert '+cTxt[0]+': $<<D:latex>>$'+sp(3)+'<<Db_>>\n\nConvert '+cTxt[1]+': $<<B:latex>>$'+sp(3)+'<<Bd_>>\n\n'
                'Convert '+cTxt[2]+': $<<D:latex>>$'+sp(3)+'<<Dh_>> (lower case)\n\nConvert '+cTxt[3]+': $<<H:latex>>$'+sp(3)+'<<Hd_>>\n\n'
                'Convert '+cTxt[4]+': $<<B:latex>>$'+sp(3)+'<<Bh_>> (lower case)\n\nConvert '+cTxt[5]+': $<<H:latex>>$'+sp(3)+'<<Hb_>>',
                Db_= String(),
                Bd_= Int(widget = Text(width=8)),
                Dh_= String(widget = Text(width=4)),
                Hd_= Int(widget = Text(width=8)),
                Bh_= String(widget = Text(width=4)),
                Hb_= String()
                )       
