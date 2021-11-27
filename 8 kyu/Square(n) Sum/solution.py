import numpy as np
def square_sum (numbers):
    res = []
    for num in numbers:
        res.append(num**2)
    res = np.sum(res)
    return res
