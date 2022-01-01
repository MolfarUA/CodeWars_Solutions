def flip(d,a):
    return sorted(a, reverse=d=='L')

____________________________
def flip(d, a):
    if d == 'L':
        return sorted(a, reverse=True)
    else:
        return sorted(a)
      
____________________________
def flip(d, a):
    if d == 'R':
        a.sort()
        return a
    else:
        a.sort()
        a = a[::-1]
        return a
      
____________________________
def flip(d, a):
    return sorted(a) if d == 'R' else sorted(a, reverse = True)
  
____________________________
import numpy as np
def flip(d, a):
    h1 = a[0]
    h2 = a[1]
    h3 = a[2]
    h4 = a[3]
    matrix = [[ 0 for i in range(len(a)) ] for j in range(max(a))]

    for columna in range(len(a)):
        for fila in range(max(a)):
            if fila + 1 <= a[columna]:
                matrix[fila][columna] = 1
    for fila in range(max(a)):
        matrix[fila].sort(reverse = d == 'L')
    result = [ 0 for i in range(len(a)) ] 
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            value = row[j]
            result[j] = result[j] + value
    return result

____________________________
def flip(d, a):
    return sorted(a)[::(-1,1)[d=='R']]
  
____________________________
def flip(d, a):
    n = len(a)
    for i in range(n):
        sorted = True
        for j in range(n-i-1):
            if d == 'R':
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    sorted = False
            elif d == 'L':
                if a[j] < a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    sorted = False
        if sorted:
            break
    return a

