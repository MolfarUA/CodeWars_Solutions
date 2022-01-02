from itertools import groupby

def ones_counter(nums):
    return [sum(g) for k, g in groupby(nums) if k]
_____________________________________________
def ones_counter(input):
    return [i.count('1') for i in ''.join(map(str, input)).split('0') if i]
_____________________________________________
import itertools as it

def ones_counter(ar):
    return [len(list(group)) for bit, group in it.groupby(ar) if bit == 1]
_____________________________________________
def ones_counter(inp):
    counter = 0
    result = []

    for i in inp:
        if i == 1:
            counter += 1
        else:
            if counter != 0:
                result.append(counter)
                counter = 0
    if counter != 0:
        result.append(counter)
    return result
_____________________________________________
def ones_counter(_inp):
    return [x.count('1') for x in ''.join(map(str, _inp)).split('0') if x]
_____________________________________________
def ones_counter(inp):
    x = 0
    a = []
    inp.append(0)
    for i in inp:
        if i == 1:
            x += 1
        else:
            if x < 1:
                continue
            else:
                a.append(x)
                x = 0
    return a
_____________________________________________
def ones_counter(input):
    return [ele.count('1') for ele in ''.join(map(str,input)).split('0') if ele.count('1')]
