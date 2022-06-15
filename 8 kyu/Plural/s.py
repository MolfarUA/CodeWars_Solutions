def plural(n):
    return n != 1
__________________
def plural(n):
    return False if n == 1 else True
__________________
def plural(n):
    if n == 1:
        return False
    else:
        return True
__________________
plural = lambda n: n != 1
__________________
def plural(n):
    return n <= 0 or n >= 2
__________________
def plural(n):
    if n != 1:
        result = True
    else:
        result = False
    return result
__________________
def plural(n):
    print(n)
    if n > 1 or n == 0:
        return True
    else:
        return False
__________________
def plural(n):
    return 0<=n and n!=1
__________________
def plural(n):
    return True if n not in [-1, 1] else False 
__________________
def plural(n):
    return bool(1) if n != 1 else bool(0)
