from itertools import count
def num_index(n):
    if(n<10): return n-1
    c = 0
    for i in count(1):
        c += i*9 * 10**(i-1)
        if(n < 10**(i+1)): return c + (i+1)*(n - 10**i)

def find_position(s):
    if not int(s): return num_index(int('1'+s))+1
    for l in range(1,len(s)+1):
        poss = []
        for i in range(0,l+1):
            sdt = s[0:l-i]; end = s[l-i:l]
            for c in ([end+sdt, str(int(end)-1)+sdt] if end and int(end)!=0 else [end+sdt]):
                if(c[0]=='0'): continue
                ds = c; n = int(c)
                while(len(ds) < len(s)+l): n += 1; ds += str(n)
                idx = ds.find(s)
                if(idx != -1): poss.append(num_index(int(c)) + idx)
        if(len(poss) > 0): return min(poss)
___________________________________________________
def pos(n):
    ans=0
    for i in range(16,-1,-1):
        if n>10**i:
            ans+=(n-10**i)*(i+1)
            n=10**i
    return ans
    
def tryexpand(string,S):
    m,l=10**99,len(S)
    for i in range(l):
        for j in range(l):
            t=int(S[i:j+1]) if i<=j else int(S[i:]+S[j:i])
            s=''.join([str(x) for x in range(t-l,t+l+1) if x>0])
            if string in s:
                temp=pos(t-l if t-l>0 else 0)+s.index(string)
                if temp<m:m=temp
    return m

def find_position(string):
    return min(tryexpand(string,string),tryexpand(string,'1'+string+'0'*14))

___________________________________________________
def is_around(num, string):
    try:
        return True, ''.join([str(n) for n in range(num-1, num+len(string)+1)]).index(string)-len(str(num-1))
    except ValueError:
        return False, 0

    
def possible_nums(string):
    return list(map(int,sum([cyc((string*2)[j:i+j+1]) for i in range(len(string)) for j in range(i+1)],[])))


def cyc(str):
    return [str[i:]+str[:i] for i in range(len(str))]


def position(num):
    return sum([i*9*10**(i-1) for i in range(1, len(str(num)))] + [(num-10**(len(str(num))-1))*len(str(num))])


def find_position(string):
    nums = sorted(possible_nums(string) + possible_nums(string+'0'*string.count('9')) + possible_nums('1'+string))
    for num in nums:
        found, rel_index = is_around(num, string)
        if found: 
            pos = position(num)
            if pos+rel_index>-1: return pos+rel_index
___________________________________________________
def find_position(string):
    lenStr=len(string)
    if string.count("0")==lenStr:
        return pos(int("1"+string)-1)+1
    na=int(10**lenStr)
    pa=0; found = False
    for i in range(1,lenStr+1):                   #test for numbers with i digits
        for j in range(i):  
            rightBound=min(lenStr,j+i)
            ss=string[j:rightBound]
            if len(ss)<i:                         # if no more digits to the right, dd it form the left
                sa=string[j-(i-len(ss)):j]
                sa2=str(int(sa)+1)                #adjust left number by adding one
                ss+=("0"*i+ sa2)[-(i-len(ss)):]   #only take necessary digits after adjustment
            n=max(2,int(ss))  
            s=""
            for k in range (max(1,n-1),n+lenStr//i+2): #create small string with sequence around n
                s+=str(k)
            p = s.find(string) 
            if p>=0:                              #Input string foud in sequ
                found = True
                if n<na:                          # value is lower to others found previously
                    pa=pos(n-1)+p-len(str(n-1))
                    na=n
        if found: break        
    return pa                                     # return lowest postion
    
def pos(n):
    sn=str(n) ; off=0
    for i in range(1,len(str(n))):
        off+=9*10**(i-1)*i
    return off+(n-int("0"+"9"*(len(sn)-1)))*len(sn)
___________________________________________________
def find_position(string):
    l = len(string)
    for length in range(1,l+1):
        guesses = []
        for offset in range(length+1):
            guess = string[offset:offset+length]
            if len(guess) < length:
                guess += str(int(string[:offset])+1)[-(length-len(guess)):].zfill(length-len(guess))
            if string == reconstruct(int(guess), offset, l):
                guesses.append(find_int(int(guess))-offset)
        if guesses:
            return min(guesses)
    string += "1"
    return find_position(string)


def reconstruct(num, start, length):
    """Given an integer, an index at which it starts and a
    total length of string, returns the expected sequence."""
    if num <= 1: return
    string = str(num-1)[len(str(num-1))-start:]
    while len(string) <= length:
        string += str(num)
        num += 1
    return string[:length]


def find_int(n):
    """Returns the index of a given integer n."""
    l = len(str(n))
    table = [i < l for i in range(1,17)]
    indices = [i*9*10**(i-1) for i in range(1,17)]
    min_index = sum([x*y for x, y in zip(table, indices)])
    rest = l * (n - 10**(l-1))
    return min_index + rest
___________________________________________________
def just1(slist):
    """
    Convert list of 1 string to first integer
    """
    s = slist[0]
    if s[0]=='0':
        return int('1'+s)
    return int(s)


def terrible2(slist):
    """
    Convert list of 2 strings to first integer.
    Let the strings be p, q. Then terrible2 solve2 for words u, v such that
        up + 1 = qv
    which minimise the number up subject to up>0.

    0. If q begins with '0' then it is impossible.
    1. Let r be the len(p) suffix of p+1, which might require zero-prefixing.
    2. Solve wr = qv by finding the least i such that
        * wr = q[:i]r
        * q is a prefix of wr
        * p is a suffix of wr-1
            (e.g. (p, q) = ['09', '1'] has wr-1 = '9' otherwise)
        * wr>1.
    3. Return wr-1.
    """
    p, q = slist
    if q[0] == '0':
        return None
    r  = str(int(p)+1).zfill(len(p))[-len(p):]
    wr = next(wr for i in range(len(q)+1)
                     for wr in [q[:i] + r]
                         if (
                                 wr.startswith(q)
                                 and int(wr)>1
                                 and str(int(wr)-1).endswith(p)
                             )
             )
    return int(wr)-1


def index_in_string(n):
    """
    Get index of start of integer n in the infinite string
    """
    d = len(str(n))
    start_of_length_d = sum([(i+1)*9*10**i for i in range(d-1)])
    return start_of_length_d + (n-10**(d-1))*d


def is_prefix(r, n):
    """
    Return indicator that r is a prefix of the string n(n+1)(n+2)...
    This could be optimised by checking one number at a time
    """
    l = len(r) // len(str(n)) + 1
    s = "".join([str(i) for i in range(n, n+l)])
    return s.startswith(r)


def find_position(s):
    """
    Find the index of the first occurrence of s in the infinite string
    This version uses the fact that finding a complete number in s
    determines the rest of s if s is indeed part of 123...

    This could by optimised by searching in order of length. This could need
    care as some two-part partitions are shorter (n/2) than some three-part
    partitions (n-2).

    1. for each length l
    2.    for each initial position i
    3.       let s = pqr where q is the word given by i, l
             (we choose i, l such that |p| > 0, |r| > 0)
    4.       store solution q-1 if
              * q does not start with '0'
              * q is not '1'
              * q-1 ends with p (this includes the case q-1 = p)
              * r is a prefix of (q+1)(q+2)...
    5. store all one-part and two-part solutions
    6. pick the minimum solution

    * Since we require |p|>0 and |r|>0, it follows that
         1 <= l < n - 1, 1 <= i and i + l - 1 < n - 1.
    * Since we require |p|<=l, it follows that i<=l
    """
    indices = []
    def store(m, p):
        off = len(str(m))-len(p) # offset from first digit of m
        indices.append(index_in_string(m) + off)

    n = len(s)
    for l in range(1, n - 1):
        for i in range(1, min(l + 1, n - l)):
            p, q, r = s[:i], s[i:i+l], s[i+l:]
            if (q[0] != '0' and
                q != '1'    and
                str(int(q)-1).endswith(p) and
                is_prefix(r, int(q)+1)
               ):
                store(int(q)-1, p)

    for i in range(1, n):
        m = terrible2([s[:i], s[i:]])
        if m is not None:
            store(m, s[:i])

    store(just1([s]), s)

    return min(indices)
___________________________________________________
def get_index(num):
  """Get the index of the number `num` in the infinite string."""
  le = len(str(num))
  return le * (num - 1) + le - 10**(le-1) - (10**(le-1) - 1)//9
  
def is_valid_partition(string, begin, length):
  """For a given `string`, partition it using windows of length `length`,
  with first beginning index at `begin`. Then check if this partition gives
  a valid consecutive natural number sequence. If so, return the smallest 
  valid integer that begins at `begin`. Otherwise, return `None`.    
  """
  le_str = len(string)
  assert le_str > 0 and length > 0
  begin = begin % length
  assert begin < le_str
  
  if string[begin] == '0':
    return None
  
  if length >= le_str:
    if begin == 0:
      return int(string)
    else:
      tail = str(int(string[:begin]) + 1).zfill(begin)[-begin:]
      return int(string[begin:] + '0'*(length - le_str) + tail)
  
  if begin + length > le_str: # no complete window is included in `string`
    tail = int(string[:begin])
    succ = str(tail + 1).zfill(begin)[-begin:]
    if succ[:(le_str-length)] == string[length:]:
      return int(string[begin:] + succ[le_str-length:])
    else:
      return None
  
  num = int(string[begin:begin + length])
  # Check for left-most incomplete window
  if begin > 0 and string[:begin] != str(num-1).zfill(begin)[-begin:]:
    return None
  should_follow_by = ''
  idx = num + 1
  while len(should_follow_by) < le_str - (begin + length):
    should_follow_by += str(idx)
    idx += 1
  if should_follow_by[:le_str - (begin + length)] != string[begin + length:le_str]:
    return None
  return num

def find_position(string):
  le_str = len(string)
  if string == '0' * le_str:
    num = int('1' + string)
    return get_index(num) + 1
    
  possible_solutions = []
  for length in range(1, le_str+1):
    for begin in range(length):
      num = is_valid_partition(string, begin, length)
      if num:
        possible_solutions.append(get_index(num) - begin)
    if possible_solutions:
      return min(possible_solutions)
  raise ValueError("Impossible to run this line!")
___________________________________________________
import math
def find_position(string):
    n = 1
    l = len(string)
    maxl = l
    ar = 0
    a0 = 0
    start = 0
    s = 0
    while n <= maxl:
        finded = True
        start = 0
        while start < n:
            factN = n
            m = 0
            finded = True
            m += start
            temp = string[m:m+n]
            if m+n <= maxl:
                a = int(temp)
            else:
                t = n-len(temp)
                t2 = (10 ** t)
                a = int(temp) * t2 + (int(string[:start][-t:]) +1)%t2
            if start == 0:
                a0 = a
                finded = a0 != 0 and not temp.startswith('0')
            else:
                a0 = a - 1
                finded = str(a0).endswith(string[:m]) and a0 != 0
                finded = finded  and not temp.startswith('0')
            while m+factN <= maxl and finded:
                m += factN
                temp = math.log(a+1,10)
                if temp == int(temp):
                    factN += 1
                if not str(a+1).startswith(string[m:m+factN]):
                    finded = False
                    break
                a += 1
            if finded or ar != 0:
                if finded:
                    if ar == 0:
                        ar = a0
                        s = start
                    elif a0 < ar:
                        ar = a0
                        s = start
                    elif a0 == ar and s !=0:
                        ar = a0
                        s = start                        
                else:
                    finded = True
            start += 1
        if finded:
            break
        n += 1
    def calc(n,start=s):
        m = int(math.log(n,10))
        if m == 0:
            return n-1
        rSide = 10**m -1
        idx = 0
        for i in range(1,m+1):
            idx += 9 * (10**(i-1)) * i
        d = (n - 1 - rSide) * (m + 1) + (m + 1 - start) % (m + 1)
        return idx + d
    if finded:
        return calc(ar)
    else:
        return calc(int('1' + string),start = l)
