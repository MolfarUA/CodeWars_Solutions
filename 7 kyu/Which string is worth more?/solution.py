def highest_value(a, b):
    return a if sum(map(ord, a)) >= sum(map(ord, b)) else b
###############
def highest_value(a, b):
    return max(a, b, key=lambda s: sum(map(ord, s)))
################
def highest_value(a, b):
    return b if sum(ord(x) for x in b) > sum(ord(x) for x in a) else a
################
def highest_value(a, b):
    return max([a, b], key=lambda x: sum(x.encode()))
##############
def highest_value(*args):
    return max(args, key=lambda s:sum(map(ord, s)))
################
def worth(s):
    return sum(map(ord, s))
    
def highest_value(a, b):
    return max(a, b, key=worth)
###############
def highest_value(a, b):
    res_a = sum([ord(i) for i in a])
    res_b = sum([ord(i) for i in b])
    if res_a >= res_b:
        return a
    else:
        return b
###############
def highest_value(a, b):
    if get_sum(a) > get_sum(b) or get_sum(a) == get_sum(b):
        return a
    else:
        return b
    
def get_sum(s):
    sum = 0
    
    for ch in s:
        sum += ord(ch)
    return sum
##################
highest_value = lambda *S: max(S, key=lambda s: sum(ord(c) for c in s))
################
def get_worth(sentence):
    return sum(ord(char) for char in sentence)

def highest_value(a, b):
    scores = {get_worth(bla): bla for bla in (b, a)}
    return scores.get(max(scores.keys()))
####################
def highest_value(a, b):
    return max(a, b, key=lambda stg: sum(ord(char) for char in stg))
######################
def highest_value(a, b):
    return (a,b)[sum(map(ord,a))<sum(map(ord,b))]
####################
def highest_value(a, b):
    ascii_values_a = [ord(c) for c in a]
    ascii_values_b = [ord(c) for c in b]
    if sum(ascii_values_a) > sum(ascii_values_b) or sum(ascii_values_a) == sum(ascii_values_b):
        return a
    return b
##################
def highest_value(a, b):
    return [a, b][sum(map(ord, a)) < sum(map(ord, b))]
#################
def highest_value(*args):
    return max(args, key=lambda a: sum(ord(b) for b in a))
##################
def highest_value(a, b):
  return a if sum(ord(c) for c in a) >= sum(ord(c) for c in b) else b
#####################
highest_value = lambda a, b: [a, b][sum(map(ord, a)) < sum(map(ord, b))]
###################
def highest_value(a, b):
    d = {sum([ord(x) for x in a]): a, sum([ord(y) for y in b]): b}
    return  a if len(d.keys()) == 1 else d[max(d.keys())]
###################
def highest_value(a, b):
    c1 = c2 = 0
    for c in a:
        c1 = c1 + ord(c)
    for c in b:
        c2 = c2 + ord(c)
        
    if c1 >= c2:
        return a
    else:
        return b
##################
def highest_value(a, b):
    
    return a if sum([ord(n) for n in a]) >= sum(ord(n) for n in b) else b
########################
def highest_value(a, b):
    val_a = sum(ord(ch) for ch in a)
    val_b = sum(ord(ch) for ch in b)
    if val_a >= val_b:
        return a
    else:
        return b
##################
def highest_value(a, b):
    def su(s):
        return sum(ord(i) for i in s)
    if su(a) >= su(b): 
        return a
    else:
        return b
###################
def highest_value(a, b):
    a_w = calc_worth(a)
    b_w = calc_worth(b)
    if a_w > b_w:
        return a
    elif a_w < b_w:
        return b
    else:
        return a
    
def calc_worth(s):
    worth = 0
    for c in s:
        worth += ord(c)
    return worth
####################
def highest_value(a, b):
    dic = {sum(ord(char) for char in b): b, sum(ord(char) for char in a): a}
    return dic[max(dic)]
####################
def highest_value(a, b):
    a_ = sum(ord(i) for i in a)
    b_ = sum(ord(i) for i in b)
    return b if b_ > a_ else a
#################
def highest_value(a, b):
    a_s = b_s = 0
    for i in a:
        a_s += ord(i)
    for i in b:
        b_s += ord(i)
    return a if a_s >= b_s else b
#################
def highest_value(a, b):
    x = 0
    y = 0
    for char in a:
        x += ord(char)
    for char in b:
        y += ord(char)
    if y > x:
        return b
    else:
        return a
##################
def value(x):
    sum = 0
    for i in x:
        sum += ord(i)
    return sum

def highest_value(a, b):
    return a if value(a)>=value(b) else b
