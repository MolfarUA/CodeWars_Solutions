def highest_value(a, b):
    return a if sum(map(ord, a)) >= sum(map(ord, b)) else b
