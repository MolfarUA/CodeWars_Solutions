def fake_bin(x):
    return ''.join('0' if c < '5' else '1' for c in x)
__________________________________
def fake_bin(x):
    result = ""
    for num in x:
        if int(num) < 5:
            result = result + "0"
        else:
            result = result + "1"
    return result
__________________________________
import string

def fake_bin(s):
    return s.translate(string.maketrans('0123456789', '0000011111'))
__________________________________
def fake_bin(x):
    if x == "":
        return x
    
    if int(x[0]) < 5:
        return '0'+fake_bin(x[1:])
    
    return '1' + fake_bin(x[1:])
__________________________________
def fake_bin(s):
  return ''.join('0' if int(c) < 5 else '1' for c in s)
__________________________________
def fake_bin(x):
    if x == "":
        return x
    
    if int(x[0]) < 5:
        return '0'+fake_bin(x[1:])
    
    return '1' + fake_bin(x[1:])
__________________________________
def fake_bin(x):
    return "".join("0" if n in "01234" else "1" for n in x)
__________________________________
def fake_bin(x):
    map = str.maketrans('123456789', '000011111')
    return x.translate(map)
__________________________________
def fake_bin(x):
    x_binary = ""
    for letter in x:
        if(int(letter) < 5):
            x_binary += "0"
        else:
            x_binary += "1"
    return x_binary
__________________________________
def fake_bin(x):
    res = ""
    for i in x:
        if int(i) >= 5:
            res += "1"
            #i = i.replace(i, "1")
        else:
            res += "0"
            #i = i.replace(i, "0")
            
    return res
__________________________________
def fake_bin(x):
    return ''.join('0' if int(d) < 5 else '1' for d in str(x))
__________________________________
def fake_bin(x):
    wynik=""
    for i in x:
        if i >= str(5):
            wynik+="1"
        else:
            wynik+="0"
    return wynik
