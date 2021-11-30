def series_sum (n):
    y = 1
    sum_numbers = 0
    for x in range (1, n+1):
        sum_numbers += 1/y
        y += 3
    return (format(sum_numbers, '.2f'))
##################
def series_sum(n):
    return '{:.2f}'.format(sum(1.0/(3 * i + 1) for i in range(n)))
##################
def series_sum(n):
    return '%.2f' % sum(1.0 / i for i in xrange(1, 3 * n, 3))
###############
def series_sum(n):
    sum = 0.0
    for i in range(0,n):
        sum += 1 / (1 + 3 * float(i))
    return '%.2f' % sum
#################
series_sum = lambda n: '{:.2f}'.format(sum(1.0/(3*i-2) for i in xrange(1, n+1)))
##############
def series_sum(n):
  return "%.2f" % sum([1.0 / (3 * i + 1) for i in range(n)])
###############
series_sum = lambda n: '{:.2f}'.format(round(sum( 1/(1+(e)*3) for e in range(n) ) ,2))
#################
def series_sum(n):
    return "{:.2f}".format(sum(1.0/(3*i+1) for i in xrange(0, n)))
##############
def series_sum(n):
    return "{0:.2f}".format(sum([1. / (1 + 3*x)for x in range(n)]))
#############
def series_sum(n):
    result = 0
    for i in range(0,n):
        result += 1.00/(1 + (3 * i))
    stringresult = str(round(result, 2))
    if stringresult == '0':
        stringresult = '0.00'
    while len(stringresult) < 4:
        stringresult += '0'
    return stringresult
#############
def series_sum(n):
    sum = 0
    for i in range(0, n):
        sum += 1.0 / (i * 3 + 1)
    return "%.2f" % sum
###############
def series_sum(n):
    x = 0
    y = 1
    for n in range(1, n+1):
        x = x + y
        y = 1/((1/y)+3)
        n = n - 1
    return format(x, '.2f')
##############
from decimal import Decimal

def series_sum(n):
    if n == 0:
        sum_ = 0
    else:
        sum_ = 1
        for i in range(n-1):
            nth_value = 1 / (4+3*i)
            sum_ += nth_value

    sum_str = str(round(Decimal(sum_), 2))
    return sum_str
##############
def series_sum(n):
    seriesSum = 0.0
    for x in range(n):
        seriesSum += 1 / (1 + x * 3)
    return '%.2f' % seriesSum
##############
from fractions import Fraction
def series_sum(n):
    total = sum(Fraction(1, 1 + i * 3) for i in range(n))
    return '{:.2f}'.format(total.numerator / total.denominator)
############
def series_sum(n):
    return '%.2f' % sum(1.0 / (3 * i + 1) for i in xrange(n))
#############
def series_sum(n):
    return "{0:.2f}".format( sum(1.0/(1+(i-1)*3) for i in range(1,n+1)) )
##########
from scipy.special import digamma

def series_sum(n):
    return f"{(digamma(1/3+n) - digamma(1/3))/3:.2f}"
############
def series_sum(n):
    if n == 0:
        return '0.00'
    return '%0.2f' % float(str(1 + sum(1/(1+i*3) for i in range(1,n))))
#############
def series_sum(n):
    return format(sum(1/(1+3*k) for k in range(n)),'.2f')
#############
def series_sum(n):
    ls = []
    if(n == 0): return str("%5.2f" % 0.00)[1:]
    for n in range(1,n):
        ls.append(1/(1+(n*3)))
    return str("%5.2f" % (float(sum(ls)+1)))[1:]
###############
def series_sum(n):
    sum = 0
    for x in range(n):
        sum = sum + 1/(3 * x + 1)
    return "%.2f" % sum
###########
def series_sum(n):
    return "%.2f" % sum([1/(1+(3*t)) for t in range(n)])
