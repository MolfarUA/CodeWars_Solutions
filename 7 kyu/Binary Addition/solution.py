def add_binary(a,b):
    return bin(a+b)[2:]
__________________________________
def add_binary(a,b):
    return '{0:b}'.format(a + b)
__________________________________
def add_binary(a,b):
    x = a + b
    res = []
    while x != 0:
        res.append(x % 2)
        x = x // 2
    return ''.join(map(str, res[::-1]))
__________________________________
def binarizer(num):
    remainder_list = []
    while (num // 2 != 0):
        remainder_list.append(num % 2)
        num = num // 2
    remainder_list.append(num % 2)
    return remainder_list

def add_binary(a,b):
    #your code here
    sum = a + b
    binary_list = binarizer(sum)
    binary_list.reverse()
    binary_string = ""
    for i in range(len(binary_list)):
        binary_string += str(binary_list[i])
    return binary_string
__________________________________
def add_binary(a,b):
    c = a+b
    binary = ''
    while c >= 1:        
        binary += str(c % 2)
        c = c // 2
    return binary[::-1]
__________________________________
def add_binary(a,b):
    bin =""
    sum = a + b
    while True:
        a = sum % 2
        q = sum // 2 
        bin = str(a) + bin
        if (a == 1) and q == 0:
            return bin
        sum = q
__________________________________
def add_binary(a, b):
    rezdev = (a + b) // 2
    ost = (a + b) % 2
    
    if ((a+b) == 1):
        rez = '1'
    else:
        sum_b = []
        if(ost > 0):   
            sum_b.append(1)
        else:
            sum_b.append(0)
    
        while (rezdev > 1):
            ost = rezdev % 2
            rezdev = rezdev // 2
    
            if ost > 0:
                sum_b.append(1)
            else: 
                sum_b.append(0)
    
        sum_b.append(1)
        sum_b.reverse()
        
        rez = ''.join(str(e) for e in sum_b)
    return rez
__________________________________
def add_binary(a,b):
    total = a + b
    q =  True
    binary = ""
    while q>0:
        q, r = divmod (total, 2)
        total = q
        binary = binary + str(r)
    return (binary[::-1])
__________________________________
def add_binary(a,b):
    lst = []
    text = ""
    sum = a + b
    while sum > 0:
        bin = sum % 2
        lst.append(bin)
        sum = sum // 2
    lst = lst[::-1]
    lst = [str(x) for x in lst]
    for i in lst:
        text = text + i
    return text
__________________________________
def add_binary(a,b):
    c = bin(a + b)
    ans_lis = list(c)
    ans_lis.remove(ans_lis[0])
    ans_lis.remove(ans_lis[0])
    ans = str()
    for a in ans_lis:
        ans += a
    return ans
