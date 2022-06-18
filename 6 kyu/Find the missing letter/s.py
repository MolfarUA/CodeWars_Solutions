def find_missing_letter(chars):
    n = 0
    while ord(chars[n]) == ord(chars[n+1]) - 1:
        n += 1
    return chr(1+ord(chars[n]))
________________________
def find_missing_letter(input):
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    start = alphabet.index(input[0])
    for i in range(len(input)):
        if not input[i] == alphabet[start+i]:
            return alphabet[start+i]
________________________
def find_missing_letter(c):
    return next(chr(ord(c[i])+1) for i in range(len(c)-1) if ord(c[i])+1 != ord(c[i+1]))
________________________
def find_missing_letter(chars):
    o = ord(chars[0])
    for letter in chars[1:]:
        if ord(letter) - 1 == o:
            o += 1
        else:
            return chr(o + 1)
________________________
def find_missing_letter(chars):
    i = ord(chars[0])
    for c in chars:
        if c != chr(i): 
            return chr(i)
        i += 1
________________________
def find_missing_letter(chars):
    print(chars)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i, char in enumerate(chars):
        if i != 0:
            expected = alphabet[alphabet.index(char.lower()) - 1]
            actual = chars[i - 1]
            if expected != actual.lower():
                return expected.upper() if char.isupper() else expected
________________________
import string
def find_missing_letter(chars):
    a=string.ascii_letters
    for i in range (len(a)):
        if chars[0]==a[i]:
            debut=i
    for j in range (len(chars)):
        if chars[j]!=a[debut+j]:
            return a[debut+j]
________________________
def find_missing_letter(chars):
    expected = (len(chars)+1) * (ord(chars[0]) + ord(chars[-1])) / 2
    actual = sum(ord(letter) for letter in chars)
    missing = int(expected - actual)
    return chr(missing)
