def narcissistic(value):
    return value == sum(int(x) ** len(str(value)) for x in str(value))
________________________
def narcissistic( value ):
    value = str(value)
    size = len(value)
    sum = 0
    for i in value:
        sum += int(i) ** size
    return sum == int(value)
________________________
def narcissistic(value):
    return bool(value==sum([int(a) ** len(str(value)) for a in str(value)]))
________________________
def narcissistic( value ):
    vstr = str(value)
    nvalue = sum(int(i)**len(vstr) for i in vstr)
    return nvalue == value
________________________
def narcissistic(value):
    string = str(value)
    length = len(string)
    sum_of_i = 0
    for i in string:
        sum_of_i += int(i) ** length
    if sum_of_i == value:
        result = True
    else:
        result = False
    return result
________________________
number = 153

def narcissistic(number):
    lenght = len(str(number))
    your_sum = 0
    for digits in str(number):
        your_sum += (int(digits) ** lenght)
    if your_sum == number:
        return True
    return False

print(narcissistic(number))
________________________
def narcissistic( value ):
    qwe = list(str(value))
    zxc = []
    for x in range(len(qwe)):
        x = pow(int(qwe[x]), len(qwe))
        zxc.append(x)
    return True if sum(zxc) == value else False
________________________
def narcissistic( value ):
    value = str(value)
    l = len(value)
    sum = 0
    for i in value:
        sum += int(i)**l
    if sum == int(value):
        return True
    else:
        return False
________________________
def narcissistic(value):
    return sum(list(map(lambda d: int(d) ** len(str(value)), str(value)))) == value
