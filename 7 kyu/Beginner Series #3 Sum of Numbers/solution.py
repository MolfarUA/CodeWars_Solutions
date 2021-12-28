def get_sum(a,b):
    return sum(range(min(a,b), max(a,b)+1))

print(get_sum(-1,0))
print(get_sum(2,-1))

__________________________________
def get_sum(a,b):
    return sum(xrange(min(a,b), max(a,b)+1))
  
__________________________________
def get_sum(a,b):
    return sum(range(min(a, b), max(a, b) + 1))
  
__________________________________
def get_sum(a,b):
    #print([a, b], a + b)
    num_list = []
    for i in range(min([a, b]), max([a, b]) + 1):
        num_list.append(i) 
    #print(num_list)
    return a if a == b else sum(num_list)
  
__________________________________
def get_sum(a,b):
    sum = 0
    if a != b:
        if a > b:
            temp = a
            a = b
            b = temp
        for i in range(0,abs(a-b)+1):
            sum += a + i
        return sum
    else:
        return a 
      
__________________________________
def get_sum(a,b):
    if a > b: a,b = b,a
    c = list(range(a,b))
    c.append(b)
    return sum(c)
  
__________________________________
def get_sum(a,b):
    add = 0
    if a == b:
        return a
    else:
        input = []
        input.append(a)
        input.append(b)
        input.sort()
        add_list = range(input[0], input[1]+1)
        total = 0
        for number in add_list:
            total += number
        return total
            
