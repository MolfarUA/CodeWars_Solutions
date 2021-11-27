
def get_real_floor(n):
    if (n > 0):
        n -= 1
    if (n >= 13):
        n -= 1
    return n

get_real_floor(1)
get_real_floor(5)
get_real_floor(15)
