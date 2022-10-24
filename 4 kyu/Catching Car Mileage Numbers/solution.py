52c4dd683bfd3b434c000292

def is_incrementing(number): return str(number) in '1234567890'
def is_decrementing(number): return str(number) in '9876543210'
def is_palindrome(number):   return str(number) == str(number)[::-1]
def is_round(number):        return set(str(number)[1:]) == set('0')

def is_interesting(number, awesome_phrases):
    tests = (is_round, is_incrementing, is_decrementing,
             is_palindrome, awesome_phrases.__contains__)
       
    for num, color in zip(range(number, number+3), (2, 1, 1)):
        if num >= 100 and any(test(num) for test in tests):
            return color
    return 0
_________________________________
def is_good(n, awesome):
    return n in awesome or str(n) in "1234567890 9876543210" or str(n) == str(n)[::-1] or int(str(n)[1:]) == 0

def is_interesting(n, awesome):
    if n > 99 and is_good(n, awesome):
        return 2
    if n > 97 and (is_good(n + 1, awesome) or is_good(n + 2, awesome)):
        return 1
    return 0
_________________________________
import re
def is_sequential(string):
    return string in "1234567890" or string in "9876543210"

def is_interesting(number, awesome_phrases):
    print (number)
    interestingness = 2
    for i in (number, number + 1, number + 2):
        if (number != i):
            interestingness = 1
        if (i < 100):
            continue
        if (i in awesome_phrases):
            return interestingness
        i = str(i)
        if re.match(r"^\d0+$", i):
            return interestingness
        if i == i[::-1]:
            return interestingness
        if is_sequential(i):
            return interestingness
        if re.match(r"^(\d)\1+$", i):
            return interestingness
    
    
    return 0
_________________________________
def is_interesting(n, awesome_phrases):
    import math
    for m in range(3):
        s = str(n + m)
        if len(s) > 2 and (zf(s) or sd(s) or seqinc(s) or seqdec(s) or pal(s) or awe(s, awesome_phrases)):
            if m == 0: return 2
            else: return 1
    return 0
    
def awe(s, l):
    return s in [str(x) for x in l]
    
def pal(s):
    return s == s[::-1]
    
def seqdec(s):
    a = '9876543210'
    for i in range(len(s)-1):
        if a.index(s[i]) + 1 != a.index(s[i+1]): return False
    return True
    
def seqinc(s):
    a = '1234567890'
    for i in range(len(s)-1):
        if a.index(s[i]) + 1 != a.index(s[i+1]): return False
    return True

def sd(s):
    for i in range(len(s)-1):
        if s[i] != s[i+1]: return False
    return True

def zf(s):
    for i in range(1, len(s)):
        if s[i] != '0': return False
    return True
_________________________________
def is_interesting(number, awesome_phrases):
    def check(n):
        nonlocal awesome_phrases
        n = str(n)
        test0 = lambda x: len(x) > 2
        test1 = lambda x: set(x[1:]) == set("0")
        test2 = lambda x: len(set(x)) == 1
        test3 = lambda x: all((int(b) or 10) - (int(a) or 10) == 1 for a, b in zip(x, x[1:]))
        test4 = lambda x: all(int(a) - int(b) == 1 for a, b in zip(x, x[1:]))
        test5 = lambda x: x == x[::-1]
        test6 = lambda x: int(x) in awesome_phrases
        return test0(n) and (test1(n) or test2(n) or test3(n) or test4(n) or test5(n) or test6(n))
    return int((check(number) and 2) or (check(number+1) or check(number+2)))
_________________________________
def is_interesting(num, awesome_phrases):
    for i in range(3):
        string = str(num)
        if num < 98:
            return 0
        if num >= 100:
            if digits(string) == True:
                if i == 0:
                    return 2
                else:
                    return 1
            elif same(string) == True:
                if i == 0:
                    return 2
                else:
                    return 1
            elif increment(string) == True:
                if i == 0:
                    return 2
                else:
                    return 1
            elif decrement(string) == True:
                if i == 0:
                    return 2
                else:
                    return 1
            elif pallindrome(string) == True and len(string) > 1:
                if i == 0:
                    return 2
                else:
                    return 1
            elif num in awesome_phrases:
                if i == 0:
                    return 2
                else:
                    return 1
        num = num + 1
    return 0 

def digits(string):
    if len(string) == 1:
        return False
    for x in range(len(string) - 1):
        if string[x + 1] != "0":
            return False
    return True
  
def same(string):
    lol = string[0]
    if len(string) == 1:
        return False
    for x in range(len(string) - 1):
        if string[x + 1] != lol:
            return False
    return True
  
def increment(string):
    if len(string) == 1:
        return False
    for x in range(len(string) - 1):
        if int(string[x]) + 1 == 10 and int(string[x + 1]) == 0:
            print("ok")
        elif int(string[x]) + 1 != int(string[x + 1]):
            return False
    return True
  
def decrement(string):
    if len(string) == 1:
        return False
    for x in range(len(string) - 1):
        uh = len(string) - 1 - x
        if int(string[uh]) + 1 == 0 and int(string[uh - 1]) != 9:
            return False
        elif int(string[uh]) + 1 != int(string[uh - 1]):
            return False
    return True
  
def pallindrome(string):
    if len(string) <= 1:
        return True
    else:
        if string[0] != string[-1:]:
            return False
        else:
            return pallindrome(string[1:-1])
_________________________________
ascending_sequence = "1234567890"
decending_sequence = "9876543210"

def is_interesting(number, awesome_phrases, recurse=True):
    nstr = str(number)
    if len(nstr) >= 3:
        if nstr.endswith("00"):
            return 2
        if len(set(nstr)) == 1:
            return 2
        if nstr in ascending_sequence:
            return 2
        if nstr in decending_sequence:
            return 2
        if nstr == nstr[::-1]:
            return 2
        if number in awesome_phrases:
            return 2
    if recurse:
        if is_interesting(number + 1, awesome_phrases, False) == 2:
            return 1
        if is_interesting(number + 2, awesome_phrases, False) == 2:
            return 1
    return 0
