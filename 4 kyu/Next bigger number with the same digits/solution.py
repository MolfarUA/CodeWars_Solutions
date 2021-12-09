def next_bigger(n):
    max_n = int(''.join(reversed(sorted(str(n)))))
    if n == max_n:
        return -1
    while True:
        n += 1
        if max_n == int(''.join(reversed(sorted(str(n))))):
            return n
###################
import itertools
def next_bigger(n):
    s = list(str(n))
    for i in range(len(s)-2,-1,-1):
        if s[i] < s[i+1]:
            t = s[i:]
            m = min(filter(lambda x: x>t[0], t))
            t.remove(m)
            t.sort()
            s[i:] = [m] + t
            return int("".join(s))
    return -1
###################
def next_bigger(n):
    # algorithm: go backwards through the digits
    # when we find one that's lower than any of those behind it,
    # replace it with the lowest digit behind that's still higher than it
    # sort the remaining ones ascending and add them to the end
    digits = list(str(n))
    for pos, d in reversed(tuple(enumerate(digits))):
        right_side = digits[pos:]
        if d < max(right_side):
            # find lowest digit to the right that's still higher than d
            first_d, first_pos = min((v, p) for p, v in enumerate(right_side) if v > d)

            del right_side[first_pos]
            digits[pos:] = [first_d] + sorted(right_side)

            return int(''.join(digits))

    return -1
###############
def next_bigger(n):
    n = str(n)[::-1]
    try:
        i = min(i+1 for i in range(len(n[:-1])) if n[i] > n[i+1])
        j = n[:i].index(min([a for a in n[:i] if a > n[i]]))
        return int(n[i+1::][::-1]+n[j]+''.join(sorted(n[j+1:i+1]+n[:j]))) 
    except:
        return -1
###################
def next_bigger(n):
    nums = list(str(n))
    for i in reversed(range(len(nums[:-1]))):
        for j in reversed(range(i, len(nums))):
            if nums[i] < nums[j]:
                nums[i], nums[j] = nums[j], nums[i]
                nums[i + 1:] = sorted(nums[i + 1:])
                return int(''.join(nums))
    return -1
###############
def next_bigger(n):
    i, ss = n, sorted(str(n))

    if str(n) == ''.join(sorted(str(n))[::-1]):
        return -1;

    while True:
        i += 1;
        if sorted(str(i)) == ss and i != n:
            return i;
###########
def next_bigger(n):
    if str(n) == ''.join(sorted(str(n))[::-1]):
        return -1
    a = n
    while True:
        a += 1
        if sorted(str(a)) == sorted(str(n)):
            return a
##############
from math import log
from itertools import permutations

def number_of_digits(n):
    if n == 0: return 1
    return int(log(n, 10)) + 1

def is_descending(n):
    if (n <= 10): return True
    n_digits = number_of_digits(n)
    prev = n % 10
    n /= 10
    for _ in xrange(n_digits - 1):
        curr = n % 10
        if curr < prev:
            return False
        prev = curr
        n /= 10
    return True

def next_bigger(n):
    if (n <= 11):
        return -1
    if (is_descending(n)):
        return -1
    m = str(n)
    for i in xrange(2, len(m) + 1):
        head = m[:len(m) - i]
        tail = map(lambda x: "".join(x), permutations(m[len(m) - i:]))
        nums = sorted(set(map(lambda x: int(head + x), tail)))
        n_index = nums.index(n)
        if (n_index >= len(nums) - 1):
            continue
        return nums[n_index + 1]
#########################################
def next_bigger(n):
    beg = ''
    lst = list(str(n))
    lst = sorted(list(str(n)), reverse=True)
    for i in lst:
        beg += i
    beg = int(beg)
    for i in range(n,beg+1):
        if sorted(list(str(n)), reverse=True) == sorted(list(str(i)), reverse=True) and n != i:
            return i
    return -1
#################
def next_bigger(n):
    if len(str(n))<2 or len(set(str(n)[i] for i in range(len(str(n)))))<2: return -1
    for i in range(n+1, 1+int(''.join(sorted(list(str(n)[i] for i in range(len(str(n)))),reverse=True)))):
        if sorted(list(str(i)[k] for k in range(len(str(i))))) == sorted(list(str(n)[k] for k in range(len(str(n))))) \
        and i>n:
            return i
    return -1
###############
def next_bigger(n):
    digits = list(str(n))
    for i in range(len(digits)-1, 0, -1):
        if digits[i] > digits[i-1]:
            break
    else:
        return -1
    
    head, tail = digits[:i], digits[i:]
    last_digit = head[-1]
    i, new_digit = [(i, n) for i, n in enumerate(tail) if n > last_digit][-1]
    head[-1], tail[i] = new_digit, last_digit
    
    tail.sort()
    return int(''.join(head) + ''.join(tail))
#################
def next_bigger(n):
    num = [int(x) for x in str(n)]
    result = [0]*len(num)
    index = -1
    min = 100
    temp = []
    min_index = -1
    print(n)
    
    print(num)
   
    
    if sorted(num,reverse = True) == num and all(i >= j for i, j in zip(num, num[1:])):
        print(num)
        return -1
    if sorted(num) == num and all(i < j for i, j in zip(num, num[1:])):
        num[-2:] = sorted(num[-2:], reverse = True)
        string = [str(integer) for integer in num]
        return int("".join(string))

    for i in range(len(num)-1, 0, -1):
        if num[i] > num[i-1]:
            index = i-1
            break
        
    for j in range(index+1):
        if j<index :
            result[j] = num[j]
        if j==index:
            list = num[index+1:]
            for k in range(len(list)):
                if list[k] > num[index] and list[k] < min:
                    min = list[k]
                    min_index = index + 1 + k
            result[j] = min



            print(index)
            print(min_index)

    temp = num[index: min_index] + num[min_index+1:]
    print(num[index: min_index])
    print(num[min_index:])
    print(temp)
    temp = sorted(temp)
    a = 0
    for x in range(index+1,len(num)):
        result[x] = temp[a]
        a+=1

    string = [str(integer) for integer in result]
    return int("".join(string))
###########################################################
from itertools import permutations

def next_bigger(n):
    alist = []
    #blist = []
    s = str(n)
    if len(s) > 4:
        sliced = s[-6:]
        first_slice = s[:-6]
    else:
        sliced = s[-3:]
        first_slice = s[:-3]
    comb = set(permutations(sliced))
    for j in list(comb):
        alist.append("".join(j))
    blist = [int(first_slice + x) for x in alist]
    blist.sort()
    #print(blist)
    if not blist[blist.index(n)] == blist[-1]:
        return blist[blist.index(n) + 1]
    else:
        return -1
############################
from itertools import permutations

def next_bigger(n):
    
    num = [int(a) for a in str(n)] 
    pos = len(num) - 1
    next_biggest = float("inf")
    next_biggest_counter = float("inf")
    
    if (len(num) == 1 or num == sorted(num, reverse = True)):
        return -1
    
    for i in range(len(num)-1, 0, -1):
        if(num[i] > num[i-1]):
            pos -=1
            break
        
        pos-=1
    
    for i in range(pos, len(num)):
        if(num[i] > num[pos] and num[i] < next_biggest):
            next_biggest = num[i]
            next_biggest_counter = i
            
    num[pos], num[next_biggest_counter] = num[next_biggest_counter], num[pos]
    
    num2 = num[pos+1:]
    num2.sort()
    
    for i in range(len(num2)):
        num[i+pos+1] = num2[i]
            
            
    num = [str(x) for x in num]
    s = "".join(num)
            
    return int(s)
