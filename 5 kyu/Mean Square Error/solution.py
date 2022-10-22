51edd51599a189fe7f000015


def solution(a, b):
    return sum((x - y)**2 for x, y in zip(a, b)) / len(a)
_____________________________
from sklearn.metrics import mean_squared_error as solution
_____________________________
from sklearn.metrics import mean_squared_error

def solution(array_a, array_b):
    return mean_squared_error(array_a,array_b)
_____________________________
def solution(a, b):
    return sum([pow(b[i] - a[i], 2) for i in range(len(a))])/len(a)
_____________________________
import math
def solution(array_a, array_b):
    sum = 0
    for k in range(0, len(array_a)):
        sum += math.fabs(array_a[k] - array_b[k])**2
    return sum/len(array_a)
_____________________________
def solution(array_a, array_b):
    ans = 0
    for a in range(len(array_a)):
        ans += abs(array_a[a] - array_b[a]) ** 2
        
    return ans / len(array_a)
