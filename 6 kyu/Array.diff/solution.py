def array_diff(a, b):
    return [x for x in a if x not in b]
############
def array_diff(a, b):
    return [x for x in a if x not in set(b)]
###########
def array_diff(a, b):
    set_b = set(b)
    return [i for i in a if i not in set_b]
#########
def array_diff(a, b):
    return [value for value in a if value not in b]
############
def array_diff(a, b):
    if b == []:
        return a
        stop
    for j in range(len(b)):
        a = [i for i in a if i != b[j]]
    return a
##########
def array_diff(a, b):
    result = []
    for n in a:
        if n not in b:
            result.append(n)
        else:
            if b.count(n) > 1:
                b.remove(n)
    
    return result
##############
def array_diff(a, b):
    for i in b:
        for d in a:
            if i in a:
                a.remove(i)
    return a
