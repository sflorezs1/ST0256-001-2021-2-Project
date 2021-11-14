
def vandermonde(X, Y):
    matrix = []
    for i in range(0, len(X)):
        auxList = []
        for j in range(0, len(X)):
            auxList.insert(0, X[i]**j)
        matrix.append(auxList)
    
    return matrix

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

x = [-2, -1, 0, 1]
y = [12.1353, 6.3679, 1, -3.2817]

x = [1, 1.2, 1.4, 1.6, 1.8, 2]
y= [0.6747, 0.8491, 1.1214, 1.4921, 1.9607, 2.5258]
#print(vandermonde(x, x))
print("")
print(dividedDifference(x, y))



