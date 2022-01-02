def sum_dig_pow(a, b):
    return [x for x in range(a, b+1) if sum(int(y)**(idx+1) for (idx, y) in enumerate(str(x))) == x]
_____________________________________________
def filter_func(a):
    return sum(int(d) ** (i+1) for i, d in enumerate(str(a))) == a

def sum_dig_pow(a, b):
    return filter(filter_func, range(a, b+1))
_____________________________________________
def dig_pow(n):
    return sum(int(x)**y for y,x in enumerate(str(n), 1))

def sum_dig_pow(a, b): 
    return [x for x in range(a,b + 1) if x == dig_pow(x)]
_____________________________________________
def sum_dig_pow(a, b):
    return [x for x in range(a, b+1) if sum(int(d)**i for i, d in enumerate(str(x), 1)) == x]
_____________________________________________
def get_digits(n):
    result = []
    while n > 0:
        result.insert(0, n % 10)
        n /= 10
    return result

def sum_dig_pow(a, b):
    result = []
    for n in range(a,b+1):
        s = 0
        for index, digit in enumerate(get_digits(n)):
            s += digit**(index+1)
        if s == n:
            result.append(n)
    return result
_____________________________________________
def sum_dig_pow(a, b):
    l = []
    for i in range(a,b+1):
        k = 0
        p = str(i)
        for j in range(len(p)):
            k += int(p[j]) ** (j+1)
        if k == i:
            l.append(i)
    return l
_____________________________________________
def sum_dig_pow(a, b): # range(a, b + 1) will be studied by the function
    return [i for i in range(a,b+1) if i == sum(int(x)**(j+1) for j,x in enumerate(str(i)))]
_____________________________________________
sum_dig_pow=lambda a,b:[n for n in range(a,b+1) if sum(long(x)**(i+1) for i,x in enumerate(str(n)))==n]
_____________________________________________
def sum_dig_pow(a, b):
    ans = []
    while a <= b:
        if sum(int(j) ** k for j,k in zip(str(a),range(1,len(str(a)) + 1))) == a:
            ans += [a]
        a += 1
    return ans
