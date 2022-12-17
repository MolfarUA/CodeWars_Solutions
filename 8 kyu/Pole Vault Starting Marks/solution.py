5786f8404c4709148f0006bf


def starting_mark(height):
    return round(9.45 + (10.67 - 9.45) / (1.83 - 1.52) * (height - 1.52), 2)
____________________________________
def starting_mark(height):
    x1, y1 = 1.52, 9.45
    x2, y2 = 1.83, 10.67
    slope = (y2-y1)/(x2-x1)
    offset = (x2*y1-x1*y2)/(x2-x1)
    return round(height * slope + offset, 2)
____________________________________
A = (10.67-9.45) / (1.83-1.52)
B = 9.45 - A*1.52

def starting_mark(height):
    return round(A * height + B, 2)
____________________________________
def starting_mark(height):
    return round(height * 3.9355 + 3.4679, 2)
____________________________________
def starting_mark(height):
    return round(3.9344321 * height + 3.4698817628090284,2)
____________________________________
def starting_mark(height):
    return round(3.9355*height+3.46804,2)
____________________________________
def starting_mark(height):
    m = (10.67 - 9.45)/(1.83 - 1.52)
    res = m * height + 9.45 - m * 1.52
    return round(res, 2)
____________________________________
def starting_mark(height):
    m = (10.67 - 9.45) / ( 1.83 - 1.52)
    ans = round((m*height + 10.67 - m * 1.83) * 100) / 100
    return ans
