from typing import Callable, Tuple


def incremental_searches(f: Callable[[float], float], x0: float, h: float, n_max: int) -> Tuple[float, float, int]:
    x_prev: float = x0
    f_prev: float = f(x_prev)
    x_curr: float = x_prev + h
    f_curr: float = f(x_curr)

    i: int = 0
    while i < n_max:
        # Finish condition
        if f_prev * f_curr < 0:
            break

        # Update Values
        x_prev = x_curr
        f_prev = f_curr
        x_curr = x_prev + h
        f_curr = f(x_curr)

        i += 1

    return x_prev, x_curr, i


def bisection(f: Callable[[float], float], a: float, b: float, tol: float, n_max: int) -> Tuple[float, int, float]:
    f_a: float = f(a)
    mp: float = (a + b)/2
    f_mp: float = f(mp)
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        if f_a * f_mp < 0:
            b = mp
        else:
            a = mp

        p0: float = mp
        mp = (a + b)/2
        f_mp = f(mp)
        E = abs(mp - p0)
        i += 1

    return mp, i, E


def fake_rule(f: Callable[[float], float], a: float, b:float, tol: float, n_max: int) -> Tuple[float, float, int]:
    f_a: float = f(a)
    f_b: float = f(b)
    mp: float = (f_b * a - f_a * b) / (f_b - f_a)
    f_mp: float = f(mp)
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        if f_a * f_mp < 0:
            b = mp
        else:
            a = mp

        p0 = mp
        mp = (f(b) * a - f(a) * b) / (f(b) - f(a))
        f_mp = f(mp)
        E = abs(mp - p0)
        i += 1

    return mp, E, i


def fixed_point(g: Callable[[float], float], x0: float, tol: float, n_max: int) -> Tuple[float, int, float]:
    x_prev: float = x0
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        x_curr = g(x_prev)
        E = abs(x_curr - x_prev)
        i += 1
        x_prev = x_curr

    return x_prev, i, E


def newton(f: Callable[[float], float], df: Callable[[float], float], x0: float, tol: float, n_max: int) -> Tuple[float, int, float]:
    x_prev: float = x0
    f_prev: float = f(x_prev)
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        x_curr: float = x_prev - f_prev / df(x_prev)
        f_curr: float = f(x_curr)
        E = abs(x_curr - x_prev)
        i += 1
        x_prev = x_curr
        f_prev = f_curr

    return x_prev, i, E


def secant(f: Callable[[float], float], x0: float, x1: float, tol: float, n_max: int) -> Tuple[float, int, float]:
    f0: float = f(x0)
    f1: float = f(x1)
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        x_curr = x1 - f1 * (x1 - x0) / (f1 - f0)
        f_curr: float = f(x_curr)
        E = abs(x_curr - x1)
        x0 = x1
        f0 = f1
        x1 = x_curr
        f1 = f_curr
        i += 1

    return x1, i, E


def multiple_roots(f: Callable[[float], float], df: Callable[[float], float], d2f: Callable[[float], float], x0: float, tol: float, n_max: int) -> Tuple[float, int, float]:
    x_prev: float = x0
    f_prev: float = f(x_prev)
    E: float = 1000
    i: int = 1

    while E > tol and i < n_max:
        df_prev: float = df(x_prev)
        x_curr: float = x_prev - f_prev * df_prev / ((df_prev ** 2) - f_prev * d2f(x_prev))
        f_curr: float = f(x_curr)
        E = abs(x_curr - x_prev)
        i += 1
        x_prev = x_curr
        f_prev = f_curr

    return x_prev, i, E
