5842df8ccbd22792a4000245



def expanded_form(num):
    num = list(str(num))
    return ' + '.join(x + '0' * (len(num) - y - 1) for y,x in enumerate(num) if x != '0')
_________________________
def expanded_form(n):
    result = []
    for a in range(len(str(n)) - 1, -1, -1):
        current = 10 ** a
        quo, n = divmod(n, current)
        if quo:
            result.append(str(quo * current))
    return ' + '.join(result)
_________________________
def expanded_form(num):
    num = str(num)
    st = ''
    for j, i in enumerate(num):
        if i != '0':
            st += ' + {}{}'.format(i, (len(num[j+1:])*'0'))
    return st.strip(' +')
_________________________
def expanded_form(num):
    return " + ".join([str(int(d) * 10**p) for p, d in enumerate(str(num)[::-1]) if d != "0"][::-1])
_________________________
def expanded_form(num):
    exp = []
    zeri = len(str(num))
    for cifra in str(num):
        zeri -= 1
        if cifra != '0':
            exp.append(cifra + '0'*zeri)
    return ' + '.join(exp)
_________________________
def expanded_form(num):
    s = str(num)
    n = len(s)
    return ' + '.join( [s[-i]+"0"*(i-1) for i in range(n,0,-1) if s[-i] != "0"])
_________________________
def expanded_form(num):
    k = 10
    x = num
    l = []
    while x>0:
        r = x % k
        k = k * 10
        x = x - r
        if r > 0:
            r = str(r)
            l.append(r)
    l = list(reversed(l))
    return " + ".join(l)
_________________________
def expanded_form(num):
    new_str = ''
    i = len(str(num))
    count = 0
    while i != 0:
        digit = num % 10
        if digit == 0:
            i -= 1
            count += 1
            num = num // 10
            new_str += '0'
        else:
            i -= 1
            new_str += str(digit)
            num = num // 10
            count += 1
            new_str += ' + '
            new_str += '0' * count

    new_str = new_str[::-1]
    new_str = new_str[count+3::]

    return new_str
_________________________
def expanded_form(num):
    digits = []
    power = 1
    while num > 0:
        if (factor := power * (num % 10)) != 0:
            digits.append(factor)
        num //= 10
        power *= 10
    return ' + '.join(str(digit) for digit in reversed(digits))
_________________________
def expanded_form(num):
    s = list(str(num))
    zeros = lambda i: '0' * (len(s) - i - 1)
    return " + ".join([s + zeros(i) for i, s in enumerate(s) if s != '0'])
