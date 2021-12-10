def elder_age(m, n, l, t):
    S = lambda x: x * (x-1) // 2 if x > 1 else 0
    D = lambda x,y: (S(y-l) - S(x-l)) % t

    if m < n: m, n = n, m
    if n == 1: return D(0, m)
    x = 1 << (m.bit_length()-1)
    res = D(0, x) * min(x, n)
    if m > x:
        if n > x:
            res += D(x, 2*x) * (m+n-2*x)
            res += elder_age(m-x, n-x, l, t)
        else:
            res += elder_age(m-x, n, l-x, t)
    return res % t
  
###############
def elder_age(m,n,l,t,s=0):
    if m > n: m, n = n, m
    if m < 2 or not n & (n - 1): # n is a power of 2
        s, p = max(s-l, 0), max(n+s-l-1, 0)
        return (p - s + 1) * (s + p) // 2 * m % t
    p = 1 << n.bit_length() - 1 # Biggest power of 2 lesser than n
    if m < p: return (elder_age(m, p, l, t, s) + elder_age(m, n-p, l, t, s+p)) % t
    return (elder_age(p, p, l, t, s) + elder_age(m-p, n-p, l, t, s) +
            elder_age(p, n-p, l, t, s+p) + elder_age(m-p, p, l, t, s+p)) % t
  
###################
def larger_pow(x):
    t = 1
    while t < x:
        t <<= 1
    return t

def range_sum(l, r):
    return (l + r) * (r - l + 1) // 2

def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0
    if m > n:
        m, n = n, m
    lm, ln = larger_pow(m), larger_pow(n)
    if l > ln:
        return 0

    if lm == ln:
        return (range_sum(1, ln - l - 1) * (m + n - ln) + elder_age(ln - n, lm - m, l, t)) % t
    
    if lm < ln:
        lm = ln // 2
        tmp = range_sum(1, ln - l - 1) * m - (ln - n) * range_sum(max(0, lm - l), ln - l - 1)
        if l <= lm:
            tmp += (lm - l) * (lm - m) * (ln - n) + elder_age(lm - m, ln - n, 0, t)
        else:
            tmp += elder_age(lm - m, ln - n, l - lm, t)
        return tmp % t
      
######################
def elder_age(m,y,l,t):
    T = 0
    while y:
        y, Y, x = y & y-1, y, m
        while x:
            x, X = x & x-1, x
            s, S = sorted((X - x, Y - y))
            h = max((x^y | S-1) + 1 - l, 0)
            w = min(h, S)
            T += s * w * (h + h - w - 1) // 2
    return T % t
  
#################
import math

def elder_age(m,n,l,t):
    
    if ( m <= 0 or n <= 0 ):
        return 0
    
    major=max(m,n)
    minor=min(m,n)
    
    # Build the biggest square with side length (2 ** square_binary_index) inside the rectangle (m x n) 
    square_binary_index = int(math.log(minor,2))
    length_square = 2 ** square_binary_index
    long_side_rect = major >> square_binary_index << square_binary_index
    
    # TOP-LEFT Area (the time from all the whole squares of side (length 2 ** square_binary_index))
    top_left = time_area(long_side_rect, length_square, l)%t
    
    # BOTTOM-LEFT Area (the square that is cut in the bottom, still one side length is (2 ** square_binary_index))
    bottom_left = time_area(length_square, major-long_side_rect, l-long_side_rect)%t
    
    # TOP-RIGHT Area (the squares that are cut in the right, still one side length is (2 ** square_binary_index))
    long_side_rect_r = major >> (square_binary_index+1) << (square_binary_index+1)
    top_right = time_area(long_side_rect_r, minor-(length_square), l)%t
    # Last square of the TOP-RIGHT area, values are not sequential compared to previous squares of the top-right area, so extra time needs to be added
    if(((major >> square_binary_index)%2)>0):
        top_right += time_area(length_square, minor-(length_square), l -(long_side_rect_r+(length_square)))%t
    
    # BOTTOM-RIGHT Area (last square, does not contain a side with length (2 ** square_binary_index))
    bottom_right = elder_age(major-long_side_rect, minor-(length_square), l-(long_side_rect^length_square), t)
        
    return (top_left + bottom_left + top_right + bottom_right)%t

#
#   Returns the time in a certain area where a > b and b=2^x
#   -l is the value of the first coordinate
#
#   This method just calculates the sum of the range (0,a-l)
#   Or (-l,a-l) when l is negative. That is, the score per column.
#   Then multiplies it by number of columns, that is the time of the whole area
#
#
#   b=2^x
#   
#   +--+
#   |  |
#   |  |
#   |  |  a
#   |  |
#   |  |
#   +--+
#
#

def time_area(a,b,l):
    
    if(l > a):
        return 0
    
    max_value=a-l
    # Time per column multiplied by number of columns
    result=(max_value*(max_value-1)/2) * b
    
    min_value=-l
    if(min_value>0):
        result-=(min_value*(min_value-1)/2) * b
    
    return result
  
###########################
# I feel like refactoring this would not express the pain this kata has caused me.
# Enjoy this solution in all its ugly glory.

def new_not_loss(x, y, loss):
    if x*y == 0:
        return 0
    if x+y == 3:
        return 2*(loss-1) + 1 if loss else 0
    if len(bin(loss-1)) > len(bin(x-1)) and len(bin(loss-1)) > len(bin(y-1)):
        return x*y*loss - new_gain(x, y)
    loss_barrier = 2**(len(bin(loss-1))-2)
    if x >= loss_barrier and y >= loss_barrier:
        under_barrier = loss_barrier*(loss+1)*loss//2 # Amount in square
        max_rep = min(x, y)//loss_barrier # Times square repeats
        # Figure out what slice for outer barrier
        if (max_rep+1)*loss_barrier <= x:
            edge_x = loss_barrier
        else:
            edge_x = x%loss_barrier
        if (max_rep+1)*loss_barrier <= y:
            edge_y = loss_barrier
        else:
            edge_y = y%loss_barrier
        outer_barrier = new_not_loss(edge_x, edge_y, loss)
        if outer_barrier is None:
            return
        return under_barrier*max_rep + outer_barrier
    if x >= loss_barrier or y >= loss_barrier:
        under_barrier = min(loss_barrier, x, y)*(loss+1)*loss//2
        max_rep = min(x, y)//loss_barrier
        # Figure out what slice for outer barrier
        if max(x, y) == loss_barrier:
            return under_barrier
        if (max_rep+1)*loss_barrier <= x:
            edge_x = loss_barrier
        else:
            edge_x = x%loss_barrier
        if (max_rep+1)*loss_barrier <= y:
            edge_y = loss_barrier
        else:
            edge_y = y%loss_barrier
        outer_barrier = new_not_loss(edge_x, edge_y, loss)
        if outer_barrier is None:
            return
        return under_barrier*max_rep + outer_barrier
    if x > loss_barrier//2 and y > loss_barrier//2:
        lb = loss_barrier//2
        core = new_not_loss(lb, lb, loss)
        bottom = new_not_loss(x-lb, y, loss-lb)
        right = new_not_loss(x, y-lb, loss-lb)
        corner = new_not_loss(x-lb, y-lb, loss)
        return core + bottom + right + corner
    lb = loss_barrier//2
    direct_loss = min(x, y)*loss*lb
    un_loss = min(x, y)*lb*(lb-1)//2
    side = new_not_loss(min(x, y), max(x, y)-lb, loss-lb)
    return direct_loss - un_loss + side

def squares(x, y, n):
    dx, dy = x%(2*n), y%(2*n)
    return (x*y - dx*dy)//2 + edge(dx, dy, n)

def edge(x, y, n):
    side = lambda a, b: max(0, (a%(2*n)-n)*min(n, b%(2*n)))
    return side(x, y) + side(y, x)

def new_gain(x, y):
    n = 1
    s = 0
    while n < x or n < y:
        s += squares(x, y, n)*n
        n *= 2
    return s

def elder_age(x, y, l, t):
    if len(bin(l)) > len(bin(x)) and len(bin(l)) > len(bin(y)):
        return 0
    g = new_gain(x, y)
    t_l = x*y*l
    n_l = new_not_loss(x, y, l)
    if n_l is None:
        return
    return (g + n_l - t_l)%t
  
############################
def elder_age(m, n, l, t):
    if not n | m:
        return 0
    
    if n < m:
        m, n = n, m
    
    k = 1 << (n.bit_length() - 1)
    
    r = min(m, k)
    s = sum_range(-l, k - l - 1) * r % t
    s = (s + elder_age(r, n - k, l - k, t)) % t
    
    if m <= k:
        return s
    
    r = m - r
    s = (s + sum_range(k - l, 2 * k - l - 1) * r) % t
    s = (s + elder_age(r, n - k, l, t)) % t
    return s

def sum_range(lo, hi):
    lo = max(lo, 0)
    hi = max(hi, 0)
    return (hi + lo) * (hi - lo + 1) // 2
  
##########################
def bigPow(x):
    t = 1
    while t < x:
        t <<= 1
    return t

def total(l, r):
    return (l + r) * (r - l + 1) // 2

def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0
    if m > n:
        m, n = n, m
    bigM, bigN = bigPow(m), bigPow(n)
    if l > bigN:
        return 0

    if bigM == bigN:
        return (total(1, bigN - l - 1) * (m + n - bigN) + elder_age(bigN - n, bigM - m, l, t)) % t
    
    if bigM < bigN:
        bigM = bigN // 2
        time = total(1, bigN - l - 1) * m - (bigN - n) * total(max(0, bigM - l), bigN - l - 1)
        if l <= bigM:
            time += (bigM - l) * (bigM - m) * (bigN - n) + elder_age(bigM - m, bigN - n, 0, t)
        else:
            time += elder_age(bigM - m, bigN - n, l - bigM, t)
        return time % t
      
######################
def highest_bit(m):
    if m > 0:
        return 1 + highest_bit(m//2)
    return 0

def triangle(n, t):
    if(n < 0):
        return 0
    if n % 2 == 0:
        r1 =( n//2) % t
        r2 = (n+1) % t
    else:
        r1 = n % t
        r2 = ((n+1)//2) % t
    return r1 * r2 % t

def elder_age(m,n,l,t):
    a = highest_bit(m)
    b = highest_bit(n)
    total = 0
    for i in range(a):
        for j in range(b):
            ibit = 1 << i
            jbit = 1 << j
            if m & ibit == 0 or n & jbit == 0:
                continue
            size = max(ibit, jbit)
            rows = min(ibit, jbit) % t
            mstart = m & ~(size - 1) & ~(2*ibit-1)
            nstart = n & ~(size - 1) & ~(2*jbit-1)
            start = mstart ^ nstart
            end = start + max(ibit,jbit) - 1
            row = triangle(end-l, t) - triangle(start - l - 1, t)
            total = (total + row * rows) % t
    return total
  
######################
# {8,9,10,11} xor x = {8,9,10,11} for 0 <= x < 4
# {8,9,10,11} xor x = {12,13,14,15} for 5 <= x < 8
# {8,9,10,11} xor x = {0,1,2,3} for 8 <= x < 12
# {8,9,10,11} xor x = {4,5,6,7} for 12 <= x < 16
def decomp(n):
    res = []
    p = 1
    while n:
        if n%2 == 1:
            res.append(p)
        n //= 2
        p *= 2
    res.reverse()
    return res

def elder_age_segment(psm,pm,psn,pn,l,t):
    if pm < pn:
        psm,pm,psn,pn = psn,pn,psm,pm
    assert pm >= pn
    psn &= ~(pm-1)
    # the xor rectangle contains pn copies of psm^psn ... psm^psn+pm-1
    psm ^= psn
    lo, hi = max(0,psm-l), max(0,psm+pm-1-l)
    res = (hi*(hi+1)//2%t - lo*(lo-1)//2%t)%t*pn%t
    return res

def elder_age(m,n,l,t):
    dm = decomp(m)
    dn = decomp(n)
    
    psm = 0
    s = 0
    for pm in dm:
        psn = 0
        for pn in dn:
            s = (s + elder_age_segment(psm,pm,psn,pn,l,t))%t
            psn += pn
        psm += pm
    return s
  
######################
def my_pow(x):
    t = 1
    while t < x:
        t <<= 1
    return t

def my_sum(l, r):
    return (l + r) * (r - l + 1) // 2

def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0
    if m > n:
        m, n = n, m
    lm, ln = my_pow(m), my_pow(n)
    if l > ln:
        return 0
    if lm == ln:
        return (my_sum(1, ln - l - 1) * (m + n - ln) + elder_age(ln - n, lm - m, l, t)) % t
    if lm < ln:
        lm = ln // 2
        tmp = my_sum(1, ln - l - 1) * m - (ln - n) * my_sum(max(0, lm - l), ln - l - 1)
        if l <= lm:
            tmp += (lm - l) * (lm - m) * (ln - n) + elder_age(lm - m, ln - n, 0, t)
        else:
            tmp += elder_age(lm - m, ln - n, l - lm, t)
        return tmp % t
      
########################
def larger_pow(hoho):
    t = 1
    while t < hoho:
        t <<= 1
    return t

def range_sum(l, r):
    return (l + r) * (r - l + 1) // 2

def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0
    if m > n:
        m, n = n, m
    lm, ln = larger_pow(m), larger_pow(n)
    if l > ln:
        return 0

    if lm == ln:
        return (range_sum(1, ln - l - 1) * (m + n - ln) + elder_age(ln - n, lm - m, l, t)) % t
    
    if lm < ln:
        lm = ln // 2
        tmp = range_sum(1, ln - l - 1) * m - (ln - n) * range_sum(max(0, lm - l), ln - l - 1)
        if l <= lm:
            tmp += (lm - l) * (lm - m) * (ln - n) + elder_age(lm - m, ln - n, 0, t)
        else:
            tmp += elder_age(lm - m, ln - n, l - lm, t)
        return tmp % t
      
#######################
def sum_(l, r):
    return (l + r) * (r - l + 1) // 2

def larger_pow(x):
    t = 1
    while t < x:
        t <<= 1
    return t


def elder_age(m,n,l,t):
    if m == 0 or n == 0:
        return 0
    if m > n:
        m, n = n, m
    lm, ln = larger_pow(m), larger_pow(n)
    if l > ln:
        return 0

    if lm == ln:
        return (sum_(1, ln - l - 1) * (m + n - ln) + elder_age(ln - n, lm - m, l, t)) % t
    
    if lm < ln:
        lm = ln // 2
        tmp = sum_(1, ln - l - 1) * m - (ln - n) * sum_(max(0, lm - l), ln - l - 1)
        if l <= lm:
            tmp += (lm - l) * (lm - m) * (ln - n) + elder_age(lm - m, ln - n, 0, t)
        else:
            tmp += elder_age(lm - m, ln - n, l - lm, t)
        return tmp % t
