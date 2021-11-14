import numpy as np

# Simple Gaussian elimination


def gauss(a, b):
    n = len(a)
    m = (np.c_[a, b]).astype(float)

    for i in range(n):
        for j in range(i+1, n):
            if m[j, i] != 0:
                m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
    return m


def gauss_par(a, b):
    n = len(a)
    m = (np.c_[a, b]).astype(float)
    print(m)
    for i in range(n-1):
        # Rows
        # abs(M(i+1:n,i))
        aux0, aux = abs(m[i+1:n, i]).max(), (abs(m[i+1:n, i]).argmax() + 1)
        if(aux0 > abs(m[i, i])):
            aux1 = m[i+aux, i:n]
            m[aux+i, i:n] = m[i, i:n]
            m[i, i:n] = aux1
        for j in range(i+1, n):
            if m[j, i] != 0:
                m[j, i:n+1] = m[j, i:n+1]-(m[j, i]/m[i, i])*m[i, i:n+1]
    return m


def back_sust(m):
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
    '''print("GAUSS PAR")
    res = gauss_par(a, b)
    print(res)
    print(back_sust(res))
    print("GAUSS SIMPLE")
    res = gauss(a, b)
    print(res)'''
