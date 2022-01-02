def make_upper_case(s): return s.upper()
_____________________________________________
def make_upper_case(strng):
    return strng.upper()
_____________________________________________
make_upper_case = str.upper
_____________________________________________
def make_upper_case(s):
    return "".join(i.capitalize() for i in s)
_____________________________________________
def make_upper_case(s):
    print(s, s.upper())
    return s.upper()
_____________________________________________
def make_upper_case(s):
    new_string = ''
    for letter in s:
        new_string += letter.upper()
    return new_string
_____________________________________________
def make_upper_case(string):
    return string.upper()

make_upper_case("hello")
_____________________________________________
def make_upper_case(s):
    hola = s.upper()
    for palabra in s:
        return hola
_____________________________________________
def make_upper_case(s): return s.upper() #1 line bb
