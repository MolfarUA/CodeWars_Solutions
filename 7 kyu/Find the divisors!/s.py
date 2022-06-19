544aed4c4a30184e960010f4


def divisors(num):
    l = [a for a in range(2,num) if num%a == 0]
    if len(l) == 0:
        return str(num) + " is prime"
    return l
__________________________________
def divisors(n):
    return [i for i in xrange(2, n) if not n % i] or '%d is prime' % n
__________________________________
def divisors(integer):
  a = []
  for i in range(2, integer):
    if integer % i == 0:
      a.append(i)
  return a if a else str(integer) + " is prime"
__________________________________
def divisors(integer):
  return [n for n in range(2, integer) if integer % n == 0] or '{} is prime'.format(integer)
__________________________________
import math
def divisors(n):
  o = [i for i in range(2, int(math.ceil(n/2)+1)) if n%i==0]
  return o if len(o) > 0 else "%d is prime" % n
__________________________________
def divisors(n):
    res = [i for i in range(2, n) if n % i == 0]
    return f'{n} is prime' if not res else res
__________________________________
def divisors(integer):
    arr = []
    for x in range(2,integer - 1):
        if integer % x == 0:
            arr.append(x)

    if len(arr) == 0:
        return f'{integer} is prime'
    else:    
        return arr

for i in [1, 3, 9, 12, 64]:
    print (i, divisors(i))
__________________________________
def divisors(integer):
    res_list = [i for i in range(2,integer) if integer % i == 0]
    return res_list if res_list else f"{integer} is prime"
__________________________________
def divisors(integer):
    ret = []
    for n in range(2, integer):
        if not integer % n:
            ret.append(n)
    if not len(ret):
        return str(integer) + " is prime"
    return ret
__________________________________
def divisors(integer):
    
    list_div = []
    for i in range (2, integer - 1):
        if integer % i == 0:
            list_div.append(i)
    
    return list_div if list_div != [] else str(integer) + " is prime"
