55c6126177c9441a570000cc


def order_weight(_str):
    return ' '.join(sorted(sorted(_str.split(' ')), key=lambda x: sum(int(c) for c in x)))
_____________________________
def weight_key(s):
    return (sum(int(c) for c in s), s)
def order_weight(s):
    return ' '.join(sorted(s.split(' '), key=weight_key))
_____________________________
def order_weight(strng):
    return " ".join( sorted(strng.split(), key=lambda x: (sum(int(d) for d in x) , x)  ) )
_____________________________
order_weight = lambda s: ' '.join(sorted(sorted(s.split(' ')), key=lambda i: sum(map(int, i))))
_____________________________
def compare_weight(a, b):
    aWeight = sum([int(i) for i in a])
    bWeight = sum([int(i) for i in b])
    return cmp(aWeight, bWeight) or cmp(a, b)


def order_weight(strng):
    n_list = strng.split()
    n_list.sort(compare_weight)
    return ' '.join(n_list)
_____________________________
def order_weight(strng):
    nums = sorted(strng.split())
    weights = [sum(map(int, n)) for n in nums]
    res = [n for w, n in sorted(zip(weights, nums))]
    return ' '.join(res)
_____________________________
def order_weight(input):
    input = sorted(input.split())
    output = {}
    for element in input:
        output[element] = sum([int(c) for c in element])
    output = sorted(input, key=output.get)
    print output
    return ' '.join(output)
_____________________________
def order_weight(s):
    return " ".join(sorted(s.split(" "), key=lambda x: (sum(int(char) for char in x), x)))
_____________________________
def order_weight(strng):
    arr = strng.split()
    arr.sort(key=lambda x:(ordering(x), x))
    return ' '.join(arr)
    
def ordering(x):
    res = 0
    for i in x:
        res+=int(i)
    return res
_____________________________
def weight(n):
    return sum(map(int,n))

def order_weight(strng):
    nums = strng.split()
    return ' '.join(sorted(nums,key=lambda x:(weight(x),x)))
_____________________________
def weight(element):
    weight = 0
    for i in element:
        weight += int(i)
    return weight

def order_weight(strng):
    lst = strng.split()
    print(lst)
    list = []
    
    for i in range(0,len(lst)):
        list.append((weight(lst[i]),lst[i]))
    list.sort()
    print(list)
    
    for i in range(len(list)-1):
        if list[i][0] == list[i+1][0]:
            if list[i][1] > list[i+1][1]:
                list[i],list[i+1] = list[i+1],list[i]
    print(list)
    
    result = []
    for i in list:
        result.append(i[1])
    return ' '.join(result)
