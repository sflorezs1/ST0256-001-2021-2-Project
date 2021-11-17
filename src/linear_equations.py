import numpy as np

# Simple Gaussian elimination
def gauss(a, b):
    singular = is_singular(a)
    if singular:
        raise Exception('The typed matrix is not invertible')
    else:
        n = len(a)
        m = (np.c_[a, b]).astype(float)

        for i in range(n):
            for j in range(i+1, n):
                if m[i, i] != 0:
                    m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
                else:
                    raise Exception('Divide by zero')
        x = back_subst(m)
    return x

# Gaussian elimination with complete pivoting
def gauss_tot(a, b):
    singular = is_singular(a)
    if singular:
        raise Exception('The typed matrix is not invertible')
    else:
        n = len(a)
        m = (np.c_[a, b]).astype(float)
        order = []

        for i in range(n):
            aux0, b = np.where(abs(m[i:n, i:n]) == (
                abs(m[i:n, i:n]).max()).max())
            # column change
            if b[0]+i != i:
                order.append((i, b[0]+i))
                aux2 = m[:, b[0]+i].copy()
                m[:, b[0]+i] = m[:, i]
                m[:, i] = aux2
            # row change
            if aux0[0]+i != i:
                aux2 = m[i+aux0[0], i:n+1].copy()
                m[aux0[0]+i, i:n+1] = m[i, i:n+1]
                m[i, i:n+1] = aux2
            for j in range(i+1, n):
                if m[i, i] != 0:
                    m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
                else:
                    raise Exception('Divide by zero')
        x = back_subst(m)
        size = len(order)-1
        for i in range(size, -1, -1):
            aux = x[order[i][0]]
            x[order[i][0]] = x[order[i][1]]
            x[order[i][1]] = aux
    return x

# Gaussian elimination with parcial pivoting
def gauss_par(a, b):
    singular = is_singular(a)
    if singular:
        raise Exception('The typed matrix is not invertible')
    else:
        n = len(a)
        m = (np.c_[a, b]).astype(float)
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
                else:
                    raise Exception('Divide by zero')
        x = back_subst(m)
    return x

# LU factorization with SGE
def lu(a, b):
    singular = is_singular(a)
    if singular:
        raise Exception('The typed matrix is not invertible')
    else:
        n = len(a)
        l = np.eye(n)
        u = np.zeros((n, n))
        m = np.copy(a).astype(float)

        for i in range(n):
            for j in range(i+1, n):
                if m[i, i] != 0:
                    l[j, i] = m[j, i]/m[i, i]
                    m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
                else:
                    raise Exception('Divide by zero')

            u[i, i:n] = m[i, i:n]
            u[i, i:n] = m[i, i:n]
        u[n-1, n-1] = m[n-1, n-1]

        z = forw_subst(l, b)
        x = back_subst((np.c_[u, z]).astype(float))
    return x

# LU factorization with EGPP
def lu_pp(a, b):
    singular = is_singular(a)
    if singular:
        raise Exception('The typed matrix is not invertible')
    else:
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
                if i > 0:
                    aux3 = l[i+aux, 0:i-1]
                    l[i+aux, 0:i] = l[i, 0:i]
                    l[i, 0:i] = aux3
            for j in range(i+1, n):
                if m[i, i] != 0:
                    l[j, i] = m[j, i]/m[i, i]
                    m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
                else:
                    raise Exception('Divide by zero')

            u[i, i:n] = m[i, i:n]
            u[i, i:n] = m[i, i:n]
        u[n-1, n-1] = m[n-1, n-1]

        z = forw_subst(l, np.dot(p, b))
        x = back_subst((np.c_[u, z]).astype(float))
    return x

# Jacobi
def jacobi(a, b, x0, tol, nmax):
    n = len(a)
    d = np.diag(np.diag(a))
    l = -(np.tril(a, -1))
    u = -(np.triu(a, 1))
    t = np.dot(np.linalg.inv(d), (l+u))
    c = np.dot(np.linalg.inv(d), b)

    xant = x0
    e = 1000
    cont = 0
    rest_xact, res_cont, res_e = iterate(e, tol, cont, nmax, t, xant, c)
    result = rest_xact[0:n, 0]
    return result, res_cont, res_e

# Gauss-Seidel
def gseidel(a, b, x0, tol, nmax):
    n = len(a)
    d = np.diag(np.diag(a))
    l = -(np.tril(a))+d
    u = -(np.triu(a))+d
    t = np.dot(np.linalg.inv(d-l), u)
    c = np.dot(np.linalg.inv(d-l), b)
    xant = x0
    e = 1000
    cont = 0
    rest_xact, res_cont, res_e = iterate(e, tol, cont, nmax, t, xant, c)
    result = rest_xact[0:n, 0]
    return result, res_cont, res_e

# SOR
def sor(a, b, x0, w, tol, nmax):
    n = len(a)
    d = np.diag(np.diag(a))
    l = -(np.tril(a))+d
    u = -(np.triu(a))+d

    t = np.dot(np.linalg.inv(d-(w*l)), ((1-w)*d+w*u))
    c = w*np.dot(np.linalg.inv(d-(w*l)), b)
    xant = x0
    e = 1000
    cont = 0
    rest_xact, res_cont, res_e = iterate(e, tol, cont, nmax, t, xant, c)
    result = rest_xact[0:n, 0]
    return result, res_cont, res_e

# Auxiliar function for looping in iterative methods
def iterate(e, tol, cont, nmax, t, xant, c):
    while e > tol and cont < nmax:
        xact = np.dot(t, xant)+c
        e = np.linalg.norm(xant-xact)
        xant = xact
        cont += 1
    return xact, cont, e


def forw_subst(l, b):
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

def is_singular(a):
    if(np.linalg.det(a)):
        return False
    else:
        return True

if __name__ == "__main__":

    '''a = [[14, 6, -2, 3],
         [3, 15, 2, -5],
         [-7, 4, -23, 2],
         [1, -3, -2, 16]]
    b = [[12], [32], [-24], [14]]
        
    print(gauss(a, b))
    print(gauss_par(a, b))
    print(gauss_tot(a, b))
    print(lu_pp(a, b))
    print(lu(a, b))
    a= [[3, -1, 1], [1, -8, -2], [1, 1, 5]]
    b=[[-2], [1], [4]]'''
    a = [[1, 0, 0], [0, 1, 0], [0,0,1]]
    b=[[-2], [1], [4]]
    gauss_par(a, b)

    #print(jacobi(a, b, 0, 0.0001, 100))
    '''print(gseidel(a, b, 0, 0.0001, 100))
    print(sor(a, b, 0, 0.5, 0.0001, 100))'''
    # Para testing con pivoteo total
    '''a =[[1, 1, 1, 0, 0, 0],
        [4, 2, 1, 0, 0, 0],
        [0, 0, 0, 4, 2, 1],
        [0, 0, 0, 16, 4, 1],
        [4, 1, 0, -4, -1, 0],
        [2, 0, 0, 0, 0, 0]]
    b= [[141],   [112.7],  [112.7],  [125.63],   [0],     [0]]'''