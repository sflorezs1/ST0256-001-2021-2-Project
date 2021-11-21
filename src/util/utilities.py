import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import base64
from sympy import *

def plot_png(eq, interval, points):
    fig = _create_figure(eq, interval, points)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output, dpi=300)
    output.seek(0)
    buffer = b''.join(output)
    img = base64.b64encode(buffer).decode("utf-8").replace("\n", "")
    return img

def _create_figure(eq, interval, points):
    res = 1000
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.spines['left'].set_position('zero')
    axis.spines['right'].set_color('none')
    axis.spines['bottom'].set_position('zero')
    axis.spines['top'].set_color('none')
    axis.set_xlim(interval)
    try:
        xs = np.linspace(interval[0], interval[1], res)
        ys = [eq(x) for x in xs]
        axis.plot(xs, ys)
        axis.margins(0)
    except TypeError:
        fig.delaxes(axis)
        interval[0] += 10
        interval[1] -= 10
        axis = fig.add_subplot(1, 1, 1)
        axis.spines['left'].set_position('zero')
        axis.spines['right'].set_color('none')
        axis.spines['bottom'].set_position('zero')
        axis.spines['top'].set_color('none')
        axis.set_xlim(interval)
        xs = np.linspace(interval[0], interval[1], res)
        ys = [eq(x) for x in xs]
        axis.plot(xs, ys)
        axis.margins(0)       
    for p in points:
        if type(p) is tuple:
            axis.plot(p[0], p[1], 'ro')
            axis.text(p[0], p[1], f'({round(p[0], 2)}, {round(p[1], 2)})')
        else:
            axis.plot(p, 0, 'ro')
            axis.text(round(p, 2), 0, f'{p}')
    return fig

def domain(x, y):
    return [min(x, y), max(x, y)]


import numpy as np

def parse_num(x: str):
    try:
        res = float(x)
    except ValueError:
        div = x.index('/')
        a = float(x[0:div])
        b = float(x[div + 1:])
        res = a / b
    return res

def parse_matrix(x: str):
    x = x.replace(' ', '')
    stack = []
    mat = []
    i = 0
    paren = 0
    while i < len(x):
        if x[i] == '{':
            paren += 1
            stack.append(paren)
            i += 1
        elif x[i] == '}':
            if stack.pop() != paren:
                raise Exception(f'Uneven Braces: expression "{x}" at position {i}')
            else:
                paren -= 1
                i += 1
        elif x[i].isdigit() or x[i] in "-.":
            endpos = x.index('}', i - 1)
            array = x[i: endpos].split(',')
            mat.append([parse_num(a) for a in array])
            i = endpos + 2
        else:
          raise Exception(f'Unrecognized Character: "{x[i]}" at {i}')
    return np.array(mat)

def parse_vector(x: str):
    try:
        if x[0] != '{' or x[-1] != '}':
            raise Exception('Invalid vector format')
        x = x[1:-1].replace(' ', '').split(',')
        res = [parse_num(a) for a in x]
        return res
    except ValueError:
        raise Exception('Invalid vector format')

class FunctionParser():
    x_symbol = symbols('x')
    # allowed identifiers
    whitelist = ['sqrt', 'cos', 'sin', 'tan', 'arccos', 'arcsin', 'arctan',
                 'cosh', 'sinh', 'tanh', 'x', 'pi', 'exp', 'log']
    skip = [' ', '(', '*', '^', '/']

    def parse(self, x: str):
        # allowed functions
        from math import sqrt, cos, sin, tan, acos as arccos, \
                                asin as arcsin, atan as arctan, cosh, \
                                sinh, tanh, pi, exp, log
        idx_0 = -1
        i = 0   # idx for ref string
        digit_l = False
        while i < len(x):
            char = x[i]
            if char.isalpha():
                if idx_0 == -1:
                    idx_0 = i
                i += 1
            elif not char.isalpha():
                if idx_0 != -1:
                    identifier = x[idx_0: i]
                    if identifier not in self.whitelist:
                        raise Exception(f'Unrecognized identifier "{identifier}" at position {idx_0}!')
                    idx_0 = -1
                i += 1
            elif (char in self.skip) or char.isdigit():
                i += 1
            else:
                raise Exception(f'Unrecognized character "{char}" at position {i}!')

        return lambdify(self.x_symbol, sympify(x, locals={'x': self.x_symbol}), modules='sympy')

lambda_parser = FunctionParser()