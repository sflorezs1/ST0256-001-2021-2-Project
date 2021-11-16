from sympy import *
from sympy.printing.printer import Printer
import linear_equations
import numpy as np
import Exception


def interpolate(method, X, Y):
    X2 = X
    # validate X, Y and sort
    if len(Y) != len(X):
        raise ""
    if len(list(set(X2))) != len(X):
        return "Error 2"

    if method == 'vandermonde':
        return vandermonde(X, Y)
    elif method == 'dividedDifference':
        return dividedDifference(X, Y)
    elif method == 'lagrange':
        return lagrange(X, Y)
    elif method == 'linearSplines':
        return linearSplines(X, Y)
    elif method == 'quadraticSplines':
        return quadraticSplines(X, Y)
    else:
        print("Invalid Method")
        return("Invalid Method") 


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


def linearSplines(X, Y):

    x = symbols('x')

    X, Y = zip(*sorted(zip(X, Y)))

    def linealEquation(x1, y1, x2, y2):
        return lambda x: (((y2-y1)/(x2-x1))*(x-x1)) + y1

    equations = []
    cont = 0
    for i in range(1, len(X)):
        value = (linealEquation(X[i-1], Y[i-1], X[i], Y[i]), ((X[i-1] <= x) if cont == 0 else (X[i-1] < x)) & (x <= X[i]))
        equations.append(value)
        cont += 1

    expr = Piecewise(*[(e[0](x), e[1]) for e in equations])

    def piecewise(xpred):
        from sympy.utilities.lambdify import lambdify, implemented_function
        return (lambdify(x, expr)(xpred).item())

    return piecewise, expr

def quadraticSplines(X, Y):
    X, Y = zip(*sorted(zip(X, Y)))
    
    conditions = []
    A = []
    # Basic equations
    for i in range(0, len(X)-1):
        auxList = []
        auxList.extend([0]*(3*i))
        auxList.extend([X[i]**2, X[i], 1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))))
        A.append(auxList)
        
        auxList = []
        auxList.extend([0]*(3*i))
        auxList.extend([X[i+1]**2, X[i+1], 1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))))
        A.append(auxList)

    # Equations of derivates
    for i in range(1, len(X)-1):
        auxList = []
        auxList.extend([0]*(3*(i-1)))
        auxList.extend([2*X[i], 1, 0,-2*X[i], -1])
        if i < (len(X)-1):
            auxList.extend([0]*(3*(len(X)-1)-(3*(i+1))+1))
        #print(auxList)
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
    
    sol = np.linalg.solve(A,Ycol)
    sol = np.round(sol, decimals = 4)

    eqs = []
    idx = 0
    x = symbols('x')
    for i in range(1, len(X)):
        c = (sol[idx], sol[idx + 1], sol[idx + 2])
        eqs.append((c[0] * x**2 + c[1] * x + c[2], ((X[i-1] <= x) if idx == 0 else (X[i-1] < x)) & (x <= X[i])))
        idx += 3

    expr = Piecewise(*eqs)

    def piecewise(xpred):
        from sympy.utilities.lambdify import lambdify, implemented_function
        return (lambdify(x, expr)(xpred).item())

    return piecewise, expr
        

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


##### Linear Splines
x = [3, -2, 1, 4]
y = [1, 5, 1, 2]
#print(linearSplines(x, y)[1])


####### Quadratic splines
#x = [1, 2, 4]
#y= [141, 112.7, 125.63]

x = [2, 3, 5, 8, 6]
y = [3.2, 4.8, 2.9, 12.4, 9.1]

#print(quadraticSplines(x, y)[0](8))
#print(len(list(set(x))) != len(x))

print(interpolate("asa",x, y))