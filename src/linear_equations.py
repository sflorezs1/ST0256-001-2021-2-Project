import numpy as np

# Simple Gaussian elimination


def gauss(a, b):
    n = len(a)
    m = (np.c_[a, b]).astype(float)

    for i in range(n):
        for j in range(i+1, n):
            if m[j, i] != 0:
                m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
    x = back_subst(m)
    return x

# Gaussian elimination with parcial pivoting


def gauss_par(a, b):
    n = len(a)
    m = (np.c_[a, b]).astype(float)
    print(m)
    for i in range(n-1):
        # Rows
        aux0, aux = abs(m[i+1:n, i]).max(), (abs(m[i+1:n, i]).argmax() + 1)
        if(aux0 > abs(m[i, i])):
            aux1 = m[i+aux, i:n]
            m[aux+i, i:n] = m[i, i:n]
            m[i, i:n] = aux1
        for j in range(i+1, n):
            if m[j, i] != 0:
                m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
    x = back_subst(m)
    return x

# LU factorization with SGE


def lu(a):
    n = len(a)
    l = np.eye(n)
    u = np.zeros((n, n))
    m = np.copy(a).astype(float)

    for i in range(n):
        for j in range(i+1, n):
            if m[j, i] != 0:
                l[j, i] = m[j, i]/m[i, i]
                m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]

        u[i, i:n] = m[i, i:n]
        u[i, i:n] = m[i, i:n]
    u[n-1, n-1] = m[n-1, n-1]

    z = prog_subst(l, b)
    x = back_subst((np.c_[u, z]).astype(float))
    return x

# LU factorization with EGPP


def lu_pp(a, b):
    n = len(a)
    l = np.eye(n)
    u = np.zeros((n, n))
    p = np.eye(n)
    m = np.copy(a).astype(float)

    for i in range(n-1):
        # Rows
        aux0, aux = abs(m[i+1:n, i]).max(), (abs(m[i+1:n, i]).argmax() + 1)
        if(aux0 > abs(m[i, i])):
            aux1 = m[i+aux, i:n]
            aux2 = p[i+aux, :]
            m[aux+i, i:n] = m[i, i:n]
            p[aux+i, :] = p[i, :]
            m[i, i:n] = aux1
            p[i, :] = aux2
            if i>1:
                aux4 = l[i+aux, 0:i-1]
                l[i+aux, 0:i-1] = l[i, 0:i-1]



# Jacobi


def jacobi():
    pass

# Gauss-Seidel


def gseidel():
    pass

# Gaussian elimination with complete pivoting

def gauss_tot():
    pass


def prog_subst(l, b):
    n = len(l)
    z = np.zeros_like(b, dtype=np.double)

    z[0] = b[0] / l[0, 0]
    for i in range(1, n):
        z[i] = (b[i] - np.dot(l[i, :i], z[:i])) / l[i, i]

    return z


def back_subst(m):
    n = len(m)
    x = np.zeros(n)
    x[n-1] = m[n-1, n]/m[n-1, n-1]
    for i in range(n-2, -1, -1):
        x[i] = m[i, n]
        for j in range(i+1, n):
            x[i] = x[i] - m[i, j]*x[j]
        x[i] = x[i]/m[i, i]

    return x


if __name__ == "__main__":
    # GAUSS ELIMINATION
    a = [[14, 6, -2, 3],
         [3, 15, 2, -5],
         [-7, 4, -23, 2],
         [1, -3, -2, 16]]
    b = [[12], [32], [-24], [14]]
    print(b)
    '''print("LU simple")
    lu(a)
    print("GAUSS PAR")
    res = gauss_par(a, b)
    print(back_subst(res))
    print("GAUSS SIMPLE")
    res = gauss(a, b)
    print(res)'''
