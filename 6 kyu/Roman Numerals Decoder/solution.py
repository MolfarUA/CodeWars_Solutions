51b6249c4612257ac0000005


def solution(roman):
    dict = {
        "M": 1000,
        "D": 500,
        "C": 100,
        "L": 50,
        "X": 10,
        "V": 5,
        "I": 1
    }

    last, total = 0, 0
    for c in list(roman)[::-1]:
        if last == 0:
            total += dict[c]
        elif last > dict[c]:
            total -= dict[c]
        else:
            total += dict[c]
        last = dict[c]
    return total
__________________________________
def solution(roman):
    """complete the solution by transforming the roman numeral into an integer"""
    letters = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000 }
    a = 0
    n = len(roman)
    sum = 0
    while a < n:
        if (a != n - 1 and letters[roman.lower()[a]] < letters[roman.lower()[a + 1]]):
            sum += letters[roman.lower()[a + 1]] - letters[roman.lower()[a]]
            a += 2
            continue
        else:
            sum += letters[roman.lower()[a]]
            a += 1
    return sum
__________________________________
ROMAN_MAP = (
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100),
        ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5),
        ('IV', 4), ('I', 1)
)

def solution(roman):
    result = 0
    index = 0
    for rom, arab in ROMAN_MAP:
        while roman[index : index + len(rom)] == rom:
            result += arab
            index += len(rom)
    return result
    
solution('XXI')
__________________________________
def solution(roman):
    """complete the solution by transforming the roman numeral into an integer"""
    num = {"I" : 1,
          "V" : 5,
          "X" : 10,
          "L" : 50,
          "C" : 100,
          "D" : 500,
          "M" : 1000}
    return sum([num[x] - 2*num[roman[i-1]] 
                if i != 0 and num[roman[i-1]] < num[x] 
                else num[x] 
                for i, x in reversed(list(enumerate(roman)))])
__________________________________
def solution(s):
    r={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    tot=0
    for i in range(len(s)-1):
        if r[s[i]] < r[s[i+1]]:
            tot-=r[s[i]]
        else:
            tot+=r[s[i]]
    tot+=r[s[-1]]
    return tot
