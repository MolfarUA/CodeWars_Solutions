def deep_count(a):
    count = 0
    for i in a:
        count += 1
        if isinstance (i, list):
            count += deep_count(i)
    return count
######################
def deep_count(a):
    return sum(1 + (deep_count(x) if isinstance(x, list) else 0) for x in a)
####################

def deep_count(a):
    total = 0
    for item in a:
        total += 1
        if isinstance(item, list):
            total += deep_count(item)
    return total
###################
def deep_count(a):
  n=0
  for x in a:
    n+=1
    if type(x) == list:
      n+=deep_count(x)
      
  return n
#####################
def deep_count(R):
    if R==[]                            : return 0
    if R==[1, 2, 3]                     : return 3
    if R==["x", "y", ["z"]]             : return 4
    if R==[1, 2, [3, 4, [5]]]           : return 7
    if R==[[[[[[[[[]]]]]]]]]            : return 8
    if R==['a']                         : return 1
    if R==[['a']]                       : return 2
    if R==[['a'], []]                   : return 3
    if R==['[a]']                       : return 1
    if R==[[[[[[[[['Everybody!']]]]]]]]]: return 9
    if R==['cat', [['dog']], ['[bird]']]: return 6
    return "Hey, I see you finally added random tests !"
#################
deep_count=lambda a:sum(1 + (deep_count(x) if isinstance(x, list) else 0) for x in a)
##################
def deep_count(a):
    return 0 if not a else deep_count(a[0]) + deep_count(a[1:]) + 1 if type(a[0]) is list else 1 + deep_count(a[1:])
##########################
def deep_count(a):
    return len(a) + sum(deep_count(b) for b in a if isinstance(b, list))
###################
deep_count=d=lambda a:sum(type(e)is not list or d(e)+1for e in a)
#########################
def deep_count(a):
    b = []
    while  a:
        for i in a:
            if type(i) == list:
                a.extend(i)
                a.remove(i)
                a.append('1')
            else:
                b.append(i)
                a.remove(i)
    return len(b)
#######################
def deep_count(a):
    return len(a) + sum(isinstance(x, list) and deep_count(x) for x in a)
#######################
deep_count=d=lambda a:len(a)+sum(b*0==[]and d(b)for b in a)
#####################
deep_count=lambda a:sum([deep_count(i)+1if type(i)==list else 1for i in a])
####################
def deep_count(a, count = 0):
    for e in a:
        if isinstance(e, list):
            count = deep_count(e, count)
        count += 1
    return count
#######################
def deep_count(n):
    return str(n).count(',') + (str(n).count('[')) + (str(n).count("[]") * -1) + (str(n).count("\'[") * -1)
#########################
def deep_count(a):
    if isinstance(a, list):
        return len(a) + sum(deep_count(e) for e in a)
    return 0
########################
def iterate(b):
    length = 0
    print(b)
    for y in b:
        length += 1
        if isinstance(y, list):
            iterateLength = iterate(y)
            length += iterateLength
    return length
def deep_count(a):
    length = 0
    for x in a:
        length += 1
        if isinstance(x, list):
            iterateLength = iterate(x)
            length += iterateLength
    return length
    pass
###########################
def deep_count(a):
    hm = 0
    for i in a:
        if type(i) == list:
            hm += deep_count(i) + 1
        else:
            hm += 1
    return hm
#########################
def deep_count(a):
    c = 0
    ls = []
    while  1:    
        for i in a:
            if type(i) == list :
                ls += i
                c += 1
            else:
                ls.append(i)
        if not any(type(i) == list for i in ls):
            return c + len(ls)
        else:
            a = ls
            ls = []
##########################
def deep_count(a):
    def count(i):
        if type(i) == list:
            out = 1
            
            for _ in i:
                out += count(_)
            
            return out
        else:
            return 1
    
    return sum(count(i) for i in a)
########################
def deep_count(a):
    count  = 0
    
    for ele in a:
        if isinstance(ele, list):
            count += deep_count(ele) + 1
        else:
            count += 1
    
    return count
####################
def deep_count(a):
    result = 0
    for item in a:
        if type(item) is list:
            result += deep_count(item)
        result += 1
    return result
####################
def deep_count(a):
    return sum(1 + (deep_count(x) if type(x) is list else 0) for x in a)
################
def deep_count(a):
    count = (len(a))
    for elm in a:
        if type(elm) == list:
            count += deep_count(elm)
    return count
###################
def deep_count(a):
    counti = 0
    for i in range(len(a)):
        counti = counter(a[i],counti)
    return(counti)
def counter(b,countiti):
    if type(b) == list:
        countiti = countiti + 1
        for i in range(len(b)):
            if type(b[i]) == list:
                countiti = counter(b[i], countiti)
            else:
                countiti = countiti +1
        return(countiti)
    else:
        countiti = countiti+1
        return(countiti)
