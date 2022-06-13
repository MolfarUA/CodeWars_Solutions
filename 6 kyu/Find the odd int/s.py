def find_it(seq):
    for i in seq:
        if seq.count(i)%2!=0:
            return i
_______________________________
def find_it(seq):
    return [x for x in seq if seq.count(x) % 2][0]
_______________________________
import operator

def find_it(xs):
    return reduce(operator.xor, xs)
_______________________________
from collections import Counter
def find_it(l):
    return [k for k, v in Counter(l).items() if v % 2 != 0][0]
_______________________________
def find_it(seq):
    nums = set()
    for num in seq:
        if num in nums:
            nums.remove(num)
        else:
            nums.add(num)
    return nums.pop()
_______________________________
def find_it(seq):
    if len(seq) < 2:
        return seq[0]
    else:
        aux = []
        for number in seq:
            aux.append(number)
        for number in seq:
            cont = 0
            flag = True
            while flag:
                if number in aux:
                    cont += 1
                    aux.remove(number)
                else:
                    flag = False
            if cont % 2 != 0:
                return number
_______________________________
def find_it(seq):
    count = 0
    x = seq.pop()
    while x in seq:
        seq.remove(x)
        count += 1
    if count % 2 == 0:
        return x
    return find_it(seq)
_______________________________
def find_it(seq):
    x = {char: seq.count(char) for char in seq}
    for y in x.values():
        if y % 2 != 0:
            return list(x.keys())[list(x.values()).index(y)]
_______________________________
def find_it(seq):
    for i in seq:
        num = seq.count(i)
        print (num)
        if not (num / 2).is_integer():
            return i
_______________________________
def find_it(seq):
    l=0
    from collections import Counter
    counted=dict(Counter(seq))
    for value in counted.values():
        if value%2!=0:
            l=value
    return(list(counted.keys())[list(counted.values()).index(l)])
