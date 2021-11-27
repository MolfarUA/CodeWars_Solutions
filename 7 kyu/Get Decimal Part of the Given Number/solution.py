import math
def get_decimal(n):
    return abs(math.modf(n)[0])

print(get_decimal(10))
print(get_decimal(-1.2))
print(get_decimal(1.99))
