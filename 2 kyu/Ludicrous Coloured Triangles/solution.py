import itertools
import operator


def triangle(row):
    # Explanation of approach:
    # We associate each of the 3 colours/characters with a unique code: 0, 1, or 2.
    # With this encoding and the rules given, 
    # we see that a pair of neighbours in one row will give rise in the next row
    # to a colour whose code is the negated sum of the two neighbours' codes, reduced modulo 3.
    # Applying this repeatedly starting with a row of length m + 1,
    # we find that the code of the colour at the bottom tip of the triangle
    # is just the dot product of the mth row (zero-indexing, always) of Pascal's triangle
    # with the codes of the initial row of colours, 
    # the result negated if m is odd, and reduced modulo 3.
    # Working modulo 3, Lucas's Theorem says that (m choose n), 
    # the nth value/coefficient in the mth row of Pascal's triangle,
    # is congruent to the product of all (m_i choose n_i),
    # where m_i and n_i are the ith base-3 digits of m and n, respectively,
    # and (m_i choose n_i) is taken to be zero if m_i < n_i.
    # Therefore nonzero coefficients appear precisely 
    # when each base-3 digit of n is no greater than the corresponding base-3 digit of m.
    # Now, for such a coefficient, the factor (m_i choose n_i) is 2 if m_i == 2 and n_i == 1.  
    # Otherwise, the factor is 1.
    # Therefore, for such a coefficient, if k denotes the number of pairs of corresponding base-3 digits of m and n
    # that are equal to 2 and 1, respectively,
    # then the coefficient is congruent to 2**k, which reduces to 1 if k is even or 2 if k is odd.

    # We map our three colours/characters to our three codes.
    colours = 'RGB'
    code_for_colour = {colour: code for code, colour in enumerate(colours)}

    # We determine m and its base-3 digit sequence (starting with the least significant digit).
    m = len(row) - 1
    m_base_3_digits = []
    q = m
    while q:
        q, r = divmod(q, 3)
        m_base_3_digits.append(r)

    # For later use, we locate all 2s in the base-3 digit sequence of m.
    positions_of_2s_in_m_base_3_digits = tuple(position for position, digit in enumerate(m_base_3_digits) if digit == 2)

    # We collect the first powers of 3, so that we can later quickly compute a number from its base-3 digit sequence.
    # (Note: The only difference between my solution for the "Insane Coloured Triangles" kata and this one occurs here.
    # Unlike the current kata, that one allowed use of Python 3.8, where itertools.accumulate's initial parameter first appeared.)
    powers_of_3 = (1, *itertools.accumulate(itertools.repeat(3, len(m_base_3_digits) - 1), operator.mul))

    # We will progressively compute the dot product of the vector of coefficients of the mth row of Pascal's triangle
    # with the vector of codes of colours in the given initial row, reducing modulo 3.
    reduced_dot_product = 0
    # We need only consider the nonzero coefficients in the mth row of Pascal's triangle,
    # so we visit all sequences of base-3 digits whose elements are no greater than the corresponding base-3 digits of m.
    for n_base_3_digits in itertools.product(*(range(m_base_3_digit + 1) for m_base_3_digit in m_base_3_digits)):
        # From the base-3 digit sequence we are now visiting, we compute the associated value of n.
        # (m choose n) is nonzero.
        n = sum(map(operator.mul, n_base_3_digits, powers_of_3))
        # We look up the code of the colour at the nth position in the given initial row.
        nth_code_in_row = code_for_colour[row[n]]
        # Only nonzero codes will result in nonzero contributions to our dot product.
        if nth_code_in_row:
            # We determine the value of (m choose n) reduced modulo 3,
            # multiply by the corresponding colour code in the given initial row,
            # and update our partial reduced dot product.
            nth_coefficient = sum(n_base_3_digits[position] == 1 for position in positions_of_2s_in_m_base_3_digits) % 2 + 1
            reduced_dot_product = (reduced_dot_product + nth_coefficient * nth_code_in_row) % 3

    # If m is even, the dot product is congruent to the code of the colour at the bottom tip of the triangle,
    # while for odd m, the negated dot product is congruent to the desired code.
    # We thus determine the final code and return the associated colour character.
    return colours[(-reduced_dot_product) % 3 if m % 2 else reduced_dot_product]
  
##################################
def triangle(x):
    G = ord('G')
    n1 = len(x)-1
    if n1<1:
        return x
    digs = []; pows = []
    pow3 = 1
    while n1:
        dig3 = n1%3
        if dig3:
            digs.append(dig3); pows.append(pow3)
        pow3 *= 3
        n1 //= 3
    n1 = len(digs)-1
    def Tri (ix, idig):
        dig3 = digs[idig]; pow3 = pows[idig]
        if idig:
            idig -= 1
            return Tri(ix,idig)+Tri(ix+pow3,idig) if dig3==1 else Tri(ix,idig)-Tri(ix+pow3,idig)+Tri(ix+2*pow3,idig)
        else:
            sum = 0
            c = ord(x[ix]) - G
            if c:
                sum += 1 if c>0 else -1
            if dig3==1:
                c = ord(x[ix+pow3]) - G
                if c:
                    sum += 1 if c > 0 else -1
            else:
                c = ord(x[ix+pow3]) - G
                if c:
                    sum += -1 if c > 0 else 1
                c = ord(x[ix+pow3+pow3]) - G
                if c:
                    sum += 1 if c > 0 else -1
            return sum
    Sum = Tri(0, n1)
    return 'GRB'[Sum%3 if len(x)%2 else -Sum%3]
  
####################################
from math import floor, log

RULE = {
    'RB': 'G',    'BR': 'G',    'GG': 'G',
    'RG': 'B',    'GR': 'B',    'BB': 'B',
    'GB': 'R',    'BG': 'R',    'RR': 'R'
}

small_cache = {}

def small_triangle(row):
    _key = row
    while len(row)>1:
        row = ''.join( a if a==b else (RULE[a+b]) for a,b in zip(row, row[1:]))
    small_cache[_key] = row
    return row

def triangle(row):
    cache = {}
    
    def _subtriangle(a, b, olength, x, y):
        t = cache.get((x,y), False) 
        if t:
            return t      
        elif olength <= 8:
            return small_cache.get(row[a:b], False) or small_triangle(row[a:b])    
        length = int(3**floor(log(b-a-1,3)))
        cache[(x,y)] = RULE[   _subtriangle(a        , b-length, olength-length, x+length, y       )
                             + _subtriangle(a+length , b       , olength-length, x+length, y+length)]
        return cache[(x,y)]
        
    return _subtriangle(0, len(row), len(row), 1,1)

#################################
index = {
    'R': 1,
    'G': -1,
    'B': 0
}
ref_index = ['B', 'R', 'G']

cx_index = [[1,0,0], [1,1,0], [1,-1,1]]
def triangle(row):
    n1 = len(row) - 1
    cx_result = []
    while n1 > 0:
        p_index = n1 % 3
        cx_result.append(p_index)
        n1 = n1 // 3
    cx_result.append(0)

    c_index = len(cx_result)-1
    result = exec_a(cx_result, row, c_index, 0)

    return ref_index[result % 3]


def exec_a(cx_result, row, c_index, start):
    if c_index == 0:
        return exec_0(cx_result, row, c_index, start)

    if cx_result[c_index] == 0:
        return exec_a(cx_result, row, c_index-1, start)

    if cx_result[c_index] == 1:
        left = exec_a(cx_result, row, c_index-1, start)
        right = exec_a(cx_result, row, c_index-1, start+3**(c_index))
        return -left-right

    if cx_result[c_index] == 2:
        left = exec_a(cx_result, row, c_index-1, start)
        mid = exec_a(cx_result, row, c_index-1, start+3**(c_index))
        right = exec_a(cx_result, row, c_index-1, start+2*3**(c_index))
        return left+right-mid
    
def exec_0(cx_result, row, c_index, start):
    if cx_result[c_index] == 0:
        return index[row[start]]

    if cx_result[c_index] == 1:
        left = index[row[start]]
        right = index[row[start+1]]
        return -left-right

    if cx_result[c_index] == 2:
        left = index[row[start]]
        mid = index[row[start+1]]
        right = index[row[start+2]]
        return left+right-mid
##################################
import math


three_pows = [1, 3, 9, 27, 81, 243, 729, 2187, 6561, 19683, 59049, 177147, 531441, 1594323, 4782969, 14348907, 43046721, 129140163, 387420489]
RGB = {'R': 0, 'G': 1, 'B': 2}


def triangle(row):
    result_code_str = 'RGB' if len(row) % 2 == 1 else 'RBG'
    return result_code_str[triangle_value(row, 0, len(row) - 1) % 3]


def triangle_value(row, start, n):
    if n == 0:
        return RGB[row[start]]
    if n == 1:
        return RGB[row[start]] + RGB[row[start + 1]]
    if n == 2:
        return RGB[row[start]] + RGB[row[start + 1]] * 2 + RGB[row[start + 2]]
    last_three_pow = three_pows[math.floor(math.log(n, 3))]
    mod_last_three_pow = n - last_three_pow
    if mod_last_three_pow < last_three_pow:
        return triangle_value(row, start, mod_last_three_pow) + \
               triangle_value(row, start + last_three_pow, mod_last_three_pow)
    else:
        return triangle_value(row, start, mod_last_three_pow - last_three_pow) + \
               triangle_value(row, start + last_three_pow, mod_last_three_pow - last_three_pow) * 2 + \
               triangle_value(row, start + last_three_pow * 2, mod_last_three_pow - last_three_pow)
#####################
import math

def choose2(a, b):
    return 'RGB'[-('RGB'.index(a) + 'RGB'.index(b)) % 3]

def choose3(a, b, c):
    return 'RGB'[('RGB'.index(a) + 2 * 'RGB'.index(b) + 'RGB'.index(c)) % 3]

def threePowerX_Xdot5(len_row):
    return math.ceil(math.log(len_row, 3))

def triangle_rec(row, len_row):
    if len_row == 1:
        return row[0]
    
    power_3 = threePowerX_Xdot5(len_row)
    
    upper = int(3 ** (power_3))
    split_3 = upper // 3
    
    if len_row > 2 * split_3:
        size = split_3 - (upper - len_row)
        half = ( len_row - size ) // 2
        return choose3(
            triangle_rec(row[:size], size),
            triangle_rec(row[half:half+size], size),
            triangle_rec(row[-size:], size)
        )
    
    size = split_3 - (2 * split_3 - len_row)
    return choose2(
        triangle_rec(row[:size], size),
        triangle_rec(row[-size:], size)
    )

def triangle(row):
    return triangle_rec(row, len(row))
#############################
import numpy as np
from operator import itemgetter

bcolormap = {b'B':0, b'R':1, b'G':2}
colormap = {'B':0, 'R':1, 'G':2}
numlist = 'BRG'
def triangle(row):
    max_row = len(row)
    if max_row == 1:
        return row
    total = 0
    steps = get_steps(max_row)
    q = np.zeros(2**len(steps), dtype=int)
    offset = 1
    odds = max_row%2==1
    for step in steps:
        q.ravel()[offset:offset<<1] = q[:offset]+step
        offset <<=1
    
    chars = np.take(np.fromstring(row, dtype="S1"), q)
    chars.dtype='int8'
    if not odds:
        chars = 3-chars
    total = np.sum(chars)
    return numlist[total%3]

def get_steps(number):
    steplist = []
    step = 1
    while step*3 < number:
          step*=3
    number-=1
    while number>0:
        while step > number:
            step //= 3   
        number -= step
        steplist.append(step)
    return steplist
