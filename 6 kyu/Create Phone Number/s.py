def create_phone_number(n):
    return "({}{}{}) {}{}{}-{}{}{}{}".format(*n)
_______________________________
def create_phone_number(n):
    n = ''.join(map(str,n))
    return '(%s) %s-%s'%(n[:3], n[3:6], n[6:])
_______________________________
def create_phone_number(n):
  str1 =  ''.join(str(x) for x in n[0:3])
  str2 =  ''.join(str(x) for x in n[3:6])
  str3 =  ''.join(str(x) for x in n[6:10])


  return '({}) {}-{}'.format(str1, str2, str3)
_______________________________
def create_phone_number(n):
    m = ''.join(map(str, n))
    return f"({m[:3]}) {m[3:6]}-{m[6:]}"
_______________________________
def create_phone_number(n):
    n = "".join([str(x) for x in n] )
    return("(" + str(n[0:3]) + ")" + " " + str(n[3:6]) + "-" + str(n[6:]))
_______________________________
def create_phone_number(n):
    c = str(f"({n[0]}{n[1]}{n[2]}) {n[3]}{n[4]}{n[5]}-{n[6]}{n[7]}{n[8]}{n[9]}")
    return c
_______________________________
def create_phone_number(n):
    code, region, number = '', '', ''
    for i in range(10):
        if i <= 2:
            code += '' + str(n[i])
        elif i >= 3 and i <= 5:
            region += '' + str(n[i])
        else:
            number += '' + str(n[i])
    phone = ''.join('(%s) %s-%s' % (code, region, number))
    return phone
_______________________________
def create_phone_number(n):
    if len(n) != 10 :
        print('It is not possible to create a phone number')
    else : 
        for digit in n:
            if digit >= 0 and digit <= 9:
                str_digits=(''.join(str(x) for x in n))
                return '('+ str_digits[:3] + ')'+ " " + str_digits[3:6] +'-'+ str_digits[6:10]
            else : 
                print("You need to change the digit composing your number")
_______________________________
def create_phone_number(n):
    number = "".join(list(map(str, n)))
    return f"({number[0:3]}) {number[3:6]}-{number[6:]}"
