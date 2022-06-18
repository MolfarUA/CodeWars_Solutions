544675c6f971f7399a000e79


def string_to_number(s):
    return int(s)
_______________________
string_to_number = int
_______________________
string_to_number = lambda n: int(n)
_______________________
def string_to_number(s):
    i = int(s)
    return i
_______________________
def char_to_digit(s):
    if s == '0':
        return 0
    elif s == '1':
        return 1
    elif s == '2':
        return 2
    elif s == '3':
        return 3
    elif s == '4':
        return 4
    elif s == '5':
        return 5
    elif s == '6':
        return 6
    elif s == '7':
        return 7
    elif s == '8':
        return 8
    else:
        return 9
    
    
def string_to_number(s):
    if isinstance(s, int):
        return s
    
    r = 0
    for c in s:
        if c == '-':
            continue
        r = r * 10 + char_to_digit(c)
    
    return r if s[0] != '-' else -1 * r
_______________________
def string_to_number(s):
    return eval('{}'.format(s))
_______________________
def string_to_number(s):
    result = 0
    result = int(s)
    return result
_______________________
def string_to_number(s):
    a=int(s)
    return a

    pass
_______________________
def string_to_number(s):
    string_to_number = int
    return int(s)
_______________________
def string_to_number(s):
    new_s = int(s)
    return new_s
    pass
_______________________
def string_to_number(s):
    return int(s)

string_to_number("242")

def str_to(d):
    print(f'{type(d)} changed to {int(d)}')
    
str_to(23.23)
_______________________
def string_to_number(str):
    return int(str)

print(type(string_to_number("605")))
_______________________
def string_to_number(s):
    if '-' in s:
        return -int(s[1:])
    else:
        return int(s)
