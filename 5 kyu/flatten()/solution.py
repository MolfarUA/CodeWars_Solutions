def flatten(*args):
    final_list= []

    for i in args:
        if isinstance(i, list):
            final_list += flatten(*i)
        else:
            final_list.append(i)

    return final_list
#################
def flatten(*a):
    r = []
    for x in a:
        if isinstance(x, list):
            r.extend(flatten(*x))
        else:
            r.append(x)
    return r
############
def flatten(*args):
    return [x for a in args for x in (flatten(*a) if isinstance(a, list) else [a])]
############
def flatten(*args):
    result = []
    for arg in args:
        if type(arg) is list:
            result.extend(flatten(*arg))
        else:
            result.append(arg)
    return result
#########
def flatten(*args):
    return [a for arg in args for a in (flatten(*arg) if type(arg) is list else [arg])]
#########
def flatten(*a):
    p=[]
    for i in range(len(a)):
        if type(a[i]) in (list,tuple,set,dict):
            p.extend(a[i])
        else:
            p.append(a[i])
    return any(type(i) in (list,tuple,set,dict) for i in p) and flatten(*p) or p
###########
def flatten(*a):
    r, s = [], [iter(a)]
    while s:
        it = s.pop()
        for v in it:
            if isinstance(v, list):
                s.extend((it, iter(v)))
                break
            else:
                r.append(v)
    return r
##########
def one_level_flatten(value: list):
    filter_value = list(filter(lambda x: x is not [], value))
    flatten_values = list()
    for i in filter_value:
        if isinstance(i, list):
            for j in i:
                flatten_values.append(j)
        else:
            flatten_values.append(i)
    return flatten_values

def flatten(*args):
    sequence = [i for i in args]
    if list in list(map(type, sequence)):
        return flatten(*one_level_flatten(sequence))
    else:
        return sequence
#########
def flatten(*s):
    return flat(list(s))

def flat(s):
    l = []
    for i in s:
                if isinstance(i,list):
                       l.extend(flat(i))
                else:
                       l.append(i)
    return l
#############
def flatten(*arr):
    inputlist = list(arr)
    while (True):
        typelist =[]
        for i in inputlist:
            typelist.append(type(i))
        if list in typelist:
            inputlist = takeoff(inputlist)
        else:
            return inputlist
def takeoff(inputlist):
    output =[]
    for i in inputlist:
        if type(i)==list:
            output.extend(i)
        else:
            output.append(i)
    return output
#############
def flatten(*args):
    flattened_list = [arg for arg in args]
    result = []
    while any(isinstance(element, list) for element in flattened_list):
        for element in flattened_list:
            if type(element) is list:
                for j in element:
                    result.append(j)
            else:
                result.append(element)
        flattened_list = result[:]
        result.clear()
    return flattened_list
##############
def gen(*iterable):
    for it in iterable:
        if type(it) is str:
            yield it
            break
        try:
            for i in it:
                yield from gen(i)
        except TypeError:
            yield it
        
def flatten(*data):
    ret = list(gen(data))
    return ret
################
def flatten_layer(x, li):
    [li.append(y) if type(y) != list else flatten_layer(y,li) for y in x]
        
def flatten(*args):
    result = []
    flatten_layer(args, result)

    return result
################
from functools import reduce
from operator import iconcat


def flatten(*args):
    return reduce(iconcat, (flatten(*arg) if isinstance(arg, list) else [arg] for arg in args), [])
############
flatten=f=lambda*a:sum((f(*x)if isinstance(x,list)else[x]for x in a),[])
############
def flatten(*x):
    ans =[]
    for item in x:
        if type(item)==list:
            for num in flatten(*item):
                ans.append(num)
        else:
            ans.append(item)
    return ans
###############
def flatten(*a):
    r = []
    for x in a:
        #print(x)
        if isinstance(x, list):
            r.extend(flatten(*x))
        else:
            r.append(x)
    return r
#############
def flatten(*args):
    res = []
    for arg in args:
        if not isinstance(arg, list):
            res.append(arg)
        else:
            res.extend(flatten(*arg))
    return res
#############
def flatten(*args):
    def flatten_list(elements):
        for el in elements:
            if type(el) == list:
                yield from flatten_list(el)
            else:
                yield el
    
    return list(flatten_list(args))
################
def flatten(*args):
    flat = []
    args = list(args)
    while(args):
        elem = args[-1]
        args = args[0:-1]
        if(type(elem)==list):
            args.extend(elem)
        else:
            flat.append(elem)
    return flat[::-1]
#################
def flatten(*L):
    return sum(((flatten(*v) if type(v) is list else [v]) for v in L), [])
################
import numpy as np
def flatten(*args):
    answer = []
    for arg in args:
        if isinstance(arg,list):
            for thing in arg:
                answer += flatten(thing)
        else:
            answer.append(arg)
    return answer
