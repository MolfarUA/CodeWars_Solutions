57f75cc397d62fc93d000059


def calc(s):
    total1 = ''.join(map(lambda c: str(ord(c)), s))
    total2 = total1.replace('7', '1')
    return sum(map(int, total1)) - sum(map(int, total2))
__________________________________
def calc(x):
    return ''.join(str(ord(ch)) for ch in x).count('7') * 6
__________________________________
def calc(x):
    total1 = "".join(str(ord(char)) for char in x)
    total2 = total1.replace("7","1")
    return sum(int(x) for x in total1) - sum(int(x) for x in total2)
__________________________________
def calc(x):
    return sum(6 for c in ''.join(map(str, map(ord, x))) if c== '7')
__________________________________
def digitsum(word: str) -> int:
    return sum(int(digit) for digit in word)

def calc(word: str) -> int:
    seven = ''.join(str(ord(char)) for char in word)
    one = seven.replace('7', '1')
    return digitsum(seven) - digitsum(one)
__________________________________
def calc(x):
    return ''.join([str(ord(x[i])) for i in range(len(x)) ]).count('7') * 6
__________________________________
calc = lambda x: ''.join(str(ord(q)) for q in x).count('7') * 6
__________________________________
def calc(x):
    a="".join(str(ord(x[z])) for z in range(len(x)))
    return sum(int(a[z])-1 for z in range(len(a)) if a[z]=='7')
__________________________________
def calc(x):
    ascii = ''.join(str(ord(i)) for i in x)
    return sum(map(int, list(ascii))) - sum(map(int, list(ascii.replace('7','1'))))
__________________________________
def calc(x):
    total_1 = int(''.join([str(ord(ascii_letter)) for ascii_letter in [letter for letter in x]]))
    total_2 = int(str(total_1).replace("7","1"))
    return sum([int(int_total_1) for int_total_1 in str(total_1)]) - sum([int(int_total_2) for int_total_2 in str(total_2)])
__________________________________
def calc(x):
    total1 = int(''.join(map(str,[ord(i) for i in x])))
    total2 = int(''.join(map(str,[1 if x =='7' else x for x in str(total1)])))
    return (sum(list(map(int,str(total1-total2)))))
__________________________________
def calc(x):
    y = list(x)
    y = [ord(x) for x in y]
    sum_y = ""
    for ele in y:
        sum_y += str(ele)
    return sum_y.count("7") * 6
