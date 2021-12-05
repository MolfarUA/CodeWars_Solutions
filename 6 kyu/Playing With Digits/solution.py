def dig_pow(n, p):
    m = sum(int(a)**(i+p) for i, a in enumerate(str(n)))
    return -1 if m % n else m // n
############
def dig_pow(n, p):
  s = 0
  for i,c in enumerate(str(n)):
     s += pow(int(c),p+i)
  return s/n if s%n==0 else -1
############
def dig_pow(n, p):
    k, fail = divmod(sum(int(d)**(p + i) for i, d in enumerate(str(n))), n)
    return -1 if fail else k
###########
def dig_pow(n, p):
  t = sum( int(d) ** (p+i) for i, d in enumerate(str(n)) )
  return t//n if t%n==0 else -1
############
def dig_pow(n, p):
    digits = str(n)
    answer = 0
    for d in digits:
        answer += int(d)**p
        p+=1
    if 0 == answer % n:
        return answer/n
    else: return -1
###############
def dig_pow(n, p):
    string_number = str(n)
    counter = 0
    sum = 0
    for char in string_number:
        sum = sum + int(char) ** (p+counter)
        counter += 1
    if sum % n == 0: return sum / n
    else: return -1
################
def dig_pow(n, p):
    total = 0
    digits_list = [int(x) for x in str(n)]
    iteration = 0
    
    for i in range(p, len(digits_list)+p):
        current_power = digits_list[iteration] ** p
        total += current_power
        iteration += 1
        p+=1
    if total % n == 0:
        return total / n
    return -1
#################
def dig_pow(n, p):
    sum = 0
    for d in str(n):
        sum += int(d)**p
        p+=1
    return int(sum/n) if sum / n == int(sum/n) else -1
#################
def dig_pow(n, p):
    return res if (res := sum([int(j)**i for i, j in enumerate(str(n), p)])/n).is_integer() else -1
##############
def dig_pow(n, p):
    num_in_n = []
    sum = 0
    for x in str(n):
        num_in_n.append(int(x))
    for x in num_in_n:
        sum += x**p
        p+=1
    if sum%n == 0:
        return sum/n
    else:
        return -1
#############
def dig_pow(n, p):
    n = str(n)
    r = 0
    for i in n:
        i = int(i)
        r += i**p
        p += 1
    if r/int(n) % 1 != 0:
        return -1
    else:
        return r/int(n)
#############
def dig_pow(n, p):
    a = 0
    for i in str(n):
        a = a + pow(int(i), p)
        p += 1
        print(a)
    if a % n == 0:
        return a/n
    else:
        return -1
###############
def dig_pow(n,p):
  digits = str(n)
  output = 0
  k = 0
  for i, digit in enumerate(digits):
    output += int(digit)**(i+p)
  k = output/n
  return k if k==int(k) else -1
##############
def dig_pow(n, p):
    num_list = list(str(n))
    result = 0
    for i,j in enumerate(num_list):
        result = result + int(j)**(p+i)
    if result % n != 0:
        return -1
    return result//n
