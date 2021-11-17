from sympy import *
import linear_equations
import numpy as np
from enum import Enum
from sympy.utilities.lambdify import lambdify


class Method(Enum):
    Vandermonde = 0
    DividedDifferences = 1
    Lagrange = 2
    LinearSpline = 3
    QuadraticSpline = 4


def interpolate(method: Method, X, Y):
    # validate X, Y and sort

    if len(Y) != len(X):
        raise Exception('MismatchedInputSize')

    if len(set(X)) != len(X):
        raise Exception('DuplicatedIndependent')

    X, Y = zip(*sorted(zip(X, Y)))

    if method == Method.Vandermonde:
        return _vandermonde(X, Y)
    elif method == Method.DividedDifferences:
        return _divided_differences(X, Y)
    elif method == Method.Lagrange:
        return _lagrange(X, Y)
    elif method == Method.LinearSpline:
        return _linear_spline(X, Y)
    elif method == Method.QuadraticSpline:
        return _quadratic_spline(X, Y)
    else:
        raise Exception(f'Method {method} does not exist')


def _vandermonde(X, Y):
    vandermonde_matrix = []
    for i in range(0, len(X)):
        auxList = []
        for j in range(0, len(X)):
            auxList.insert(0, X[i] ** j)
        vandermonde_matrix.append(auxList)

    Ycol = np.array(Y).T
    vandermonde_matrix = np.array(vandermonde_matrix)

    solutions = linear_equations.linear_solve(vandermonde_matrix, Ycol)

    x = symbols('x')
    expr = 0
    exp = len(solutions) - 1
    for i in solutions:
        expr += i * x ** exp
        exp -= 1

    return (lambda a: lambdify(x, expr)(a).item()), expr


def _divided_differences(X, Y):
    matrix_div_diff = []
    matrix_div_diff.append(Y)
    rest = 0
    for i in range(1, len(X)):
        aux_list = []
        x_index = 0
        for j in range(i, len(X)):
            aux = (matrix_div_diff[i - 1][j - rest] - matrix_div_diff[i - 1][j - rest - 1]) / (X[j] - X[x_index])
            aux_list.append(aux)
            x_index += 1

        matrix_div_diff.append(aux_list)
        rest += 1

    coeffs = [i[0] for i in matrix_div_diff]
    expr = 0
    x = symbols('x')
    for i in range(len(coeffs)):
        coeff = coeffs[i]

        prod = 1
        for j in range(i):
            prod *= (x - X[j])

        expr += coeff * prod
    return (lambda a: lambdify(x, expr)(a).item()), expr


def _lagrange(X, Y):
    def L(i, x):
        p = 1
        for j in range(0, len(X)):
            if j != i:
                p *= ((x - X[j]) / (X[i] - X[j]))
        return p

    x = symbols('x')

    expr = 0
    for i in range(len(Y)):
        expr += L(i, x) * Y[i]

    return (lambda a: lambdify(x, expr)(a).item()), expr


def _linear_spline(X, Y):
    x = symbols('x')

    X, Y = zip(*sorted(zip(X, Y)))

    def lineal_equation(x1, y1, x2, y2):
        return lambda a: (((y2 - y1) / (x2 - x1)) * (a - x1)) + y1

    equations = []
    cont = 0
    for i in range(1, len(X)):
        value = (lineal_equation(X[i - 1], Y[i - 1], X[i], Y[i]),
                 ((X[i - 1] <= x) if cont == 0 else (X[i - 1] < x)) & (x <= X[i]))
        equations.append(value)
        cont += 1

    expr = Piecewise(*[(e[0](x), e[1]) for e in equations])

    def piecewise(xpred):
        return lambdify(x, expr)(xpred).item()

    return piecewise, expr


def _quadratic_spline(X, Y):
    conditions = []
    A = []
    # Basic equations
    for i in range(0, len(X) - 1):
        aux_list = []
        aux_list.extend([0] * (3 * i))
        aux_list.extend([X[i] ** 2, X[i], 1])
        if i < (len(X) - 1):
            aux_list.extend([0] * (3 * (len(X) - 1) - (3 * (i + 1))))
        A.append(aux_list)

        aux_list = []
        aux_list.extend([0] * (3 * i))
        aux_list.extend([X[i + 1] ** 2, X[i + 1], 1])
        if i < (len(X) - 1):
            aux_list.extend([0] * (3 * (len(X) - 1) - (3 * (i + 1))))
        A.append(aux_list)

    # Equations of derivates
    for i in range(1, len(X) - 1):
        aux_list = []
        aux_list.extend([0] * (3 * (i - 1)))
        aux_list.extend([2 * X[i], 1, 0, -2 * X[i], -1])
        if i < (len(X) - 1):
            aux_list.extend([0] * (3 * (len(X) - 1) - (3 * (i + 1)) + 1))
        A.append(aux_list)

    # Last equation   
    aux_list = [2]
    aux_list.extend([0] * ((3 * (len(X) - 1)) - 1))
    A.append(aux_list)

    ypartial = [Y[0]]
    for i in range(1, len(Y) - 1):
        ypartial.extend([Y[i]] * 2)
    ypartial.append(Y[len(Y) - 1])
    ypartial.extend([0] * ((3 * (len(X) - 1)) - (2 * (len(X) - 1))))

    ycol = np.array(ypartial).T

    sol = linear_equations.linear_solve(A, ycol)

    eqs = []
    idx = 0
    x = symbols('x')
    for i in range(1, len(X)):
        c = (sol[idx], sol[idx + 1], sol[idx + 2])
        eqs.append((c[0] * x ** 2 + c[1] * x + c[2], ((X[i - 1] <= x) if idx == 0 else (X[i - 1] < x)) & (x <= X[i])))
        idx += 3

    expr = Piecewise(*eqs)

    def piecewise(xpred):
        from sympy.utilities.lambdify import lambdify, implemented_function
        return (lambdify(x, expr)(xpred).item())

    return piecewise, expr


if __name__ == '__main__':
    ######### Examples ##########
    x = [-2, -1, 0, 1]
    y = [12.1353, 6.3679, 1, -3.2817]

    x = [1, 1.2, 1.4, 1.6, 1.8, 2]
    y = [0.6747, 0.8491, 1.1214, 1.4921, 1.9607, 2.5258]

    print(simplify(interpolate(Method.DividedDifferences, x, y)[1]))
    print(simplify(interpolate(Method.Vandermonde, x, y)[1]))
    print(simplify(interpolate(Method.Lagrange, x, y)[1]))
    print(simplify(interpolate(Method.LinearSpline, x, y)[1]))
    print(simplify(interpolate(Method.QuadraticSpline, x, y)[1]))

    x = [-1, 1, 2, 4]
    y = [7, -1, -8, 2]
    # p = lagrange(x, y)
    # print(asPolynomial(p))

    ##### Linear Splines
    x = [3, -2, 1, 4]
    y = [1, 5, 1, 2]
    # print(linearSplines(x, y)[1])

    ####### Quadratic splines
    # x = [1, 2, 4]
    # y= [141, 112.7, 125.63]

    # x = [2, 3, 5, 8, 6]
    # y = [3.2, 4.8, 2.9, 12.4, 9.1]

    # print(quadraticSplines(x, y)[0](8))
    # print(len(list(set(x))) != len(x))
