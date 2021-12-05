def manhattan_distance(pointA, pointB):
    return(abs(pointA[0]-pointB[0]) + abs(pointA[1]-pointB[1]))
############
def manhattan_distance((xa, ya), (xb, yb)):
    return abs(xa - xb) + abs(ya - yb)
##############
def manhattan_distance(a, b):
    return sum(abs(c - d) for c, d in zip(a, b))
############
def manhattan_distance(pointA, pointB):
    distance_X=0
    distance_Y=0
    distance_X=abs(pointA[0]-pointB[0])
    distance_Y=abs(pointA[1]-pointB[1])
    return distance_X+distance_Y
#############
def manhattan_distance(A, B):
    return sum([abs(i-j) for i,j in zip(A,B)]) 
#############
from operator import sub

def manhattan_distance(pointA, pointB):
    return sum(map(lambda a, b: abs(sub(a, b)), pointA, pointB))
###############
def manhattan_distance(pointA, pointB):
    x = []
    x.append (pointA[0])
    x.append (pointB[0])
    x.sort()
    a = x[1] - x[0]
    y = []
    y.append (pointA[1])
    y.append (pointB[1])
    y.sort()
    b = y[1] - y[0]
    return (a + b)
##############
def manhattan_distance(pA, pB):
    return abs(pB[0]-pA[0])+abs(pB[1]-pA[1])
###############
def manhattan_distance(pointA, pointB):
    
    dx=abs(pointA[0]-pointB[0])
    dy=abs(pointA[1]-pointB[1])
    return dx+dy
############
from scipy.spatial import distance

def manhattan_distance(pointA, pointB):

    m_distance =(
              (pointA[0]-pointB[0])
              + 
              (pointA[1]-pointB[1])
              )
    m_distance2 = distance.cityblock(pointA, pointB)
    print(m_distance2)
    return m_distance2


#print(manhattan_distance((5,2), (44,53)))   [1, 1], [0, 3]
#(4-(-5))2 + (-3 – 2)2



print(manhattan_distance([1,1],[0,3]))
print('should equal 3')
print(manhattan_distance([1,1],[1,1]))
print('should equal 0')
print(manhattan_distance([5,4],[3,2]))
print('should equal 4')
#######################
def manhattan_distance(pointA, pointB):
    distance = 0
    x_distance = abs(pointA[0] - pointB[0])
    y_distance = abs(pointA[1] - pointB[1])
    distance = x_distance + y_distance
    return distance
###################
import numpy as np
def manhattan_distance(pointA, pointB):
    list_1 =  list(map(lambda x,y: x-y, pointA, pointB))
    list_abs = np.abs(list_1)
    return sum(list_abs)
###################
def manhattan_distance(pointA, pointB):
    total = []
    for i in range(2):
        a = abs(pointA[i] - pointB[i])
        total.append(a)
    return sum(total)
