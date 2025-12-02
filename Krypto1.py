from pyrope import *

import numpy as np
import random as rd

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

wordList = ['GRETEL','HAENSEL','JORINDE','JORINGEL','ROSENROT','RAPUNZEL','DORNROESCHEN','FROSCHKOENIG','ROTKAEPPCHEN','SCHNEEWITTCHEN','ASCHENPUTTEL',
            'SCHNEEWEISSCHEN','RUMPELSTILZCHEN']

#Caesar mit fester Verschiebung
def caesar0(word, key):
    wordEncr = ''
    for l in word:
        wordEncr += chr(65 + (ord(l)-65 + key)%26)
    return wordEncr

#Caesar mit positionsabhängiger Verschiebung
def caesar1(word):
    wordEncr = ''
    for i in range(len(word)):
        wordEncr += chr(65 + (ord(word[i])-65 + (i+1))%26)
    return wordEncr

#Vigenere: Substitution mit random Schlüssel der random Länge 3-5
def vigenere(word,key):
    wordEncr = ''
    for i in range(len(word)):
        shift = ord(key[i%len(key)]) - 65; 
        wordEncr += chr(65 + (ord(word[i])-65 + shift)%26)
    return wordEncr

def chaos(word):
    word1 = word
    while word1==word:
        new = rd.sample(list(word),len(word))
        word1 = ''.join(new)
    return word1

def beaufort(word,key):
    wordEncr = ''
    for i in range(len(word)):
        nrI = ord(word[i])-65 #lfd. Nr des Buchst im Alphabet, beginnend mit 0 (für A)
        keyI = key[i%len(key)]
        nrKeyI = ord(keyI)-65
        NrEncr = (-nrI + nrKeyI)%26
        wordEncr += chr(65 + NrEncr)
    return wordEncr

TF = String(widget = Text(width = 28))

class Crypto1(Exercise):

    preamble = titel('Simple Caesar Encryption')
    
    def parameters(self):
        word1 = rd.choice(wordList)
        key1 = rd.randint(1,25)
        code1 = caesar0(word1, key1)
        wL = wordList.copy()
        wL.remove(word1)
        word2 = rd.choice(wL)
        key2 = rd.randint(1,25)
        code2 = caesar0(word2, key2)
        return {'word1': word1, 'key1': chr(key1+64), 'code1': code1, 'word2': word2, 'key2': chr(key2+64), 'code2': code2}

    def problem(self):
        return Problem(
        '''Entschlüsseln Sie über einfache Caesar-Verschiebung mit dem Schlüssel $<<key1:latex>>$, 
        welche Märchenfigur sich hinter $<<code1:latex>>$ versteckt!\n\n<<word1_>>\n\n
        Verschlüsseln Sie $<<word2:latex>>$ über einfache Caesar-Verschiebung mit dem Schlüssel 
        $<<key2:latex>>$!\n\nCode: <<code2_>>\n\n''',
        word1_= TF, code2_= TF
        )
    

class Crypto2(Exercise):

    preamble = titel('Position Depending Caesar Encryption')
    
    def parameters(self):
        word1 = rd.choice(wordList)
        code1 = caesar1(word1)
        wL = wordList.copy()
        wL.remove(word1)
        word2 = rd.choice(wL)
        code2 = caesar1(word2)
        return {'word1': word1, 'code1': code1, 'word2': word2, 'code2': code2}

    def problem(self):
        return Problem(
        '''Entschlüsseln Sie $<<code1:latex>>$ über positionsabhängige Caesar-Verschiebung!\n\n<<word1_>>\n\n
        Verschlüsseln Sie $<<word2:latex>>$ über positionsabhängige Caesar-Verschiebung!\n\nCode: <<code2_>>''',
        word1_= TF, code2_= TF
        )

    
class Crypto3(Exercise):

    preamble = titel('Vigenère Encryption 1')
    
    def parameters(self):
        def getWKC(wL):
            word = rd.choice(wL)
            key = ''
            lenKey = rd.randint(3,5)
            for i in range (lenKey):
                key += chr(rd.randint(65,90))
            code = vigenere(word,key)
            return word, key, code
        word1, key1, code1 = getWKC(wordList)
        wL = wordList.copy()
        wL.remove(word1)
        word2, key2, code2 = getWKC(wL)
        return {'word1': word1, 'key1': key1, 'code1': code1, 'word2': word2, 'key2': key2, 'code2': code2}

    def problem(self):
        return Problem(
        '''Entschlüsseln Sie das über Vigenère-Chiffre mit dem Schlüssel $<<key1:latex>>$ verschlüsselte Wort!\n\n
        Code: $<<code1:latex>>~~~~~~~~$Wort: <<word1_>>\n\n
        Verschlüsseln Sie $<<word2:latex>>$ über Vigenère-Chiffre mit dem Schlüssel $<<key2:latex>>$!\n\n
        Code: <<code2_>>''',
        word1_= TF, code2_= TF
        )


class Crypto4(Exercise):

    preamble = titel('Vigenère Encryption 2')
    
    def parameters(self):
        word = 'RUMPELSTILZCHEN'
        #zum Ausprobieren key auswechseln:
        key = 'MICKYMAUS'
        code = vigenere(word, key)
        return {'word': word, 'key': key, 'code': code}

    def problem(self):
        return Problem(
        '''Verschlüsseln Sie $<<word:latex>>$ über Vigenère-Chiffre mit Ihrem Vornamen 
        als Schlüssel (Großbuchstaben, keine Umlaute)!\n\nCode: <<Code_>>''',
        Code_= TF
        )
    
    def a_solution(self, code):
        return {'Code_': code}
   
    def feedback(self, word, Code_):
        if Code_ == None:
            return ('Kein Plan? Lesen Sie [**hier**](https://studyflix.de/informatik/vigenere-verschlusselung-1607) nach!')
        Code_.strip()
        if len(Code_) != len(word): return ('Der Code muss die gleiche Länge wie das zu verschlüsselnde Wort haben!')
        name = ''
        shiftList = []
        for i in range(len(word)):
            if not 65 <= ord(Code_[i]) <= 90: return ('Ungültige Zeichen!')
            shift = (ord(Code_[i]) - ord(word[i]))%26
            shiftList.append(shift)
            name += chr(65 + shift)
        iList = []
        lenTest = 5
        while len(iList)==0 and lenTest > 3:
            lenTest -= 1
            for i in range (2, len(word)-lenTest+1):
                if shiftList[:lenTest] == shiftList[i:i+lenTest]:
                    iList.append(i)
        if len(iList) > 0: name = name[:iList[0]]
        elif shiftList[0]==shiftList[-1]: name = name[:-1]
        return 'Wenn Sie $'+name+'$ heißen, haben Sie es richtig gemacht!'
    
    def scores(self):
        return (1,1)


class Crypto5(Exercise):

    preamble = titel('Beaufort-Chiffre mit geschütteltem Schlüssel')
    
    def parameters(self):
        word1 = rd.choice(wordList[:6])
        code1 = chaos(word1)
        word2 = rd.choice(wordList)
        code2 = beaufort(word2,word1)
        return {'word1': word1, 'code1': code1, 'word2': word2, 'code2': code2, 'code3': word2}

    def problem(self):
        return Problem(
        '''Upps - hier sind die Buchstaben durcheinandergeraten. Welche Märchenfigur versteckt sich hinter 
        $<<code1:latex>>$ ?$~~~~$<<word1_>> \n\n
        Verschlüsseln Sie $<<word2:latex>>$ über Beaufort-Chiffre mit dem eben ermittelten Wort als Schlüssel!\n\n
        Code: <<code2_>>\n\n
        Verschlüsseln Sie den eben ermittelten Code wieder über Beaufort-Chiffre mit dem gleichen Schlüssel!\n\n
        Neuer Code: <<code3_>>''',
        word1_= TF, code2_= TF, code3_= TF
        )
