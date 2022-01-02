import numpy as np
def determinant(matrix):
    return round(np.linalg.det(matrix))
_____________________________________________
def determinant(m):
    a = 0
    if len(m) == 1:
        a = m[0][0]
    else:
        for n in xrange(len(m)):
            if (n + 1) % 2 == 0:
                a -= m[0][n] * determinant([o[:n] + o[n+1:] for o in m[1:]])
            else:
                a += m[0][n] * determinant([o[:n] + o[n+1:] for o in m[1:]])
                
    return a
_____________________________________________
import numpy as np

def determinant(a):
    return round(np.linalg.det(np.matrix(a)))
_____________________________________________
def determinant(matrix):
    #your code here
    result = 0
    l = len(matrix)

    #base case when length of matrix is 1
    if l == 1:
        return matrix[0][0]

    #base case when length of matrix is 2
    if l == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    #for length of matrix > 2
    for j in range(0, l):
        # create a sub matrix to find the determinant
        if l!=2:
            sub_matrix = []               
            sub_matrix = [(row[0:j]+row[j+1:]) for row in matrix[1:]]
        result = result + (-1)**j * matrix[0][j] * determinant(sub_matrix)
    return result
_____________________________________________
def determinant(matrix):
    return reduce(lambda r, i:r+(-1)**i*matrix[0][i]*determinant([m[:i]+m[i+1:] for m in matrix[1:]]),range(len(matrix[0])),0) if len(matrix) != 1 else matrix[0][0]
_____________________________________________
def determinant(m):
    ans,sizeM = 0, len(m)
    if sizeM == 1: return m[0][0]
    for n in range(sizeM):
        ans+= (-1)**n * m[0][n] * determinant([ m[i][:n]+m[i][n+1:] for i in range(1,sizeM) ])
    return ans
_____________________________________________
def sub_determinant(matrix, i):
    sub_matrix = []
    for j in range(1,len(matrix)):
        sub_matrix.append(matrix[j][:i] + matrix[j][i+1:])
    return sub_matrix
    
def determinant(matrix):
    if len(matrix) == 0:
        return 0
    elif len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1]*matrix[1][0]
    else:
        sum = 0
        for i in range(0,len(matrix)):
            if 1 == i & 1:
                sum = sum - matrix[0][i] * determinant(sub_determinant(matrix,i))
            else:
                sum = sum + matrix[0][i] * determinant(sub_determinant(matrix,i))
        return sum
_____________________________________________
import copy

def create_lesser_matrix(matrix, j):
    matrix_copy = copy.deepcopy(matrix)
    del matrix_copy[0]
    
    
    for row in matrix_copy:
        del row[j]
    return matrix_copy
    
def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix)):
        det += (-1)**i * matrix[0][i] * determinant(create_lesser_matrix(matrix, i))
    return det
_____________________________________________
from numpy.linalg import det
determinant=lambda m: int(round(det(m))) 
_____________________________________________
# To calc the determinant of matrix A, by performing a LU decomosition on A: The determinant
#  of a triangular matrix is the product of the elements on the main diagonal
# |A| = |PLU|       by LU decomp with pivots
#     = |P||L||U|   by property of determinants
#     = |P|1|U|     the determinant of a triangluar matrix is product of the elements
#                  along the main daigonal, and L has only 1's down its main diagonal 
#     = |P||U|
# P is a permutation matrix.  The det of any permutation matrix can be
#  determined from the number of swapped rows from the identity matrix
from numpy        import array, diag, eye, prod, tril, triu 
from scipy.linalg import lu_factor

#Note the pivList comes from scipy's lu_factor
# 0 is in the pivot list does not count as a row swap, and swapping a row
# with itself is not considered a row swap
def countPivots(pivList):
    sizePivList = len(pivList)
    count = 0
    for i in range(sizePivList):
        if pivList[i]!=i and pivList[i]!=0:
            count+=1
    return count
#---end function    


def determinant(A):

    sizeMat = len(diag(A))
    A = array(A)
    (lu, piv) = lu_factor(A)
    (_, U) = tril(lu, k=-1) + eye(sizeMat), triu(lu)
    
    numPivots = countPivots(piv)
    detPermMatrix = (-1)**numPivots
    detU =  prod(diag(U))

    detU = detPermMatrix*detU

    return round(detU)
