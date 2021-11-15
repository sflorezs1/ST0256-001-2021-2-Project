from sympy import *
from sympy.printing.printer import Printer
import linear_equations
import numpy as np


def vandermonde(X, Y):
    vandermondeMatrix = []
    for i in range(0, len(X)):
        auxList = []
        for j in range(0, len(X)):
            auxList.insert(0, X[i]**j)
        vandermondeMatrix.append(auxList)
    
    Ycol = np.array(Y).T
    vandermondeMatrix = np.array(vandermondeMatrix)

    print(vandermondeMatrix)
    print(Ycol)

    solutions = linear_equations.gauss(vandermondeMatrix, Ycol)

    return solutions

def dividedDifference(X, Y):
    matrixDivDiff = []
    matrixDivDiff.append(Y)
    rest = 0
    for i in range(1, len(X)):
        auxList = []
        xIndex = 0
        for j in range(i, len(X)):
            #print("Diff act: ", matrixDivDiff[i-1][j])
            aux = (matrixDivDiff[i-1][j-rest]-matrixDivDiff[i-1][j-rest-1])/(X[j]-X[xIndex])
            #print("(", matrixDivDiff[i-1][j-rest], "-", matrixDivDiff[i-1][j-rest-1] , ") / (", X[j], "-" ,  X[xIndex], ") = ", aux)
            auxList.append(aux)
            xIndex += 1
        
        matrixDivDiff.append(auxList)
        rest +=1
    return matrixDivDiff

def asPolynomial(p):
    x = symbols('x')
    init_printing()
    return simplify(p(x))

def lagrange(X, Y):

    def L(i, x):
        p = 1
        for j in range(0, len(X)):
            if j != i :
                p *= ((x-X[j])/(X[i]-X[j]))
        return p

    def P(x):
        yval = 0
        for i in range(len(Y)):
            yval += L(i, x) * Y[i]
        return yval

    return P


# def linealSplines(X, Y, xValue):
    
#     def linealEquation(x1, y1, x2, y2, x):
#         return (((y2-y1)/(x2-x1))*(x-x1)) + y1
    
#     equations = []
#     cont = 0
#     for i in range(1, len(X)):
#        value = linealEquation(X[i-1], Y[i-1], X[i], Y[i], xValue)
#        equations.append(value)
#        cont += 1

def linealSplines(X, Y):

    X, Y = zip(*sorted(zip(X, Y)))

    def linealEquation(x1, y1, x2, y2):
        return lambda x: (((y2-y1)/(x2-x1))*(x-x1)) + y1

    def condition(rhs, xp, xc):
        return lambda x: rhs(xp, x) and xc >= x

    equations = []
    cont = 0
    for i in range(1, len(X)):
        if cont == 0:
            cond = lambda x, y: x <= y
        else:
            cond = lambda x, y: x < y
        value = (linealEquation(X[i-1], Y[i-1], X[i], Y[i]), condition(cond, X[i-1], X[i]))
        equations.append(value)
        cont += 1

    def piecewise(x):
        for i in equations:
            if i[1](x):
                return i[0](x)
        return None

    return piecewise, equations



def quadraticSplines(X,Y, xValue):
    A = []
    # Basic equations
    for i in range(0, len(X)-1):
        auxList = []
        auxList.extend([0]*(3*i))
        auxList.extend([X[i]**2, X[i], 1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))))
        #print(auxList)
        A.append(auxList)
        
        auxList = []
        auxList.extend([0]*(3*i))
        auxList.extend([X[i+1]**2, X[i+1], 1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))))
        #print(auxList)
        A.append(auxList)

    # Equations of derivates
    for i in range(1, len(X)-1):
        auxList = []
        auxList.extend([0]*(3*(i-1)))
        auxList.extend([2*X[i], 1, 0,-2*X[i], -1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))+1))
        print(auxList)
        A.append(auxList)

    # Last equation   
    auxList = [2]
    auxList.extend([0]*((3*(len(X)-1))-1))
    A.append(auxList)
    
    Ypartial = [Y[0]]
    for i in range(1, len(Y)-1):
        Ypartial.extend([Y[i]]*2)
    Ypartial.append(Y[len(Y)-1])
    Ypartial.extend([0]*((3*(len(X)-1))-(2*(len(X)-1))))

    Ycol = np.array(Ypartial).T
    #sol = linear_equations.gauss(A, Ycol)
    for i in range(0, len(A)):
        print(A[i])
    print("")
    print(Ycol)
    
    sol = np.linalg.solve(A,Ycol)
    sol = np.round(sol, decimals = 4)
    #sol = linear_equations.gauss_par(A, Ycol)
    print(sol)
        

######### Examples ##########
x = [1, 2, 4.5]
y = [6.7, 5, 2.5]

#print(vandermonde(x, y))
#print("")


x = [1, 1.2, 1.4, 1.6, 1.8, 2]
y= [0.6747, 0.8491, 1.1214, 1.4921, 1.9607, 2.5258]

#print(dividedDifference(x, y))

x = [-1, 1, 2, 4]
y = [7, -1, -8, 2]
#p = lagrange(x, y)
#print(asPolynomial(p))

x = [3, -2, 1, 4]
y = [1, 5, 1, 2]
print(linealSplines(x, y)[0](2))


####### Quadratic splines
x = [1, 2, 4]
y= [141, 112.7, 125.63]

x = [2, 3, 5, 6, 8]
y = [3.2, 4.8, 2.9, 9.1, 12.4]

#quadraticSplines(x, y, 6)