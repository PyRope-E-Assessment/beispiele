from pyrope import *

import random as rd
import numpy as np
import sympy as sym

#Large lightgrey font for preamble
def titel(txt, level = 1):
    if level==0: return '$\\color{gray}{\\Large{\\textsf{'+txt+'}}}$'
    return '$\\color{gray}{\\large{\\textsf{'+txt+'}}}$'

#Adjungierte eines Matrixelementes
def adjoint(M,i,j):
    [z,s] = np.shape(M)        
    aij = np.zeros([z-1,s-1])
    for ii in range (z):
        if ii<i:
            for jj in range (s):
                if jj<j:
                    aij[ii][jj] = M[ii][jj]
                elif jj>j:
                    aij[ii][jj-1] = M[ii][jj]
        elif ii>i:
            for jj in range (s):
                    if jj<j:
                        aij[ii-1][jj] = M[ii][jj]
                    elif jj>j:
                        aij[ii-1][jj-1] = M[ii][jj]
    return (-1)**(i+j)*np.linalg.det(aij)
        

class MatrixOp1(Exercise):

    preamble = titel('Matrixoperationen: Determinante')
   
    def parameters(self):
        global M, detM
        M = list(np.zeros([3,3], dtype=int))
        [z,s] = np.shape(M)
        for i in range (z):
            for j in range (s):
                M[i][j] = rd.randint(-9,9)
        detM = round(np.linalg.det(M))
        return {'detM': detM, 'matrix': sym.Matrix(M)}
    
    def problem(self):
        return  Problem (
        'Berechnen Sie die Determinante folgender Matrix M:\n\n'
        '<<matrix>>\n\n'
        '$Det(M)$ =  <<detM_>>',
        detM_ = Int()
        )

      
class MatrixOp2(Exercise):

    preamble = titel('Matrixoperationen: Adjunkte')
   
    def parameters(self):
        global adjM
        [z, s] = np.shape(M)
        adjM = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range (z):
            for j in range (s):
                adjM[j][i] = round(adjoint(M,i,j))       
        param = {}
        for i in range (3):
            for j  in range(3):
                param.update([('a'+str(i+1)+str(j+1), adjM[i][j])])
        return param

    def problem(self):
        aij = Int(widget = Text(width = 5))
        return  Problem ('''
        Berechnen Sie die Adjunkte der Matrix M:\n\n
        <<a11_>> <<a12_>> <<a13_>>\\
        <<a21_>> <<a22_>> <<a23_>>\\
        <<a31_>> <<a32_>> <<a33_>>''',
        a11_ = aij, a12_ = aij, a13_ = aij,
        a21_ = aij, a22_ = aij, a23_ = aij,
        a31_ = aij, a32_ = aij, a33_ = aij
        )

      
class MatrixOp3(Exercise):

    preamble = titel('Matrixoperationen: Inverse')
   
    def parameters(self):        
        def getRdQuot(M, div, dp):
            for i in range (np.shape(M)[0]):
                for j in range (np.shape(M)[1]):                
                    M[i][j] = round(M[i][j]/div, dp)     
            return M
        invM = getRdQuot(adjM, detM, 3)
        param = {}
        for i in range (3):
            for j  in range(3):
                param.update([('inv'+str(i+1)+str(j+1), invM[i][j])])
        return param

    def problem(self):
        invij  = Real(atol = 0.00050000001, widget = Text(width = 7))
        return  Problem ('''
        Berechnen Sie die Inverse der Matrix M (Genauigkeit >= 3 NK-Stellen):\n\n
        <<inv11_>> <<inv12_>> <<inv13_>>\\
        <<inv21_>> <<inv22_>> <<inv23_>>\\
        <<inv31_>> <<inv32_>> <<inv33_>>''',
        inv11_ = invij, inv12_ = invij, inv13_ = invij,
        inv21_ = invij, inv22_ = invij, inv23_ = invij,
        inv31_ = invij, inv32_ = invij, inv33_ = invij
        )
